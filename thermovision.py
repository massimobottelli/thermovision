import matplotlib.pyplot as plt
from skimage import io, color, transform, filters, morphology, feature
from skimage.transform import probabilistic_hough_line
import numpy as np
import json

# import CONFIG with parameters
with open('config.json', 'r') as f:
    image_config = json.load(f)

CONFIG = {**image_config,
          'image_path': 'image.jpg',  # Image path
          'resize_shape': (480, 640),  # Image resizing dimensions
          'sigma': 1.0,  # Parameter for Gaussian filter
          'roi_size': 50,  # Size of the ROI (square)
          'hough_threshold': 50,  # Threshold for Hough transform (line detection)
          'hough_line_length': 30,  # Minimum line length detected by Hough
          'hough_line_gap': 4,  # Maximum gap between segments to consider as a single line
          "angles": [135, 270],  # Reference angles for the thermometer
          "temperatures": [0, 80]  # Temperatures corresponding to reference angles
          }


# Function to load and resize the image
def load_image(image_path):
    """Loads the image, converts it to grayscale, and resizes it."""
    image = io.imread(image_path)
    image_resized = transform.resize(image, CONFIG['resize_shape'], anti_aliasing=True)
    return color.rgb2gray(image_resized)


# Function to preprocess the image
def preprocess_image(image, sigma=CONFIG['sigma']):
    """Applies a Gaussian filter to reduce noise and detects edges."""
    blurred_image = filters.gaussian(image, sigma=sigma)
    edges = filters.sobel(blurred_image)
    return morphology.dilation(edges, morphology.disk(2))


# Function to get the ROI centered
def get_roi_from_center(center, size=CONFIG['roi_size'], image_size=CONFIG['resize_shape']):
    """Creates a square ROI centered on a point, with dimensions 'size' x 'size'."""
    x, y = center
    half_size = size // 2
    x_min = max(x - half_size, 0)
    x_max = min(x + half_size, image_size[0])
    y_min = max(y - half_size, 0)
    y_max = min(y + half_size, image_size[1])
    return x_min, y_min, x_max, y_max


# Function to detect lines with the Hough transform
def detect_lines(image, threshold=CONFIG['hough_threshold'], line_length=CONFIG['hough_line_length'],
                 line_gap=CONFIG['hough_line_gap']):
    """Detects lines in the entire image using probabilistic Hough transform."""
    # Detect edges in the image
    edges = feature.canny(image)

    # Hough transform
    lines = probabilistic_hough_line(edges, threshold=threshold, line_length=line_length, line_gap=line_gap)

    return lines


# Function to check if a point is within one of the two ROIs
def is_point_in_roi(point, roi_coords):
    """Checks if a point is within the ROI defined by roi_coords."""
    x, y = point
    x_min, y_min, x_max, y_max = roi_coords
    return x_min <= x <= x_max and y_min <= y <= y_max


# Function to calculate the angle of a line with respect to the horizontal axis
def calculate_angle(line):
    """Calculates the angle of a line in degrees with respect to the horizontal axis."""
    x1, y1 = line[0]
    x2, y2 = line[1]
    angle_rad = np.arctan2(y2 - y1, x2 - x1)  # Arctangent for angle in radians
    angle_deg = np.degrees(angle_rad)  # Converts to degrees
    return angle_deg


def angle_to_temperature(angle):
    # Extract the min and max values for angle and temperature
    angle_min, angle_max = CONFIG["angles"][0], CONFIG["angles"][1]
    temp_min, temp_max = CONFIG["temperatures"][0], CONFIG["temperatures"][1]

    # Calculate temperature using linear interpolation
    temperature = temp_min + (angle - angle_min) * (temp_max - temp_min) / (angle_max - angle_min)
    return temperature


def display_line(line, ax):
    # Calculate the angle
    angle = 180 + calculate_angle(line)

    # Convert angle to degrees Celsius
    temperature = angle_to_temperature(angle)

    # Calculate start and end points
    x1, y1 = line[0]
    x2, y2 = line[1]

    # Display the segment
    ax.plot([x1, x2], [y1, y2], color='red', linewidth=2)

    # Add the temperature as text above the line
    mid_point = [(line[0][0] + line[1][0]) / 2, (line[0][1] + line[1][1]) / 2 - 10]
    ax.text(mid_point[0], mid_point[1], f'{temperature:.0f}°C',
            color='red', fontsize=10, ha='center', va='center')

    return True


def main():
    # Load the image
    image = load_image(CONFIG['image_path'])

    # Check if the image was loaded correctly
    if image is None:
        print("Error loading the image.")

    # Get the ROI centers from CONFIG
    center_1 = CONFIG['center_1']
    center_2 = CONFIG['center_2']

    # Get the ROIs
    roi_1_coords = get_roi_from_center(center_1)
    roi_2_coords = get_roi_from_center(center_2)

    # Detect lines in image
    lines = detect_lines(image)

    # Display the original image and the ROIs
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    # Show the image
    ax.imshow(image, cmap='gray')

    # Add rectangles for the ROIs
    roi_1_x1, roi_1_y1, roi_1_x2, roi_1_y2 = roi_1_coords
    roi_2_x1, roi_2_y1, roi_2_x2, roi_2_y2 = roi_2_coords
    rect_1 = plt.Rectangle((roi_1_y1, roi_1_x1), width=roi_1_y2 - roi_1_y1, height=roi_1_x2 - roi_1_x1, linewidth=2,
                           edgecolor='yellow', facecolor='none')
    rect_2 = plt.Rectangle((roi_2_y1, roi_2_x1), width=roi_2_y2 - roi_2_y1, height=roi_2_x2 - roi_2_x1, linewidth=2,
                           edgecolor='yellow', facecolor='none')

    # Add the rectangles to the image
    ax.add_patch(rect_1)
    ax.add_patch(rect_2)

    # Draw the detected lines in the image
    roi_1_display = False
    roi_2_display = False

    for line in lines:
        x0, y0 = line[0]  # Start point
        x1, y1 = line[1]  # End point
        # Check if one of the line's endpoints is within one of the two ROIs
        if (is_point_in_roi((y0, x0), roi_1_coords) or is_point_in_roi((y1, x1), roi_1_coords)) and not roi_1_display:
            roi_1_display = display_line(line, ax)

        if (is_point_in_roi((y0, x0), roi_2_coords) or is_point_in_roi((y1, x1), roi_2_coords)) and not roi_2_display:
            roi_2_display = display_line(line, ax)

        else:
            ax.plot([x0, x1], [y0, y1], color='green', linewidth=1)

    # Show the image
    plt.show()


# Run the main function
if __name__ == "__main__":
    main()

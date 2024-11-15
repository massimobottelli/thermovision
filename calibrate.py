import time
from skimage import io, color, transform
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import json

# Configuration dictionary
CONFIG = {
    'image_path': 'image.jpg',  # Image path (will not be saved in the JSON file)
    'resize_shape': (480, 640),  # Dimensions for resizing the image (will not be saved in the JSON file)
    'roi_size': 50,  # Size of the ROI square side
}

# Path to the JSON configuration file
CONFIG_PATH = 'config.json'


# Function to load and resize the image
def load_image(image_path):
    """Loads the image, converts it to grayscale, and resizes it."""
    image = io.imread(image_path)
    image_resized = transform.resize(image, CONFIG['resize_shape'], anti_aliasing=True)
    return color.rgb2gray(image_resized)


# Function to save coordinates to the JSON file
def save_config(config, path):
    """Saves the configuration dictionary to the specified JSON file (without 'image_path' and 'resize_shape')."""
    # Remove unwanted parameters before saving
    config_to_save = {key: value for key, value in config.items() if key not in ['image_path', 'resize_shape', 'roi_size']}

    # Save the JSON file
    with open(path, 'w') as f:
        json.dump(config_to_save, f, indent=4)
    print(f"Configuration saved in {path}")


# Callback for user click
def on_click(event):
    # Check if the click occurred within the image
    if event.inaxes is not None:
        # Get the click coordinates
        x, y = int(event.xdata), int(event.ydata)

        # Save the clicked coordinates as the center
        CONFIG['center'] = (y, x)

        # Calculate the ROI rectangle coordinates
        roi_size = CONFIG['roi_size']
        rect_x = x - roi_size // 2
        rect_y = y - roi_size // 2

        # Add the rectangle at the clicked position
        rect = patches.Rectangle((rect_x, rect_y), roi_size, roi_size,
                                 linewidth=2, edgecolor='yellow', facecolor='none')
        event.inaxes.add_patch(rect)
        plt.draw()

        # Save the points to the JSON file
        save_config(CONFIG, CONFIG_PATH)

        # Disable further clicks
        plt.gcf().canvas.mpl_disconnect(cid)


# Main function
def main():
    # Load the image
    image = load_image(CONFIG['image_path'])

    # Check if the image was loaded correctly
    if image is None:
        print("Error loading the image.")
        return

    # Display the image and set up the click event
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.imshow(image, cmap='gray')
    ax.set_title("Select the center of the thermometer")
    ax.axis('off')

    # Connect the click event and save the ID to disable it later
    global cid
    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    # Show the interactive window
    plt.show()


# Run the program
if __name__ == "__main__":
    main()

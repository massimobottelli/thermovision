# ThermoVision
## Analog Thermometer Digitization System

This project demonstrates how to digitize the readings of an analog dial thermometer using a Raspberry Pi, computer vision, and Python. The system captures an image of the thermometer, processes it to determine the position of the needle, and calculates the corresponding temperature.


## Features

- Capture thermometer images using a Raspberry Pi with a PiCamera.
- Transfer images to a more powerful server for processing.
- Calibrate the system to identify the thermometer needle center.
- Analyze the image using computer vision to determine the needle's angle and convert it into a temperature reading.
- Modular design that can be adapted for other analog instruments or IoT applications.


## System Overview

The system consists of the following components:

1. **Image Capture Script** (`get_image.py`):
   - Captures an image of the thermometer using a Raspberry Pi.
   - Resizes the image to optimize for processing.
   - Transfers the image to a server via SFTP using `paramiko`.

2. **Calibration Script** (`calibrate.py`):
   - Allows the user to select the center of the thermometer needle.
   - Saves the calibration data (needle center) in a `config.json` file.

3. **Image Analysis Script** (`thermovision.py`):
   - Processes the captured image using the `scikit-image` library.
   - Detects lines in the image using probabilistic Hough transform.
   - Identifies the needle and calculates its angle relative to the horizontal axis.
   - Converts the angle to a temperature using reference data.


## Installation

### Prerequisites

Ensure you have the following installed on your systems:

#### Raspberry Pi
- Python 3
- Libraries:
  - `Picamera2`
  - `Pillow`
  - `paramiko`

Install the required libraries using:
```bash
pip install picamera2 pillow paramiko
```

#### Server
- Python 3
- Libraries:
  - `scikit-image`
  - `matplotlib`
  - `numpy`

Install the required libraries using:
```bash
pip install scikit-image matplotlib numpy
```


## How to Use

### Raspberry Pi: Capturing Images
1. Connect the Raspberry Pi with the PiCamera module.
2. Clone the repository:
   ```bash
   git clone https://github.com/massimobottelli/thermovision.git
   cd thermovision
   ```
3. Configure the server details in `get_image.py`:
   ```python
   server_address = "your-server-ip"
   username = "your-username"
   password = "your-password"
   remote_path = "/path/to/server/image.jpg"
   ```
4. Run the image capture script:
   ```bash
   python get_image.py
   ```

### Server: Calibration
1. Ensure you have a captured image (`image.jpg`) in the server directory.
2. Run the calibration script:
   ```bash
   python calibrate.py
   ```
3. Select the center of the thermometer needle when prompted. The coordinates will be saved in `config.json`.

### Server: Image Analysis
1. Transfer the captured image (`image.jpg`) from the Raspberry Pi to the server.
2. Run the image analysis script:
   ```bash
   python thermovision.py
   ```
3. The script will display the image, the detected needle, and the calculated temperature.


## Configuration

The configuration file (`config.json`) stores:
- `center`: Coordinates of the needle's center.
- `angles`: Reference angles for the thermometer scale (e.g., 0° and 90°).
- `temperatures`: Corresponding temperatures for the reference angles (e.g., 20°C and 80°C).


## Possible Applications
- Integrating analog instruments into IoT systems.
- Digitizing legacy equipment for automated monitoring and data logging.


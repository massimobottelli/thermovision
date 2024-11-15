from picamera2 import Picamera2
from datetime import datetime
from PIL import Image
import os
import paramiko

# Server credentials and details
server_address = "your-ip-address"
username = "your-username"
password = "your-password"
remote_path = "/<remote-path>/image.jpg"
local_directory = "/<local-path>"


def capture_and_save_images():
    # Create an instance of Picamera2
    picam2 = Picamera2()

    # Temporary file name for the captured image
    temp_image_path = os.path.join(local_directory, "temp_image.jpg")

    # Capture and save the image temporarily
    picam2.start_and_capture_file(temp_image_path)
    print(f"Image captured and temporarily saved as {temp_image_path}")

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_image_path = os.path.join(local_directory, f"{timestamp}.jpg")

    # Create backup with timestamped name
    os.makedirs(local_directory, exist_ok=True)
    os.rename(temp_image_path, backup_image_path)
    print(f"Backup image saved as {backup_image_path}")

    # Resize the backup image to 640x480 and save as image.jpg
    resized_image_path = os.path.join(local_directory, "image.jpg")
    with Image.open(backup_image_path) as img:
        resized_img = img.resize((640, 480))
        resized_img.save(resized_image_path)
        print(f"Resized image saved as {resized_image_path}")

    return resized_image_path


def transfer_file_via_sftp(local_path, remote_path):
    try:
        # Create an SSH client and connect to the server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_address, username=username, password=password)

        # Open an SFTP session from the SSH connection
        sftp = ssh.open_sftp()

        # Transfer the file
        sftp.put(local_path, remote_path)
        print(f"File successfully transferred to {remote_path}")

    except Exception as e:
        print(f"Error during file transfer: {e}")

    finally:
        # Close the connections
        sftp.close()
        ssh.close()


# Run the capture, backup, resizing, and transfer process
local_image_path = capture_and_save_images()
transfer_file_via_sftp(local_image_path, remote_path)

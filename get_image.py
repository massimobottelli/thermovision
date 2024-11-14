from picamera2 import Picamera2
from datetime import datetime
from PIL import Image
import os
import paramiko

# Configura le credenziali e i dettagli del server
server_address = "192.168.1.143"
username = "massimo"
password = "maxmil"
remote_path = "/Users/massimo/image.jpg"
local_path = "/home/massimo/thermovision/image.jpg"
local_backup_directory = "/home/massimo/thermovision"


def capture_and_resize_image():
    # Crea un'istanza di Picamera2
    picam2 = Picamera2()

    # Nome temporaneo per l'immagine acquisita
    temp_image_path = "/home/massimo/thermovision/temp_image.jpg"

    # Cattura e salva l'immagine in un file temporaneo
    picam2.start_and_capture_file(temp_image_path)
    print(f"Immagine acquisita e salvata temporaneamente come {temp_image_path}")

    # Genera il nome del file di backup con timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_image_path = os.path.join(local_backup_directory, f"{timestamp}.jpg")

    # Salva la copia con nome basato sul timestamp
    os.makedirs(local_backup_directory, exist_ok=True)
    os.rename(temp_image_path, backup_image_path)
    print(f"Immagine di backup salvata come {backup_image_path}")

    # Ridimensiona l'immagine di backup a 640x480 e salva come image.jpg
    with Image.open(backup_image_path) as img:
        resized_img = img.resize((640, 480))
        resized_img.save(local_resized_path)
        print(f"Immagine ridimensionata e salvata come {local_resized_path}")

    return local_resized_path


def transfer_file_via_sftp(local_path, remote_path):
    try:
        # Crea un client SSH e connettiti al server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_address, username=username, password=password)

        # Crea un client SFTP dalla connessione SSH
        sftp = ssh.open_sftp()

        # Trasferisce il file
        sftp.put(local_path, remote_path)
        print(f"File trasferito con successo a {remote_path}")

    except Exception as e:
        print(f"Errore durante il trasferimento del file: {e}")

    finally:
        # Chiude le connessioni
        sftp.close()
        ssh.close()


# Esegui l'acquisizione, ridimensionamento e trasferimento dell'immagine
local_image_path = capture_and_resize_image()
transfer_file_via_sftp(local_image_path, remote_path)

from picamera2 import Picamera2
from datetime import datetime
import os
import paramiko

# Configura le credenziali e i dettagli del server
server_address = "indirizzo_IP_del_server"
username = "nome_utente"
password = "password"
remote_directory = "/path/remoto/dove/salvare"


def capture_image_with_timestamp():
    # Crea un'istanza di Picamera2
    picam2 = Picamera2()

    # Configura la fotocamera e acquisisce l'immagine
    timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    filename = f"{timestamp}.jpg"
    local_path = os.path.join("/path/locale/dove/salvare", filename)

    # Cattura e salva l'immagine
    picam2.start_and_capture_file(local_path)
    print(f"Immagine salvata localmente come {local_path}")

    return local_path, filename


def transfer_file_via_sftp(local_path, remote_directory, filename):
    try:
        # Crea un client SSH e connettiti al server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server_address, username=username, password=password)

        # Crea un client SFTP dalla connessione SSH
        sftp = ssh.open_sftp()

        # Definisce il percorso di destinazione sul server
        remote_path = os.path.join(remote_directory, filename)

        # Trasferisce il file
        sftp.put(local_path, remote_path)
        print(f"File trasferito con successo a {remote_path}")

    except Exception as e:
        print(f"Errore durante il trasferimento del file: {e}")

    finally:
        # Chiude le connessioni
        sftp.close()
        ssh.close()


# Esegui l'acquisizione e trasferimento dell'immagine
local_path, filename = capture_image_with_timestamp()
transfer_file_via_sftp(local_path, remote_directory, filename)

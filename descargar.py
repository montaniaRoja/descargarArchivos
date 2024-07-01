import os
import threading
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Configuración de autenticación
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = './pollochucoapp-3378e6f87612.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=credentials)


# Función para descargar un archivo desde Google Drive
def descargar_archivo(file_id, file_name, save_path):
    request = service.files().get_media(fileId=file_id)
    full_path = os.path.join(save_path, file_name)
    with open(full_path, 'wb') as file:
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Descargando {file_name}: {int(status.progress() * 100)}% completado")
    print(f"Archivo {file_name} guardado en {full_path}")


# Lista de archivos a descargar (IDs de Google Drive, nombres de archivos locales y ruta de destino)
archivos = [
    ('16fJ8G8QwLCOovtZqZ9UMOS7fHRGKICVI', 'Seleccion.pdf', '/home/adolfo/Descargas'),
    ('1TFq1d13H5qAF-NMVg3DF7umEaUkuRTlB', 'Azul.pdf', '/home/adolfo/Descargas'),
    ('1zcPn7zD4YIbORPSq5BVAhOPaaKFxxS2A', 'motor.pdf', '/home/adolfo/Descargas')
]

# Crear y gestionar los hilos para cada descarga
hilos = []
for file_id, file_name, save_path in archivos:
    hilo = threading.Thread(target=descargar_archivo, args=(file_id, file_name, save_path))
    hilos.append(hilo)
    hilo.start()

# Esperar a que todos los hilos terminen
for hilo in hilos:
    hilo.join()

print("Todas las descargas han sido completadas.")

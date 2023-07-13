from utils import YtInitialData
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Ruta al archivo JSON de credenciales
credenciales = 'dup-utn-haedo-q1-2023.json'

# Definir el alcance de la API y las credenciales
alcance = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credenciales = Credentials.from_service_account_file(credenciales, scopes=alcance)

# Autenticar y acceder a la hoja de cálculo existente
cliente = gspread.authorize(credenciales)
hoja_calculo = cliente.open('Copia de YouTube Trending Data [hoja de trabajo compartida]')
hoja = hoja_calculo.get_worksheet(0)  # Índice de la hoja de cálculo (0 para la primera hoja)

yt_initial_data = YtInitialData()

tabs = ["Música", "Videojuegos", "Películas"] #futura implementacion de una iteracion para recorrer todas las tabs
videos = yt_initial_data.get_video_category('Música') #le paso Música como parámetro de ejemplo.

for video in videos:
   tab = video['tab']
   channel_name = video['channel_name']
   video_id = video['video_id']
   title = video['title']
   description = video['desecription']
   view_count = video['view_count']
   length = video['length']
   insert_timestamp = datetime.now()
   
   fila = [tab, channel_name, video_id, title, description, view_count, length, insert_timestamp]
   
   hoja.append_row(fila)




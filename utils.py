import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
chrome_options = Options()
chrome_options.add_argument("--headless")

class YtInitialData:
  	
   #clase que permite el manejo del arhivo YtInitialData.json recibido como parametro.
   #tambien realiza el web scrapping de la pagina de "tendencias de youtube", obteniendo los 
   #videos de las categorias que se pidan.
   
    #constructor de la calse, con la direccion hacia el archivo .json
	def __init__(self, path):
		self.path = path
  
	#sobrecarga del constructor para poder llamar a las funciones que trabajan sobre la web, 
	#tales como get_video_category()
	def __init__(self):
		return
  
	#Funcion que, dado un archivo.json del contenido de ytInitialData te devuelve los videos trending de "Now"
	def get_videos(self):
		videos = [] 

		try:
      
			with open(self.path, "rb") as file:
				yt_initial_data = json.load(file)
    
    
		except FileNotFoundError:
			print("Error al abrir el archivo")
			
		for item in yt_initial_data['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents']:
			if 'shelfRenderer' in item['itemSectionRenderer']['contents'][0]:
				for video in item['itemSectionRenderer']['contents'][0]['shelfRenderer']['content']['expandedShelfContentsRenderer']['items']:
					videos.append((video['videoRenderer']['title']['runs'][0]['text']))
      
		return videos


	#Funcion que recibe como parametro una categoria de YouTube y te devuelve una lista de videos con sus 
	#elementos.
	def get_video_category(self, categoria):
		videos = []
		driver = webdriver.Chrome(options=chrome_options)
		driver.get("https://www.youtube.com/feed/trending")
		tab_element = driver.find_element(By.XPATH, f"//*[text()='{categoria}']")
		tab_element.click()
		sleep(1)
		self.scroll_to_bottom(driver)
		sleep(1)
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
  
		video_elements = soup.find_all('ytd-video-renderer', {'class': 'style-scope ytd-expanded-shelf-contents-renderer'})
		
		for video_element in video_elements:
			
			#el id del video lo obtengo de la url, este if es para incorporar tambien los "yt shorts".
			video_url = video_element.find('a', {'id': 'thumbnail'})["href"]
			if "/watch" in video_url:
				video_id = video_element.find('a', {'id': 'thumbnail'})["href"].split("v=")[1].split("&")[0]
			elif "/shorts/" in video_url:
				video_id = video_id = video_url.split("/shorts/")[1]
    
			video = {
				"video_id": video_id,
				"title": video_element.find('a', {'id': 'video-title'}).text.strip(),
				"channel_name": video_element.find('a', {'class': 'yt-simple-endpoint style-scope yt-formatted-string'}).text.strip(),
				"description": video_element.find('yt-formatted-string', {'id': 'description-text'}).text.strip(),
				"view_count": video_element.find('span', {'class': 'inline-metadata-item style-scope ytd-video-meta-block'}).text.strip(),
				"length": video_element.find('span', {'class': 'style-scope ytd-thumbnail-overlay-time-status-renderer'}).text.strip(),
				"tab": categoria
			}
			
			videos.append(video)
			
		driver.close()
		return videos
		
  
	
	#Esta funcion se encarga de recibir el driver con la url de la pagina web y hacer "scroll" hasta el fin
	#de la pagina para poder cargar todo su contenido.
	def scroll_to_bottom(self, driver):
		scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
		while True:
			driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
			sleep(1)
			new_scroll_height = driver.execute_script("return document.documentElement.scrollHeight")
			if new_scroll_height == scroll_height:
				break
			scroll_height = new_scroll_height
	

   
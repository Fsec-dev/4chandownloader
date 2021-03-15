#!/usr/bin/env python3
# Creado por Andrew
import os, sys, random, math
import requests, re
from bs4 import BeautifulSoup

# Eligiendo un User Agent Aleatoriamente
def randomUA():
	UA = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
		  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5',
		  'Mozilla/5.0 (X11; FreeBSD amd64; rv:40.0) Gecko/20100101 Firefox/40.0',
		  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.49 Safari/537.36 OPR/48.0.2685.7',
		  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
		  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
		  'Mozilla/5.0 (Linux; Android 7.0; PLUS Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36']
		  
	return random.choice(UA)
	
# Convirtiendo los bytes a tamaño de archivo leible para humanos
def convertSize(size):
   if (size == 0):
       return '0 Bytes'
   size_name = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   return '{} {}'.format(s,size_name[i])

# Descargando imagenes
def downloader(urlfile):
	try:
		s = 256
		r = requests.get(urlfile, headers={"User-Agent":randomUA()}, stream=True)
		fsize = r.headers['content-length'] # Obteniendo el tamaño del fichero (Bytes)
		fname = urlfile.split("/")[-1] # Obteniendo el nombre del fichero

		with open(fname, 'wb') as f:
			for chunk in r.iter_content(chunk_size=s):
				f.write(chunk)
		
		print ("\n[+] Archivo: {} Tamaño: {} descargado\n".format(fname, format(convertSize(float(fsize)))))

	except Exception as ex:
		print("Ooops!! ha ocurrido un error: " + str(ex))
		exit(-1)

# Funcion encargada de recolectar las URL de las imagenes
def getURL(url, fileext):
	# Obteniendo el nombre del hilo para crear el directorio donde se guardaran los ficheros
	outdir = url.split('/')[-1] + "/"

	print ("\n[+] Conectando con el servidor...")
	r = requests.get(url, headers={"User-Agent":randomUA()})

	print ("[+] Lo descargado se guardara en el directorio: " + outdir)
	
	if not os.path.exists(outdir):
		os.mkdir(outdir) # Crear directorio donde se guardara los ficheros
		os.chdir(outdir) # Cambiar la ruta en el directorio creado 
	else:
		print ("[!] El directorio {} ya existe".format(outdir))

	if (r.status_code != 200):
		print("Error: %s"%(r.status_code))
	else:
		# Obtener el codigo fuente de la pagina
		sHTML = r.text
		# Obteniendo etiquetas con los ficheros
		soup = BeautifulSoup(sHTML, 'html.parser')
		files = soup.find_all("a", {"href":re.compile("."+fileext)})
		
		for _files in files:
			downloader("https:" + _files.get("href"))
			
if __name__ == "__main__":
	if len(sys.argv) < 3:
		os.system('clear')
		print ("\n\t[ 4ChanDownloader v0.1 ]\n")
		print ("\nInfo: Descarga de Imagenes(png, jpg, gif) y Videos de 4Chan")
		print("\nAyuda: %s <URL> <formato de fichero>\n"%(sys.argv[0]))
	else:
		getURL(sys.argv[1], sys.argv[2])

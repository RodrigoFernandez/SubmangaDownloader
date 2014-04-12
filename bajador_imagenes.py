#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from BeautifulSoup import BeautifulSoup
import re
import os
import zipfile
import shutil
import time
import random


def zipeador(carpeta_origen, carpeta_destino, nombre_zip):
	destino_zip = zipfile.ZipFile(os.path.join(carpeta_destino, nombre_zip), "w", zipfile.ZIP_DEFLATED)
	for archivo in os.listdir(carpeta_origen):
		ruta_completa = os.path.join(carpeta_origen, archivo)
		if os.path.isdir(ruta_completa):
			continue
		destino_zip.write(ruta_completa, archivo)
	destino_zip.close()
	
def bajar_codigo_pagina(url):
	return urllib.urlopen(url).read()

def bajar_imagen(url_origen, nombre_destino, url_destino):
	print "Url origen: " + url_origen
	print "Destino: " + url_destino + '/' + nombre_destino
	urllib.urlretrieve(url_origen, url_destino + '/' + nombre_destino)

def pagina_beautifulsoup(url):
	return BeautifulSoup(bajar_codigo_pagina(url))

def obtener_siguiente_e_imagen(pagina_beautifulsoup):
	aux = BeautifulSoup(str(pagina_beautifulsoup.findAll('div')[0]))
	return (aux.a.attrs[0][1], aux.a.img.attrs[0][1])

def obtener_nombre_imagen(url_imagen):
	en_partes = url_imagen.split('/')
	return en_partes[len(en_partes) - 1]

def obtener_indicador(url):
	return url.split('/')[len(url.split('/')) - 2]

def obtener_url_para_descarga(url_capitulo):
	# Toma url_capitulo y genera la url correspondiente
	# reemplazando Naruto/<numero_capitulo> por una c.
	return 'c'.join(re.split('Naruto/\d*', url_capitulo))

def obtener_numero_capitulo(url_capitulo):
	# Toma el numero de capitulo de la url.
	return re.search('Naruto/\d*', url_capitulo).group().split('/')[1]

def crear_directorio_destino(raiz_dir_destino, nro_capitulo):
	nuevo_directorio = "%s/%s" % (raiz_dir_destino, nro_capitulo)
	os.mkdir(nuevo_directorio) #se crea el directorio
	return nuevo_directorio

def eliminar_directorio(directorio_a_eliminar):
	shutil.rmtree(directorio_a_eliminar, True)

def bajar_capitulo(raiz_dir_destino, url_capitulo): 
	print 'empieza'
	
	url = obtener_url_para_descarga(url_capitulo)
	
	nro_capitulo = obtener_numero_capitulo(url_capitulo)
	
	dir_destino = crear_directorio_destino(raiz_dir_destino, nro_capitulo)
	
	# Mientras0 no se haya descargado la ultima imagen.
	indicador = obtener_indicador(url)
	while not indicador.startswith('r'):
		print "Indicador: " + obtener_indicador(url)
		# 	se obtiene la url de la imagen se obtiene la url de la siguiente pagina
		siguiente_e_imagen = obtener_siguiente_e_imagen(pagina_beautifulsoup(url))
		nombre_img = obtener_nombre_imagen(siguiente_e_imagen[1])
		print "Se va a descargar la imagen: %s" % (nombre_img,)
		# 	se descarga la imagen
		bajar_imagen(siguiente_e_imagen[1], nombre_img, dir_destino)
		# 	se pasa a la siguiente url
		url = siguiente_e_imagen[0]
		time.sleep(random.choice([4,5,6]))
		indicador = obtener_indicador(url)
	
	zipeador(dir_destino, raiz_dir_destino, nro_capitulo)
	eliminar_directorio(dir_destino)
	
	print 'termina'
	return 0
	
if __name__ == '__main__':
	# La idea es tener el listado de los capitulos de naruto que me faltan bajar
	# Se lee la lista y por cada url se bajan las imagenes y se guardan en la
	# carpeta correspondiente al capitulo. Todo esto desde submanga.com
	bajar_capitulo('.', 'http://submanga.com/Naruto/568/140712')

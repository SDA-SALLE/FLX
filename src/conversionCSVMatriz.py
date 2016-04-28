#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Created by @ceapalaciosal
#Codigo bajo Creative Commons

from clasificacion import *
from wjsoncsv import *
import csv
import datetime
import numpy as np
import os


#Enlista los archivos CSV de la carpeta.
def listaCSV(direccion):
   	#Variable para la ruta al directorio
	path = os.path.join(direccion,'')
	#print direccion

	#Lista vacia para incluir los ficheros
	lstFilesEmissions = []

	#Lista con todos los ficheros del directorio:
	lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros
	datos = {}
	#Crea una lista de los ficheros que existen en el directorio y los incluye a la lista.
	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == ".csv"):
	        	lstFilesEmissions.append(nombreFichero+extension)

	print "El numero de archivos en CSV es: ", len(lstFilesEmissions)


	lectura(lstFilesEmissions, direccion, datos)

	#Hace promedio estacion, fecha, hora

	estacion = datos.keys()
	for est in estacion:
		fechas = datos[est].keys()
		primerDia =  datos[est][fechas[0]]

		#print primerDia

		for i in range(1, len(fechas)):
			datosDia = datos[est][fechas[i]]
			keys = datosDia.keys()
			for key in keys:
				datosHora = datosDia[key]
				types = datosHora.keys()			
				for tipo in types:
					primerDia[key][tipo] += datosHora[tipo]		
		

		hora = primerDia.keys()

		for hour in hora: 
			flows =  primerDia[hour].keys()
			
			for flow in flows:
				primerDia[hour][flow] = primerDia[hour][flow]/len(fechas)


		datos[est] = primerDia
		
		for hour in hora: 
			flows =  primerDia[hour].keys()
			suma = 0
			for flow in flows:
				suma +=  primerDia[hour][flow]
			
			primerDia[hour]['TOTAL'] = suma

		datos[est] = primerDia

	write(datos, direccion)
	

#Lee los datos de cada archivo CSV y los pone en una matriz
def lectura(lstFilesEmissions, direccion, datos):
	tamano = len (lstFilesEmissions)

	for emissions in lstFilesEmissions[0:]:
		direccionuno = os.path.join(direccion,'') #Para linux cambiar por '/'
		direccioncsv = direccionuno + emissions
		matriz = np.genfromtxt(direccioncsv, delimiter='|', dtype=None)

		a = len(matriz) #Saca el tamano o longitud completa de la matriz
		tratamiento(matriz, a, datos)


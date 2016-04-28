#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#Created by @ceapalaciosal
#Codigo bajo Creative Commons
import json

#Limpieza de la matriz, descartando las filas y columnas que no se necesitan. 
def tratamiento(matriz, a, datos):
	
	dia = matriz[a-1,0]
	fecha = matriz[a-1,1]
	nodo = matriz[a-1,2]
	direccion = matriz[a-1,3]
	porDireccion = False
	

	vn = a-1
	

	head = matriz[2,:]
	colHora = 0  #indice de la columna del periodo
	colSentido = 0
	colData = 0
	colObservaciones = 0
	index = 0
	#print head
	for value in head:
		if value == "PERIODO" or value == "PERÍODO": #La columna del periodo(HORA...)
			colHora = index
		if value == "SENTIDO": #Aunque no se use, sirve para saber donde comienzan los datos
			colSentido = index
		if value == "OBSERVACIONES":
			colObservaciones=index #Marca el final de las columnas de datos
		index+=1

	colData = max(colHora, colSentido)+1 # Esto marca el comienzo de los datos
	matriz = matriz[3:vn,:]

	clasificaciondatos(matriz, dia, fecha, nodo, direccion, datos, head, colHora, colSentido, colData, colObservaciones)

def entero(numero):
	numero = float(numero)
	valor = int(numero)
	return valor

def clasificaciondatos(matriz, dia, fecha, nodo, direccion, datos, head, colHora, colSentido, colData, colObservaciones):

	sentt = sent1 = sent1B = sent2 = sent2B = sent3 = sent3B = sent4 = sent4B = 0
	tamano = len(matriz[:,1]) #Numero de filas

	cont = 0
	tamano = len(matriz[:,1]) #Numero de filas

	
	#Obtenemos la informacion del archivo 
	tipoDia = "HABIL" #No usar tildes. Se ve feo pero es mejor. Por eso se escibe el codigo fuente en ingles
	if dia in ["SABADO","DOMINGO"]:
		tipoDia = "NOHABIL"

	#Podria hacerse de muchas formas, pero yo voy a definir una llave compuesta asi:
	key = tipoDia+"_"+direccion+"_"+nodo

	if datos.get(key) is None:
		datos[key]={}
	
	entry = datos[key]

	if entry.get(fecha) is None:
		entry[fecha]={}


	entryFecha = entry[fecha]

	for i in range(0, tamano):
		#print i
		#print type(matriz[i, colHora])
		h = int(float(matriz[i, colHora])/100)
		sentido = matriz[i][colSentido]
		#Si no existe entrada para esta fecha y hora, creamos el objeto que la contendra
		if entryFecha.get(h) is None:
			entryFecha[h]={}
			for j in range(colData, colObservaciones-1):
				entryFecha[h][head[j]]=[]
			#entryFecha[h]['TOTAL'] = []

		for j in range(colData, colObservaciones-1):
			entryFecha[h][head[j]].append(matriz[i][j])
		#entryFecha[h]['TOTAL'].append('0')
		

		#Se saca el numero de sentidos contenidos en la colSentido
		if sentido == '1.0': 
			sent1 = 1
		if sentido == '1B':
			sent1B = 1
		if sentido == '2.0':
			sent2 = 1
		if sentido == '2B':
			sent2B = 1
		if sentido == '3.0':
			sent3 = 1
		if sentido == '3B': 
			sent3B = 1
		if sentido == '4.0':
			sent4 = 1
		if sentido == '4B': 
			sent4B = 1	

	sentt = sent1 + sent2 + sent3 + sent4 + sent1B + sent2B + sent3B + sent4B	
	keys = datos[tipoDia+"_"+direccion+"_"+nodo][fecha].keys()
	for key in keys:
		datosHora = datos[tipoDia+"_"+direccion+"_"+nodo][fecha][key]
		types = datosHora.keys()
		for tipo in types:
			datosHora[tipo] = eval('+'.join(datosHora[tipo]))/sentt

	#print datos[tipoDia+"_"+direccion+"_"+nodo][fecha][0]

#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
import csv
import json
import os
import xlrd
import numpy as np

def convertCSVMatriz(direccioncsv):
	matriz = np.genfromtxt(direccioncsv, delimiter=',', dtype=None)
	return  matriz


def convertXLSCSV(direccion):

	direccionexcel = direccion
	workbook = xlrd.open_workbook(direccionexcel)
	all_worksheets = workbook.sheet_names()
	data = workbook.sheet_by_index(0) #Numero de Sheet donde se encuentran los datos
	direccioncsv = direccionexcel + '.csv'
	data_emissions = open(''.join([direccioncsv]), 'wb') #crea el csv datos Base
	emissions = csv.writer(data_emissions, delimiter=',') #quoting=csv.QUOTE_ALL) #Abre el CSV para escritura de emsiones
 	for rownum in xrange(data.nrows):
 		#if(data.row_values(rownum)[0]!=0):
 		emissions.writerow([entry for entry in data.row_values(rownum)]) #unicode(entry).encode("utf-8")
 	data_emissions.close()
 	matriz = convertCSVMatriz(direccioncsv)
 	return matriz

def write(datos, folder):

	IDEstation = os.path.join("..","BD","IDNodos.xlsx")
	out = os.path.join("..", "out", "")
	IDEstation = convertXLSCSV(IDEstation)
	csvsalida = open(out + "promFinal.csv", 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	salida.writerow(["Estacion","Tipo","IDEstacion","IDNodo", "hora", '>C5', 'AL', 'AT', 'B', 'BA', 'BT', 'C', 'C2G', 'C2P', 'C3-C4', 'C5', 'ESP', 'INT', 'L', 'M', 'TOTAL'])

	estacion = datos.keys()
	for est in estacion:
		cont = 0
		for ray in est:
			if ray == "_":
				pos = cont 
			cont += 1
		pos = pos + 1	
		if "HABIL" in est: 
			day = est[:5]
			estacion = est[6:pos-1]
		else:
			day = est[:3]
			estacion = est[4:pos-1]
		
		IDNodo = est[pos:]

		
		for pos in range(1, len(IDEstation)):
			NNodo = int(float(IDEstation[pos][1]))
			if int(NNodo) == int(IDNodo): 
				NEstation = int(float(IDEstation[pos][0]))
				break

			

		hora = datos[est].keys()
		for hour in hora:
			flujos = []
			tipo = datos[est][hour].keys()
			tipo = sorted(tipo)
			#print tipo
			for tip in tipo:
				flujos.append(datos[est][hour][tip])
			csvsalida.write(estacion+","+day+","+str(NEstation)+","+IDNodo+","+str(int(float(hour)))+",")

			salida.writerow(flujos)
	csvsalida.close()			

	print "Proceso Finalizado, el archivo salida se encuentra en la carpeta: ", out

#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
from excelmatriz import *
from wcsv import *
import json
import os
import csv


def brinding(flows, links, noun):
	
	data = {}
	Mdata = convertXLSCSV(links)
	MFlows = convertCSVMatriz(flows)

	headData = Mdata[0,:] 
	headFlows = MFlows[0,:]
	
	index = 0
	for name in headData: 
		if name == 'FID_LINK': 
			colLinkID = index
		index += 1

	index = 0

	for name in headFlows:
		if name == 'IDEstacion':
			colIDEstation = index
		if name == 'hora':
			colhour = index
		if name == 'Tipo':
			colType = index
		index += 1

	for y in range(1, Mdata.shape[0]):

		FID = int(float(Mdata[y][colLinkID]))

		if data.get(FID) is None: 
			data[FID] = {}

		entrygrid =  data[FID]

		if entrygrid.get('link') is None:
			entrygrid['link'] = {}
		
		if entrygrid.get('flows') is None:
			entrygrid['flows'] = {}

		entryname = entrygrid['link']

		for x in range(1, Mdata.shape[1]):
			name = headData[x]
			if entryname.get(name) is None:
				entryname[name] = []

			entryname[name].append(Mdata[y][x])

	for y in range(1, MFlows.shape[0]):
		IDflowsEstation = int(float(MFlows[y][colIDEstation]))
		hr = MFlows[y][colhour]

		FID = data.keys()

		for ID in FID:
			
			IDdataEstation = int(float(data[ID]['link']['IDEstacion'][0]))

			if IDdataEstation == IDflowsEstation:
				typ = MFlows[y][colType]
				
				entryType = data[ID]['flows']
				
				if entryType.get(typ) is None: 
					entryType[typ] = {}

				entryhour = entryType[typ]

				if entryhour.get(hr) is None:
					entryhour[hr] = {}

				entryVehicle = entryhour[hr]


				for x in range(colhour+1, MFlows.shape[1]):
				 	headFlows = MFlows[0][x]
				 	if entryVehicle.get(headFlows) is None:
				 		entryVehicle[headFlows] = []
				
				 	entryVehicle[headFlows].append(MFlows[y][x])

	folder = os.path.join("..", 'data', 'datalink', '')
	#print data
	writebinding(folder, data, noun)

def brindingsecondary(flows, links):

	data = {}
	Mdata = convertXLSCSV(links)
	MFlows = convertCSVMatriz(flows)
	
	Intermedia = 0.37
	Local = 0.22
	Activity = ['L', 'C', 'ESP', 'M']
	ResidencialAct = 0.22
	NotActivity = [ 'B', 'C2P', 'BT', 'AL', 'AT', 'BA', 'INT', 'C2G', 'C3-C4', 'C5', '>C5']
	ResidencialNotAct = 0


	headData = Mdata[0,:] 
	headFlows = MFlows[0,:]
	#print headData
	
	index = 0
	for name in headData: 
		if name == 'FID_LINK': 
			colLinkID = index
		index += 1

	index = 0

	for name in headFlows:
		if name == 'IDEstacion':
			colIDEstation = index
		if name == 'hora':
			colhour = index
		if name == 'Tipo':
			colType = index
		index += 1

	for y in range(1, Mdata.shape[0]):

		FID = int(float(Mdata[y][colLinkID]))

		if data.get(FID) is None: 
			data[FID] = {}

		entrygrid =  data[FID]

		if entrygrid.get('link') is None:
			entrygrid['link'] = {}
		
		if entrygrid.get('flows') is None:
			entrygrid['flows'] = {}

		entryname = entrygrid['link']

		for x in range(1, Mdata.shape[1]):
			name = headData[x]
			if entryname.get(name) is None:
				entryname[name] = []

			entryname[name].append(Mdata[y][x])

	for y in range(1, MFlows.shape[0]):
		IDflowsEstation = int(float(MFlows[y][colIDEstation]))
		hr = MFlows[y][colhour]

		FID = data.keys()

		for ID in FID:
			
			IDdataEstation = int(float(data[ID]['link']['IDEstacion'][0]))

			if IDdataEstation == IDflowsEstation:
				typ = MFlows[y][colType]
				
				entryType = data[ID]['flows']
				
				if entryType.get(typ) is None: 
					entryType[typ] = {}

				entryhour = entryType[typ]

				if entryhour.get(hr) is None:
					entryhour[hr] = {}

				entryVehicle = entryhour[hr]


				for x in range(colhour+1, MFlows.shape[1]):
				 	headFlows = MFlows[0][x]
				 	if entryVehicle.get(headFlows) is None:
				 		entryVehicle[headFlows] = []
				
				 	entryVehicle[headFlows].append(MFlows[y][x])

	FID = data.keys()
	
	for ID in FID:
		clasifi = data[ID]['link']['CLASIFI_SU'][0]
		#print clasifi
		types = data[ID]['flows'].keys()
		for typ in types:
			hour = data[ID]['flows'][typ].keys()
			for hr in hour:
				namevehicle = sorted(data[ID]['flows'][typ][hr].keys())
				
				if clasifi == 'Local':
					for Vehicle in namevehicle: 
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * Local

				if clasifi == 'Intermedia':
					for Vehicle in namevehicle: 
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * Intermedia 

				if clasifi == 'Residencial':

					for Vehicle in Activity: 
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * ResidencialAct

					for Vehicle in NotActivity:
						data[ID]['flows'][typ][hr][Vehicle][0] = float(data[ID]['flows'][typ][hr][Vehicle][0]) * ResidencialNotAct


	folder = os.path.join("..", "data", "datalink", '')
	writebinding(folder, data, "secundary")

def brindingfinality(folderbrinding):
	
	folder2 = os.path.join('..', 'out', 'emissions', '')
	if 'wear' in folderbrinding:
		csvsalida1 = open (folder2 + 'emissionsHabilWear.csv', 'w')
		csvsalida2 = open (folder2 + 'emissionsNoHabilWear.csv', 'w')
	elif 'combustion' in folderbrinding:
		csvsalida1 = open (folder2 + 'emissionsHabilConbustion.csv', 'w')
		csvsalida2 = open (folder2 + 'emissionsNoHabilConbustion.csv', 'w')


	salida1 = csv.writer(csvsalida1, delimiter=',')
	salida2 = csv.writer(csvsalida2, delimiter=',')

	listHabil = []
	listNHabil = []
	
	#Lista con todos los ficheros del directorio:
	lstDir = os.walk(folderbrinding)   #os.walk()Lista directorios y ficheros
	datos = {}
	lstFilesEmissions = []
	
	#Crea una lista de los ficheros que existen en el directorio y los incluye a la lista.
	for root, dirs, files in lstDir:
	    for fichero in files:
	        (nombreFichero, extension) = os.path.splitext(fichero)
	        if(extension == ".csv"):
	        	lstFilesEmissions.append(nombreFichero+extension)
	
	#Clasificacion Archivos
	for name in lstFilesEmissions: 
		index = 0
		for l in name:
			if "_" == l:
				possub = index

			index += 1 
		
		if  "_Habil" in name:
			listHabil.append(name)
		elif "_NHabil" in name:
			listNHabil.append(name)

	cont = 0
	for name in listHabil:
		archive = folderbrinding + name 
		matriz = convertCSVMatriz(archive)
		if cont == 0:
			salida1.writerow(["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"])			
			cont += 1

		for i in range(1, matriz.shape[0]):
			cod = matriz[i][0] + matriz[i][1]
			salida1.writerow(matriz[i,:])

	csvsalida1.close()

	cont = 0
	for name in listNHabil:
		archive = folderbrinding + name 
		matriz = convertCSVMatriz(archive)

		if cont == 0:
			salida2.writerow(["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"])			
			cont += 1

		for i in range(1, matriz.shape[0]):
			salida2.writerow(matriz[i,:])

	csvsalida2.close()

def final(Archive):
	
	data = {}

	matriz = convertCSVMatriz(Archive)
	head = matriz[0,:]
	index = 0
	
	for value in head: 
		if value == 'ROW': 
			colROW = index
		if value == 'COL': 
			colCOL = index
		if value == 'LAT': 
			colLAT = index
		if value == 'LON':
			colLON = index
		if value == 'POLNAME':
			colPollname = index
		if value == 'UNIT':
			colUnit = index
		index += 1


	for i in range(1, matriz.shape[0]):
		keys = matriz[i][colROW] + matriz[i][colCOL] + matriz[i][colPollname]
		
		if data.get(keys) is None: 
			data[keys] = {}
			data[keys]['hours'] = {}
			data[keys]['GENERAL'] = {'ROW': [], 'COL': [], 'LAT': [], 'LON': [], 'POLNAME': [], 'UNIT':[]}

		
		for hour in range(0, 25):
			data[keys]['hours'][hour] = []

	
	for i in range(1, matriz.shape[0]):
		keys = matriz[i][colROW] + matriz[i][colCOL] + matriz[i][colPollname]
		if data[keys]['GENERAL']['ROW'] == []:
			data[keys]['GENERAL']['ROW'].append(matriz[i][colROW])
			data[keys]['GENERAL']['COL'].append(matriz[i][colCOL])
			data[keys]['GENERAL']['LAT'].append(matriz[i][colLAT])
			data[keys]['GENERAL']['LON'].append(matriz[i][colLON])
			data[keys]['GENERAL']['POLNAME'].append(matriz[i][colPollname])
			data[keys]['GENERAL']['UNIT'].append(matriz[i][colUnit])

		hour = 0
		for x in range(6, matriz.shape[1]):
			data[keys]['hours'][hour].append(matriz[i][x])
			hour += 1

	keys = data.keys()
	for key in keys: 
		hours = data[key]['hours'].keys()
		for hour in hours:
			if hour == 'GENERAL': 
				pass
			else:
				suma = eval('+'.join(data[key]['hours'][hour]))
				data[key]['hours'][hour] = []
				data[key]['hours'][hour].append(suma)

	
	csvsalida = open(Archive, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	salida.writerow(["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"])
	names = data.keys()

	for key in names: 
		csvsalida.write(data[key]['GENERAL']['ROW'][0])
		csvsalida.write(',')
		csvsalida.write(data[key]['GENERAL']['COL'][0])
		csvsalida.write(',')
		csvsalida.write(data[key]['GENERAL']['LAT'][0])
		csvsalida.write(',')
		csvsalida.write(data[key]['GENERAL']['LON'][0])
		csvsalida.write(',')
		csvsalida.write(data[key]['GENERAL']['POLNAME'][0])
		csvsalida.write(',')
		csvsalida.write(data[key]['GENERAL']['UNIT'][0])
		csvsalida.write(',')
		hours = data[key]['hours'].keys()
		for hour in hours:
			csvsalida.write(str(data[key]['hours'][hour][0]))
			csvsalida.write(',')
		csvsalida.write('\n')

	csvsalida.close ()






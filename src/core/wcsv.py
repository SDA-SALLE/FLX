#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
import csv
import os
import xlrd

def wcsv(data, name, folder):	
	csvsalida = open (folder + name, 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	
	if 'combustion' in folder:
		FEmissions = os.path.join('..', 'data', 'FEmition', 'FactoresEmision.xlsx')
	if 'wear' in folder:
		FEmissions = os.path.join('..', 'data', 'FEmition', 'FEBrake.xlsx')
	
	workbook = xlrd.open_workbook(FEmissions)
	names = workbook.sheet_by_index(1)

	listpollutant = []
	for pos in range (1, names.nrows):
		listpollutant.append(str(names.cell_value(pos, 0)))
	salida.writerow(["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"])
	ID_Grilla = data.keys()

	for ID in ID_Grilla:
		pollutant = data[ID]['pollutants'].keys()
		pollutant = pollutant[0]
		csvsalida.write(data[ID]['General']['ROW'][0])
		csvsalida.write(',')
		csvsalida.write(data[ID]['General']['COL'][0])
		csvsalida.write(',')
		csvsalida.write(data[ID]['General']['LAT'][0])
		csvsalida.write(',')
		csvsalida.write(data[ID]['General']['LON'][0])
		csvsalida.write(',')
		csvsalida.write(pollutant)
		csvsalida.write(',')
		if pollutant in listpollutant:
			csvsalida.write('mol/h')	
		else:
			csvsalida.write('g/h')
		csvsalida.write(',')
		hours = data[ID]['pollutants'][pollutant].keys()
		for hour in hours:
			csvsalida.write(str(data[ID]['pollutants'][pollutant][hour][0]))
			csvsalida.write(',')
		csvsalida.write(str(data[ID]['pollutants'][pollutant][0][0]))
		csvsalida.write('\n')

	csvsalida.close()

def writematriz(matriz, folder):

	csvsalida = open(folder + ".csv", 'w')
	salida = csv.writer(csvsalida, delimiter=',')#, quoting=csv.QUOTE_ALL

	for x in range(0, matriz.shape[0]):
		salida.writerow(matriz[x])

	csvsalida.close()

def writesum(data):
	folder = os.path.join("..", "data", "flows", '')
	csvsalida = open(folder +"sumcol.csv", 'w')
	salida = csv.writer(csvsalida, delimiter=',')

	salida.writerow(['Estacion', 'IDEstacion', 'IDNodo', '>C5', 'AL', 'AT', 'B', 'BA', 'BT', 'C', 'C2G', 'C2P', 'C3-C4', 'C5', 'ESP', 'INT', 'L', 'M', 'TOTAL', 'NH_>C5', 'NH_AL', 'NH_AT', 'NH_B', 'NH_BA', 'NH_BT', 'NH_C', 'NH_C2G', 'NH_C2P', 'NH_C3-C4', 'NH_C5', 'NH_ESP', 'NH_INT', 'NH_L', 'NH_M', 'NH_TOTAL'])

	IDEstation = data.keys()
	
	for ID in IDEstation: 

		flujos = sorted(data[ID]['HABIL'].keys())
		#print flujos

		for veh in range(0, 3):
			csvsalida.write(data[ID]['GENERAL'][veh])
			csvsalida.write(",")
		
		for vehicles in flujos:
				csvsalida.write(str(data[ID]['HABIL'][vehicles]))
				csvsalida.write(",")

		for vehicles in flujos:
				csvsalida.write(str(data[ID]['NOHAB'][vehicles]))
				csvsalida.write(",")
		csvsalida.write('\n')
	
	csvsalida.close()

def writebinding(folder, data, name):

	csvsalida = open(folder + name +"brinding.csv", 'w')
	namevehiclefull = ['FID','hora','>C5', 'AL', 'AT', 'B', 'BA', 'BT', 'C', 'C2G', 'C2P', 'C3-C4', 'C5', 'ESP', 'INT', 'L', 'M', 'TOTAL', 'NH_>C5', 'NH_AL', 'NH_AT', 'NH_B', 'NH_BA', 'NH_BT', 'NH_C', 'NH_C2G', 'NH_C2P', 'NH_C3-C4', 'NH_C5', 'NH_ESP', 'NH_INT', 'NH_L', 'NH_M', 'NH_TOTAL']
	
	FID = data.keys()

	cont = 0
	for ID in FID:
		nameslinks = data[ID]['link'].keys()

		namevehicle = sorted(data[ID]['flows']['HABIL']['0'].keys())
		hours = data[ID]['flows']['HABIL'].keys()

		if cont == 0:
			for name in nameslinks:
				csvsalida.write(name)
				csvsalida.write(',')

			rest = 0
			for name in namevehiclefull:
				if rest == 0:
					csvsalida.write(name)
					rest += 1
				else: 
					csvsalida.write(',')
					csvsalida.write(name)
			csvsalida.write('\n')

			cont += 1
	 	

		for hour in hours:

		 	for name in nameslinks:
		 		csvsalida.write(data[ID]['link'][name][0])
		 		csvsalida.write(',')
		 	csvsalida.write(str(ID))
		 	csvsalida.write(',')
		 	csvsalida.write(hour)
		 	csvsalida.write(',')

		 	for vehicle in namevehicle:
		 		csvsalida.write (str(data[ID]['flows']['HABIL'][hour][vehicle][0]))
		 		csvsalida.write(',')
		 	cont = 0
		 	for vehicle in namevehicle:
		 		if cont == 0:
		 			csvsalida.write (str(data[ID]['flows']['HABIL'][hour][vehicle][0]))
		 			cont += 1
		 		else:
		 			csvsalida.write(',')
		 			csvsalida.write (str(data[ID]['flows']['NOHAB'][hour][vehicle][0]))


		 	csvsalida.write('\n')

def writeemsions(data, name, pollutant, id): 

	name1 = name + "_" + pollutant + "_Habil"
	name2 = name + "_" + pollutant +"_NHabil"
	if id == 1: 
		folder = os.path.join("..", "out",'emissions', 'link', 'combustion', '')
	if id == 2:
		folder = os.path.join("..", "out",'emissions', 'link', 'wear', '')

	csvsalida1 = open(folder + name1 + ".csv", 'w')
	csvsalida2 = open(folder + name2 + ".csv", 'w')
	salida1 = csv.writer(csvsalida1, delimiter=',')
	salida2 = csv.writer(csvsalida2, delimiter=',')

	salida1.writerow(["FID_LINK", "FID_Grilla", "ROW", "COL", "LAT", "LON", "Contaminante", "Hora 0",'', "Hora 1",'', "Hora 2",'', "Hora 3",'', "Hora 4",'', "Hora 5",'', "Hora 6",'', "Hora 7",'', "Hora 8",'', "Hora 9",'', "Hora 10",'', "Hora 11",'', "Hora 12",'', "Hora 13",'', "Hora 14",'', "Hora 15",'', "Hora 16",'', "Hora 17",'', "Hora 18",'', "Hora 19",'', "Hora 20",'', "Hora 21",'', "Hora 22",'', "Hora 23",''])
	salida2.writerow(["FID_LINK", "FID_Grilla", "ROW", "COL", "LAT", "LON", "Contaminante", "Hora 0",'', "Hora 1",'', "Hora 2",'', "Hora 3",'', "Hora 4",'', "Hora 5",'', "Hora 6",'', "Hora 7",'', "Hora 8",'', "Hora 9",'', "Hora 10",'', "Hora 11",'', "Hora 12",'', "Hora 13",'', "Hora 14",'', "Hora 15",'', "Hora 16",'', "Hora 17",'', "Hora 18",'', "Hora 19",'', "Hora 20",'', "Hora 21",'', "Hora 22",'', "Hora 23",''])
	#hours = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
	
	FID_LINK = data.keys()

	for ID in FID_LINK:
		csvsalida1.write(str(int(float(ID))))
		csvsalida1.write(',')
		csvsalida1.write(str(data[ID]['General']['FID_Grilla'][0]))
		csvsalida1.write(',')
		csvsalida1.write(str(data[ID]['General']['ROW'][0]))
		csvsalida1.write(',')
		csvsalida1.write(str(data[ID]['General']['COL'][0]))
		csvsalida1.write(',')
		csvsalida1.write(str(data[ID]['General']['LAT'][0]))
		csvsalida1.write(',')
		csvsalida1.write(str(data[ID]['General']['LON'][0]))
		csvsalida1.write(',')
		csvsalida1.write(pollutant)
		csvsalida1.write(',')

		csvsalida2.write(str(int(float(ID))))
		csvsalida2.write(',')
		csvsalida2.write(str(data[ID]['General']['FID_Grilla'][0]))
		csvsalida2.write(',')
		csvsalida2.write(str(data[ID]['General']['ROW'][0]))
		csvsalida2.write(',')
		csvsalida2.write(str(data[ID]['General']['COL'][0]))
		csvsalida2.write(',')
		csvsalida2.write(str(data[ID]['General']['LAT'][0]))
		csvsalida2.write(',')
		csvsalida2.write(str(data[ID]['General']['LON'][0]))
		csvsalida2.write(',')
		csvsalida2.write(pollutant)
		csvsalida2.write(',')
		
		hours = data[ID]['pollutants'].keys()
		#print hours

		for hour in hours:
			if hour == 23:
				csvsalida1.write(str(data[ID]['pollutants'][hour]['Habil'][0]))
				csvsalida1.write(',')
				csvsalida1.write(str(data[ID]['pollutants'][hour]['Habil'][1]))

				csvsalida2.write(str(data[ID]['pollutants'][hour]['NHabil'][0]))
				csvsalida2.write(',')
				csvsalida2.write(str(data[ID]['pollutants'][hour]['NHabil'][1]))
			
			else:
				csvsalida1.write(str(data[ID]['pollutants'][hour]['Habil'][0]))
				csvsalida1.write(',')
				csvsalida1.write(str(data[ID]['pollutants'][hour]['Habil'][1]))
				csvsalida1.write(',')

				csvsalida2.write(str(data[ID]['pollutants'][hour]['NHabil'][0]))
				csvsalida2.write(',')
				csvsalida2.write(str(data[ID]['pollutants'][hour]['NHabil'][1]))
				csvsalida2.write(',')


		csvsalida1.write('\n')
		csvsalida2.write('\n')
	data = {}
	csvsalida1.close()	
	csvsalida2.close()

def PMC(data, noun, folder):

	if 'TIRE' in noun or 'BRAKE' in noun:
		folder = os.path.join('..', 'out', 'emissions', 'grid', 'PMC', 'Wear', '')
	else: 
		folder = os.path.join('..', 'out', 'emissions', 'grid', 'PMC', 'Combustion', '')
	#print folder
	csvsalida = open(folder + noun + '.csv', 'w')
	salida = csv.writer(csvsalida, delimiter=',')
	keys = data.keys()

	salida.writerow(["ROW", "COL", "LAT", "LON", "POLNAME", "UNIT", "E00h", "E01h", "E02h", "E03h", "E04h", "E05h", "E06h" ,"E07h", "E08h", "E09h", "E10h", "E11h", "E12h", "E13h", "E14h", "E15h", "E16h", "E17h", "E18h", "E19h", "E20h", "E21h", "E22h", "E23h", "E24h"])
	for key in keys: 
		csvsalida.write(str(int(data[key]['GENERAL']['ROW'][0])))
		csvsalida.write(',')
		csvsalida.write(str(int(data[key]['GENERAL']['COL'][0])))
		csvsalida.write(',')
		csvsalida.write(str(data[key]['GENERAL']['LAT'][0]))
		csvsalida.write(',')
		csvsalida.write(str(data[key]['GENERAL']['LON'][0]))
		csvsalida.write(',')
		csvsalida.write('PMC')
		csvsalida.write(',')
		if data[key]['GENERAL']['UNIT'][0] == 'mol/h':
			csvsalida.write('mol/s')
		if data[key]['GENERAL']['UNIT'][0] == 'g/h':
			csvsalida.write('g/s')
		hours = data[key]['hours'].keys()
		for hour in hours:
			csvsalida.write(',')
			csvsalida.write(str(data[key]['hours'][hour][0]))
		csvsalida.write('\n')
			
	csvsalida.close()
	


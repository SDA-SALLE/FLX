#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
from conversionExcelCSV import*
from conversionCSVMatriz import*


#Realiza operacion con archivo EXCEL

print ("Realizando Proceso para Fuentes Moviles")
folder = os.path.join("..", "data")


listaExcel (folder)
listaCSV(folder)
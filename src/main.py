#created by @ceapalaciosal
#under code Creative Commons
# -*- encoding: utf-8 -*-

#! /usr/bin/env python
from conversionExcelCSV import*
from conversionCSVMatriz import*
from disolver import*


#Realiza operacion con archivo EXCEL
folder = os.path.join("..", "data")


listaExcel (folder)
listaCSV(folder)
flows = os.path.join('..', 'out', 'promFinal.csv')
category = os.path.join ('..', 'BD', 'CATEGORY.xlsx')
disolver(flows, category)

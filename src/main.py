# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons
import sys
import os
sys.path.append('core')
from clear import *
from conversionExcelCSV import*
from conversionCSVMatriz import*
from disolver import*

folder = os.path.join('..', 'out', '')
clear(folder)

print ('Realizando Proceso para Fuentes Moviles')
folder = os.path.join('..', 'data')

listaExcel (folder)
listaCSV(folder)
flows = os.path.join('..', 'out', 'promFinal.csv')
category = os.path.join ('..', 'BD', 'CATEGORY.xlsx')
disolver(flows, category)

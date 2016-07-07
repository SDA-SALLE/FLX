# -*- encoding: utf-8 -*-

#! /usr/bin/env python
#created by @ceapalaciosal
#under code Creative Commons
import sys
import os
sys.path.append('core')
from clear import *
from ExcelCSV import*
from CSVMatriz import*
from disolver import*
from projection import *

folder = os.path.join('..', 'data','out', '')
clear(folder)

print ('Realizando Proceso para Fuentes Moviles')
folder = os.path.join('..', 'data', 'in', 'Flows', '')

listaExcel (folder)
listaCSV(folder)
flows = os.path.join('..', 'data', 'out', 'promFinal.csv')
category = os.path.join ('..', 'data', 'in','Constants', 'CATEGORY.xlsx')
disolver(flows, category)

flows = os.path.join('..', 'data', 'out', 'promFinal.csv')
projections = os.path.join('..', 'data','in', 'Projection', 'Resuspended_grow_factors.xlsx')
projection(flows, projections, 0)

flows = os.path.join('..', 'data', 'out', 'promFinal_2.csv')
projections = os.path.join('..', 'data','in', 'Projection', 'Movile_grow_factors.xlsx')
projection(flows, projections, 1)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 09:36:13 2022

@author: nicolastreps
"""

import pandas

mondict = {'ET1' : {('nom','nom'):'nom1', ('UE1', 'note1'):[10], ('UE1', 'note2'):[11]}, 'ET2' : {('nom','nom'):'nom2', ('UE1', 'note1'):[12], ('UE1', 'note2'):[13]}}
multdf = pandas.DataFrame(mondict)
multdfT=multdf.transpose()
#multdfT.to_csv(r'genessai.csv', index = True, header=True)
multdfT.to_csv(r'genessai.csv', index = True, header=True, sep=';')
multdfT.to_excel(r'genessai.xlsx', index = True, header=True)

readDF = pandas.read_excel(r'genessai.xlsx', index_col = 0, header=[0,1])
readdict2 = readDF.to_dict('index')

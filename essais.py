#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 09:36:13 2022

@author: nicolastreps
"""

import pandas
from stats_library import *

#mondict = {'ET1' : {('nom','nom'):'nom1', ('UE1', 'note1'):10, ('UE1', 'note2'):11}, 'ET2' : {('nom','nom'):'nom2', ('UE1', 'note1'):12, ('UE1', 'note2'):13}}
#multdf = pandas.DataFrame(mondict)
#multdfT=multdf.transpose()
####multdfT.to_csv(r'genessai.csv', index = True, header=True)
#multdfT.to_csv(r'genessai.csv', index = True, header=True, sep=';')
#multdfT.to_excel(r'genessai.xlsx', index = True, header=True)

#readDF = pandas.read_excel(r'genessai.xlsx', index_col = 0, header=[0,1])
#readdict2 = readDF.to_dict('index')

dico = GetDictionary(2021)

### Tester la fusion de 2 dicos
#dico2 = GetDictionary(2020)
#MergeDictionary(dico, dico2)

mescles = GetInnerKeys(dico)
lesparcours = GetParcours(dico)

### L2 Mono
NotesS1LU2PY103 = GetGrades(dico, lesparcours[4], mescles[9])

### bac 2020, L2 MONO
NotesS1LU2PY103_bac2020 = GetGradesKeycomp(dico, mescles[9], False, [mescles[1],2020],[mescles[113],lesparcours[4]])

NotesS1LU3PY101_LN = GetGradesKeycompLN(dico, 'LU3PY101', 3, 2021, ('annee_bac', 2019), ('bourse', 'oui'))

### Extraire une liste d'étudiants
dicoEtd = ExtractStudentsLN(dico, ('annee_bac', 2020), ('parcours', 'L2 SPRINT')) 


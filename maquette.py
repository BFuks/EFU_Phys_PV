##########################################################
###                                                    ###
###                Maquette  Apogee                    ###
###                                                    ###
###                Date: 21/01/2026                    ###
###                                                    ###
###                                                    ###
##########################################################

# Blocs
Blocs = {
    # Physique
    'LB3PYJ00': { 'nom': "MAJ", 'UE': [['UL2PY103', 'UL2PY110', 'UL2PY126']]},
    'LB3PY013': { 'nom': "MAJ", 'UE': [['UL2PY103', 'UL2PY110', 'UL2PY126']]},
    'LK3PYJ03': { 'nom': "MAJ", 'UE': [['LU2PY403', 'LU2PY410', 'LU2PY424', 'LU2LVAN1']]},
    'LK3PYJ05': { 'nom': "MAJ", 'UE': [['LU2PY103', 'LU2PY110', 'LU2PY125', 'LU2LVAN1']]},
    'LK3PYJ06': { 'nom': "MAJ", 'UE': [['LU2PY103', 'LU2PY222', 'LU2PY125', 'LU2LVAN1']]},
    'LB3PYC00': { 'nom': "CMP", 'UE': [['UL2PY212', 'UL2PY222']]},
    'LK3PYC00': { 'nom': "CMP", 'UE': [['LU2PY212', 'LU2PY220']]},
    'LK3PYC01': { 'nom': "CMP", 'UE': [['LU2PY212', 'LU2PY520','LU2PY531']], 'SX':['LU2PY531']},
    'LB4PYJ00': { 'nom': "MAJ", 'UE': [['UL2PY125', 'UL2PY130', 'UL2PY131', 'UL2PY210']]},
    'LB4PY013': { 'nom': "MAJ", 'UE': [['UL2PY125', 'UL2PY130', 'UL2PY131', 'UL2PY210']]},
    'LK4PYJ03': { 'nom': "MAJ", 'UE': [['LU2PY404', 'LU2PY421', 'LU2PY423']]},
    'LK4PYJ05': { 'nom': "MAJ", 'UE': [['LU2PY126', 'LU2PY121', 'LU2PY123'],['LU2PY104','LU2PY121','LU2PY123']]},
    'LK4PYJ06': { 'nom': "MAJ", 'UE': [['LU2PY126', 'LU2PY121', 'LU2PY215']]},
    'LK4PYJ11': { },
    'LB4PYC00': { 'nom': "CMP", 'UE': [['UL2PY215', 'UL2PY216', 'UL2LVAN2']]},
    'LK4PYC00': { 'nom': "CMP", 'UE': [['LU2PY215', 'LU2PY222']]},
    'LK4PYC01': { 'nom': "CMP", 'UE': [['LU2PY215', 'LU2PY222','LU2PY532']], 'SX':['LU2PY532']},
    'LK5PYJ00': { 'nom': "MAJ", 'UE': [['LU3PY101', 'LU3PY121', 'LU3PYOIP']]},
    'LK5PYJ01': { 'nom': "MAJ", 'UE': [['LU3PY401', 'LU3PY421', 'LU3PYOIP']]},
    'LK5PYC00': { 'nom': "CMP", 'UE': [['LU3PY213', 'LU3PY214', 'LU3PY215']]},
    'LK5PYC01': { 'nom': "CMP", 'UE': [['LU3PY513', 'LU3PY514', 'LU3PY215', 'LU3PY536']], 'SX': ['LU3PY536']},
    'LK6PYJ00': { 'nom': "MAJ", 'UE': [['LU3PY103','LU3PY111','LY6PY120','LU3LVAN2']] },
    'LK6PYJ01': { 'nom': "MAJ", 'UE': [['LU3PY403','LU3PY411','LY6PY120','LU3LVAN2']] },
    'LK6PYJ30': { 'nom': "MAJ", 'UE': [['LU3PY403','LU3PY411','LU3MA120','LU3LVAN2'], ['LU3PY103','LU3PY111','LU3ST061','LU3LVAN2'],
        ['LU3PY103','LU3PY111','LU3ST062','LU3LVAN2'], ['LU3PY103','LU3PY111','LU3CI121','LU3LVAN2'],
        ['LY6PY120','LU3PY111','LU3ME010','LU3LVAN2'], ['LU3PY103','LU3PY111','LU3PY537','LU3LVAN2'],
        ['LY6PY120','LU3PY111','LU3EE203','LU3LVAN2']]},
    'LK6PYC00': { 'nom': "CMP", 'UE': [['LY6PY220','LU3PY205']] },
    'LK6PYC02': { 'nom': "CMP", 'UE': [ ['LU3PY238', 'LU3PY205'], ['LU3PY238', 'LU3PY206'],
          ['LU3PY235', 'LU3PY205'], ['LU3PY235', 'LU3PY206'], ['LU3PY234', 'LU3PY205'], ['LU3PY234', 'LU3PY206'],
          ['LU3PY233', 'LU3PY205'], ['LU3PY233', 'LU3PY206'], ['LU3PY232', 'LU3PY205'], ['LU3PY232', 'LU3PY206'],
          ['LY5PY090', 'LU3PY206']] },
    'LK6PYC01': { 'nom': "CMP", 'SX': ['LU3PY537'], 'UE': [ ['LU3PY238', 'LU3PY205', 'LU3PY537'],
          ['LU3PY235', 'LU3PY205', 'LU3PY537'], ['LU3PY234', 'LU3PY205', 'LU3PY537'],
          ['LU3PY233', 'LU3PY205', 'LU3PY537'], ['LU3PY232', 'LU3PY205', 'LU3PY537'] ] },

     # Mineures
    'LK5CHM00': { 'nom': "MIN", 'UE': [['L5LACHCI','L5LACHLA']]},
    'LK6CHM00': { 'nom': "MIN", 'UE': [['L6LACHCI','L6LACHLA']]},
    'LK3CIM00': { 'nom': "MIN", 'UE': [['LU2CI012','LU2CI011']]},
    'LK4CIM00': { 'nom': "MIN", 'UE': [['LU2CI101','LU2CI102']]},
    'LK5CIM00': { 'nom': "MIN", 'UE': [['LU3CI052','LU3CI011']]},
    'LK6CIM00': { 'nom': "MIN", 'UE': [['LU3CI141','LU3CI113']]},
    'LK3DSM00': { 'nom': "MIN", 'UE': [['LU2DS001']]},
    'LK4DSM00': { 'nom': "MIN", 'UE': [['LU2DS002','LU2DS003']]},
    'LK5DSM00': { 'nom': "MIN", 'UE': [['LU3DS001','LU3DS002','LU3DS003']]},
    'LK6DSM00': { 'nom': "MIN", 'UE': [['LU3DS004','LU3DS005']]},
    'LK3EVM00': { 'nom': "MIN", 'UE': [['LU2EVE01','LU2EVE02','LU2EVE03']]},
    'LK4EVM00': { 'nom': "MIN", 'UE': [['LU2EVE04','LU2EVE05']]},
    'LK3EEM00': { 'nom': "MIN", 'UE': [['LU2EE100','LU2EE200']]},
    'LK4EEM00': { 'nom': "MIN", 'UE': [['LU2EE204','LU2EE201']]},
    'LK5EEM00': { 'nom': "MIN", 'UE': [['LU3EE100','LU3EE101']]},
    'LK6EEM00': { 'nom': "MIN", 'UE': [['LU3EE200','LU3EE204']]},
    'LK5EVM00': { 'nom': "MIN", 'UE': [['LU3EV001','LU3EV002','LU3EV003']]},
    'LK6EVM00': { 'nom': "MIN", 'UE': [['LU3EV004']]},
    'LK3GSM00': { 'nom': "MIN", 'UE': [['LU2GSG31','LU2GSG32']]},
    'LK4GSM00': { 'nom': "MIN", 'UE': [['LU2GSG41','LU2GSG42']]},
    'LK3HNM00': { 'nom': "MIN", 'UE': [['LU2HNP31','LU2HNP32','LU2HNP33','LU2HNP41']]},
    'LK4HNM00': { 'nom': "MIN", 'UE': [['LU2HNP34','LU2HNP42','LU2HNP43']]},
    'LK5IAM00': { 'nom': "MIN", 'UE': [['LU3IAS53','LU3IAS54']]},
    'LK6IAM00': { 'nom': "MIN", 'UE': [['LU3IAS61']]},
    'LK3INM00': { 'nom': "MIN", 'UE': [['LU2IN005','LU2IN018','LU2IN019']]},
    'LK4INM00': { 'nom': "MIN", 'UE': [['LU2IN003','LU2IN014']]},
    'LK5INM00': { 'nom': "MIN", 'UE': [['LU2IN002','LU2IN015','LU3IN006']]},
    'LK6INM00': { 'nom': "MIN", 'UE': [['LU2IN009','LU2IN023']]},
    'LK3MAM00': { 'nom': "MIN", 'UE': [['LU2MA221','LU2MA260']]},
    'LK4MAM00': { 'nom': "MIN", 'UE': [['LU2MA122','LU2MA241']]},
    'LK5MAM00': { 'nom': "MIN", 'UE': [['LU2MA216','LU2MA220']]},
    'LK6MAM00': { 'nom': "MIN", 'UE': [['LU2MA236','LU2MA100'], ['LU2MA100','LU2MA211']]},
    'LK3MEM02': { 'nom': "MIN", 'UE': [['LU2ME001','LU2ME005']]},
    'LB3MEM00': { 'nom': "MIN", 'UE': [['UL2ME001','UL2ME006']]},
    'LK3MEM03': { 'nom': "MIN", 'UE': [['LU2ME001','LU2ME006']]},
    'LB4MEM00': { 'nom': "MIN", 'UE': [['UL2ME004']]},
    'LK4MEM04': { 'nom': "MIN", 'UE': [['LU2ME004','LU2ME102']]},
    'LK4MEM06': { 'nom': "MIN", 'UE': [['LU2ME004','LU2ME102']]},
    'LK5MEM00': { 'nom': "MIN", 'UE': [['LU3ME103','LU3ME004']]},
    'LK5MEM02': { 'nom': "MIN", 'UE': [['LU3ME103','LU3ME004']]},
    'LK6MEM00': { 'nom': "MIN", 'UE': [['LU3ME105','LU3ME007'], ['LU3MEE01','LU3ME007'],  ['LU3ME108','LU3ME007'],  ['LU3ME111','LU3ME007']]},
    'LK6MEM03': { 'nom': "MIN", 'UE': [['LU3ME105','LU3ME006']]},
    'LK3PHM00': { 'nom': "MIN", 'UE': [['L3PHM011','L3PHM02C']]},
    'LK4PHM00': { 'nom': "MIN", 'UE': [['L4PHM02E','L4PHM03A']]},
    'LK3PTM00': { 'nom': "MIN", 'UE': [['LU2PT001','LU2PT003']]},
    'LK4PTM00': { 'nom': "MIN", 'UE': [['LU2PT005','LU2PT007']]},
    'LK3STM01': { 'nom': "MIN", 'UE': [['LU2ST303','LU2ST302','LU2ST321'], ['LU2ST301','LU2ST303','LU2ST035']]},
    'LK3STM00': { },
    'LK4STM00': { 'nom': "MIN", 'UE': [['LU2ST045','LU2ST043','LU2ST044'], ['LU2ST421','LU2ST403']]},
    'LK4STM02': { 'nom': "MIN", 'UE': [['LU2ST421','LU2ST403']]},
    'LK5STM00': { 'nom': "MIN", 'UE': [['LU3ST057','LU3ST059']]},
    'LK6STM01': { 'nom': "MIN", 'UE': [['LU3ST061','LU3ST066']]},

    # Double majeure
    'LK5CID00': { 'nom':'MAJ2', 'UE': [['LU3CI032','LU3CI011','LU3CI035','LU3CI003']], 'SX':['LU3CI003', 'LU3CI035']},
    'LK6CID00': { 'nom':'MAJ2', 'UE': [['LU3CI113', 'LU3CI101','LY6PY120']], 'SX':['LU3CI101']},
    'LK5EED00': { 'nom':'MAJ2', 'UE': [['LU3EE100','LU3EE101','LU3EE105']], 'SX':['LU3EE105']},
    'LK6EED00': { 'nom':'MAJ2', 'UE': [['LU3EE200','LU3EE204','LU3EE210','LY6PY120']], 'SX':['LU3PY122', 'LU3PY124', 'LU3PY126', 'LU3PY105']},
    'LK5MAD00': { 'nom':'MAJ2', 'UE': [['LU3MA260','LU3MA263','LU3MA232']], 'SX':['LU3MA232']},
    'LK6MAD00': { 'nom':'MAJ2', 'UE': [['LY6PY120','LU3MA210','LU3MA290'], ['LY6PY120','LU3MA210','LU3MA261']], 'SX':['LU3MA290', 'LU3MA261'] },
    'LK5MED00': { 'nom':'MAJ2', 'UE': [['LU3ME103', 'LU3ME004', 'LU3ME008']], 'SX':['LU3ME008']},
    'LK6MED00': { 'nom':'MAJ2', 'UE': [['LU3ME006','LU3ME007','LU3ME009']], 'SX':['LU3ME009']},
    'LK5IND00': { 'nom':'MAJ2', 'UE': [['LU3IN029','LU3IN033','LU3IN003']], 'SX':['LU3IN003']},
    'LK6IND00': { 'nom':'MAJ2', 'UE': [['LU2IN024','LU3IN010','LU3IN024']], 'SX':['LU3IN024']},
    'LK5STD00': { 'nom':'MAJ2', 'UE': [['LU3ST057', 'LU3ST059', 'LU3ST507']], 'SX':['LU3ST507']},
    'LK6STD00': { 'nom':'MAJ2', 'UE': [['LU3ST060', 'LU3ST603', 'LU3ST605', 'LY6PY120']], 'SX':['LU3PY122', 'LU3PY124', 'LU3PY126', 'LU3PY105']}
}

Listes = {
    'LY6PY120':['LU3PY122', 'LU3PY124', 'LU3PY126', 'LU3PY105'],
    'LY6PY220':['LU3PY231', 'LU3PY232', 'LU3PY233', 'LU3PY234', 'LU3PY235'],
    'LY5PY090':[]
}



# Liste des UE avec le nombre de credits
UEs = {
  # L2 Phys
  'LU2PY041': {'ects': 6, 'nom':'PhysActn'},
  'LU2PY103': {'ects': 6, 'nom':'Thermo'  },   'UL2PY103': {'ects': 6, 'nom':'Thermo'  },
  'LU2PY104': {'ects': 6, 'nom':'Meca'    },
  'LU2PY110': {'ects': 6, 'nom':'Math-S3' },   'UL2PY110': {'ects': 6, 'nom':'Maths 1' },
  'LU2PY121': {'ects':12, 'nom':'OEM'     },
  'LU2PY123': {'ects': 3, 'nom':'Math-S4' },
  'LU2PY124': {'ects': 3, 'nom':'Relat'   },
  'LU2PY125': {'ects': 3, 'nom':'Climat'  },   'UL2PY125': {'ects': 3, 'nom':'Climat'  },
  'LU2PY126': {'ects': 6, 'nom':'MecaRel' },   'UL2PY126': {'ects': 6, 'nom':'MecaRel' },
                                               'UL2PY130': {'ects': 6, 'nom':'Ondes'   },
                                               'UL2PY131': {'ects': 6, 'nom':'Elctrmag'},
  'LU2PY215': {'ects': 3, 'nom':'PhysExp2'},   'UL2PY215': {'ects': 3, 'nom':'PhysExp2'},
                                               'UL2PY216': {'ects': 3, 'nom':'CmplPhys'},
  'LU2PY212': {'ects': 6, 'nom':'PhysExp1'},   'UL2PY212': {'ects': 6, 'nom':'PhysExp1'},
  'LU2PY220': {'ects': 6, 'nom':'MathCmp' },   'UL2PY210': {'ects': 6, 'nom':'Maths 2' },
  'LU2PY222': {'ects': 6, 'nom':'PhysNum' },   'UL2PY222': {'ects': 6, 'nom':'PhysNum' },
  'LU2PY403': {'ects': 6, 'nom':'Thermo'  },
  'LU2PY404': {'ects': 6, 'nom':'MecaRel' },
  'LU2PY410': {'ects': 6, 'nom':'Math-S3' },
  'LU2PY421': {'ects':12, 'nom':'OEM'     },
  'LU2PY423': {'ects': 3, 'nom':'Math-S4' },
  'LU2PY424': {'ects': 3, 'nom':'Relat'   },
  'LU2PY520': {'ects': 6, 'nom':'MathCmp' },
  'LU2PY531': {'ects': 6, 'nom':'Astro'   },
  'LU2PY532': {'ects': 6, 'nom':'ML'      },

  # L3 Phys
  'LU3PY024': {'ects': 6, 'nom':'ProjAutn'},
  'LU3PY206': {'ects': 3, 'nom':'HistMeca'},
  'LU3PY101': {'ects': 6, 'nom':'PhysQ1'  },
  'LU3PY103': {'ects': 6, 'nom':'Thermo'  },
  'LU3PY105': {'ects': 6, 'nom':'Stage'   },
  'LU3PY111': {'ects': 6, 'nom':'PhysQ2'  },
  'LU3PY121': {'ects': 9, 'nom':'OEM'     },
  'LU3PY122': {'ects': 6, 'nom':'ProjNmXp'},
  'LU3PY126': {'ects': 6, 'nom':'ProjNum' },
  'LU3PY124': {'ects': 6, 'nom':'ProjNmXp'},
  'LU3PY205': {'ects': 3, 'nom':'Stage'   },
  'LU3PY213': {'ects': 3, 'nom':'Math-S5' },
  'LU3PY214': {'ects': 6, 'nom':'MilCont' },
  'LU3PY215': {'ects': 3, 'nom':'PhysExp3'},
  'LU3PY231': {'ects': 6, 'nom':'Matiere' },
  'LU3PY232': {'ects': 6, 'nom':'Astro'   },
  'LU3PY233': {'ects': 6, 'nom':'PhysTheo'},
  'LU3PY234': {'ects': 6, 'nom':'OcnAtm'  },
  'LU3PY235': {'ects': 6, 'nom':'MecaAnl' },
  'LU3PY401': {'ects': 6, 'nom':'PhysQ1'  },
  'LU3PY403': {'ects': 6, 'nom':'Thermo'  },
  'LU3PY411': {'ects': 6, 'nom':'PhysQ2'  },
  'LU3PY421': {'ects': 9, 'nom':'OEM'     },
  'LU3PY513': {'ects': 3, 'nom':'Math-S5' },
  'LU3PY514': {'ects': 6, 'nom':'MilCont' },
  'LU3PY536': {'ects': 6, 'nom':'MecaRel' },
  'LU3PY537': {'ects': 6, 'nom':'InfoQ'   },
  'LU3PYOIP': {'ects': 3, 'nom':'OIP'     },

  # Autres Departements
  'LU2CI011': {'ects': 6, 'nom':'Thermo'  },
  'LU2CI012': {'ects': 6, 'nom':'ChimInrg'},
  'LU2CI101': {'ects': 3, 'nom':'Liaisons'},
  'LU2CI102': {'ects': 6, 'nom':'ChimOrga'},
  'LU3CI003': {'ects': 3, 'nom':'Polymrs' },
  'LU3CI011': {'ects': 6, 'nom':'Elctroch'},
  'LU3CI032': {'ects': 6, 'nom':'ChiMolec'},
  'LU3CI035': {'ects': 3, 'nom':'ChmMolec'},
  'LU3CI052': {'ects': 6, 'nom':'ChiMolec'},
  'LU3CI101': {'ects': 6, 'nom':'McaQSpct'},
  'LU3CI113': {'ects': 6, 'nom':'MatInorg'},
  'LU3CI121': {'ects': 3, 'nom':'CaractAv'},
  'LU3CI141': {'ects': 3, 'nom':'AnaStrct'},
  'LU2DS001': {'ects':12, 'nom':'ScDnnees'},
  'LU2DS002': {'ects': 6, 'nom':'DataBDD' },
  'LU2DS003': {'ects': 3, 'nom':'StatProb'},
  'LU3DS001': {'ects': 3, 'nom':'StatsInf'},
  'LU3DS002': {'ects': 6, 'nom':'ScDnnees'},
  'LU3DS003': {'ects': 3, 'nom':'ResNeur' },
  'LU3DS004': {'ects': 6, 'nom':'Projet'  },
  'LU3DS005': {'ects': 3, 'nom':'Ethique' },
  'LU2EE100': {'ects': 6, 'nom':'ElecAnNm'},
  'LU2EE200': {'ects': 6, 'nom':'NrgCapt '},
  'LU2EE201': {'ects': 6 ,'nom':'Maths'   },
  'LU2EE204': {'ects': 3, 'nom':'InterfAN'},
  'LU3EE100': {'ects': 6, 'nom':'Electr3' },
  'LU3EE101': {'ects': 6, 'nom':'SignlSys'},
  'LU3EE105': {'ects': 6, 'nom':'ImgSons' },
  'LU3EE200': {'ects': 6, 'nom':'Electr4' },
  'LU3EE203': {'ects': 3, 'nom':'TrtAnalg'},
  'LU3EE204': {'ects': 3, 'nom':'MicrCtrl'},
  'LU3EE210': {'ects': 3, 'nom':'ElctrMg4'},
  'LU2EVE01': {'ects': 3, 'nom':'HstEnv'  },
  'LU2EVE02': {'ects': 3, 'nom':'ChgtClm1'},
  'LU2EVE03': {'ects': 6, 'nom':'EnjBioDv'},
  'LU2EVE04': {'ects': 3, 'nom':'ChgtClm2'},
  'LU2EVE05': {'ects': 6, 'nom':'StagePrj'},
  'LU3EV001': {'ects': 3, 'nom':'UrbAgri' },
  'LU3EV002': {'ects': 3, 'nom':'Energie' },
  'LU3EV003': {'ects': 6, 'nom':'Vivant'  },
  'LU3EV004': {'ects': 9, 'nom':'StagePrj'},
  'LU2GSG31': {'ects': 6, 'nom':'Entreprs'},
  'LU2GSG32': {'ects': 6, 'nom':'Economie'},
  'LU2GSG41': {'ects': 6, 'nom':'Entreprs'},
  'LU2GSG42': {'ects': 3, 'nom':'Compta'  },
  'LU2HNP31': {'ects': 3, 'nom':'AnthrBio'},
  'LU2HNP32': {'ects': 3, 'nom':'LngstPop'},
  'LU2HNP33': {'ects': 3, 'nom':'PatrmLoc'},
  'LU2HNP41': {'ects': 3, 'nom':'MilHmPre'},
  'LU2HNP34': {'ects': 3, 'nom':'Deplcmnt'},
  'LU2HNP42': {'ects': 3, 'nom':'PaleoPsg'},
  'LU2HNP43': {'ects': 3, 'nom':'Primato' },
  'LU3IAS53': {'ects': 3, 'nom':'PatSoign'},
  'LU3IAS54': {'ects': 9, 'nom':'RechMedc'},
  'LU3IAS61': {'ects': 9, 'nom':'Semantiq'},
  'LU2IN002': {'ects': 6, 'nom':'ProgObj1'},
  'LU2IN003': {'ects': 6, 'nom':'Algo'    },
  'LU2IN005': {'ects': 6, 'nom':'MathDisc'}, #'SX':True
  'LU2IN014': {'ects': 3, 'nom':'ArchOrdi'},
  'LU2IN009': {'ects': 6, 'nom':'BaseDonn'},
  'LU2IN015': {'ects': 3, 'nom':'SysExpl' },
  'LU2IN018': {'ects': 3, 'nom':'CAvancé' },
  'LU2IN019': {'ects': 3, 'nom':'ProgFctn'},
  'LU2IN023': {'ects': 3, 'nom':'Reseaux' },
  'LU2IN024': {'ects': 3, 'nom':'LogqSmPr'},
  'LU3IN003': {'ects': 6, 'nom':'Algo2'   },
  'LU3IN006': {'ects': 3, 'nom':'LogSmImp'},
  'LU3IN010': {'ects': 6, 'nom':'Systemes'},
  'LU3IN024': {'ects': 6, 'nom':'Crypto'  },
  'LU3IN029': {'ects': 6, 'nom':'Archi'   },
  'LU3IN033': {'ects': 6, 'nom':'Reseaux' },
  'LU2MA100': {'ects': 3, 'nom':'Python'  },
  'LU2MA122': {'ects': 3, 'nom':'AlgLin2' },
  'LU2MA211': {'ects': 6, 'nom':'Lebesgue'}, # 'SX':True
  'LU2MA221': {'ects': 6, 'nom':'AlgLin1' },
  'LU2MA216': {'ects': 6, 'nom':'Topo'    }, # 'SX':True
  'LU2MA220': {'ects': 6, 'nom':'Algebre' },
  'LU2MA236': {'ects': 6, 'nom':'EquaDiff'},
  'LU2MA241': {'ects': 6, 'nom':'Probas'  },
  'LU2MA260': {'ects': 6, 'nom':'SerieFct'},
  'LU3MA120': {'ects': 3, 'nom':'AlgArthm'},
  'LU3MA210': {'ects': 6, 'nom':'AnlsFct' },
  'LU3MA232': {'ects': 6, 'nom':'AnlNum'  },
  'LU3MA261': {'ects': 6, 'nom':'CalcDiff'},
  'LU3MA260': {'ects': 6, 'nom':'TCD2'    },
  'LU3MA263': {'ects': 6, 'nom':'MsrProba'},
  'LU3MA290': {'ects': 6, 'nom':'Probas2' },
  'LU2ME001': {'ects': 6, 'nom':'MecaSold'},   'UL2ME001': {'ects': 6, 'nom':'MecaSold'},
  'LU2ME004': {'ects': 6, 'nom':'Fluides1'},   'UL2ME004': {'ects': 6, 'nom':'Fluides1'},
  'LU2ME005': {'ects': 6, 'nom':'PrgClcSc'},
  'LU2ME006': {'ects': 6, 'nom':'AnlsVect'},   'UL2ME006': {'ects': 6, 'nom':'AnlsVect'}, # 'SX':True
  'LU3ME009': {'ects': 6, 'nom':'MathsNm3'},
  'LU3ME010': {'ects': 3, 'nom':'ThermoAp'},
  'LU2ME102': {'ects': 3, 'nom':'TrsfThrm'},
  'LU3ME004': {'ects': 6, 'nom':'MilCont' },
  'LU3ME006': {'ects': 6, 'nom':'SrctElst'},
  'LU3ME007': {'ects': 6, 'nom':'Fluides2'},
  'LU3ME008': {'ects': 6, 'nom':'MathsNm2'},
  'LU3ME103': {'ects': 6, 'nom':'Vibratn' },
  'LU3ME105': {'ects': 3, 'nom':'Acoustiq'},
  'LU3ME108': {'ects': 3, 'nom':'Eolien'  },
  'LU3ME111': {'ects': 3, 'nom':'Struct'  },
  'LU3MEE01': {'ects': 3, 'nom':'SystRobo'},
  'LU2PT001': {'ects': 6, 'nom':'CltBioCh'},
  'LU2PT003': {'ects': 6, 'nom':'Français'},
  'LU2PT005': {'ects': 3, 'nom':'CltHmnst'},
  'LU2PT007': {'ects': 6, 'nom':'CltScnt' },
  'LU2ST035': {'ects': 3, 'nom':'DynTerre'},
  'LU2ST043': {'ects': 3, 'nom':'ExplNat' },
  'LU2ST044': {'ects': 3, 'nom':'Stage'   },
  'LU2ST045': {'ects': 3, 'nom':'Météo'   },
  'LU2ST301': {'ects': 6, 'nom':'Cartgrph'},
  'LU2ST302': {'ects': 6, 'nom':'MPM'     }, #'SX':True
  'LU2ST303': {'ects': 3, 'nom':'Stage'   },
  'LU2ST321': {'ects': 3, 'nom':'Cartgrph'},
  'LU2ST403': {'ects': 6, 'nom':'Sedimnto'}, # 'SX':True
  'LU2ST421': {'ects': 3, 'nom':'Paléo'   },
  'LU3ST057': {'ects': 6, 'nom':'Seismes' },
  'LU3ST059': {'ects': 6, 'nom':'Ocenano' },
  'LU3ST060': {'ects': 6, 'nom':'ClmPaleo'},
  'LU3ST061': {'ects': 3, 'nom':'BioOcAtm'},
  'LU3ST062': {'ects': 3, 'nom':'FabLab'  },
  'LU3ST066': {'ects': 6, 'nom':'PalEvol' },
  'LU3ST603': {'ects': 3, 'nom':'Stage'   },
  'LU3ST605': {'ects': 3, 'nom':'Petrlg'  },
  'LU3ST507': {'ects': 6, 'nom':'EnvSdGeo'},
  'L3PHM02C': {'ects': 6, 'nom':'HistMdvl'},
  'L3PHM011': {'ects': 6, 'nom':'PhiloGen'},
  'L4PHM02E': {'ects': 5, 'nom':'PhilCont'},
  'L4PHM03A': {'ects': 4, 'nom':'Ethique' },
  'L5LACHCI': {'ects': 4, 'nom':'Civilstn'},
  'L5LACHLA': {'ects': 8, 'nom':'Langue'  },
  'L6LACHCI': {'ects': 3, 'nom':'Civilstn'},
  'L6LACHLA': {'ects': 6, 'nom':'Langue'  },

  # Langues
  'LU2LVAN1': {'ects': 3, 'nom':'Anglais' },  'UL2LVAN2': {'ects': 3, 'nom':'Anglais' },
  'LU3LVAN2': {'ects': 3, 'nom':'Anglais' }
}


##     'LU1CI001': {'ects':6,   'nom':'Chimie-1' },
##     'LU1MA001': {'ects':9,   'nom':'Maths-1'  },           'LU1MA002': {'ects':6,   'nom':'Maths-2'  },  'LU1MA003': {'ects':9,   'nom':'Maths-3'  },
##     'LU1MEPY3': {'ects':9,   'nom':'McPhs-1'  },           'LU1MEPY2': {'ects':9,   'nom':'McPhs-2'  },
##     'LU1PY001': {'ects':6,   'nom':'Phys-1'   },
##     'LU1SXM06': {'ects':3,   'nom':'Methodo', 'SX':True }, 'LU1SXARE': {'ects':3,   'nom':'ARE'      },  'LU1PY002': {'ects':3,   'nom':'PAD', 'SX':True },
## 
##       'LU3PY002': {'ects': 6, 'nom':'PhysNum'},
##     'LU2PY102': {'ects':6,   'nom':'Stage', 'SX':True}, 'LU3PY015': {'ects': 6, 'nom':'PhysExp2'},

##          'LU3PY101': {'ects': 6, 'nom':'PhysQ1'  },
##        
        
##             'LU3PY121': {'ects': 9, 'nom':'OEM'     },
##     'LU2PY127': {'ects':6,   'nom':'Satllts'  },
##     'LU2PY403': {'ects':6,   'nom':'Thermo'   },        
##     'LU2PY404': {'ects':6,   'nom':'Meca'     },        
##     'LU2PY410': {'ects':6,   'nom':'Math-S3'  },        'LU3PY216': {'ects': 3, 'nom':'MicroElc'},
##             
##     'LU2PY424': {'ects':3,   'nom':'Relat'    },        
## 'LU3PY238': {'ects': 6, 'nom':'MesuPhys'},
##                                                         'LU3PY23X': {'ects': 6, 'nom':'Option'  },
##                                                         
##                                                         'LU3PY403': {'ects': 6, 'nom':'Thermo'  },
##                                                         'LU3PY411': {'ects': 6, 'nom':'PhysQ2'  },
##                                                         
##                                                         
## 
##     'LU1LVAN2': {'ects':3,   'nom':'Anglais'  },    ##     'LU2FLE01': {'ects':3,   'nom':'FLE'      },    'LU2LVAL2': {'ects':3,   'nom':'Allemand' },
##     'LU3LVAD1': {'ects':3,   'nom':'Anglais'  },
##     'LU3LVRU1': {'ects':3,   'nom':'Russe', 'SX':True },
##     'LU3LVRU2': {'ects':3,   'nom':'Russe', 'SX':True },
## 
## ##     'LU3PY014': {'ects':6,  'nom':'MicMac'},
## ##     'LU3PY004': {'ects':6,  'nom':'StrcMat'},
## ##     'LU3PY022': {'ects':6,  'nom':'Projet'},
## ##     'LU3PY125': {'ects':6,  'nom':'Projet'},
## ##     'LU3PYSO3': {'ects':6,  'nom':'Stage'},
## ##     'LU3PYSO5': {'ects':3,  'nom':'Stage'},
## ##     'LU2PY105': {'ects':6,  'nom':'Stage'},
## ##     'LU3PY033': {'ects':6,  'nom':'OcnAtm'},
## ##     'LU3PY031': {'ects':6,  'nom':'Astro'},
## ##     'LU2PY022': {'ects':3,  'nom':'PhysNum'},
## ##     'LU2PY041': {'ects':6,  'nom':'PhysAct'},
## ##     'LU3PY041': {'ects':6,  'nom':'PhysAct'},
## ##     'LU3PY035': {'ects':6,  'nom':'PhysTh'},
## ##     'LU3PY040': {'ects':9,  'nom':'MesPhys'},
## ##     'LU3PY043': {'ects':6,  'nom':'Transp'},
## ##     'LU3PY042': {'ects':6,  'nom':'HistMeca'},
## ##     'LU3CI021': {'ects': 3, 'nom':'MinChim1'},
## 
##     'LU2CI031': {'ects': 6,  'nom':'MinChim3', 'SX':True},
##     'LU2CI105': {'ects': 6,  'nom':'MinChim2', 'SX':True},      
##                                                                 ##     'LU2EE105': {'ects': 3,  'nom':'MinElec2', 'SX':True},      

##     'LU2EE203': {'ects': 6,  'nom':'MinElec2', 'SX':True},      
##     'LU2EE11A': {'ects': 3,  'nom':'MinElec3', 'SX':True},     
##      'LU3GSG51': {'ects': 6, 'nom':'MinGest1' },
##      'LU3GSG53': {'ects': 6, 'nom':'MinGest2' },
##                     'LU3GSG61': {'ects': 6, 'nom':'MinGest1' },
##                     'LU3GSG62': {'ects': 3, 'nom':'MinGest2' },
##     'LU2IN006': {'ects': 6,  'nom':'MinInfo3', 'SX':True},
## 
##     'LU2ME002': {'ects': 6,  'nom':'MinMeca1' },                
##     'LU2ME003': {'ects': 6,  'nom':'MinMeca2', 'SX':True},      
##     
##                                                                 
## 
##     'LU2ST402': {'ects': 6,  'nom':'MinSDT2'  },
##                                                                 'LU3HS009': {'ects': 6, 'nom':'MinHPST2' },
##                                                                 'LU3HS015': {'ects': 3, 'nom':'MinHPST1' },
##                                                                 'LU3HST51': {'ects': 6, 'nom':'MinHPST1' },
##                                                                 'LU3HST52': {'ects': 3, 'nom':'MinHPST2' },
##                                                                 'LU3HST80': {'ects': 3, 'nom':'MinHPST3' },
##                                                                 'LU3HST61': {'ects': 3, 'nom':'MinHPST1' },
##     'LU2IAS31': {'ects': 6,  'nom':'MinInSnt1'},                
##     'LU2IAS32': {'ects': 6,  'nom':'MinInSnt2'},                
##     'LU2IAS41': {'ects': 9,  'nom':'MinInSnt1'},                
##     'LU2MT017': {'ects': 6,  'nom':'MedSc1'   },                'LU3MT551': {'ects': 9, 'nom':'MedSc1'   },
##     'LU2MT001': {'ects': 3,  'nom':'MedSc1'   },                'LU3MT552': {'ects': 3, 'nom':'MedSc2'   },
##     'LU2MT002': {'ects': 6,  'nom':'MedSc2'   },                'LU3MT560': {'ects': 6, 'nom':'MedSc1'   },
##     'LU2MT018': {'ects': 6,  'nom':'MedSc2'   },                'LU3MT561': {'ects': 3, 'nom':'MedSc2'   },
##     'LU2SXHI1': {'ects':12,  'nom':'MajHist1' },                'LU2SXHI2': {'ects':12, 'nom':'MajHist1' },
##     'LU2SXAL1': {'ects':12,  'nom':'MajAlmd'  },                'LU2SXAL2': {'ects':12, 'nom':'MajAlmd0' },
##     'LU2SXDE1': {'ects':12,  'nom':'MajDsgn'  },                'LU3SXDE1': {'ects':12, 'nom':'MajDsgn'  },     'LU3SXDE2': {'ects':12, 'nom':'MajDsgn'  },
## 
##     'LU2SXDR1': {'ects':12,  'nom':'MajDroit' },                'LU3SXDR1': {'ects':12, 'nom':'MajDroit' },     'LU3SXDR2': {'ects':12, 'nom':'MajDroit'},
##     'LU2SXPH1': {'ects':12,  'nom':'MajPhilo1'},                'LU2SXPH2': {'ects':12, 'nom':'MajPhilo1'},
##     'L3LACHCI': {'ects': 4,  'nom':'MajChinois1'},              'L4LACHCI': {'ects': 3, 'nom':'MajChinois1'},   
##     'L3LACHLA': {'ects': 8,  'nom':'MajChinois2'},              'L4LACHLA': {'ects': 6, 'nom':'MajChinois2'},   
##     'LU3SXSS1': {'ects':12,  'nom':'MinDroit0'},
## 
##     'LU3SXCE1': {'ects': 6, 'nom':'MinGestion1', 'SX':True},    # SX for CMI
## 
## 
## ##     'LK3EVE01': {'ects': 3, 'nom':'MinEnv1'},
## ##     'LK3EVE02': {'ects': 3, 'nom':'MinEnv2'},
## ##     'LK3EVE03': {'ects': 6, 'nom':'MinEnv3'},
## ##     'LU5SX06E': {'ects': 6, 'nom':'MinGestion2'},
## ##     'LK3HSM00': {'ects':12, 'nom':'MinHPST0'},
## ##     'LU2HS003': {'ects': 6, 'nom':'MinHPST1'},
## ##     'LU2HS012': {'ects': 3, 'nom':'MinHPST2'},
## ##     'LU2HST31': {'ects': 3, 'nom':'MinHPST3'},
## ##     'LK3SSK00': {'ects':12, 'nom':'MinSS0'},
## ##     'LK3SSD00': {'ects':12, 'nom':'MajSS0'},
## ##     'LK4SSD00': {'ects':12, 'nom':'MajSS0'},
## ##     'LK5SSD00': {'ects':12, 'nom':'MajSS0'},
## ##     'LK6SSD00': {'ects':12, 'nom':'MajSS0'},
## ##     'LU2SXSS1': {'ects':12, 'nom':'MinSS0'},
## ##     'LK4SSK00': {'ects':12, 'nom':'MinSS0'},
## ##     'LU2SXSS2': {'ects':12, 'nom':'MinSS0'},
## ##     'LK3EWK00': {'ects':12, 'nom':'MinJourn0'},
## ##     'LK3DRKK0': {'ects':12, 'nom':'MinDroit0'},
## ##     'LK3DRD00': {'ects':12, 'nom':'MajDroit0'},
## ##     'LK4DRD00': {'ects':12, 'nom':'MajDroit0'},
## ##     'LU2SXEW1': {'ects':12, 'nom':'MinJourn0'},
## ##     'LU2SXDR1': {'ects':12, 'nom':'MinJourn0'},
## ##     'LK4EWK00': {'ects':12, 'nom':'MinJourn0'},
## ##     'LK4DRK00': {'ects':12, 'nom':'MinDroit0'},
## ##     'LU2SXEW2': {'ects':12, 'nom':'MinJourn0'},
## ##     'LU2SXDR2': {'ects':12, 'nom':'MinJourn0'},
## ##     'LU3SXDR1': {'ects':12, 'nom':'MinDroit0'},
## ##     'LU3SXSS2': {'ects':12, 'nom':'MinDroit0'},
## ##     'LK3MEM02': {'ects':12, 'nom':'MinMeca0'},
## ##     'LK3MEM00': {'ects':12, 'nom':'MinMeca0'},
## ##     'LU2ME113': {'ects': 6, 'nom':'MinMeca2', 'SX':True},
## ##     'L4PHM02E': {'ects': 5, 'nom':'MajPhilo0'},
## ##     'LU2XSAL1': {'ects':12, 'nom':'MajAlmd0'},
## ##     'LK3STM00': {'ects':12, 'nom':'MinSDT0'},
## ##     'LU2ST032': {'ects': 3, 'nom':'MinSDT3'},
## ##     'LU2ST042': {'ects': 3, 'nom':'MinSDT1'},
## ##     'LU3ST361': {'ects': 3, 'nom':'MinSDT3'},
## ##     'LU3ST113': {'ects': 6, 'nom':'MinSDT3'},
## ##     'LK3SVM00': {'ects':12, 'nom':'MinSDV0'},
## ##     'LU2SV301': {'ects': 6, 'nom':'MinSDV1'},
## ##     'LU2SV302': {'ects': 3, 'nom':'MinSDV2'},
## ##     'LU2SV311': {'ects': 3, 'nom':'MinSDV2'},
## ##     'LU2SV313': {'ects': 3, 'nom':'MinSDV3'},
## ##     'LU2EE298': {'ects': 3, 'nom':'MinElec2'},
## ##     'LU2EE199': {'ects': 6, 'nom':'MinElec2'},
## ##     'LU2EE299': {'ects': 6, 'nom':'MinElec2'},
## ##     'LU2EVE04': {'ects': 3, 'nom':'MinEnv1'},
## ##     'LU2EVE05': {'ects': 6, 'nom':'MinEnv2'},
## ##     'LK4HNM00': {'ects': 9, 'nom':'MinHistNat0'},
## ##     'LK4HSM00': {'ects': 9, 'nom':'MinHPST0'},
## ##     'LU2HS008': {'ects': 3, 'nom':'MinHPST1'},
## ##     'LU2HST53': {'ects': 3, 'nom':'MinHPST2'},
## ##     'LU2HS016': {'ects': 3, 'nom':'MinHPST3'},
## ##     'LU2HST61': {'ects': 3, 'nom':'MinHPST3'},
## ##     'LK4MEM00': {'ects': 9, 'nom':'MinMeca0'},
## ##     'LU2ME202': {'ects':6,  'nom':'MinMeca1'},
## ##     'LK4PHM00': {'ects': 9, 'nom':'MinPhilo0'},
## ##     'LU2ST042': {'ects': 3, 'nom':'MinSDT1'},
## ##     'LU2ST043': {'ects': 3, 'nom':'MinSDT2'},
## ##     'LU2ST044': {'ects': 3, 'nom':'MinSDT3'},
## ##     'LU2ST045': {'ects': 3, 'nom':'MinSDT1'},
## ##     'LU2ST402': {'ects': 6, 'nom':'MinSDT2'},
## ##     'LK4SVM00': {'ects': 9, 'nom':'MinSDV0'},
## ##     'LU2SV404': {'ects': 3, 'nom':'MinSDV1'},
## ##     'LU2SV415': {'ects': 6, 'nom':'MinSDV2'},
## ##     'LU3ME112': {'ects': 3, 'nom':'MinMeca1'},
## ##     'LU3ME109': {'ects': 3, 'nom':'MinMeca2'},
## ##     'LU2MA123': {'ects': 3, 'nom':'Minmath1'},
## ##     'LK5SVM00': {'ects': 12,'nom':'MinSdV0'},
## ##     'LK6SVM00': {'ects':  9,'nom':'MinSdV0'},
## ##     'LU3SV611': {'ects': 6, 'nom':'MinSdV1'},
## ##     'LU3SV619': {'ects': 3, 'nom':'MinSdV2'},
## ##     'LU3SV513': {'ects': 3, 'nom':'MinSdV1'},
## ##     'LU3SV515': {'ects': 6, 'nom':'MinSdV1'},
## ##     'LU3SV517': {'ects': 3, 'nom':'MinSdV2'},
## ##     'LU3SV518': {'ects': 3, 'nom':'MinSdV3'},
## ##     'LK5IAM00': {'ects': 12,'nom':'MinInnovSante0'},
## ##     'LK6IAM00': {'ects': 12,'nom':'MinInnovSante0'},
## ##     'LU3IAS53': {'ects': 3, 'nom':'MinInnovSante1'},
## ##     'LU3IAS54': {'ects': 9, 'nom':'MinInnovSante2'},
## ##     'LU3IN000': {'ects':12, 'nom':'MinInfo0'},
## ##     'LU2IN018': {'ects': 3, 'nom':'MinInfo3'},
## ##     'LU2IN023': {'ects': 3, 'nom':'MinInfo3'},
## ##     'LU3CI013': {'ects': 6, 'nom':'Chimie2'},
## ##     'LK6HSM01': {'ects': 3, 'nom':'MinHPST1'},
## ##     'LK6HS009': {'ects': 6, 'nom':'MinHPST2'},
## ##     'LK6STM00': {'ects': 9, 'nom':'SdT0'},
## ##     'LU3ST053': {'ects': 6, 'nom':'SdT1'},
## ##     'LU3ST055': {'ects': 6, 'nom':'SdT1'},
## ##     'LU3ST056': {'ects': 6, 'nom':'SdT2'},
## ##     'LK6ST113': {'ects': 6, 'nom':'SdT1'},
## ##     'LK6ST116': {'ects': 3, 'nom':'SdT2'},
## ##     'LU3ST069': {'ects': 6, 'nom':'SdT2'},
## ##     'LK5EEJ13': {'ects':12, 'nom':'MajElec0'},
## ##     'LK5PHM00': {'ects':12, 'nom':'Philo0'},
## ##     'LK6PHM00': {'ects': 9, 'nom':'Philo0'},
## ##     'LK5PHM99': {'ects': 6, 'nom':'Philo2'},
## ##     'L5PHM03A': {'ects': 6, 'nom':'Philo1'},
## ##     'L5PHM3A1': {'ects': 6, 'nom':'Philo1'},
## ##     'L6PHM3A1': {'ects': 4.5, 'nom':'Philo1'},
## ##     'L6PHM03A': {'ects': 4.5, 'nom':'Philo1'},
## ##     'L6PHM011': {'ects': 4.5, 'nom':'Philo1'},
## ##     'L5PHM510': {'ects': 6, 'nom':'Philo2'},
## ##     'LK5HNM00': {'ects':12, 'nom':'MinHNP0'},
## ##     'LK6HNM00': {'ects': 9, 'nom':'MinHNP0'},
## ##     'LU3HNP61': {'ects': 3, 'nom':'MinHNP1'},
## ##     'LU3HNP63': {'ects': 3, 'nom':'MinHNP2'},
## ##     'LU3HNP64': {'ects': 3, 'nom':'MinHNP3'},
## ##     'LU3HNP51': {'ects': 3, 'nom':'MinHNP1'},
## ##     'LU3HNP52': {'ects': 3, 'nom':'MinHNP2'},
## ##     'LU3HNP53': {'ects': 6, 'nom':'MinHNP3'},
## ##     'LK4PYC03': {'ects': 18,'nom':'MinCMI0'},
## ##     'LU6SX21E': {'ects': 21,'nom':'Moblite'},
## ##     'LU3HI000': {'ects': 12, 'nom':'MinHist1'},
## ##     'LK5HIM00': {'ects': 12, 'nom':'MinHist'},
## ##     'LK6HIM00': {'ects': 9,  'nom':'MinHist'},
## ##     'LU3HI001': {'ects': 5,  'nom':'MinHist1'},
## ##     'LU3HI002': {'ects': 4,  'nom':'MinHist2'},
## ##     'LK5HSM00': {'ects': 12, 'nom':'MinHPST'},
## ##     'LU3HS000': {'ects': 12, 'nom':'MinHPST1'},
## ##     'LU3LVAN1': {'ects': 3, 'nom':'Anglais'},
## ##     'LU3PY001': {'ects': 6, 'nom':'PhysQ1'},
## ##     'LU3PY003': {'ects': 9, 'nom':'Thermo'},
## ##     'LU3PY020': {'ects': 6, 'nom':'PhysQ1'},
## ##     'LU3PY401': {'ects': 6, 'nom':'PhysQ1'},
## ##     'LU3PY101_GS': {'ects': 6, 'nom':'PhysQ1'},
## ##     'LU3PY021': {'ects': 9, 'nom':'OEM'},
## ##     'LU3PY421': {'ects': 9, 'nom':'OEM'},
## ##     'LU3PY121_GS': {'ects': 9, 'nom':'OEM'},
## ##     'LU3PY010': {'ects': 6, 'nom':'Math-S5'},
## ##     'LU3PY013': {'ects': 3, 'nom':'Math-S5'},
## ##     'LU3PY213_GS': {'ects': 3, 'nom':'Math-S5'},
## ##     'LU3PY214_GS': {'ects': 6, 'nom':'MilCont'},
## ##     'LU3PY034': {'ects': 6, 'nom':'MilCont'},
## ##     'LU3PY044': {'ects': 3, 'nom':'Hydro'},
## ##     'LU3PY214': {'ects': 6, 'nom':'MilCont'},
## ##     'LU3PY011': {'ects': 6, 'nom':'Thermo'},
## ##     'LU3PY303': {'ects': 6, 'nom':'Thermo'},
## ##     'LU3PY303_GS': {'ects': 6, 'nom':'Thermo'},
## ##     'LU3PY012': {'ects': 6, 'nom':'PhysExp1'},
## ##     'LU3PY215_GS': {'ects': 3, 'nom':'PhysExp3'},
## ##     'LU3MEOIP': {'ects': 3, 'nom':'OIP'},
## ##     'LU3PYOIP_GS': {'ects': 3, 'nom':'OIP'}
## };
## 
## # Maquette MONO
## Maquette = {
##     # block L1
##     '1SLPY001': {
##       'UE'      : [ ['LU1PY001', 'LU1CI001', 'LU1MA001', 'LU1MEPY3', 'LU1SXM06'] ],
##       'parcours': ['SPRINT'],
##       'nom'     : "MAJ",
##       'semestre': "S1"
##     },
##     '2SLPY001': {
##       'UE'      : [ ['LU1MA002', 'LU1MA003', 'LU1MEPY2', 'LU1PY002', 'LU1SXARE', 'LU1LVAN2'] ],
##       'parcours': ['SPRINT'],
##       'nom'     : "MAJ",
##       'semestre': "S2"
##     },
## 
##     # bloc Majeure
##     'LK3PYJ02': {
##       'UE'      : [ ['LU2PY103', 'LU2PY110', 'LU2PY124', 'LU2FLE01'] ],
##       'parcours': ['SUAD'],
##       'nom'     : "MAJ",
##       'semestre': "S3"
##     },
##     'LK3PYJ03': {
##         'UE'      : [  ['LU2PY403', 'LU2PY424', 'LU2PY410', 'LU2LVAN1'] ],
##         'parcours': ['SPRINT'],
##         'nom'     : "MAJ",
##         'semestre': "S3"
##     },
##     'LK3PYJ11': {
##       'UE'      : [ ['LU2PY103', 'LU2PY110', 'LU2PY125', 'LU2LVAN1'], ['LU2PY403', 'LU2PY222', 'LU2PY424', 'LU2LVAN1'] ],
##       'parcours': ['DM'],
##       'nom'     : "MAJ",
##       'semestre': "S3"
##     },
## #     'LK3PYJ00': {
## #       'UE'      : [ ['LU2PY103', 'LU2PY110', 'LU2PY124', 'LU2LVAN1'] ],
## #       'parcours': ['PADMAJ', 'PADMONO'],
## #       'nom'     : "MAJ",
## #       'semestre': "S3"
## #     },
##     'LK4PYJ03': {
##         'UE'      : [ ['LU2PY404', 'LU2PY421', 'LU2PY423'] ],
##         'parcours': ['SPRINT'],
##         'nom'     : "MAJ",
##         'semestre': "S4"
##     },
##     'LK4PYJ22': {
##         'UE'      : [ ['LU2PY404', 'LU2PY421'], ['LU2PY126', 'LU2PY121'], ['LU2PY215', 'LU2PY121', 'LU2PY123'] ],
##         'parcours': ['DM'],
##         'nom'     : "MAJ",
##         'semestre': "S4"
##     },
##     'LK5PYJ00' : {
##       'UE'      : [ ['LU3PY101', 'LU3PY121', 'LU3PYOIP'], ['LU3PY401', 'LU3PY421', 'LU3PYOIP'] ],
##       'parcours': ['CMI', 'DM', 'MAJ', 'MONO', 'PADMAJ', 'PADMONO', 'SUAD', 'SPRINT'],
##       'nom'     : "MAJ",
##       'semestre': "S5"
##     },
##     'LK6PYJ00' : {
##       'UE'      : [
##         ['LU3PY103','LU3PY111','LU3PY126','LU3LVAN2'], ['LU3PY103','LU3PY111','LU3PY122','LU3LVAN2'], ['LU3PY103','LU3PY111','LU3PY124','LU3LVAN2'],
##         ['LU3PY103','LU3PY111','LU3PY105','LU3LVAN2'], ['LU3PY403','LU3PY411','LU3PY124','LU3LVAN2'] 
##       ],
##       'parcours': ['MONO', 'MAJ', 'PADMONO', 'PADMAJ', 'CMI', 'SPRINT'],
##       'nom'     : "MAJ",
##       'semestre': "S6"
##     },
##     'LK6PYJ30' : {
##         'UE'      : [
##            ['LU3PY103', 'LU3PY111', 'LU3PY537','LU3LVAN2'],
##            ['LU3PY403', 'LU3PY411', 'LU3MA120','LU3LVAN2'],
##            ['LU3PY103', 'LU3PY111', 'LU3ST061','LU3LVAN2'],
##            ['LU3PY103', 'LU3PY111', 'LU3ST062','LU3LVAN2'],
##            ['LU3PY103', 'LU3PY111', 'LU2IN024','LU3LVAN2'],
##            ['LU3PY103', 'LU3PY111', 'LU3EE204','LU3LVAN2'],
##            ['LU3PY103', 'LU3PY111', 'LU3EE203','LU3LVAN2'],
##            ['LU3PY103', 'LU3PY111', 'LU3CI121','LU3LVAN2'],
##            ['LU3ME010', 'LU3PY111', 'LU3PY122','LU3LVAN2'],
##            ['LU3ME010', 'LU3PY111', 'LU3PY124','LU3LVAN2'],
##            ['LU3ME010', 'LU3PY111', 'LU3PY105','LU3LVAN2'],
##            ['LU3PY103', 'LU3PY111', 'LU3PY122'],
##         ],
##         'parcours': ['DM'],
##         'nom'     : "MAJ",
##         'semestre': "S6"
##     },
## 
## 
## ##     'LK3PYJ06': {
## ##         'UE'      : [ 
## ##            ['LU2PY103', 'LU2PY222', 'LU2PY125', 'LU2LVAN1']
## ##         ],
## ##         'parcours': ['MAJ'],
## ##         'nom'     : "MAJ",
## ##         'semestre': "S3"
## ##     },
## ##     'LK3PYJ00': {
## ##         'UE'      : [ 
## ##            ['LU2PY103', 'LU2PY110', 'LU2PY124', 'LU2LVAN1'],
## ##            ['LU2PY103', 'LU2PY124', 'LU2PY222', 'LU2LVAN1']
## ##         ],
## ##         'parcours': ['MONO','MAJ', 'PADMONO', 'PADMAJ', 'CMI'],
## ##         'nom'     : "MAJ",
## ##         'semestre': "S3"
## ##     },
## ##     'LK3PYJ10': {
## ##         'UE'      : [ 
## ##            ['LU2PY103', 'LU2PY110', 'LU2PY124', 'LU2LVAN1'],
## ##            ['LU2PY403', 'LU2PY424', 'LU2PY222', 'LU2LVAN1']
## ##         ],
## ##         'parcours': ['DM', 'DK'],
## ##         'nom'     : "MAJ",
## ##         'semestre': "S3"
## ##     },
## ## 
## ##     'LK4PYJ21': {
## ##         'UE'      : [
## ##            ['LU2PY104', 'LU2PY121'],
## ##            ['LU2PY404', 'LU2PY421'],
## ##            ['LU2PY104', 'LU2PY121', 'LU2PY123'],
## ##            ['LU2PY215', 'LU2PY121', 'LU2PY123']
## ##         ],
## ##         'parcours': ['DK', 'DM'],
## ##         'nom'     : "MAJ",
## ##         'semestre': "S4"
## ##     }
## ## ,
## ##     'LK5PYJ00' : {
## ##         'UE'      : [
## ##            ['LU3PY101', 'LU3PY121', 'LU3PYOIP'],
## ##            ['LU3PY401', 'LU3PY421', 'LU3PYOIP']
## ##         ],
## ##         'parcours': ['MONO', 'MAJ', 'DM', 'PADMONO', 'PADMAJ', 'DK'],
## ##         'nom'     : "MAJ",
## ##         'semestre': "S5"
## ##     },
## ## 
## ##     'LK6PY120' : {
## ##         'UE'      : [
## ##            ['LU3PY103', 'LU3PY111', 'LU3PY122']
## ##         ],
## ##         'parcours': ['DK'],
## ##         'nom'     : "MAJ",
## ##         'semestre': "S6"
## ##     },
## 
## ##     'LK6PYJ01' : {
## ##         'UE'      : [
## ##            ['LU3PY403', 'LU3PY411', 'LU3PY124','LU3LVAN2'],
## ##            ['LU3PY403', 'LU3PY411', 'LU3PY125','LU3LVAN2']
## ##         ],
## ##         'parcours': ['SPRINT'],
## ##         'nom'     : "MAJ",
## ##         'semestre': "S6"
## ##     },
## ## 
## ## 
## ##     'LK6PYJEE' : {
## ##         'UE'      : [
## ##            ['LU3PY020', 'LU3PY021'],
## ##            ['LU3PY004', 'LU3PY021'],
## ##            ['LU3PY004', 'LU3PY021', 'LU3PYSO5']
## ##         ],
## ##         'parcours': ['DM'],
## ##         'nom'     : "MAJ",
## ##         'semestre': "S6"
## ##     },
## 
##     # bloc Complementaire
##     'LK3PYC01': {
##         'UE'      : [ ['LU2PY212', 'LU2PY520', 'LU2PY531']],
##         'parcours': ['SPRINT'],
##         'nom'     : "CMP",
##         'semestre': "S3"
##     },
##     'LK3PYC03': {
##       'UE'      : [['LU2CI011', 'LU2CI012', 'LU2GSG31'], ['LU2EE100', 'LU2EE200', 'LU2GSG31'] ],
##       'parcours': ['CMI'],
##       'nom'     : "CMP",
##       'semestre': "S3"
##     },
##     'LK3PYC04': {
##       'UE'      : [['LU2PY220', 'LU2PY222', 'LU2GSG31']],
##       'parcours': ['CMI'],
##       'nom'     : "CMP",
##       'semestre': "S3"
##     },
##     'LK4PYC01': {
##         'UE'      : [['LU2PY215', 'LU2PY222', 'LU2PY532']],
##         'parcours': ['SPRINT'],
##         'nom'     : "CMP",
##         'semestre': "S4"
##     },
##     'LK4PYC04': {
##         'UE'      : [ ['LU2CI101', 'LU2PY127', 'LU2PY102']],
##         'parcours': ['CMI'],
##         'nom'     : "CMP",
##         'semestre': "S4"
##     },
##     'LK5PYC00': {
##       'UE'      : [['LU3PY213', 'LU3PY214', 'LU3PY215']],
##       'parcours': ['MONO', 'PADMONO', 'CMI'],
##       'nom'     : "CMP",
##       'semestre': "S5"
##     },
##     'LK5PYC02': {
##       'UE'      : [['LU3PY213', 'LU3PY215', 'LU3PY216', 'LU3LVAD1'] ],
##       'parcours': ['SUAD'],
##       'nom'     : "CMP",
##       'semestre': "S5"
##     },
##     'LK5PYMI0': {
##       'UE'      : [ ['LU3CI052', 'LU3CI011', 'LU3SXCE1'], ['LU3EE100', 'LU3EE101', 'LU3SXCE1'] ],
##       'parcours': ['CMI'],
##       'nom'     : "CMP",
##       'semestre': "S5"
##     },
##     'LK6PYC00': {
##         'UE'      : [ ['LU3PY23X','LU3PY205'], ['LU3PY235','LU3PY205'], ['LU3PY234','LU3PY205'], ['LU3PY233','LU3PY205'], ['LU3PY232','LU3PY205'], ['LU3PY231','LU3PY205'] ],
##         'parcours': ['MONO'],
##         'nom'     : "CMP",
##         'semestre': "S6"
##     },
##     'LK6PYC01': {
##         'UE'      : [ ['LU3PY235','LU3PY205','LU3PY537'], ['LU3PY234','LU3PY205','LU3PY537'], ['LU3PY233','LU3PY205','LU3PY537'], ['LU3PY232','LU3PY205','LU3PY537'], ['LU3PY231','LU3PY205','LU3PY537'] ],
##         'parcours': ['SPRINT'],
##         'nom'     : "CMP",
##         'semestre': "S6"
##     },
##     'LK6PYMI0': {
##         'UE'      : [['LU3CI141', 'LU3PY232', 'LU3PY105'], ['LU3CI141', 'LU3PY234', 'LU3PY105'], ['LU3CI141', 'LU3PY235', 'LU3PY105'] ],
##         'parcours': ['CMI'],
##         'nom'     : "CMP",
##         'semestre': "S6"
##     },
## 
## 
## 
## ##     'LK3PYC02': {
## ##         'UE'      : [['LU2PY041', 'LU2PY220'], ['LU2PY220', 'LU2PY212'] ],
## ##         'parcours': ['PADMONO'],
## ##         'nom'     : "CMP",
## ##         'semestre': "S3"
## ##     },
## 
## ## 
## ##     'LK6PYC00': {
## ##         'UE'      : [ 
## ##            ['LU3PY23X', 'LU3PY205'],
## ##            ['LU3PY235', 'LU3PY205'],
## ##            ['LU3PY234', 'LU3PY205'],
## ##            ['LU3PY233', 'LU3PY205'],
## ##            ['LU3PY232', 'LU3PY205'],
## ##            ['LU3PY231', 'LU3PY205']
## ##         ],
## ##         'parcours': ['MONO'],
## ##         'nom'     : "CMP",
## ##         'semestre': "S6"
## ##     },
## 
## 
##     # bloc mineure
##     'LK3CHM00' : { 'UE' : [ ['L3LACHCI', 'L3LACHLA']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4CHM00' : { 'UE' : [ ['L4LACHCI', 'L4LACHLA']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S4" },
##     'LK5GSM00' : { 'UE' : [ ['LU3GSG51', 'LU3GSG53']             ], 'parcours': ['PADMAJ'], 'nom' : "MIN", 'semestre': "S5" },
##     'LK6GSM00' : { 'UE' : [ ['LU3GSG61', 'LU3GSG62']             ], 'parcours': ['PADMAJ'], 'nom' : "MIN", 'semestre': "S6" },
##     'LK5HSM00' : { 'UE' : [ ['LU3HST51', 'LU3HST52', 'LU3HST80'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S5" },
##     'LK6HSM00' : { 'UE' : [ ['LU3HS015', 'LU3HS009'], ['LU3HST61', 'LU3HS009'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S6" },
##     'LK3IAM00' : { 'UE' : [ ['LU2IAS31', 'LU2IAS32']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4IAM00' : { 'UE' : [ ['LU2IAS41']                         ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S4" },
##     'LK4INM00' : { 'UE' : [ ['LU2IN003', 'LU2IN014']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S4" },
##     
##     ##     'LK3MTM00' : { 'UE' : [ ['LU2MT017', 'LU2MT018']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4MTM00' : { 'UE' : [ ['LU2MT001', 'LU2MT002']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S4" },
##     'LK5MTM00' : { 'UE' : [ ['LU3MT551', 'LU3MT552']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S5" },
##     'LK6MTM00' : { 'UE' : [ ['LU3MT560', 'LU3MT561']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S6" },
##     'LK5STM00' : { 'UE' : [ ['LU3ST057', 'LU3ST059']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S5" },
##     # bloc double majeure
##     'LK3ALD00' : { 'UE' : [ ['LU2SXAL1']                         ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4ALD00' : { 'UE' : [ ['LU2SXAL2', 'LU2PY123']             ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S4" },
##     'LK3CID00' : { 'UE' : [ ['LU2CI012', 'LU2CI011', 'LU2CI031'] ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4CID00' : { 'UE' : [ ['LU2CI101', 'LU2CI102', 'LU2CI105', 'LU2PY123'] ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S4" },
##     'LK3DEK00' : { 'UE' : [ ['LU2SXDE1']                         ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK5DEK00' : { 'UE' : [ ['LU3SXDE1']                         ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S5" },
##     'LK6DEK00' : { 'UE' : [ ['LU3SXDE2']                         ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S6" },
##     'LK5DRK00' : { 'UE' : [ ['LU3SXDR1']                         ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S5" },
##     'LK6DRK00' : { 'UE' : [ ['LU3SXDR2']                         ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S6" },
##     'LK3EED00' : { 'UE' : [ ['LU2EE100', 'LU2EE200', 'LU2EE105', 'LU2EE11A'] ], 'parcours': ['DM'] , 'nom' : "MIN", 'semestre': "S3" },
##     'LK4EED00' : { 'UE' : [ ['LU2EE201', 'LU2EE203', 'LU2EE204', 'LU2PY123'] ], 'parcours': ['DM'] , 'nom' : "MIN", 'semestre': "S4" },
##     'LK3HID00' : { 'UE' : [ ['LU2SXHI1']                         ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4HID00' : { 'UE' : [ ['LU2SXHI2', 'LU2PY123']             ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S4" },
##     'LK3IND00' : { 'UE' : [ ['LU2IN002', 'LU2IN019', 'LU2IN005', 'LU2IN018'] ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4IND00' : { 'UE' : [ ['LU2IN003', 'LU2IN006', 'LU2IN009'] ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S4" },
##     'LK3MAD00' : { 'UE' : [ ['LU2MA221', 'LU2MA260', 'LU2MA216'] ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4MAD00' : { 'UE' : [ ['LU2MA122', 'LU2MA211', 'LU2MA241', 'LU2PY215'] ], 'parcours': ['DM' ], 'nom' : "MIN", 'semestre': "S4" },
##     'LK3MED00' : { 'UE' : [ ['LU2ME001', 'LU2ME005', 'LU2ME006'] ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4MED00' : { 'UE' : [ ['LU2ME002', 'LU2ME003', 'LU2ME004'] ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S4" },
##     'LK3PHD00' : { 'UE' : [ ['LU2SXPH1']                         ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4PHD00' : { 'UE' : [ ['LU2SXPH2', 'LU2PY123']             ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S4" },
##     'LK3STD00' : { 'UE' : [ ['LU2ST035', 'LU2ST301', 'LU2ST302', 'LU2ST303'] ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S3" },
##     'LK4STD00' : { 'UE' : [ ['LU2ST402', 'LU2ST045', 'LU2ST403', 'LU2PY123'], ['LU2ST043', 'LU2ST044', 'LU2ST045', 'LU2PY123', 'LU2ST403'] ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S4" },
##     'LK5SSD00' : { 'UE' : [ ['LU3SXSS1']                         ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S5" },
##     'LK6SSD00' : { 'UE' : [ ['LU3SXSS2']                         ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S6" },
## 
## ##     'LK3MEM00' : { 'UE' : [ ['LU2ME001', 'LU2ME113']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S3" },
## ##     'LK4MEM00' : { 'UE' : [ ['LU2ME004', 'LU2ME102']], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S4" },
## ##     'LK3SVM00' : { 'UE' : [ ['LU2SV301', 'LU2SV311', 'LU2SV313'], ['LU2SV301', 'LU2SV302', 'LU2SV313'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S3" },
## ##     'LK4SVM00' : { 'UE' : [ ['LU2SV404', 'LU2SV415'            ] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S4" },
## ##     'LK3STM00' : { 'UE' : [ ['LU2ST301', 'LU2ST303', 'LU2ST035'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S3" },
## ##     'LK3HSM00' : { 'UE' : [ ['LU2HS003', 'LU2HS012', 'LU2HST31'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S3" },
## ##     'LK4HSM00' : { 'UE' : [ ['LU2HS016', 'LU2HS008', 'LU2HST53'], ['LU2HST61', 'LU2HS008', 'LU2HST53'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S4" },
## ## 
## ##     'LK5SVM00' : { 'UE' : [ ['LU3SV513', 'LU3SV515', 'LU3SV518'], ['LU3SV515', 'LU3SV517', 'LU3SV518'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S5" },
## ##     'LK6SVM00' : { 'UE' : [ ['LU3SV611', 'LU3SV619'            ] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S6" },
## ##     'LK6STM00' : { 'UE' : [ ['LK6ST113', 'LK6ST116'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S6" },
## ##     'LK5IAM00' : { 'UE' : [ ['LU3IAS54', 'LU3IAS53']             ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S5" },
## ##     'LK5PHM00' : { 'UE' : [ ['L5PHM3A1', 'L5PHM510'], ['L5PHM03A', 'LK5PHM99'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S5" },
## ##     'LK6PHM00' : { 'UE' : [ ['L6PHM03A', 'L6PHM011'], ['L6PHM3A1', 'L6PHM011']                         ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S6" },
## ##     'LK6HSM00' : { 'UE' : [ ['LU3HST51', 'LU3HST52', 'LU3HST80'] ], 'parcours': ['MAJ', 'PADMAJ'], 'nom' : "MIN", 'semestre': "S5" },
## ##     'LK5HNM00' : { 'UE' : [ ['LU3HNP51', 'LU3HNP52', 'LU3HNP53'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S5" },
## ##     'LK6HNM00' : { 'UE' : [ ['LU3HNP61', 'LU3HNP64', 'LU3HNP63'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S6" },
## ##     'LK3SSD00' : { 'UE' : [ ['LU2SXSS1'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S3" },
## ##     'LK3SSK00' : { 'UE' : [ ['LU2SXSS1'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S3" },
## ##     'LK4SSD00' : { 'UE' : [ ['LU2SXSS2'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S4" },
## ##     'LK4SSK00' : { 'UE' : [ ['LU2SXSS2'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S4" },
## ##     'LK3EWK00' : { 'UE' : [ ['LU2SXEW1'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S3" },
## ##     'LK4EWK00' : { 'UE' : [ ['LU2SXEW2'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S4" },
## ##     'LK3DRD00' : { 'UE' : [ ['LU2SXDR1'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S3" },
## ##     'LK3DRKK0' : { 'UE' : [ ['LU2SXDR1'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S3" },
## ##     'LK4DRD00' : { 'UE' : [ ['LU2SXDR2'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S4" },
## ##     'LK4DRK00' : { 'UE' : [ ['LU2SXDR2'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S4" },
## ##     'LK5HIM00' : { 'UE' : [ ['LU3HI000'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S5" },
## ##     'LK6HIM00' : { 'UE' : [ ['LU3HI001', 'LU3HI002'] ], 'parcours': ['MAJ'], 'nom' : "MIN", 'semestre': "S5" },
## ##     'LK5SSD00' : { 'UE' : [ ['LU3SXSS1'], ['LU3SXDR1'] ], 'parcours': ['DM'], 'nom' : "MIN", 'semestre': "S5" },
## ##     'LK6PYDK0' : { 'UE' : [ ['LU3SXSS2'], ['LU3SXDR2'] ], 'parcours': ['DK'], 'nom' : "MIN", 'semestre': "S6" }
## ## 
## 
## };
## 
## Irrelevant = ['LU2LVAN1', 'LU2LVAL2', 'LU3LVRU1', 'LU3LVRU2'];
## HorsContrat= ['LU2LVAL2', 'LU3LVRU1', 'LU3LVRU2'];
## 
## Swap = {
##     'LU2PY041' : ['LU2PY212'],
##     'LU2PY104' : ['LU2PY126'],
##     'LU2PY212' : ['LU2PY222'],
##     'LU3PY002' : ['LU3PY126'],
##     'LU3PY024' : ['LU3PY238'],
##     'LU3PY015' : ['LU3PY215', 'LU3PYOIP'],
##     'LU3PY401' : ['LU3PY101'],
##     'LU2PY124' : ['LU2PY125']
## }
## 
## IsModule = [
##   'L3LACHCI', 'L3LACHLA', 'L4LACHCI', 'L4LACHLA', 'L5LACHCI', 'L5LACHLA', 'L6LACHCI', 'L6LACHLA',
##   'L3PHM011', 'L3PHM02C', 'L4PHM02E', 'L4PHM03A', 'L5PHM3A1', 'L5PHM510', 'L6PHM011', 'L6PHM3A1'
## ];
## 
## BlocsDisc = {
##   'S3': {
##      'PY': [ ['LU2PY103', 'LU2PY110', 'LU2PY125'], ['LU2PY103', 'LU2PY110', 'LU2PY124'], ['LU2PY403', 'LU2PY222', 'LU2PY424'] ],
##      'AL': [ ['LU2SXAL1'] ],
##      'CI': [ ['LU2CI011', 'LU2CI012', 'LU2CI031'] ],
##      'DE': [ ['LU2SXDE1'] ],
##      'DR': [ ['LU2SXDR1'] ],
##      'EE': [ ['LU2EE100', 'LU2EE200', 'LU2EE105', 'LU2EE11A'] ],
##      'HI': [ ['LU2SXHI1'] ],
##      'IN': [ ['LU2IN002', 'LU2IN018', 'LU2IN019', 'LU2IN005'] ],
##      'MA': [ ['LU2MA260', 'LU2MA221', 'LU2MA216'] ],
##      'ME': [ ['LU2ME001', 'LU2ME005', 'LU2ME006'] ],
##      'PH': [ ['LU2SXPH1'] ],
##      'SS': [ ['LU2SXSS1'] ],
##      'ST': [ ['LU2ST301', 'LU2ST303', 'LU2ST035', 'LU2ST302'] ]
##    },
##   'S4': {
##      'PY': [ ['LU2PY121', 'LU2PY126'], ['LU2PY121', 'LU2PY104', 'LU2PY123'], ['LU2PY121', 'LU2PY104'], ['LU2PY421', 'LU2PY404', 'LU2PY215'], ['LU2PY121', 'LU2PY123', 'LU2PY215'] ],
##      'CI': [ ['LU2CI101', 'LU2CI102', 'LU2CI105'] ],
##      'EE': [ ['LU2EE201', 'LU2EE298', 'LU2EE203'], ['LU2EE201', 'LU2EE204', 'LU2EE203'] ],
##      'HI': [ ['LU2SXHI2'] ],
##      'IN': [ ['LU2IN003', 'LU2IN006', 'LU2IN009'] ],
##      'MA': [ ['LU2MA122', 'LU2MA241', 'LU2MA211'] ],
##      'ME': [ ['LU2ME004', 'LU2ME002', 'LU2ME003'] ],
##      'PH': [ ['LU2SXPH2'] ],
##      'AL': [ ['LU2SXAL2'] ],
##      'ST': [ ['LU2ST402', 'LU2ST045', 'LU2ST403'] , ['LU2ST043', 'LU2ST044', 'LU2ST045', 'LU2ST403'] ]
##    },
##   'S5': {
##      'PY': [ ['LU3PY011', 'LU3PY012', 'LU3PY013'], ['LU3PY001', 'LU3PY003'], ['LU3PY001', 'LU3PY014', 'LU3PY015'], ['LU3PY101', 'LU3PY121'], ['LU3PY101', 'LU3PY121', 'LU2PY532'], ['LU3PY401', 'LU3PY421'] ],
##      'CI': [ ['LU3CI011', 'LU3CI032', 'LU3CI003', 'LU3CI035'] ],
##      'DE': [ ['LU3SXDE1'] ],
##      'DR': [ ['LU3SXDR1'] ],
##      'EE': [ ['LK5EEJ13'], ['LU3EE100', 'LU3EE101', 'LU3EE105'] ],
##      'IN': [ ['LU3IN029', 'LU3IN033', 'LU3IN003'] ],
##      'MA': [ ['LU3MA260', 'LU3MA263', 'LU3MA232'] ],
##      'ME': [ ['LU3ME004', 'LU3ME008'] ,['LU3ME004', 'LU3ME103', 'LU3ME008'] ],
##      'ST': [ ['LU3ST057', 'LU3ST059', 'LU3ST507'] ],
##      'DK': [ ['LU3SXSS1'] ],
##    },
##   'S6': {
##      'PY': [
##        ['LU3PY111', 'LU3PY103', 'LU3PY105'], ['LU3PY111', 'LU3PY103', 'LU3PY122'], ['LU3PY111', 'LU3PY103', 'LU3PY124'], ['LU3PY111', 'LU3PY103', 'LU3PY125'],
##        ['LU3PY111', 'LU3PY103', 'LU3PY105', 'LU3PY537'], ['LU3PY111', 'LU3PY103', 'LU3PY122', 'LU3PY537'], ['LU3PY111', 'LU3PY103', 'LU3PY124', 'LU3PY537'], ['LU3PY111', 'LU3PY103', 'LU3PY125', 'LU3PY537'] ,
##        ['LU3PY111', 'LU3PY105'], ['LU3PY111', 'LU3PY122'], ['LU3PY111', 'LU3PY124'], ['LU3PY111', 'LU3PY125'],
##        ['LU3PY411', 'LU3PY403', 'LU3PY105'], ['LU3PY411', 'LU3PY403', 'LU3PY122'], ['LU3PY411', 'LU3PY403', 'LU3PY124'], ['LU3PY411', 'LU3PY403', 'LU3PY125'],
##        ['LU3PY103', 'LU3PY111', 'LU3PY537'], ['LU3PY020', 'LU3PY021'], ['LU3PY004', 'LU3PY021'], ['LU3PY004', 'LU3PY021', 'LU3PYSO5'] 
##       ],
##      'CI': [ ['LU3CI113', 'LU3CI121', 'LU3CI101'] ],
##      'EE': [ ['LU3EE203', 'LU3EE200', 'LU3EE210', 'LU3EE204'], ['LU3EE200', 'LU3EE204', 'LU3EE210'] ],
##      'IN': [ ['LU2IN024', 'LU3IN024', 'LU3IN010'] ],
##      'MA': [ ['LU3MA120', 'LU3MA210', 'LU3MA261'], ['LU3MA120', 'LU3MA210', 'LU3MA290'] ],
##      'ME': [ ['LU3ME010', 'LU3ME007', 'LU3ME006', 'LU3ME009'] ],
##      'ST': [ ['LU3ST060', 'LU3ST603', 'LU3ST605'] ]
##    }
## }

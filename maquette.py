##########################################################
###                                                    ###
###                  Maquette  Apogee                  ###
###                                                    ###
##########################################################

# Liste des UE avec le nombre de credits
UEs = {
    'LU2PY103': {'ects':6,  'nom':'Thermo'},
    'LU2PY104': {'ects':6,  'nom':'Meca'},
    'LU2PY110': {'ects':6,  'nom':'Math-S3'},
    'LU2LVAN1': {'ects':3,  'nom':'Anglais'},
    'LU2PY121': {'ects':12, 'nom':'OEM'},
    'LU2PY123': {'ects':3,  'nom':'Math-S4'},
    'LU2PY124': {'ects':3,  'nom':'Relat'},
    'LU2PY212': {'ects':6,  'nom':'PhysExp1'},
    'LU2PY215': {'ects':3,  'nom':'PhysExp2'},
    'LU2PY220': {'ects':6,  'nom':'Math-Comp'},
    'LU2PY222': {'ects':6,  'nom':'PhysNum'},
    'LK3CIM00': {'ects':12, 'nom':'MinChimie0'},
    'LU2CI012': {'ects': 6, 'nom':'MinChimie1'},
    'LU2CI011': {'ects': 6, 'nom':'MinChimie2'},
    'LK3EEM00': {'ects':12, 'nom':'MinElec0'},
    'LU2EE199': {'ects': 6, 'nom':'MinElec1'},
    'LU2EE299': {'ects': 6, 'nom':'MinElec2'},
    'LK3EVM00': {'ects':12, 'nom':'MinEnv0'},
    'LU2EVE01': {'ects': 3, 'nom':'MinEnv1'},
    'LU2EVE02': {'ects': 3, 'nom':'MinEnv2'},
    'LU2EVE03': {'ects': 6, 'nom':'MinEnv3'},
    'LK3GSM00': {'ects':12, 'nom':'MinGestion0'},
    'LU2GSG31': {'ects': 6, 'nom':'MinGestion1'},
    'LU2GSG32': {'ects': 6, 'nom':'MinGestion2'},
    'LK3HNM00': {'ects':12, 'nom':'MinHistNat0'},
    'LU2HNP31': {'ects': 3, 'nom':'MinHistNat1'},
    'LU2HNP32': {'ects': 3, 'nom':'MinHistNat2'},
    'LU2HNP33': {'ects': 3, 'nom':'MinHistNat3'},
    'LU2HNP41': {'ects': 3, 'nom':'MinHistNat4'},
    'LK3HSM00': {'ects':12, 'nom':'MinHPST0'},
    'LU2HS003': {'ects': 6, 'nom':'MinHPST1'},
    'LU2HS012': {'ects': 3, 'nom':'MinHPST2'},
    'LU2HST31': {'ects': 3, 'nom':'MinHPST3'},
    'LK3IAM00': {'ects':12, 'nom':'MinInnovSante0'},
    'LU2IAS31': {'ects': 6, 'nom':'MinInnovSante1'},
    'LU2IAS32': {'ects': 6, 'nom':'MinInnovSante2'},
    'LK3INM00': {'ects':12, 'nom':'MinInfo0'},
    'LU2IN005': {'ects': 6, 'nom':'MinInfo1'},
    'LU2IN018': {'ects': 3, 'nom':'MinInfo2'},
    'LU2IN019': {'ects': 3, 'nom':'MinInfo3'},
    'LK3MAM00': {'ects':12, 'nom':'MinMath0'},
    'LU2MA221': {'ects':6,  'nom':'MinMath1'},
    'LU2MA260': {'ects':6,  'nom':'MinMath2'},
    'LK3MEM00': {'ects':12, 'nom':'MinMeca0'},
    'LU2ME001': {'ects': 6, 'nom':'MinMeca1'},
    'LU2ME113': {'ects': 6, 'nom':'MinMeca2'},
    'LK3PHM00': {'ects':12, 'nom':'MinPhilo0'},
    'L3PHM02C': {'ects': 6, 'nom':'MinPhilo1'},
    'L3PHM011': {'ects': 6, 'nom':'MinPhilo2'},
    'LK3PTM00': {'ects':12, 'nom':'MinProfEcoles0'},
    'LU2PT001': {'ects':6,  'nom':'MinProfEcoles1'},
    'LU2PT003': {'ects':6,  'nom':'MinProfEcoles2'},
    'LK3STM00': {'ects':12, 'nom':'MinSDT0'},
    'LU2ST032': {'ects': 3, 'nom':'MinSDT3'},
    'LU2ST035': {'ects': 3, 'nom':'MinSDT3'},
    'LU2ST301': {'ects': 6, 'nom':'MinSDT1'},
    'LU2ST303': {'ects': 3, 'nom':'MinSDT2'},
    'LK3SVM00': {'ects':12, 'nom':'MinSDV0'},
    'LU2SV301': {'ects': 6, 'nom':'MinSDV1'},
    'LU2SV302': {'ects': 3, 'nom':'MinSDV2'},
    'LU2SV311': {'ects': 3, 'nom':'MinSDV2'},
    'LU2SV313': {'ects': 3, 'nom':'MinSDV3'},
    'LK4CIM00': {'ects': 9, 'nom':'MinChimie0'},
    'LU2CI101': {'ects': 3, 'nom':'MinChimie1'},
    'LU2CI102': {'ects': 6, 'nom':'MinChimie2'},
    'LK4EEM00': {'ects': 9, 'nom':'MinElec0'},
    'LU2EE201': {'ects': 6, 'nom':'MinElec1'},
    'LU2EE298': {'ects': 3, 'nom':'MinElec2'},
    'LK4EVM00': {'ects': 9, 'nom':'MinEnv0'},
    'LU2EVE04': {'ects': 3, 'nom':'MinEnv1'},
    'LU2EVE05': {'ects': 6, 'nom':'MinEnv2'},
    'LK4GSM00': {'ects': 9, 'nom':'MinGestion0'},
    'LU2GSG41': {'ects': 6, 'nom':'MinGestion1'},
    'LU2GSG42': {'ects': 3, 'nom':'MinGestion2'},
    'LK4HNM00': {'ects': 9, 'nom':'MinHistNat0'},
    'LU2HNP34': {'ects': 3, 'nom':'MinHistNat1'},
    'LU2HNP42': {'ects': 3, 'nom':'MinHistNat2'},
    'LU2HNP43': {'ects': 3, 'nom':'MinHistNat3'},
    'LK4HSM00': {'ects': 9, 'nom':'MinHPST0'},
    'LU2HS008': {'ects': 3, 'nom':'MinHPST1'},
    'LU2HST53': {'ects': 3, 'nom':'MinHPST2'},
    'LU2HS016': {'ects': 3, 'nom':'MinHPST3'},
    'LU2HST61': {'ects': 3, 'nom':'MinHPST3'},
    'LK4IAM00': {'ects': 9, 'nom':'MinInnovSante0'},
    'LU2IAS41': {'ects': 9, 'nom':'MinInnovSante1'},
    'LK4INM00': {'ects': 9, 'nom':'MinInfo0'},
    'LU2IN003': {'ects': 6, 'nom':'MinInfo1'},
    'LU2IN014': {'ects': 3, 'nom':'MinInfo2'},
    'LK4MAM00': {'ects': 9, 'nom':'MinMath0'},
    'LU2MA122': {'ects': 3, 'nom':'MinMath1'},
    'LU2MA241': {'ects': 6, 'nom':'MinMath2'},
    'LK4MEM00': {'ects': 9, 'nom':'MinMeca0'},
    'LU2ME102': {'ects': 3, 'nom':'MinMeca1'},
    'LU2ME004': {'ects': 6, 'nom':'MinMeca2'},
    'LK4PHM00': {'ects': 9, 'nom':'MinPhilo0'},
    'L4PHM02E': {'ects': 5, 'nom':'MinPhilo1'},
    'L4PHM03A': {'ects': 4, 'nom':'MinPhilo2'},
    'LK4PTM00': {'ects': 9, 'nom':'MinProfEcoles0'},
    'LU2PT005': {'ects': 6, 'nom':'MinProfEcoles1'},
    'LU2PT007': {'ects': 3, 'nom':'MinProfEcoles2'},
    'LK4STM00': {'ects': 9, 'nom':'MinSDT0'},
    'LU2ST042': {'ects': 3, 'nom':'MinSDT1'},
    'LU2ST043': {'ects': 3, 'nom':'MinSDT2'},
    'LU2ST044': {'ects': 3, 'nom':'MinSDT3'},
    'LU2ST045': {'ects': 3, 'nom':'MinSDT1'},
    'LU2ST402': {'ects': 6, 'nom':'MinSDT2'},
    'LK4SVM00': {'ects': 9, 'nom':'MinSDV0'},
    'LU2SV404': {'ects': 3, 'nom':'MinSDV1'},
    'LU2SV415': {'ects': 6, 'nom':'MinSDV2'},

    'LU3PY101': {'ects': 6, 'nom':'PhysQuant1'},
    'LU3PY121': {'ects': 9, 'nom':'OEM'},
    'LU3PY213': {'ects': 3, 'nom':'Math-S5'},
    'LU3PY214': {'ects': 6, 'nom':'MilieuxContinus'},
    'LU3PY215': {'ects': 3, 'nom':'PhysExp3'},
    'LU3PYOIP': {'ects': 3, 'nom':'OIP'}
};

# Maquette MONO
Maquette = {
    # bloc Majeure
    'LK3PYJ00': {
        'UE'      : [ 
           ['LU2PY103', 'LU2PY110', 'LU2PY124', 'LU2LVAN1'],
           ['LU2PY103', 'LU2PY124', 'LU2PY222', 'LU2LVAN1']
        ],
        'parcours': ['MONO', 'MAJ'],
        'nom'     : "MAJ",
        'semestre': "S3"
    },
    'LK4PYJ00': {
        'UE'      : [
           ['LU2PY104', 'LU2PY121', 'LU2PY123'],
           ['LU2PY104', 'LU2PY121', 'LU2PY215']
        ],
        'parcours': ['MONO', 'MAJ'],
        'nom'     : "MAJ",
        'semestre': "S4"
    },

    'LK5PYJ00' : {
        'UE'      : [
           ['LU3PY101', 'LU3PY121', 'LU3PYOIP'],
        ],
        'parcours': ['MONO', 'MAJ'],
        'nom'     : "MAJ",
        'semestre': "S5"
    },

    # bloc Complementaire
    'LK3PYC00': {
        'UE'      : [['LU2PY212', 'LU2PY220']],
        'parcours': ['MONO'],
        'nom'     : "CMP",
        'semestre': "S3"
    },
    'LK4PYC00': {
        'UE'      : [['LU2PY215', 'LU2PY222']],
        'parcours': ['MONO'],
        'nom'     : "CMP",
        'semestre': "S4"
    },

    'LK5PYC00': {
        'UE'      : [['LU3PY213', 'LU3PY214', 'LU3PY215']],
        'parcours': ['MONO'],
        'nom'     : "CMP",
        'semestre': "S5"
    },

    # bloc Mineure
    'LK3PYMI0': {
        'UE'      : [ ['LU2MA221', 'LU2MA260'], ['LU2PT001', 'LU2PT003'], ['LU2SV301', 'LU2SV311', 'LU2SV313'],
                      ['LU2SV301', 'LU2SV302', 'LU2SV313'],['LU2IN005', 'LU2IN018', 'LU2IN019'], ['LU2IAS31', 'LU2IAS32'],
                      ['LU2ME001', 'LU2ME113'], ['LU2HS003', 'LU2HS012', 'LU2HST31'], ['LU2CI011', 'LU2CI012'],
                      ['LU2ST301', 'LU2ST303', 'LU2ST032'], ['LU2ST301', 'LU2ST303', 'LU2ST035'], ['L3PHM011', 'L3PHM02C'],
                      ['LU2GSG31', 'LU2GSG32'], ['LU2HNP31', 'LU2HNP32', 'LU2HNP33', 'LU2HNP41'], ['LU2EE199', 'LU2EE299'],
                      ['LU2EVE01', 'LU2EVE02', 'LU2EVE03']
         ],
        'parcours': ['MAJ'],
        'nom'     : "MIN",
        'semestre': "S3"
    },
    'LK4PYMI0': {
        'UE'      : [ ['LU2MA122', 'LU2MA241'], ['LU2SV404', 'LU2SV415'], ['L4PHM02E','L4PHM03A'],
                      ['LU2PT005', 'LU2PT007'], ['LU2IN003', 'LU2IN014'], ['LU2ST045', 'LU2ST402'],
                      ['LU2CI101', 'LU2CI102'], ['LU2EE201', 'LU2EE298'], ['LU2ME102', 'LU2ME004'],
                      ['LU2ST042', 'LU2ST043', 'LU2ST044'], ['LU2IAS41'], ['LU2HS008', 'LU2HST53', 'LU2HS016'],
                      ['LU2HS008', 'LU2HST53', 'LU2HST61'], 
                      ['LU2GSG41', 'LU2GSG42'], ['LU2EVE04', 'LU2EVE05'], ['LU2HNP34', 'LU2HNP42', 'LU2HNP43']
        ],
        'parcours': ['MAJ'],
        'nom'     : "MIN",
        'semestre': "S4"
    }

};

Irrelevant = ['LU2LVAN1'];
Ignore     = [item for sublist in Maquette['LK3PYMI0']['UE'] for item in sublist] + \
             [item for sublist in Maquette['LK4PYMI0']['UE'] for item in sublist];

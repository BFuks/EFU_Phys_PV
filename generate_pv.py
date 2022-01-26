#!/usr/bin/env python3

##########################################################
###                       Logger                       ###
###                                                    ###
### Permet d'afficher des messages en couleurs variees ###
###                                                    ###
##########################################################
import logging
import colored_log

colored_log.Init()
logger = logging.getLogger('mylogger')


##########################################################
###                     Main  code                     ###
###                                                    ###
##########################################################

## Welcome message
from misc import Start;
Start();


## Obtention de la liste des PV disponible
logger.info("");
logger.info("Obtention de la liste des PV disponibles");
from misc import GetPVList;
PV_dico = GetPVList();


## Choice du niveau
logger.warning("Choisir un niveau parmi:");
niveaux         = [x for x in PV_dico.keys()];
allowed_answers = [str(x+1) for x in list(range(len(niveaux)))];
for i in range(len(niveaux)):
    print('         *** ', i+1, ':', niveaux[i]);

answer = ""
answer = input("INFO   : Choix ? ")
while answer not in allowed_answers:
    logger.error('Reponse non pertinente');
    answer = input("INFO   : Choix parmi [" + ''.join(allowed_answers) + "]: ")
niveau = niveaux[int(answer)-1];

## Choice de l'annee
logger.warning("Choisir une annee parmi:");
annees          = [x for x in PV_dico[niveau].keys()];
allowed_answers = [str(x+1) for x in list(range(len(annees)))];
for i in range(len(annees)):
    print('         *** ', i+1, ':', annees[i]);

answer          = ""
answer = input("INFO   : Choix ? ")
while answer not in allowed_answers:
    logger.error('Reponse non pertinente');
    answer = input("INFO   : Choix parmi [" + ''.join(allowed_answers) + "]: ")
annee    = annees[int(answer)-1];

## Choice du parcours
logger.warning("Choisir un parcours parmi:");
parcours        = [x for x in PV_dico[niveau][annee].keys()];
allowed_answers = [str(x+1) for x in list(range(len(parcours)))];
for i in range(len(parcours)):
    print('         *** ', i+1, ':', parcours[i]);

answer = ""
answer = input("INFO   : Choix ? ")
while answer not in allowed_answers:
    logger.error('Reponse non pertinente');
    answer =input("INFO   : Choix parmi [" + ', '.join(allowed_answers) + "]: ")
parcours = parcours[int(answer)-1];


semestres = sorted([x for x in PV_dico[niveau][annee][parcours].keys()]);
if len(semestres)==1:
    logger.warning("Generation du PV pour le semestre : " + ', '.join(semestres) );
else:
    logger.warning("Generation du PV pour les semestres : " + ', '.join(semestres) );

## Obtention des infos
from xml_reader import GetXML, DecodeXML;
from pv_checker import SanityCheck;
from pv_writer  import PDFWriter;
all_PVs = {};
for semestre in semestres:
    logger.info("Lecture da la version XML du PV pour le semestre " + semestre);
    print("         *** Decodage des infos dans le PV");
    PV_semestre = GetXML(niveau, annee, semestre, parcours);
    PV_semestre = DecodeXML(PV_semestre);
    print("         *** Verification des moyennes du PV");
    SanityCheck(PV_semestre, parcours);
    all_PVs[semestre] = PV_semestre;

logger.info("Creation de la version PDF du PV " + parcours + " (" + annee + ")");
PDFWriter(all_PVs, annee, niveau, parcours, semestres);


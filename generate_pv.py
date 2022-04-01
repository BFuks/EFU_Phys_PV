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
from misc import Start,Bye;
Start();

# Options
import getopt, sys;

try:   optlist, arglist = getopt.getopt(sys.argv[1:], "d", ["debug"]);
except getopt.GetoptError as err:
    logger.error(str(err));
    Bye();

for o,a in optlist:
    if o in ["-d", "--debug"]: logger.setLevel(logging.DEBUG);

## Obtention de la liste des PV disponible
logger.info("");
logger.info("Obtention de la liste des PV disponibles");
from misc import GetPVList;
PV_dico = GetPVList();

# Safety
if len(PV_dico) == 0:
  logger.error("Pas de PV disponibles");
  Bye();

## Choice du niveau
logger.warning("Choisir un niveau parmi:");
niveaux         = sorted([x for x in PV_dico.keys()]);
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

## Obtention des infos et verifications
from xml_reader import GetXML, DecodeXML;
from pv_checker import SanityCheck;
all_PVs = {};
for semestre in semestres:
    logger.info("Lecture da la version XML du PV pour le semestre " + semestre);
    print("         *** Decodage des infos dans le PV");
    PV_semestre = GetXML(niveau, annee, semestre, parcours);
    PV_semestre = DecodeXML(PV_semestre);
    print("         *** Verification des moyennes du PV");
    all_PVs[semestre] = SanityCheck(PV_semestre, parcours, semestre);

## Statistics
from statistics import GetStatistics;
for semestre in semestres:
    logger.info("Generation des satistique du PV pour le semestre " + semestre);
    all_PVs[semestre] = GetStatistics(all_PVs[semestre], parcours, semestre);

## Creation des PV pirates
from pv_writer  import PDFWriter;
logger.info("Creation de la version PDF du PV " + parcours + " (" + annee + ")");
PDFWriter(all_PVs, annee, niveau, parcours, semestres);


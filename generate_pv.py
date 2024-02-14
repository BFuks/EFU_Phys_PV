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

## Choix du niveau, de l'annee et du parcours
from misc import Niveau, Year, Parcours;
niveau   = Niveau(PV_dico.keys());
annee    = Year(PV_dico[niveau].keys());
parcours = Parcours(PV_dico[niveau][annee].keys());

# Semestres disponibles
semestres = sorted([x for x in PV_dico[niveau][annee][parcours].keys()]);
if len(semestres)==1: logger.warning("Generation du PV pour le semestre : " + ', '.join(semestres) );
else:                 logger.warning("Generation du PV pour les semestres : " + ', '.join(semestres) );

## Obtention des infos et verifications
from xml_reader import GetXML, DecodeXML, Patch_DM;
from pv_checker import SanityCheck;
all_PVs = {};
for semestre in semestres:
    logger.info("Lecture da la version XML du PV pour le semestre " + semestre);
    print("         *** Decodage des infos dans le PV");
    if parcours in ['DM'] and 'S3' in semestre:
        PV_semestre = {};
        for i in range(1,3):
            PV_tmp = DecodeXML(GetXML(niveau, annee, semestre, parcours+str(i)));
            PV_semestre = Patch_DM(PV_tmp, PV_semestre);
    else: PV_semestre = DecodeXML(GetXML(niveau, annee, semestre, parcours));
    print("         *** Verification des moyennes du PV");
    all_PVs[semestre] = SanityCheck(PV_semestre, parcours, semestre);

## Merging 1st and 2nd session
from session_merger import Merge;
for sess2 in [x for x in all_PVs.keys() if "Session2" in x]:
    # safety
    if not sess2.replace('2', '1') in all_PVs.keys():
        logger.error('2nde session disponible (' + sess2+') pour un semestre sans 1ere session');
        all_PVs[sess2.replace('2','1')] = all_PVs[sess2];
    # merging 
    all_PVs[sess2.replace('2','1')] = Merge(all_PVs[sess2.replace('2','1')], all_PVs[sess2]);
    del all_PVs[sess2];
semestres = [x for x in semestres if not 'Session2' in x];

## Statistics
from stat_efu import GetStatistics, GetMoyenneAnnuelle;
for semestre in semestres:
    logger.info("Generation des statistiques du PV pour le semestre " + semestre);
    all_PVs[semestre] = GetStatistics(all_PVs[semestre], parcours, semestre);
logger.info("Calcul des moyennes annuelles");
all_PVs = GetMoyenneAnnuelle(all_PVs);

## Creation des PV pirates
from pv_writer  import PDFWriter;
logger.info("Creation de la version PDF du PV " + parcours + " (" + annee + ")");
PDFWriter(all_PVs, annee, niveau, parcours, semestres,redoublants=False, success=False);

## # CSV writer
## from csv_converter import merge, convert, ToExcelPV
## logger.info("Creation de la version Excel du PV " + parcours + " (" + annee + ")");
## merged_pvs = convert(merge(all_PVs));
## ToExcelPV(merged_pvs, annee, niveau, parcours);


# Bye bye
Bye();

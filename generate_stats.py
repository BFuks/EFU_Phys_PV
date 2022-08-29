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
logger.info("Statistiques extraites sur les annees :");
from misc import GetStatList;
years = GetStatList();


# Safety
if len(years) == 0:
  logger.error("Pas de donnees disponibles pour generer les stats");
  Bye();

## Obtention des infos et verifications
from xml_reader import GetXMLStats, DecodeXMLStats;
# from pv_checker import SanityCheck;
# from session_merger import Merge;
all_stats = {};
for year in years:
    logger.info("Lecture da la version XML des stats pour l'annee " + year);
    print("         *** Decodage des infos dans le traitement 24");
    ind_stats = GetXMLStats(year);
    ind_stats = DecodeXMLStats(ind_stats);
    all_stats[year] = ind_stats;

# en attendant, a fixer plus tard
logger.warning('Attention : merging a implementer lorsqu\'on aura le traitement 24 de deux annees');
for k in all_stats.keys(): all_stats = all_stats[k];

# CSV / xlsx writer
from csv_converter import StatConverter, ToExcel;
csv_stats = ToExcel(StatConverter(all_stats));

# bye bye
Bye();

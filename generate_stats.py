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
from xml_reader     import GetXMLStats, DecodeXMLStats, GetXML, DecodeXML;
from pv_stat_merger import PVtoStats;
from pv_checker import SanityCheck;
import glob;
import os;
all_stats = {};
for year in years:
    logger.info("Lecture da la version XML des stats pour l'annee " + year);
    # traitement 24
    print("         *** Decodage des infos dans le traitement 24");
    ind_stats = GetXMLStats(year);
    ind_stats = DecodeXMLStats(ind_stats);

    # PVs
    print("         *** Extraction de l'information des PVs");
    pvs = [x.split('/')[-1] for x in glob.glob(os.path.join(os.getcwd(), 'data/L*')) if year in x ];
    i=0
    for pv_name in pvs:
        print(pv_name);
        niveau = pv_name.split('_')[0];
        semestre = pv_name.split('_')[3] + '_' +pv_name.split('_')[4];
        parcours = pv_name.split('_')[5].split('.')[0];
        PV = GetXML(niveau, year, semestre, parcours);
        PV = SanityCheck(DecodeXML(PV),parcours,semestre);
        ind_stats = PVtoStats(ind_stats, PV, semestre);
        if i!=2:i+=1;
        else: break;

    # save 
    all_stats[year] = ind_stats;

# en attendant, a fixer plus tard
logger.warning('Attention : merging a implementer lorsqu\'on aura le traitement 24 de deux annees');
for k in all_stats.keys(): all_stats = all_stats[k];

# CSV / xlsx writer
from csv_converter import StatConverter, ToExcel;
csv_stats = ToExcel(StatConverter(all_stats));

# bye bye
Bye();

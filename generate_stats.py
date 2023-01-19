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
    for pv_name in sorted(pvs):
        niveau = pv_name.split('_')[0];
        semestre = pv_name.split('_')[3] + '_' +pv_name.split('_')[4];
        parcours = pv_name.split('_')[5].split('.')[0];
        PV = DecodeXML(GetXML(niveau, year, semestre, parcours));
        if 'DM' in parcours and not 'PAD' in parcours: parcours='DM';
        logger.disabled = True;
        PV = SanityCheck(PV,parcours,semestre);
        logger.disabled = False;
        ind_stats = PVtoStats(ind_stats, PV, semestre, parcours);

    # save 
    all_stats[year] = ind_stats;

# en attendant, a fixer plus tard
from pv_stat_merger import MergeStats;
logger.info('Fusion des differentes annees disponibles');
new_stats = MergeStats(all_stats);
known_ids = [];
for k in all_stats.keys(): known_ids =  known_ids + list(all_stats[k].keys());

# Reader des stats de Marion
from csv_provenance import MergeProvenance;
logger.info("Fusion de l'information \"provenance\"");
years, new_stats = MergeProvenance(years, new_stats, known_ids);

# Reader des listes de Casper
from casper_tools import ReadCasperLists;
logger.info("Extraction des listes \"Casper\"");
casper_data = ReadCasperLists();

# Reader pour les notes de Casper
from casper_tools import ReadCasperNotes;
logger.info("Extraction des notes \"Casper\"");
years, casper_data = ReadCasperNotes(casper_data, years);

# Merging all Casper lists
from casper_tools import MergeCasper;
logger.info("Fusion des infos \"Casper\"");
new_stats = MergeCasper(casper_data, new_stats);

# Reader de l'info Apogee pre 2021-2022
from apogee_tools import ReadApogeeLists;
logger.info("Extraction des listes Apogée antérieures à 2021")
new_stats = ReadApogeeLists(new_stats);

# Selection of the year to generate the file for
years = sorted(years);
logger.warning("Choisir une annee parmi:");
allowed_answers = [str(x+1) for x in list(range(len(years)))];
for i in range(len(years)): print('         *** ', i+1, ':', years[i].replace('_',' - '));
answer = ""
answer = input("INFO   : Choix ? ")
while answer not in allowed_answers:
    logger.error('Reponse non pertinente');
    answer = input("INFO   : Choix parmi [" + ', '.join(allowed_answers) + "]: ")
my_year = years[int(answer)-1];

# CSV / xlsx writer
from csv_converter import StatConverter, ToExcel;
output_stats = {};
for etu, value in new_stats.items():
    # no register for the current student and the year considered
    if not my_year in value['parcours'].keys(): continue;
    # we need to record the student
    output_stats[etu] = {};
    for key, keyvalue in new_stats[etu].items():
        if key in ['sexe', 'nom', 'prenom', 'date_naissance', 'mail', 'bourse', 'annee_bac', 'pays_bac', 'inscr_SU']: output_stats[etu][key] = keyvalue;
        elif key == 'parcours': output_stats[etu][key] = keyvalue[my_year];
        elif key == 'N-1': output_stats[etu][key] = keyvalue[my_year];
    if my_year in new_stats[etu].keys(): output_stats[etu] = {**output_stats[etu], **new_stats[etu][my_year]};
    else: output_stats[etu]['notes Session1'] = {};
csv_stats = ToExcel(StatConverter(output_stats),my_year);


## # Data pour Edouard
## from pv_stat_merger import FormatiseStats;
## logger.warning('Infos pour Edouard');
## output_stats = FormatiseStats(output_stats,my_year);

# bye bye
Bye();

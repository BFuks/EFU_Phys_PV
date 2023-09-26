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

## Obtention de la liste des PV disponibles
logger.info("");
logger.info("Obtention de la liste des PV disponibles");
from misc import GetPVList;
PV_dico = GetPVList();

# Safety
if len(PV_dico) == 0:
  logger.error("Pas de donnees disponibles pour generer les histos");
  Bye();

## Choix du niveau, de l'annee et du parcours
from misc import Niveau, Year, Parcours;
all_parcours = {
  'Intensif': ['SPRINT', 'CMI', 'DM'],
  'Standard': ['MONO', 'MAJ'],
  'PAD':      ['PADMONO', 'PADMAJ']
};
niveau    = Niveau(PV_dico.keys());
annee     = Year(PV_dico[niveau].keys());
prcrs_key = Parcours(all_parcours.keys());
parcours  = sorted(all_parcours[prcrs_key]);

# Semestres disponibles
semestres = [];
for my_parcours in parcours: semestres+=[x for x in PV_dico[niveau][annee][my_parcours].keys()];
semestres = sorted(list(set(semestres)));
if len(semestres)==1: logger.warning("Generation du PV pour le semestre : " + ', '.join(semestres) );
else:                 logger.warning("Generation du PV pour les semestres : " + ', '.join(semestres) );

## Obtention des infos et verifications
import os;
from xml_reader import GetXML, DecodeXML, Patch_DMS6;
from pv_checker import SanityCheck;
all_PVs = {};
for semestre in semestres:
    # Initialisation
    all_PVs[semestre] = {};

    # Now the loop
    #  if 'DM' in parcours: parcours+= ['DM2', 'DM3', 'DM4', 'DM5', 'DM6'] ;  ### OLD STUFF, not needed from 2022
    for my_parcours in parcours:
        # Safety
        if not os.path.isfile(os.path.join(os.getcwd(),'data', niveau+'_'+annee+'_'+semestre+'_'+my_parcours+'.dat')): continue;

        # Getting PV information (and using the patch DM-S6 to merge all PVs)
        logger.info("Lecture de la version XML du PV " + my_parcours + " pour le semestre " + semestre);
        PV_tmp = DecodeXML(GetXML(niveau, annee, semestre, my_parcours));

        # Extra computations
        tag = 'DM' if my_parcours.startswith('DM') else my_parcours;
#        if parcours == 'PAD': tag = my_parcours;
        logger.disabled = True; PV_tmp = SanityCheck(PV_tmp,tag,semestre); logger.disabled = False;

        # Fusion des infos avec les PVs deja existants
        all_PVs[semestre] = Patch_DMS6(PV_tmp, all_PVs[semestre]);

## Merging 1st and 2nd session
from session_merger import Merge;
for sess2 in [x for x in all_PVs.keys() if "Session2" in x]:
    # safety
    if not sess2.replace('2', '1') in all_PVs.keys():
        logger.error('2nde session disponible (' + sess2+') pour un semestre sans 1ere session');
        all_PVs[sess2.replace('2','1')] = all_PVs[sess2];
    # merging 
    logger.disabled = True;
    all_PVs[sess2.replace('2','1')] = Merge(all_PVs[sess2.replace('2','1')], all_PVs[sess2]);
    logger.disabled = False;
    del all_PVs[sess2];
semestres = [x for x in semestres if not 'Session2' in x];


# Histograms
from histogram import GetCCIData, GetHistoData, MakePlot2, MakePie2;
all_stats, stats_session1, stats_session2 = GetHistoData(all_PVs);
success_session1, success_session2 =  GetCCIData(all_PVs);
for variable in [x for x in stats_session1.keys() if x.startswith('S')]:
    title = 'Parcours ' + prcrs_key.lower() + '; ' + variable + ' (' + annee.replace('_','-') + ')';
    filename  = 'cci/' + variable + '_' + prcrs_key.lower() +'_' +annee.replace('_','-') + '.png'
    MakePlot2(variable, [ stats_session1[variable], stats_session2[variable]], title, filename);
    MakePie2(title, [success_session1[variable+'_validation'], success_session2[variable+'_validation']], filename.replace('cci/','cci/pie_'));

# Bye bye
Bye();

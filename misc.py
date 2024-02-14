##########################################################
###                        Misc                        ###
###                                                    ###
###         Boite a outils avec un peu de tout         ###
###                                                    ###
##########################################################


##########################################################
###                                                    ###
###                       Logger                       ###
###                                                    ###
##########################################################
import logging;
logger = logging.getLogger('mylogger');


##########################################################
###                                                    ###
###                  Welcome message                   ###
###                                                    ###
##########################################################
import time;
def Start():
    logger.info('Debut du run le ' + time.asctime(time.localtime(time.time())))


##########################################################
###                                                    ###
###                  Bye bye message                   ###
###                                                    ###
##########################################################
import sys
def Bye():
    logger.info('Fin du run le ' + time.asctime(time.localtime(time.time())))
    sys.exit();


##########################################################
###                                                    ###
###              Liste des PV disponibles              ###
###                                                    ###
##########################################################
import glob, os

def GetPVList():
    # Init
    dico = {};

    # liste des ficheirs disponibles
    for pv in glob.glob(os.path.join(os.getcwd(), 'data/L*')):
        # infos generales sur le PV
        pv_data  = pv.split('/')[-1].split('_');
        niveau   = pv_data[0];
        year     = pv_data[1]+'_'+pv_data[2];
        parcours = pv_data[-1].split('.')[0];
        session  = pv_data[3]+'_'+pv_data[4];

        # Patch DM
        if parcours[0:2]=='DM': parcours = 'DM';

        # sauvegarde des infos
        if not niveau in dico.keys():
            dico[niveau] = {};
        if not year in dico[niveau].keys():
            dico[niveau][year] = {};
        if not parcours in dico[niveau][year].keys():
            dico[niveau][year][parcours] = {};
        if not session in dico[niveau][year][parcours].keys():
            dico[niveau][year][parcours][session] = {};

    # Output
    return dico;



##########################################################
###                                                    ###
###    Liste des annees disponibles pour les stats     ###
###                                                    ###
##########################################################
def GetStatList():
    # Init
    dico = [];

    # liste des ficheirs disponibles
    for myfile in glob.glob(os.path.join(os.getcwd(), 'data/stat*')):

        # infos generales sur le PV
        stat_data = myfile.split('/')[-1].split('.')[0].split('_');
        year     = stat_data[-2]+'_'+stat_data[-1];

        # sauvegarde des infos
        dico.append(year);

    # Output
    return dico;


##########################################################
###                                                    ###
###                List flattening                     ###
###                                                    ###
##########################################################
from collections.abc import Iterable
def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)): yield from flatten(el)
        else: yield el



##########################################################
###                                                    ###
###         Get information from the structure         ###
###                                                    ###
##########################################################
from maquette import Maquette, UEs;
def GetBlocsMaquette(semestre,parcours):
    return sorted([x for x in Maquette.keys() if parcours in Maquette[x]['parcours'] and semestre == Maquette[x]['semestre']]);

import itertools;
def GetUEsMaquette(blocs_maquette):
    length = len( [Maquette[x]['UE'] for x in blocs_maquette ] );
    UEs_maquette = [Maquette[x]['UE'] for x in blocs_maquette][length-1];
    while length>1:
        UEs_maquette = [sorted(list(flatten(x))) for  x in itertools.product(UEs_maquette, [Maquette[x]['UE'] for x in blocs_maquette][length-2])];
        length-=1;
    return UEs_maquette;



##########################################################
###                                                    ###
###    Liste des niveaux disponibles pour les PVs      ###
###                                                    ###
##########################################################
def Niveau(all_niveaux):
    # Allowed options
    logger.warning("Choisir un niveau parmi:");
    niveaux         = sorted([x for x in all_niveaux]);
    allowed_answers = [str(x+1) for x in list(range(len(niveaux)))];

    # Printout
    for i in range(len(niveaux)): print('         *** ', i+1, ':', niveaux[i]);

    # Choice
    answer = ""
    answer = input("INFO   : Choix ? ")
    while answer not in allowed_answers:
        logger.error('Reponse non pertinente');
        answer = input("INFO   : Choix parmi [" + ''.join(allowed_answers) + "]: ")

    # Output
    return niveaux[int(answer)-1];



##########################################################
###                                                    ###
###     Liste des années disponibles pour les PVs      ###
###                                                    ###
##########################################################
from __version__ import __version__
def Year(all_years):
    # Allowed options
    logger.warning("Choisir une annee parmi:");
    annees          = sorted([x for x in all_years], reverse=True);
    allowed_answers = [str(x+1) for x in list(range(len(annees)))];

    # Printout
    for i in range(len(annees)): print('         *** ', i+1, ':', annees[i]);

    # Choice
    answer          = ""
    answer = input("INFO   : Choix ? ")
    while answer not in allowed_answers:
        logger.error('Reponse non pertinente');
        answer = input("INFO   : Choix parmi [" + ''.join(allowed_answers) + "]: ")

    # Output
    if int(annees[int(answer)-1].split('_')[0])>=int(__version__[1:]):
        return annees[int(answer)-1];
    else:
        logger.error('Pour des PV antérieurs à 2023, il faut utiliser la version v2020-2023 du code (git switch v2020-2023)')
        logger.error('Exiting...')
        sys.exit()


##########################################################
###                                                    ###
###    Liste des parcours disponibles pour les PVs     ###
###                                                    ###
##########################################################
def Parcours(all_parcours):
    # Allowed options
    logger.warning("Choisir un parcours parmi:");
    parcours        = sorted([x for x in all_parcours]);
    allowed_answers = [str(x+1) for x in list(range(len(parcours)))];

    # Printout
    for i in range(len(parcours)): print('         *** ', i+1, ':', parcours[i]);

    # Choice
    answer = ""
    answer = input("INFO   : Choix ? ")
    while answer not in allowed_answers:
        logger.error('Reponse non pertinente');
        answer =input("INFO   : Choix parmi [" + ', '.join(allowed_answers) + "]: ")

    # Output
    return parcours[int(answer)-1];


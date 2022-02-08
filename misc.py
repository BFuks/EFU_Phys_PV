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
    for pv in glob.glob(os.path.join(os.getcwd(), 'data/*')):
        # infos generales sur le PV
        pv_data  = pv.split('/')[-1].split('_');
        niveau   = pv_data[0];
        year     = pv_data[1]+'_'+pv_data[2];
        parcours = pv_data[-1].split('.')[0];
        session  = pv_data[3]+'_'+pv_data[4];

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


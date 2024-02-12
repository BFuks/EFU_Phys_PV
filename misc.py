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

        # Patch L3 - S6 and L2
        if parcours[0:2]=='DM': parcours = 'DM';
        # Patch L2 - S3/S4
        if parcours[0:3]=='MAJ': parcours = 'MAJ';

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
    if int(annees[int(answer)-1].split('_')[0])<=int(__version__[1:]):
        return annees[int(answer)-1];
    else:
        logger.error('Pour des PV de 2023 ou ultérieurs, il faut utiliser la version 2023 du code  (git switch main)')
        logger.error('Exiting...')
        sys.exit()
    bla


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




##########################################################
###                                                    ###
###    Hack special pour generer les PVs pour 2020     ###
###                                                    ###
##########################################################
def Hack2020(parcours, semestre, pv):
    PV_semestre = pv;
    prefix_to_nsem = {'S3': '3', 'S4': '4', 'S5': '5', 'S6': '6'}
    nsem = prefix_to_nsem.get(semestre[:2], None)

    if nsem=='3' and 28626888 in PV_semestre.keys(): del PV_semestre[28626888];
    if nsem=='6' and 3802880 in PV_semestre.keys(): del PV_semestre[3802880];
    if nsem=='6' and 3802777 in PV_semestre.keys(): del PV_semestre[3802777];

    if parcours in ['MAJ', 'DM'] and int(nsem)<=4:
        for k,v in PV_semestre.items():
            muf = [k.split('-')[1].strip() for k,v in v['results'].items() if not 'PY' in k and ('note' in v.keys() or ('UE' in v.keys() and v['UE'] != None and v['UE'].startswith('LU2'))) and k!='999999'];
            muf = [x for x in muf if x.startswith('L') and not 'LV' in x]
            if 'LK3SSK00' in muf or 'LK4SSK00' in muf: muf = ['SS']
            if 'LU2SXDR2' in muf or 'LU2SXDR1' in muf: muf = ['DR']
            sumMIN=0.; ectsMIN=0;
            sumMAJ=0.; ectsMAJ=0;
            for kk, vv in v['results'].items():
                if kk=='999999' or 'MI0' in kk or 'LK' in kk or 'LY4ST' in kk or not 'note' in vv.keys() or not kk.split('-')[1].startswith('LU'): continue
                if 'PY' in kk or 'LV' in kk and not vv['validation'] in ['DIS', 'VAC']:
                    if ('LU2PY423' in kk and muf[0] in ['CI']) or ('LU2PY215' in kk and 'MA' in muf[0]):
                        ectsMIN += UEs[kk.split('-')[1].strip()]['ects']
                        sumMIN  += float(vv['note'])*UEs[kk.split('-')[1].strip()]['ects']
                    else:
                        if 'LU2PY123' in kk and muf[0] in ['ME', 'EE']: continue
                        ectsMAJ += UEs[kk.split('-')[1].strip()]['ects'];
                        sumMAJ  += float(vv['note'])*UEs[kk.split('-')[1].strip()]['ects'];
                elif 'LU2' in kk and not vv['validation'] in ['DIS', 'VAC']:
                    if parcours=='DM' and 'SX' in UEs[kk.split('-')[1].strip()].keys(): continue
                    mynote = 0 if vv['validation']=='AJ' and vv['note']==None else float(vv['note']);
                    ectsMIN += UEs[kk.split('-')[1].strip()]['ects']
                    sumMIN  += mynote*UEs[kk.split('-')[1].strip()]['ects']
                elif not vv['validation'] in ['DIS', 'VAC']:
                    mynote=vv['note'];
                    mynote = 0 if mynote==None else float(mynote);
                    sumMIN  += UEs[vv['UE']]['ects']*mynote
                    ectsMIN += UEs[vv['UE']]['ects']
            if muf!=['SS'] and muf!=['DR']: muf = [x[3:5] for x in muf ]
            muf = list(set(muf))
            if len(muf)==1:
               my_v = v;
               MAJ = 0 if ectsMAJ==0 else sumMAJ/ectsMAJ;
               MIN = 0 if ectsMIN==0 else sumMIN/ectsMIN;
               if not muf==['SX'] and parcours=='MAJ':
                   my_v['results']['LK' + nsem + muf[0]+'M00'] = { 'tag': 'LK'+nsem+muf[0]+'M00', 'bareme':100, 'note':MIN, 'validation': None, 'annee_val': None, 'UE': None};
               elif (not muf==['SX'] and parcours=='DM' and not '71-LY3PYDM0 ' in my_v['results'].keys() and not '31-LK3PYDK0 ' in my_v['results'].keys())\
                   or '41-LU2SXDR1 ' in my_v['results'].keys() or '41-LU2SXDR2 ' in my_v['results'].keys() :
                   my_v['results']['LK' + nsem + muf[0]+'D00'] = { 'tag': 'LK'+nsem+muf[0]+'M00', 'bareme':100, 'note':MIN, 'validation': None, 'annee_val': None, 'UE': None};
               if '21-LY3PYJ10 ' in my_v['results'].keys() and '11-LK3PYJ10 ' in my_v['results'].keys(): del my_v['results']['21-LY3PYJ10 ']
               if not '11-LK3PYJ10 ' in my_v['results'].keys() and not '11-LK4PYJ21 ' in my_v['results'].keys():
                   my_v['results']['LK' + nsem + 'PYJ00']      = { 'tag': 'LK'+nsem+'PYJ00', 'bareme':100, 'note':MAJ, 'validation': None, 'annee_val': None, 'UE': None};
               if 'LK4CID00' in my_v['results'].keys():
                   tmp = my_v['results']['51-LU2PY423 '];
                   my_v['results']['51-LU2PY423 '] = my_v['results']['41-LU2PY123 '];
                   my_v['results']['41-LU2PY123 '] = tmp;
               PV_semestre[k] = my_v
            else:
               print([k for k,v in v['results'].items() if not 'PY' in k and ('note' in v.keys() or ('UE' in v.keys() and v['UE'] != None and v['UE'].startswith('LU2')) )])
               print('\n', v)
               bla

    elif parcours in ['MAJ', 'DM'] and int(nsem)>=5:
        for k,v in PV_semestre.items():
            muf = [k.split('-')[1].strip() for k,v in v['results'].items() if not 'PY' in k and ('note' in v.keys() or ('UE' in v.keys() and v['UE'] != None and v['UE'].startswith('LU2'))) and k!='999999'];
            muf = [x for x in muf if x.startswith('L') and not 'LV' in x]
            sumMIN=0.; ectsMIN=0;
            sumMAJ=0.; ectsMAJ=0;
            for kk, vv in v['results'].items():
                if kk=='92-LY6EEM00 ': ue = 'LU3EE200'
                elif 'LY' in kk and 'UE' in vv.keys() and vv['UE']!=None: ue = vv['UE'];
                elif (kk=='999999' or 'MI0' in kk or 'LK' in kk or not 'note' in vv.keys() or not kk.split('-')[1].startswith('LU')) and not kk in ['81-LK5HIM00 ', '81-LK5HSM00 ', '81-LK5INM00 ']: continue
                else: ue = kk.split('-')[1].strip();
                if ue=='LK5HIM00': ue='LU3HI000';
                if ue=='LK5HSM00': ue='LU3HS000';
                if ue=='LK5INM00': ue='LU3IN000';
                if ue=='LK6EEM02': ue='LU3EE200';
                if ue=='LK6EEM01': ue='LU3EE204';
                if kk=='101-LY6SVM10 ': continue
                if ue in ['LK6CID02', 'LK5MAD01', 'LK6MAD02', 'LK5MED01', 'LK6MED01', 'LK5ST112', 'LK5ST113', 'LU3ST504', 'LK6STD15']: continue
                if 'PY' in ue or ('LV' in ue and (parcours!='DM' or 'LY5MAD01' in muf)) and not vv['validation'] in ['DIS', 'VAC']:
                    #print(kk, 'MAJ', ue, vv)
                    ectsMAJ += UEs[ue]['ects'];
                    sumMAJ  += float(vv['note'])*UEs[ue]['ects'];
                elif 'validation' in vv.keys() and 'note' in vv.keys() and not vv['validation'] in ['DIS', 'VAC']:
                    mynote=vv['note'];
                    mynote = 0 if mynote==None else float(mynote);
                    if ue in ['LU3HI000']: mynote*=5;
                    #print(kk, 'MIN', ue, vv)
                    sumMIN  += UEs[ue]['ects']*mynote
                    ectsMIN += UEs[ue]['ects']
                elif not ('validation' in vv.keys() and vv['validation'] in ['DIS', 'VAC']):
                    #print(kk, '???', ue, vv)
                    ectsMIN += UEs[ue]['ects']
            muf = [x[3:5] for x in muf ]
            muf = list(set(muf))
            if len(muf)==1:
               my_v = v;
               MAJ = 0 if ectsMAJ==0 else sumMAJ/ectsMAJ;
               MIN = 0 if ectsMIN==0 else sumMIN/ectsMIN;
               if parcours=='MAJ':
                   my_v['results']['LK' + nsem + muf[0]+'M00'] = { 'tag': 'LK'+nsem+muf[0]+'M00', 'bareme':100, 'note':MIN, 'validation': None, 'annee_val': None, 'UE': None};
                   my_v['results']['LK' + nsem + 'PYJDD']      = { 'tag': 'LK'+nsem+'PYJDD', 'bareme':100, 'note':MAJ, 'validation': None, 'annee_val': None, 'UE': None};
               elif parcours=='DM':
                   my_v['results']['LK' + nsem + muf[0]+'D00'] = { 'tag': 'LK'+nsem+muf[0]+'M00', 'bareme':100, 'note':MIN, 'validation': None, 'annee_val': None, 'UE': None};
                   my_v['results']['LK' + nsem + 'PYJEE']      = { 'tag': 'LK'+nsem+'PYJEE', 'bareme':100, 'note':MAJ, 'validation': None, 'annee_val': None, 'UE': None};
               if '91-LY6EEM00 ' in my_v['results'].keys():
                    my_v['results']['91-LU3EE204 '] = my_v['results']['91-LY6EEM00 '];
                    my_v['results']['91-LU3EE204 ']['UE']=None;
                    del my_v['results']['91-LY6EEM00 '];
               if '92-LY6EEM00 ' in my_v['results'].keys():
                    my_v['results']['92-LU3EE200 '] = my_v['results']['92-LY6EEM00 '];
                    my_v['results']['92-LU3EE200 ']['UE']=None;
                    if not 'note' in my_v['results']['92-LU3EE200 ']:
                        my_v['results']['92-LU3EE200 ']['note']='0'
                        my_v['results']['92-LU3EE200 ']['validation']='AJ'
                        my_v['results']['92-LU3EE200 ']['annee_val']= None
                    del my_v['results']['92-LY6EEM00 '];
               if 'LK5EED00' in my_v['results'].keys():
                   my_v['results']['LK5EED00'] = my_v['results']['91-LY5EED00 '];
                   del  my_v['results']['91-LY5EED00 ']
               keys_to_remove = [ '111-6ZVPYME1 ', '101-LY6SVM10 ', '51-LY5PYDM0 ', '61-LY5MED00 ', '141-LY6CID00 ','61-LK6SSK00 ',
                   '61-LK5SSK00 ', '71-LY5MAD00 ', '101-LY5STD00 ', '102-LY5STD00 ', '131-LY6MAD00 ', '191-LK6STD15 ',
                   '103-LY5STD00 ', '11-LK5PY900 ', '91-LY6MED00 ', '11-LK6PY900 ', '81-LK6PYDM0 ', '151-LY6STD00 ']
               for key in keys_to_remove:
                   if key in my_v['results']: del my_v['results'][key]
               PV_semestre[k] = my_v
               if k==3800504:print(my_v); #bla
            else:
               print(muf);
               print(k, [ke for ke,kv in v['results'].items() if not 'PY' in ke and ('note' in kv.keys() or ('UE' in kv.keys() and kv['UE'] != None and kv['UE'].startswith('LU2')) )])
               print('\n', v)
               bla

    elif parcours in ['CMI']:
        for k,v in PV_semestre.items():
            if k=='resume': continue;
            sumMIN=0.; ectsMIN=0;
            sumMAJ=0.; ectsMAJ=0;
            for kk, vv in v['results'].items():
                if 'LY' in kk and 'UE' in vv.keys() and vv['UE']!=None: ue = vv['UE'];
                elif kk=='999999' or 'LK' in kk or not 'note' in vv.keys() or not kk.split('-')[1].startswith('LU'): continue
                else: ue = kk.split('-')[1].strip();
                if 'PY' in ue or 'LV' in ue and not vv['validation'] in ['DIS', 'VAC']:
                    #print(kk, 'MAJ', ue, vv)
                    ectsMAJ += UEs[ue]['ects'];
                    sumMAJ  += float(vv['note'])*UEs[ue]['ects'];
                elif 'validation' in vv.keys() and 'note' in vv.keys() and not vv['validation'] in ['DIS', 'VAC']:
                    mynote=vv['note'];
                    mynote = 0 if mynote==None else float(mynote);
                    #print(kk, 'MIN', ue, vv)
                    sumMIN  += UEs[ue]['ects']*mynote
                    ectsMIN += UEs[ue]['ects']
                elif not ('validation' in vv.keys() and vv['validation'] in ['DIS', 'VAC']):
                    #print(kk, '???', ue, vv)
                    ectsMIN += UEs[ue]['ects']
                MAJ = 0 if ectsMAJ==0 else sumMAJ/ectsMAJ;
                MIN = 0 if ectsMIN==0 else sumMIN/ectsMIN;
            my_v = v;
            if int(nsem)>4:
                my_v['results']['LK' + nsem + 'PYJDD'] = { 'tag': 'LK'+nsem+'PYJDD', 'bareme':100, 'note':MAJ, 'validation': None, 'annee_val': None, 'UE': None};
                my_v['results']['LK' + nsem + 'PYMI0'] = { 'tag': 'LK'+nsem+'PYMI0', 'bareme':100, 'note':MIN, 'validation': None, 'annee_val': None, 'UE': None};
#            if k==3800328: print(my_v); bla
            keys_to_remove = ['82-LY3PY090 ', '51-LK3EEM00 ', '71-LK3PY090 ']
            for key in keys_to_remove:
                   if key in my_v['results']: del my_v['results'][key]
            PV_semestre[k] = my_v

    return PV_semestre;


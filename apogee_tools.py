##########################################################
###                                                    ###
###           Data from Marion -> Apogee               ###
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
###                  List of students                  ###
###                                                    ###
##########################################################
import math, pandas;
from csv_provenance import ParcoursApogee;
def ReadApogeeLists(stats):
    # init
    new_stats = stats;

    # raw data
    for sheet in ['2019', '2020']:

        # Initialisation of the excel sheet
        year = sheet + '_' + str(int(sheet)+1);
        print("         *** Extraction de l'année " + year);
        apogee_infos = pandas.read_excel('data/Apogee_liste1.xls', sheet_name=sheet, index_col=19, header=0);
        apogee_dico  = apogee_infos.to_dict('index');

        # List of all students
        for etu_id,value in apogee_dico.items():
            # Safety
            ok, parcours = ParcoursApogee(value['IAE - Etape (code)']);
            if not ok: continue;

            # bac
            try:
                if math.isnan(value['Bac - Département obtention (code)']): bac = '';
            except:
                dpt_bac = value['Bac - Département obtention (code)'].replace('02A','02').replace('02B','02');
                bac = 'France' if int(dpt_bac)<99 else 'Etranger';

            # notes
            session1 = -1 if value['VET - Note session 1']=='*' else value['VET - Note session 1'];
            session2 = -1 if value['VET - Note session 2']=='*' else value['VET - Note session 2'];

            # Existing student
            if etu_id in new_stats.keys():
                if new_stats[etu_id]['date_naissance'] == '': new_stats[etu_id]['date_naissance'] = value['Naissance - Date'].strftime("%d/%m/%Y");
                if new_stats[etu_id]['inscr_SU']       == '': new_stats[etu_id]['inscr_SU']       = value['Année de l\'inscription'];
                if not year in new_stats[etu_id]['bourse'].keys():   new_stats[etu_id]['bourse'][year] = value['Boursier (O/N)'].replace('O','oui').replace('N','non');
                if not year in new_stats[etu_id]['parcours'].keys(): new_stats[etu_id]['parcours'][year] = parcours;
                if not year in new_stats[etu_id]['N-1'].keys():      new_stats[etu_id]['N-1'][year] = '';
                if new_stats[etu_id]['pays_bac']       == '': new_stats[etu_id]['pays_bac']       = bac;
                if new_stats[etu_id]['sexe']           == '': new_stats[etu_id]['sexe']           = value['Individu - Sexe'];
                if not year in new_stats[etu_id].keys():
                     if session1!=-1 or session2!=-1: new_stats[etu_id][year] = {};
                     if session1!=-1: new_stats[etu_id][year]['notes Session1'] = {'Session1':session1};
                     if session2!=-1: new_stats[etu_id][year]['notes Session2'] = {'Session2':session2};
                else:
                    if session1!=-1:
                        if not 'notes Session1' in new_stats[etu_id][year].keys(): new_stats[etu_id][year]['notes Session1'] = {'Session1':session1};
                        else : new_stats[etu_id][year]['notes Session1']['Session1'] = session1;
                    if session2!=-1:
                         if not 'notes Session2' in new_stats[etu_id][year].keys(): new_stats[etu_id][year]['notes Session2'] = {'Session2':session2};
                         else : new_stats[etu_id][year]['notes Session2']['Session2'] = session2;

            # new student
            else:
                notes = {};
                if session1!=-1: notes['notes Session1'] = {'Session1':session1};
                if session2!=-1: notes['notes Session2'] = {'Session2':session2};
                new_stats[etu_id] = {
                    'N-1'            : {year:''},
                    'annee_bac'      : '',
                    'bourse'         : {year: value['Boursier (O/N)'].replace('O','oui').replace('N','non')},
                    'date_naissance' : value['Naissance - Date'].strftime("%d/%m/%Y"),
                    'inscr_SU'       : value['Année de l\'inscription'],
                    'mail'           : '',
                    'nom'            : '',
                    'prenom'         : '',
                    'parcours'       : {year:parcours},
                    'pays_bac'       : bac,
                    'prenom'         : '',
                    'sexe'           : value['Individu - Sexe'],
                     year            : notes
                };

            # cleaning
            new_stats[etu_id] = dict(sorted(new_stats[etu_id].items()));

    # Exit
    return new_stats;



def ReadApogeeT24(stats):
    # init
    new_stats = stats;

    # Initialisation of the excel sheet
    print("         *** Extraction de l'année 2020");
    year = '2020_2021';
    apogee_infos = pandas.read_excel('data/Apogee_T24_2020.xls', sheet_name='Traitement 24', header=0);
    apogee_infos.reset_index(inplace=True);
    apogee_dico  = apogee_infos.to_dict('index');

    # List of all students
    for value in apogee_dico.values():
        # Safety
        if value['CGE']!='L50': continue;

        # parcours
        ok, parcours = ParcoursApogee(value['VET'][:-4]);
        if not ok: continue;

        # Etu ID
        etu_id = value['Code étudiant'];

        # bourse
        bourse = 'non' if (isinstance(value['Code bourse'],str) or math.isnan(value['Code bourse'])) else 'oui';

        # Existing student
        if etu_id in new_stats.keys():
            if new_stats[etu_id]['sexe']           == '': new_stats[etu_id]['sexe']           = value['Sexe'];
            if new_stats[etu_id]['nom']            == '': new_stats[etu_id]['nom']            = value['NOM'];
            if new_stats[etu_id]['prenom']         == '': new_stats[etu_id]['prenom']         = value['PRENOM'];
            if new_stats[etu_id]['date_naissance'] == '': new_stats[etu_id]['date_naissance'] = value['Date de naissance'];
            if not year in new_stats[etu_id]['parcours'].keys(): new_stats[etu_id]['parcours'][year] = parcours;
            if not year in new_stats[etu_id]['bourse'].keys(): new_stats[etu_id]['bourse'][year] = bourse;

        # safety
        else:
            logger.error('Problème avec la lecture du traitement 24 2020');
            logger.error(etu_id + " : " + parcours +  '\n' + value);
            logger.error('old = ' + new_stats[etu_id]);
            import sys; sys.exit();

    # Output
    return new_stats;


def ReadApogee2020S3(stats):
    # init
    new_stats = stats;

    # Initialisation of the excel sheet
    print("         *** Extraction des infos du S3 2020");
    year = '2020_2021';
    apogee_infos = pandas.read_excel('data/Apogee_2020_S3.xls', sheet_name='Feuil1', header=0);
    apogee_infos.reset_index(inplace=True);
    apogee_dico  = apogee_infos.to_dict('index');

    # List of all students
    for value in apogee_dico.values():
        # Safety
        if not value['COD_ETU'] in new_stats.keys():
            logger.error('Étudiant inconnu (Apogee_2020_S3.xls) : ' + value['COD_ETU']);
            logger.error(value)
            import sys; sys.exit();

        # Update des informations
        if not '2020_2021' in new_stats[value['COD_ETU']].keys():
            new_stats[value['COD_ETU']]['2020_2021'] = {};
            new_stats[value['COD_ETU']]['2020_2021']['notes Session1'] = {};
        new_stats[value['COD_ETU']]['2020_2021']['notes Session1']['S3_Session1'] = value['NOT_ETU'];

        if value['LIC_ETU'] == 'S3 Physique Mono-I': new_stats[value['COD_ETU']]['parcours']['2020_2021']  = 'L2 SPRINT'

    # Output
    return new_stats;

import math;
from maquette import UEs;
def ReadApogee2020UEs(stats):
    # init
    new_stats = stats;

    # Initialisation of the excel sheet
    print("         *** Extraction des infos des UEs de 2020");
    year = '2020_2021';
    apogee_infos = pandas.read_excel('data/Apogee_2020_UEs.xlsx', sheet_name='Feuil1', header=0);
    apogee_infos.reset_index(inplace=True);
    apogee_dico  = apogee_infos.to_dict('index');

    # List of all students
    for value in apogee_dico.values():

        # safety
        if not value['COD_ETU'] in new_stats.keys(): continue;
        if not value['COD_ELP'] in UEs.keys(): continue;
        if not year in new_stats[value['COD_ETU']].keys(): new_stats[value['COD_ETU']][year] = {};

        # session 1
        if isinstance(value['NOT_ELP'],float) and not math.isnan(value['NOT_ELP']):
            if not 'notes Session1' in new_stats[value['COD_ETU']][year].keys(): new_stats[value['COD_ETU']][year]['notes Session1'] = {};
            new_stats[value['COD_ETU']][year]['notes Session1'][value['COD_ELP']] = value['NOT_ELP'];
        # session 2
        if isinstance(value['NOT_ELP1'],float) and not math.isnan(value['NOT_ELP1']):
            if not 'notes Session2' in new_stats[value['COD_ETU']][year].keys(): new_stats[value['COD_ETU']][year]['notes Session2'] = {};
            new_stats[value['COD_ETU']][year]['notes Session2'][value['COD_ELP']] = value['NOT_ELP1'];

    # Output
    return new_stats;


##########################################################
###                                                    ###
###                  List of notes                     ###
###                                                    ###
##########################################################
def ReadApogeeNotes(stats):
    # init
    new_stats = stats;

    # raw data
    for sheet in ['2019', '2020']:

            # Initialisation of the "list" excel sheet
            year = sheet + '_' + str(int(sheet)+1);
            print("         *** Check des listes de l'année " + year);
            apogee_infos = pandas.read_excel('data/Apogee_notes.xls', sheet_name=sheet, index_col=1, header=2);
            apogee_dico  = apogee_infos.to_dict('index');

            # List of all students
            for etu_id,value in apogee_dico.items():
                # Safety
                ok, parcours = ParcoursApogee(value['IAE - Etape (code)']);
                if not ok: continue;

                # The student must exist
                if etu_id in new_stats.keys(): continue;
                logger.error("new Apogee student not included in the " + sheet + " lists", etu_id);
                sys.exit();

            # Initialisation of the "notes" excel sheet
            print("         *** Extraction des notes de l'année " + year);
            apogee_infos = pandas.read_excel('data/Apogee_notes.xls', sheet_name="Note_"+sheet, header=0);
            apogee_infos.reset_index(inplace=True);
            apogee_dico  = apogee_infos.to_dict('index');

            # List of all students
            for value in apogee_dico.values():
                # Safety
                ok, parcours = ParcoursApogee(value['IAE - Etape (code)']);
                if not ok: continue;

                # Etu ID
                etu_id = value['Individu - Code Etudiant'];

                # The student must exist
                if not etu_id in new_stats.keys():
                    logger.error("new Apogee student not included in the " + sheet + " lists", etu_id);
                    sys.exit();

                # new information
                ue      = value['ELP (code)'];
                note    = value['ELP - Note'];
                session = value['ELP - Session (lib.)'];

                # Saving the information
                if not year in new_stats[etu_id].keys(): new_stats[etu_id][year] = {};
                if   session == 'Session 1':
                    if not 'notes Session1' in new_stats[etu_id][year].keys(): new_stats[etu_id][year]['notes Session1'] = {};
                    new_stats[etu_id][year]['notes Session1'][ue] = note;
                elif session == 'Session 2':
                    if not 'notes Session2' in new_stats[etu_id][year].keys(): new_stats[etu_id][year]['notes Session2'] = {};
                    new_stats[etu_id][year]['notes Session2'][ue] = note;

    # Exit
    return new_stats;

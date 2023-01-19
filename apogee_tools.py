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
            session1 = 0 if value['VET - Note session 1']=='*' else value['VET - Note session 1'];
            session2 = 0 if value['VET - Note session 2']=='*' else value['VET - Note session 2'];

            # Existing student
            if etu_id in new_stats.keys():
                if new_stats[etu_id]['bourse']         == '': new_stats[etu_id]['bourse']         = value['Boursier (O/N)'].replace('O','oui').replace('N','non');
                if new_stats[etu_id]['date_naissance'] == '': new_stats[etu_id]['date_naissance'] = value['Naissance - Date'].strftime("%d/%m/%Y");
                if new_stats[etu_id]['inscr_SU']       == '': new_stats[etu_id]['inscr_SU']       = value['Année de l\'inscription'];
                if not year in new_stats[etu_id]['parcours'].keys(): new_stats[etu_id]['parcours'][year] = parcours;
                if not year in new_stats[etu_id]['N-1'].keys():      new_stats[etu_id]['N-1'][year] = '';
                if new_stats[etu_id]['pays_bac']       == '': new_stats[etu_id]['pays_bac']       = bac;
                if new_stats[etu_id]['sexe']           == '': new_stats[etu_id]['sexe']           = value['Individu - Sexe'];
                if not year in new_stats[etu_id].keys(): new_stats[etu_id][year] = { 'Session1':session1, 'Session2':session2 };
                else:
                    new_stats[etu_id][year]['Session1'] = session1;
                    new_stats[etu_id][year]['Session2'] = session2;

            # new student
            else:
                new_stats[etu_id] = {
                    'N-1'            : {year:''},
                    'annee_bac'      : '',
                    'bourse'         : value['Boursier (O/N)'].replace('O','oui').replace('N','non'),
                    'date_naissance' : value['Naissance - Date'].strftime("%d/%m/%Y"),
                    'inscr_SU'       : value['Année de l\'inscription'],
                    'mail'           : '',
                    'nom'            : '',
                    'prenom'         : '',
                    'parcours'       : {year:parcours},
                    'pays_bac'       : bac,
                    'prenom'         : '',
                    'sexe'           : value['Individu - Sexe'],
                     year            : { 'Session1':session1, 'Session2':session2 }
                };

            # cleaning
            new_stats[etu_id] = dict(sorted(new_stats[etu_id].items()));

    # Exit
    return new_stats;

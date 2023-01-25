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
                if not year in new_stats[etu_id].keys(): new_stats[etu_id][year] = { 'notes Session1': {'Session1':session1}, 'notes Session2': {'Session2':session2} };
                else:
                    if not 'notes Session1' in new_stats[etu_id][year].keys(): new_stats[etu_id][year]['notes Session1'] = {'Session1':session1};
                    else : new_stats[etu_id][year]['notes Session1']['Session1'] = session1;
                    if not 'notes Session2' in new_stats[etu_id][year].keys(): new_stats[etu_id][year]['notes Session2'] = {'Session2':session2};
                    else : new_stats[etu_id][year]['notes Session2']['Session2'] = session2;

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
            print("         *** CHeck des listes de l'année " + year);
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
                if   session == 'Session 1': new_stats[etu_id][year]['notes Session1'][ue] = note;
                elif session == 'Session 2': new_stats[etu_id][year]['notes Session2'][ue] = note;

    # Exit
    return new_stats;

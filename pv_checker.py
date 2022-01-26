##########################################################
###                                                    ###
###                    PV checker                      ###
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
###        Verification et calcul de la note/100       ###
###                                                    ###
##########################################################
def CheckValidation(UE, id_etudiant, nom_etudiant, Silent=False):

    # safetfy check
    if UE['note']==None and UE['validation']=='DIS': return 'DIS';
    elif UE['note']==None: return -1;

    # verification du statut de validation
    note = float(UE['note'])/float(UE['bareme']);
    if note<0.5 and UE['validation']!='AJ' and UE['UE'] != None and not Silent:
        logger.error('Probleme avec le PV ' + str(id_etudiant) + ' (' + nom_etudiant +') : ' + UE['UE'] + ' devrait etre AJ');
    elif note>=0.5 and not UE['validation'] in ['VAC', 'ADM', 'U ADM'] and UE['UE'] != None  and not Silent:
        logger.error('Probleme avec le PV ' + str(id_etudiant) + ' (' + nom_etudiant +') : ' + UE['UE'] + ' devrait etre ADM');

    # calcul de la moyenne sur 100
    if UE['bareme']!='100': note = float(UE['note'])/float(UE['bareme'])*100.;
    return float(UE['note']);


##########################################################
###                                                    ###
###             Verification des moyennes              ###
###                                                    ###
##########################################################
from maquette import Maquette, UEs;
from misc     import Bye;
def CheckMoyennes(notes, blocs, parcours, etudiant_id, etudiant_nom):

    # Obtentien et verification de la liste  des blocs
    blocs_maquette = sorted([x for x in Maquette.keys() if parcours in Maquette[x]['parcours']]);
    blocs_pv       = [];
    for bloc in blocs_maquette:
        for set_ue in Maquette[bloc]['UE']:
            if True in [ set(x).issubset(set(list(notes.keys()))) for x in Maquette[bloc]['UE']] and not bloc in blocs_pv: blocs_pv.append(bloc)

    if not set(blocs_pv).issubset(set(blocs_maquette)):
        logger.error("Problemes de blocs dans le PV " + parcours + " (" + etudiant_id + ", " + etudiant_nom + "):");
        logger.error("  *** Blocs maquette = " + ', '.join(blocs_maquette));
        logger.error("  *** Blocs pv       = " + ', '.join(blocs_pv));
        Bye();

    # Verification des moyennes
    moyenne_tot  = 0.; coeff_tot    = 0.;
    for bloc in blocs_pv:
        temp_UEs = [x for x in Maquette[bloc]['UE'] if set(x).issubset(set(notes.keys())) ][0];
        moyenne_bloc = 0.; coeff_bloc   = 0.;
        for ue in temp_UEs:
            if ue not in UEs.keys():
                logger.error("Renseigner le coefficient de l'UE " + ue + " dans la maquette Apogee. Bye bye...");
                Bye();
            if notes[ue]=='DIS': continue;
            moyenne_bloc += notes[ue]*UEs[ue]['ects'];  coeff_bloc += UEs[ue]['ects'];
            moyenne_tot  += notes[ue]*UEs[ue]['ects'];  coeff_tot  += UEs[ue]['ects'];
        try:
           moyenne_bloc = round(moyenne_bloc/coeff_bloc,3);
        except:
           moyenne_bloc = 0.
        if bloc in blocs and moyenne_bloc != blocs[bloc]:
            logger.error("Problemes de moyenne de blocs dans le PV " + parcours  + " (" + etudiant_id + ", " + etudiant_nom + "):");
            logger.error("  *** Moyenne calculee " + bloc + " : " + str(moyenne_bloc));
            logger.error("  *** Moyenne Apogee   " + bloc + " : " + str(blocs[bloc]));
    try:
        moyenne_tot  = round(moyenne_tot/(5.*coeff_tot),3);
    except:
        moyenne_tot = -1;
    if(moyenne_tot != blocs['total']):
        logger.error("Problemes de moyenne totale dans le PV " + parcours  + " (" + etudiant_id + ", " + etudiant_nom + "):");
        logger.error("  *** Moyenne calculee : " + str(moyenne_tot));
        logger.error("  *** Moyenne Apogee   : " + str(blocs['total']));

    # output
    return;


##########################################################
###                                                    ###
###                 Main  routine                      ###
###                                                    ###
##########################################################
def SanityCheck(pv, parcours):
    # loop over all students
    for etudiant in [x for x in pv.keys() if isinstance(x, int)]:
        # Initialisation
        all_notes = {}; all_blocs = {};

        # Boucle sur les elements du PV
        for label, UE in pv[etudiant]['results'].items():
            # On a une UE
            if 'UE' not in UE.keys(): continue;
            if UE['UE'] != None or label.split('-')[-1] in UEs.keys():
                if UE['UE'] == None: UE['UE'] = label.split('-')[-1];
                all_notes[UE['UE']] = CheckValidation(UE, str(etudiant), pv[etudiant]['nom']);

            # On a un bloc
            else:
                all_blocs[label.split('-')[-1]] = CheckValidation(UE, str(etudiant), pv[etudiant]['nom']);

        # verification moyennes
        CheckMoyennes(all_notes, all_blocs, parcours,  str(etudiant), pv[etudiant]['nom']);

    # return
    return all_notes;

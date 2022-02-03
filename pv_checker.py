##########################################################
###                                                    ###
###                    PV checker                      ###
###                                                    ###
##########################################################



##########################################################
###                                                    ###
###                       Data                         ###
###                                                    ###
##########################################################
from maquette import Maquette, UEs;



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
def CheckValidation(nom_UE, data_UE, etu_id, etu_nom):
    # safetfy check
    ## ANCIENNE MAQUETTE - - - SIMPLFICIATION EFFECTUEE - - - A SUPPRIMER A UN MOMENT - - - TAG BENJ
    ## if UE['note']==None and UE['validation']=='DIS': return 'DIS';
    ## elif UE['note']==None: return -1;
    if data_UE['note']==None: return -1;

    # Calcul de la note
    note = float(data_UE['note'])/float(data_UE['bareme'])*100. if nom_UE!='total' else float(data_UE['note']);

    # Si on a un bloc, il n'y a rien a faire
    if nom_UE in Maquette.keys(): return round(note,3);

    # Verification du statut de validation
    if note<50. and data_UE['validation']!='AJ':
        logger.error('Probleme avec le PV de ' + str(etu_id) + ' (' + etu_nom +') : ' + nom_UE + ' devrait etre AJ');
    elif note>=50. and not data_UE['validation'] in ['VAC', 'ADM', 'U ADM']:
        logger.error('Probleme avec le PV de ' + str(etu_id) + ' (' + etu_nom +') : ' + nom_UE+ ' devrait etre ADM');

    # On a un UE; retour de la note sur 100
    return note;


##########################################################
###                                                    ###
###             Verification des moyennes              ###
###                                                    ###
##########################################################
def CheckMoyennes(data_pv, parcours, semestre, etu_id, etu_nom):

    # Obtentien des blocs et verification que la liste est complete
    blocs_maquette = sorted([x for x in Maquette.keys() if parcours in Maquette[x]['parcours'] and semestre == Maquette[x]['semestre']]);
    ## ANCIENNE MAQUETTE - - - SIMPLFICIATION EFFECTUEE - - - A SUPPRIMER A UN MOMENT - - - TAG BENJ
    ## blocs_pv= [];
    ## for bloc in blocs_maquette:
    ##     for set_ue in Maquette[bloc]['UE']:
    ##         if True in [ set(x).issubset(set(list(data_pv.keys()))) for x in Maquette[bloc]['UE']]: blocs_pv.append(bloc);

    ## if not set(blocs_pv).issubset(set(blocs_maquette)):
    ##     logger.error("Problemes de blocs dans le PV " + parcours + " (" + etudiant_id + ", " + etudiant_nom + "):");
    ##     logger.error("  *** Blocs maquette = " + ', '.join(blocs_maquette));
    ##     logger.error("  *** Blocs pv       = " + ', '.join(blocs_pv));
    ##     Bye();
    blocs_pv = sorted([x for x in data_pv.keys() if not x in UEs and not x in ['total', '999999']]);
    if blocs_maquette != blocs_pv:
         from misc     import Bye;
         logger.error("Problemes de blocs dans le PV de " + etu_nom + " (" + etu_id + "):");
         logger.error("  *** Blocs maquette = " + ', '.join(blocs_maquette));
         logger.error("  *** Blocs pv       = " + ', '.join(blocs_pv));
         Bye();

    # Verification des moyennes (blocs)
    moyenne_tot  = 0.; coeff_tot    = 0.;
    for bloc in blocs_pv:
        ## Calcul de la moyenne du bloc
        bloc_ues = [x for x in Maquette[bloc]['UE'] if set(x).issubset(set(data_pv.keys())) ][0];
        moyenne_bloc = 0.; coeff_bloc   = 0.;
        for ue in bloc_ues:
            if data_pv[ue]=='DIS': continue;
            moyenne_bloc += float(data_pv[ue]['note'])*UEs[ue]['ects'];  coeff_bloc += UEs[ue]['ects'];
            moyenne_tot  += float(data_pv[ue]['note'])*UEs[ue]['ects'];  coeff_tot  += UEs[ue]['ects'];
        try:    moyenne_bloc = round(moyenne_bloc/coeff_bloc,3);
        except: moyenne_bloc = 0.

        ## Verification de la moyenne du bloc
        if moyenne_bloc != float(data_pv[bloc]['note']):
            logger.error("Problemes de moyenne de blocs dans le PV de "  + etu_nom + " (" + etu_id + "):");
            logger.error("  *** Moyenne calculee " + bloc + " : " + str(moyenne_bloc));
            logger.error("  *** Moyenne Apogee   " + bloc + " : " + str(data_pv[bloc]['note']));

    ## Calcul de la moyenne du semestre
    try:    moyenne_tot  = round(moyenne_tot/(5.*coeff_tot),3);
    except: moyenne_tot = -1;
    if(moyenne_tot != float(data_pv['total']['note'])):
        logger.error("Problemes de moyenne totale dans le PV de "  + etu_nom + " (" + etu_id + "):");
        logger.error("  *** Moyenne calculee : " + str(moyenne_tot));
        logger.error("  *** Moyenne Apogee   : " + str(data_pv['total']));

    # output
    return;


##########################################################
###                                                    ###
###                 Main  routine                      ###
###                                                    ###
##########################################################
def SanityCheck(pv, parcours, semestre):
    # output
    new_pv = {};

    # loop over all students
    for etudiant in [x for x in pv.keys() if isinstance(x, int)]:
        # Initialisation
        logger.debug("etudiant = " + str( etudiant));
        pv_individuel = {};

        # Boucle sur les elements du PV
        for label, data_UE in pv[etudiant]['results'].items():
            ## On a un element de PV, qui peut etre a ce stade soit une UE soit un bloc
            my_label = label.split('-')[-1];

            ## Ici l'element est vide : on l'ignore
            if 'UE' not in data_UE.keys(): continue;

            ## DEBUG :  on print le nom de l'element et ce qu'il contient
            logger.debug('  > label = ' + my_label + "; UE = " + str(data_UE));

            ## ANCIENNE MAQUETTE - - - SIMPLFICIATION EFFECTUEE - - - A SUPPRIMER A UN MOMENT - - - TAG BENJ
            ## if data_UE['UE'] != None or label.split('-')[-1] in UEs.keys():
            ##     if data_UE['UE'] == None: data_UE['UE'] = label.split('-')[-1];
            ##     all_notes[data_UE['UE']] = CheckValidation(data_UE, str(etudiant), pv[etudiant]['nom']);
            pv_individuel[my_label] = {'note':CheckValidation(my_label, data_UE, str(etudiant), pv[etudiant]['nom']), 'annee_val':data_UE['annee_val']};

        # Verification des moyennes (blocs et semestre)
        CheckMoyennes(pv_individuel, parcours, semestre.split('_')[0], str(etudiant), pv[etudiant]['nom']);

        # Saving
        new_pv[etudiant] = { 'nom': pv[etudiant]['nom'], 'results':pv_individuel};
        logger.debug('  > saved_pv = ' + str(new_pv[etudiant]));

    # exit
    return new_pv;

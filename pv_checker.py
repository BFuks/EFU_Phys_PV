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
    if data_UE['validation']=='DIS': return 'DIS';
    if data_UE['validation']=='ABJ': data_UE['note']=0;
    if data_UE['note']==None: return -1;

    # Calcul de la note
    note = float(data_UE['note'])/float(data_UE['bareme'])*100. if nom_UE!='total' else float(data_UE['note']);

    # Si on a un bloc, il n'y a rien a faire
    if nom_UE in Maquette.keys() or nom_UE=='total': return round(note,3);

    # Verification du statut de validation
    if note<50. and data_UE['validation']!='AJ':
        logger.warning('Probleme avec le PV de ' + str(etu_id) + ' (' + etu_nom +') : ' + nom_UE.replace('_GS','') + ' devrait etre AJ');
    elif note>=50. and not data_UE['validation'] in ['VAC', 'ADM', 'U ADM']:
        logger.warning('Probleme avec le PV de ' + str(etu_id) + ' (' + etu_nom +') : ' + nom_UE.replace('_GS','') + ' devrait etre ADM');

    # On a un UE; retour de la note sur 100
    return note;


##########################################################
###                                                    ###
###             Verification des moyennes              ###
###                                                    ###
##########################################################
from misc import flatten, GetBlocsMaquette, GetUEsMaquette;
from maquette import GrosSac, GrosSac2;
def CheckMoyennes(data_pv, parcours, semestre, etu_id, etu_nom):

    # Obtentien des blocs et verification que la liste est complete
    blocs_maquette = GetBlocsMaquette(semestre, parcours);
    blocs_pv = sorted([x for x in data_pv.keys() if (x.startswith('LK') or not x in UEs) and not x in ['total', '999999'] and not x in GrosSac.keys()]);
    blocs_maquette = [x for x in blocs_maquette if not x in [x for x in UEs if x.startswith('LK')] or x in blocs_pv];

    # Verification qu'en cas d'UE dans le gros sac, les UE correspondent ne sont pas dans le PV
    for to_del in [x for x in data_pv.keys() if x+'_GS' in data_pv.keys()]:
       logger.warning("Problemes d'UE a supprimer dans le PV de " + etu_nom + " (" + etu_id + "): " + to_del);
       del data_pv[to_del];

    # Le POV est noettye, cest parti
    if blocs_maquette != blocs_pv:
         from misc     import Bye;
         logger.warning("Problemes de blocs sans notes dans le PV de " + etu_nom + " (" + etu_id + ")");
         for missing_bloc in [x for x in blocs_maquette if not x in blocs_pv]:
             logger.debug("  > Adding block " + missing_bloc);
             data_pv[missing_bloc] =  {'tag': Maquette[missing_bloc]['nom'], 'bareme': '100', 'validation': 'AJ', 'note': '-1', 'annee_val': None, 'UE': None};
             blocs_pv.append(missing_bloc);
         used_ues = [];
         for missing_ue in [x for x in GetUEsMaquette(blocs_maquette)[0] if not x in list(data_pv.keys())]:
             logger.debug("  > Ajout de l'UE manquante " + missing_ue);

             # est-ce que l'UE est dans le premier gros sac ?
             grossac = [x for x in data_pv.keys() if x in GrosSac.keys() and missing_ue in GrosSac[x] and not x in used_ues];
             if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac2.keys() and missing_ue in GrosSac2[x] ];

             # test si l'UE fait partie du 1er gros sac
             if len(grossac)>0:
                 annee = data_pv[grossac[0]]['note'];
                 coeff = sum([UEs[ue]['ects'] for ue in grossac]);
                 note = sum( [data_pv[ue]['note']*UEs[ue]['ects']/coeff for ue in grossac] );
                 data_pv[missing_ue] = {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': None, 'note': note, 'annee_val': None, 'UE': 'GrosSac'};
                 used_ues += grossac;

             # On a vraiment une UE manquante -> COVID
             elif not missing_ue+'_GS' in data_pv.keys():
                 logger.debug("  > Ajout de l'UE "+ missing_ue);
                 data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': 'AJ', 'note': 'COVID', 'annee_val': None, 'UE': None};
             else:
                 logger.debug("  > Ajout de l'UE "+ missing_ue);
                 data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': 'GS', 'note':'DIS', 'annee_val': None, 'UE': None};


    # Verification des moyennes (blocs)
    moyenne_tot  = 0.; coeff_tot    = 0.;
    for bloc in blocs_pv:
        ## Checking whether all UEs are present
        first = True;
        for missing_ue in [x for x in Maquette[bloc]['UE'][0] if not x in list(data_pv.keys())]:
            if first:
                logger.warning("Problemes d'UEs manquantes dans le PV de " + etu_nom + " (" + etu_id + "): bloc " + bloc);
                first=False;
            logger.warning("  > Ajout de l'UE manquante "+ missing_ue);
            val = 'ADM' if float(data_pv[bloc]['note'])>=50. else 'AJ';
            data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': val, 'note':data_pv[bloc]['note'],\
               'annee_val': None, 'UE': None};

        ## Calcul de la moyenne du bloc
        bloc_ues = [x for x in Maquette[bloc]['UE'] if set(x).issubset(set(data_pv.keys())) ][0];
        moyenne_bloc = 0.; coeff_bloc   = 0.;
        for ue in bloc_ues:
            if data_pv[ue]['note']=='DIS': continue;
            if data_pv[ue]['note'] != 'COVID':
                moyenne_bloc += float(data_pv[ue]['note'])*UEs[ue]['ects'];
                moyenne_tot  += float(data_pv[ue]['note'])*UEs[ue]['ects'];
            coeff_tot  += UEs[ue]['ects'];
            coeff_bloc += UEs[ue]['ects'];
        try:    moyenne_bloc = round(moyenne_bloc/coeff_bloc,3);
        except: moyenne_bloc = 0.

        ## Output and save if necessary
        if data_pv[bloc]['note']=='-1':
            logger.warning('  > Bloc ' + bloc + ' : moyenne calculee = ' + str(moyenne_bloc));
            data_pv[bloc]['note']=moyenne_bloc;

        ## Verification de la moyenne du bloc
        if abs(moyenne_bloc-float(data_pv[bloc]['note']))>0.002:
            logger.error("Problemes de moyenne de blocs dans le PV de "  + etu_nom + " (" + etu_id + "):");
            logger.error("  *** Moyenne calculee " + bloc + " : " + str(moyenne_bloc));
            logger.error("  *** Moyenne Apogee   " + bloc + " : " + str(data_pv[bloc]['note']));

    # Verification du nombre de credits
    credits = sum([UEs[x]['ects'] for x in data_pv.keys() if x in UEs.keys() and not '_GS' in x and not x.startswith('LK') and not ('UE' in data_pv[x].keys() and data_pv[x]['UE']=='GrosSac')]);
    if credits!=30: logger.warning("Problemes de nombre total d'ECTS dans le PV de " + etu_nom + " (" + etu_id + "): " + str(credits) + " ECTS");

    ## Calcul de la moyenne du semestre
    try:    moyenne_tot  = round(moyenne_tot/(5.*coeff_tot),3);
    except: moyenne_tot = -1;
    if data_pv['total']['note'] ==-1:
        logger.warning("Problemes de moyenne totale non calculee dans le PV de " + etu_nom + " (" + etu_id + ")");
        logger.warning("  > Moyenne calculee = " + str(moyenne_tot));
        data_pv['total']['note'] = moyenne_tot;
    if(moyenne_tot != float(data_pv['total']['note'])):
        logger.error("Problemes de moyenne totale dans le PV de "  + etu_nom + " (" + etu_id + "):");
        logger.error("  *** Moyenne calculee : " + str(moyenne_tot));
        logger.error("  *** Moyenne Apogee   : " + str(data_pv['total']['note']));

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
            my_label = label.split('-')[-1].strip();

            ## Ici l'element est vide : on l'ignore
            if 'UE' not in data_UE.keys(): continue;

            ## DEBUG :  on print le nom de l'element et ce qu'il contient
            logger.debug('  > label = ' + my_label + "; UE = " + str(data_UE));

            ## Extraction du PV
            if   my_label == 'LY5PY090': new_label = data_UE['UE'];
            elif my_label == 'LY5PY092': new_label = data_UE['UE'] + '_GS';
            else: new_label = my_label;
            if my_label in ['LY5PY090', 'LY5PY092']: data_UE['UE']=None;
            pv_individuel[new_label] = {'note':CheckValidation(new_label, data_UE, str(etudiant), pv[etudiant]['nom']), 'annee_val':data_UE['annee_val']};

        # Verification des moyennes (blocs et semestre)
        CheckMoyennes(pv_individuel, parcours, semestre.split('_')[0], str(etudiant), pv[etudiant]['nom']);

        # Saving
        new_pv[etudiant] = { 'nom': pv[etudiant]['nom'], 'results':pv_individuel};
        logger.debug('  > saved_pv = ' + str(new_pv[etudiant]));

    # exit
    return new_pv;

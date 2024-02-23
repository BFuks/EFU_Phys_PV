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
from maquette import IsModule;
def CheckValidation(nom_UE, data_UE, etu_id, etu_nom, nobloc=True, parcours='', compensation=False):
    # logger
    logger.debug("    -> Check validation de " + nom_UE + " : " + str(data_UE))

    # safety check
    if data_UE['validation'] in ['NCAE', 'ENCO', 'DIS', 'U VAC']: return data_UE['validation'];
    if data_UE['validation']=='ABJ': data_UE['note']=0;
    if data_UE['note']==None and data_UE['validation']=='VAC': return 'VAC';
    if data_UE['note']==None: return -1;
    if data_UE['note']=='???': return '???';

    # Calcul de la note
    note = float(data_UE['note'])/float(data_UE['bareme'])*100. if nom_UE!='total' and nobloc else float(data_UE['note']);
    if nom_UE in IsModule or (nom_UE.startswith('LK') and nobloc): return note;

    # Verification du statut de validation
    threshold = 50. if nom_UE!='total' else 10.
    if note<threshold and not data_UE['validation'] in ['AJ', 'ABJ']:
        logger.warning('Probleme avec le PV de ' + str(etu_id) + ' (' + str(etu_nom) +') : ' + nom_UE + ' devrait etre AJ');
    elif note>=threshold and not data_UE['validation'] in ['VAC', 'ADM', 'U ADM'] and not compensation:
        logger.warning('Probleme avec le PV de ' + str(etu_id) + ' (' + etu_nom +') : ' + nom_UE + ' devrait etre ADM');

    # On a un UE; retour de la note sur 100
    return note;


##########################################################
###                                                    ###
###             Verification des moyennes              ###
###                                                    ###
##########################################################
from misc import GetBlocsMaquette, GetUEsMaquette;
from maquette import Swap;
def CheckMoyennes(data_pv, parcours, semestre, etu_id, etu_nom):
    # Obtentien des blocs et verification que la liste est complete
    blocs_maquette = GetBlocsMaquette(semestre, parcours)
    blocs_pv       = sorted([x for x in data_pv.keys() if (x.startswith('LK') or x.startswith('1SL') or not x in UEs) and not x in ['total', '999999']])
    blocs_maquette = [x for x in blocs_maquette if not x in [x for x in UEs if x.startswith('LK')] or x in blocs_pv]

    # Comparaison de la maquette et du pv au niveau des blocs
    logger.debug('  > Comparaison de la maquette et du pv au niveau des blocs')
    logger.debug('     * blocs maq=' + str(blocs_maquette))
    logger.debug('     * blocs pv =' + str(blocs_pv))
    if (len(blocs_pv)!=2 and blocs_pv!=['1SLPY001']) and data_pv['total']['note']!='NCAE':
       logger.warning("Problemes de bloc manquant dans le PV de " + etu_nom + " (" + etu_id + "). Blocs detectes : " + ", ".join(blocs_maquette)  );

    # Ajout des blocs manquants
    to_del = [];
    for missing_bloc in [x for x in blocs_maquette if not x in blocs_pv]:
        logger.warning("  > Adding block " + missing_bloc  + " dans le PV de " + etu_nom + " (" + etu_id + ")")
        data_pv[missing_bloc] =  {'tag': Maquette[missing_bloc]['nom'], 'bareme': '100', 'validation': 'AJ', 'note': '???', 'annee_val': None, 'UE': None};
        blocs_pv.append(missing_bloc);


    # Ajout des UE manquantes
    missings = [  [x for x in z if not x in list(data_pv.keys()) ] for z in GetUEsMaquette(blocs_maquette) ];
    missings = [x for x in missings if len(x)==min([len(y) for y in missings]) ][0];
    for missing_ue in missings:
        logger.warning("  > Ajout de l'UE manquante " + missing_ue + " dans le PV de " + etu_nom + " (" + etu_id + ")");

        # UE remplacée par une autre
        grossac = [x for x in data_pv.keys() if x in Swap.keys() and missing_ue in Swap[x]];
        if len(grossac)==1:
            logger.warning("    -> UE remplacée par " + grossac[0])
            data_pv[missing_ue] = data_pv[grossac[0]].copy()
            data_pv[grossac[0]]['SX'] = True
            to_del.append(missing_ue)

        else: data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': 'AJ', 'note': '???', 'annee_val': None, 'UE': None};

    # Verification des moyennes (blocs)
    moyenne_tot  = 0.; coeff_tot    = 0.;
    logger.debug('  > Vérification des moyennes des blocs')
    for bloc in blocs_pv:
        moyenne_bloc = 0.; coeff_bloc = 0.; compensated = False;

        ## Calcul de la moyenne du bloc
        bloc_ues = [x for x in Maquette[bloc]['UE'] if set(x).issubset(set(data_pv.keys())) ][0];
        logger.debug('     * bloc ' + str(bloc) + " : " + str(bloc_ues))

        for ue in bloc_ues:
            if data_pv[ue]['note'] in ['U VAC', 'DIS', 'ENCO', 'VAC']: continue;
            if not parcours in ['DM', 'SPRINT', 'CMI'] or (not 'SX' in UEs[ue].keys()):
                if data_pv[ue]['note'] != '???' and not 'SX' in data_pv[ue].keys():
                    moyenne_bloc += float(data_pv[ue]['note'])*UEs[ue]['ects'];
                    moyenne_tot  += float(data_pv[ue]['note'])*UEs[ue]['ects'];
                coeff_tot  += UEs[ue]['ects'];
                coeff_bloc += UEs[ue]['ects'];
                if data_pv[ue]['note'] == '???' or float(data_pv[ue]['note']) < 50: compensated = True;
        try:    moyenne_bloc = round(moyenne_bloc/coeff_bloc,3);
        except: moyenne_bloc = 0.
        logger.debug('       -> moyenne bloc  calculée = ' + str(moyenne_bloc) + ' : ' + str(compensated))
        data_pv[bloc]['compensation']=compensated;

        ## Output and save if necessary
        if data_pv[bloc]['note']=='???' and data_pv['total']['note']!='NCAE':
            logger.warning("Problemes de moyenne de blocs dans le PV de "  + etu_nom + " (" + etu_id + "):");
            logger.warning('  > Bloc ' + bloc + ' : moyenne calculee = ' + str(moyenne_bloc));
            data_pv[bloc]['note']=moyenne_bloc;

        ## Verification de la moyenne du bloc
        threshold = 0.002 if not '1SLPY001' in data_pv.keys() else 0.1
        if data_pv['total']['note']!='NCAE' and abs(moyenne_bloc-float(data_pv[bloc]['note']))>threshold:
            logger.error("Problemes de moyenne de blocs dans le PV de "  + etu_nom + " (" + etu_id + "):");
            logger.error("  *** Moyenne calculee " + bloc + " : " + str(moyenne_bloc));
            logger.error("  *** Moyenne Apogee   " + bloc + " : " + str(data_pv[bloc]['note']));

        ## Verification du résultat du bloc
        CheckValidation(bloc, data_pv[bloc], str(etu_id), etu_nom, nobloc=False, parcours=parcours, compensation=compensated)

    # Verification du nombre de credits
    creds = sum([UEs[x]['ects'] for x in data_pv.keys() if x in UEs.keys() and not x.startswith('LK') and (not parcours in ['DM', 'SPRINT', 'CMI'] or not 'SX' in UEs[x].keys()) and not 'SX' in data_pv[x].keys()]);

    if creds!=30 and data_pv['total']['note']!='NCAE':
        logger.warning("Problemes de nombre total d'ECTS dans le PV de " + etu_nom + " (" + etu_id + "): " + str(creds) + " ECTS");
    if data_pv['total']['note']=='NCAE':
        ncae_creds = sum([UEs[x]['ects'] for x in data_pv.keys() if x in UEs.keys() and not x.startswith('LK') and (not parcours in ['DM', 'SPRINT', 'CMI'] or not 'SX' in UEs[x].keys()) and isinstance(data_pv[x]['note'],float)]);
        if ncae_creds==30: logger.error("L'étudiant " +  etu_nom + " (" + etu_id + ") a un contrat complet (NCAE incorrect)");

    ## Calcul de la moyenne du semestre
    try:    moyenne_tot  = round(moyenne_tot/(5.*coeff_tot),3);
    except: moyenne_tot = -1;
    if data_pv['total']['note'] in ['NCAE', 'ENCO']: return;
    if data_pv['total']['note'] in [-1]:
        logger.warning("Problemes de moyenne totale non calculee dans le PV de " + etu_nom + " (" + etu_id + ")");
        logger.warning("  > Moyenne calculee = " + str(moyenne_tot));
        data_pv['total']['note'] = moyenne_tot;
    if abs(moyenne_tot-float(data_pv['total']['note'])) > 0.001:
        logger.error("Problemes de moyenne totale dans le PV de "  + etu_nom + " (" + etu_id + "):");
        logger.error("  *** Moyenne calculee : " + str(moyenne_tot));
        logger.error("  *** Moyenne Apogee   : " + str(data_pv['total']['note']));

    # output
    for ue in to_del: del data_pv[ue]
    return


##########################################################
###                                                    ###
###             Verification blocs disc.               ###
###                                                    ###
##########################################################
from maquette import BlocsDisc;
def CalculBlocsDisc(pv_etu, semestre):
    # list UEs
    ues = [x for x in pv_etu.keys() if x=='LK5EEJ13' or ('LU' in x and not 'LV' in x and not 'OIP' in x)];
    phys= [x for x in BlocsDisc[semestre]['PY'] if all([y in ues for y in x])][0];
    tag = list(set([x[3:5] for x in [y.replace('SX','').replace('XS','') for y in ues] if x[3:5]!='PY']));
    if len(tag)==0: tag=''; MIN='';
    else: tag = tag[0];
    try:    MIN = [x for x in BlocsDisc[semestre][tag] if all([y in ues for y in x])][0];
    except: MIN = '';

    # calcul de la moyenne
    MAJ1 = [ [float(str(pv_etu[x]['note']).replace('COVID','0')), UEs[x]['ects']] for x in phys if not pv_etu[x]['note'] in ['ENCO', 'DIS'] ];
    MAJ2 = [ [float(str(pv_etu[x]['note']).replace('COVID','0')), UEs[x]['ects']] for x in MIN  if not pv_etu[x]['note'] in ['ENCO', 'DIS'] ];
    logger.debug("  > Bloc Disc Phys = " + str(MAJ1));
    logger.debug("  > Bloc Disc " + tag+ " = " + str(MAJ2));

    return {
     'MAJ1':[sum([x[0]*x[1] for x in MAJ1]), sum([x[1] for x in MAJ1])],
     'MAJ2':[sum([x[0]*x[1] for x in MAJ2]), sum([x[1] for x in MAJ2])]
    };

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

            # patch L1
            if 'LU1' in label or '1SL' in label and not 'UE' in data_UE.keys():
                data_UE['UE'] = label.split('-')[1].strip()
                data_UE['annee_val'] = None

            ## Ici l'element est vide : on l'ignore
            if 'UE' not in data_UE.keys() : continue;

            ## Simplification -> quelques blocs sont ignorés
            if my_label in ['LK5PY092', 'LK3STM01', 'LK3PYDM0', '999999', 'LY3PYJ11', 'LY3PYDM0', 'LK3PYJ04']: continue
            if my_label in ['LK3PYJ05'] and parcours in ['DM']: continue


##             ## Hack double majeure et MAJ/Min math L2
##             if my_label in ['LY4PYMI0', 'LK3PYMI0', 'LK3PYDM0', 'LK4PYDM0', 'LY3PYJ10', 'LY3PYJ11', 'LK3PYJ04', 'LK4PYJ10', 'LK4PYJ20', 'LK6PY090', 'LK3PYDK0']: continue;

##             ## Patch pour le PV des L2
##             if my_label.startswith('LY'):
##                 my_label =data_UE['UE'];
##                 data_UE['UE']  = None;

            ## DEBUG :  on print le nom de l'element et ce qu'il contient
            logger.debug('  > label = ' + my_label + "; UE = " + str(data_UE));

            ## Extraction du PV + some hack to reduce the amount of blocknames
            new_label = my_label
            if my_label in ['LK3PYJ06']: new_label = 'LK3PYJ05';
            elif my_label.startswith('LY') and  data_UE['UE']!=None: new_label = data_UE['UE'];
##             if my_label == 'LY5PY090': new_label = data_UE['UE'];
##             elif my_label == 'LY5PY092': new_label = data_UE['UE'] + '_GS';
##             else: new_label = my_label;
##             if my_label == 'LK3PYJ01': new_label = 'LK3PYJ00';
##             if my_label == 'LK4PYJ01': new_label = 'LK4PYJ00';
##             if my_label == 'LK5PYJ01' and parcours!='SPRINT': new_label = 'LK5PYJ00';
##             if my_label == 'LK5PYJ01' and parcours=='SPRINT': new_label = 'LK5PYJ03';
##             if my_label == 'LK6PYJ20' and parcours=='DK': new_label = 'LK6PYDK0';
##             if my_label == 'LK4PYJ22': new_label = 'LK4PYJ21';
##             if my_label == 'LK3STM00': new_label = 'LK3STM01';
##             if my_label == 'LK4PYJ23': new_label = 'LK4PYJ21';
##             if my_label == 'LK5PY092' and parcours=='CMI': new_label = 'LK5PYMI0';
##             if my_label in ['LY5PY090', 'LY5PY092']: data_UE['UE']=None;
##             if my_label == 'LK3PYC00' and parcours=='PADMONO': new_label='LK3PYC02';
            mynote = CheckValidation(new_label, data_UE, str(etudiant), pv[etudiant]['nom'])
            if '1SL' in label: pv_individuel['total'] = {'note':mynote/5., 'annee_val':data_UE['annee_val'], 'validation':data_UE['validation']}
            pv_individuel[new_label] = {'note':mynote, 'annee_val':data_UE['annee_val'], 'validation':data_UE['validation']};

        # patch philo
##         if 'LU2SXPH2' in pv_individuel.keys(): pv_individuel['LK4PHD00'] = pv_individuel['LU2SXPH2'];
##         elif 'LU2SXHI2' in pv_individuel.keys(): pv_individuel['LK4HID00'] = pv_individuel['LU2SXHI2'];
##         elif 'LU2EE201' in pv_individuel.keys() and 'LU2PY123' in pv_individuel.keys() and \
##             'LU2EE203' in pv_individuel.keys() and 'LU2EE204' in pv_individuel.keys():
##             pv_individuel['LK4EED00'] = {'tag': 'Bloc DM EEA S4', 'bareme': '100', 'validation': 'ADM', 'note': '-1', 'annee_val': None, 'UE': None}
##         elif 'LU2ST045' in pv_individuel.keys() and 'LU2ST402' in pv_individuel.keys() and \
##             'LU2ST403' in pv_individuel.keys() and 'LU2PY123' in pv_individuel.keys():
##             pv_individuel['LK4STD00'] = {'tag': 'Bloc DM ST S4', 'bareme': '100', 'validation': 'ADM', 'note': '-1', 'annee_val': None, 'UE': None}

        # Verification des moyennes (blocs et semestre)
        CheckMoyennes(pv_individuel, parcours, semestre.split('_')[0], str(etudiant), pv[etudiant]['nom']);

        # Verification des blocs disciplinaires
        if parcours in ['DM']: pv_individuel[semestre] = CalculBlocsDisc(pv_individuel, semestre.split('_')[0]);

        # Saving
        new_pv[etudiant] = { 'nom': pv[etudiant]['nom'], 'results':pv_individuel};
        logger.debug('  > saved_pv = ' + str(new_pv[etudiant]));

    # exit
    return new_pv;

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
def CheckValidation(nom_UE, data_UE, etu_id, etu_nom):
    # safetfy check
    if data_UE['validation'] in ['ENCO', 'DIS', 'U VAC']: return data_UE['validation'];
    if data_UE['validation']=='ABJ': data_UE['note']=0;
    if data_UE['note']==None: return -1;

    # Calcul de la note
    note = float(data_UE['note'])/float(data_UE['bareme'])*100. if nom_UE!='total' else float(data_UE['note']);

    # Si on a un bloc, il n'y a rien a faire
    if nom_UE in Maquette.keys() or nom_UE=='total': return round(note,3);

    # Verification du statut de validation
    if not nom_UE in IsModule  and note<50. and not data_UE['validation'] in ['AJ', 'ABJ']:
        logger.warning('Probleme avec le PV de ' + str(etu_id) + ' (' + etu_nom +') : ' + nom_UE.replace('_GS','') + ' devrait etre AJ');
    elif not nom_UE in IsModule  and note>=50. and not data_UE['validation'] in ['VAC', 'ADM', 'U ADM']:
        logger.warning('Probleme avec le PV de ' + str(etu_id) + ' (' + etu_nom +') : ' + nom_UE.replace('_GS','') + ' devrait etre ADM');

    # On a un UE; retour de la note sur 100
    return note;


##########################################################
###                                                    ###
###             Verification des moyennes              ###
###                                                    ###
##########################################################
from misc import GetBlocsMaquette, GetUEsMaquette;
from maquette import GrosSac, GrosSacP2, GrosSac2, GrosSac3;
def CheckMoyennes(data_pv, parcours, semestre, etu_id, etu_nom):

    # patch SX bizarre
    no123=False;
    if 'LU2SXPH2' in data_pv.keys():no123=True;
    if 'LU2SXHI2' in data_pv.keys():no123=True;

    # Obtentien des blocs et verification que la liste est complete
    blocs_maquette = GetBlocsMaquette(semestre, parcours);
    blocs_pv = sorted([x for x in data_pv.keys() if (x.startswith('LK') or not x in UEs) and not x in ['total', '999999'] and not x in GrosSac.keys() and not x in GrosSacP2.keys()]);
    blocs_maquette = [x for x in blocs_maquette if not x in [x for x in UEs if x.startswith('LK')] or x in blocs_pv];
    if len(blocs_maquette)!=2:
       logger.warning("Problemes de bloc manquant dans le PV de " + etu_nom + " (" + etu_id + "). Blocs detectes : " + ", ".join(blocs_maquette)  );

    # Verification qu'en cas d'UE dans le gros sac, les UE correspondent ne sont pas dans le PV
    for to_del in [x for x in data_pv.keys() if x+'_GS' in data_pv.keys()]:
       logger.warning("Problemes d'UE a supprimer dans le PV de " + etu_nom + " (" + etu_id + "): " + to_del);
       del data_pv[to_del];

    # UE checking
    printed = False;
    if blocs_maquette != blocs_pv:
         from misc     import Bye;
         if not(parcours=='MONO' and semestre in ['S5', 'S6']):
             printed = True
             logger.warning("Problemes de blocs sans notes dans le PV de " + etu_nom + " (" + etu_id + ")");
         for missing_bloc in [x for x in blocs_maquette if not x in blocs_pv]:
             if not(parcours=='MONO' and semestre in ['S5', 'S6']): logger.debug("  > Adding block " + missing_bloc);
             data_pv[missing_bloc] =  {'tag': Maquette[missing_bloc]['nom'], 'bareme': '100', 'validation': 'AJ', 'note': '-1', 'annee_val': None, 'UE': None};
             blocs_pv.append(missing_bloc);
         used_ues = [];
         missings = [  [x for x in z if not x in list(data_pv.keys()) ] for z in GetUEsMaquette(blocs_maquette) ];
         missings = [x for x in missings if len(x)==min([len(y) for y in missings]) ][0];
         for missing_ue in missings:
             logger.debug("  > Ajout de l'UE manquante " + missing_ue);

             # est-ce que l'UE est dans le premier gros sac ?
             grossac = [x for x in data_pv.keys() if x in GrosSac.keys() and missing_ue in GrosSac[x] and not x in used_ues] + \
                 [x for x in data_pv.keys() if x in GrosSacP2.keys() and missing_ue in GrosSacP2[x] and not x in used_ues];
             if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac2.keys() and missing_ue in GrosSac2[x] ];
             if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac3.keys() and missing_ue in GrosSac3[x] ];
             if missing_ue=='LU3PY122' and not any([ (x in data_pv.keys()) for x in ['LU3PY231', 'LU3PY232', 'LU3PY233', 'LU3PY234', 'LU3PY235']]) and 'LU3PY033' in data_pv.keys(): grossac=['LU3PY033']

             # test si l'UE fait partie du 1er gros sac
             if len(grossac)>0:
                 annee = data_pv[grossac[0]]['note'];
                 coeff = sum([UEs[ue]['ects'] for ue in grossac if not parcours in ['DM', 'SPRINT'] or not 'SX' in UEs[ue].keys()]);
                 list_note = [ ue for ue in grossac if data_pv[ue]['note']!='ENCO'];
                 if   [ data_pv[ue]['note'] for ue in list_note ] in ['DIS']: note = 'DIS';
                 elif [ data_pv[ue]['note'] for ue in list_note ] in ['U VAC']: note = 'U VAC';
                 else: note = sum( [ data_pv[ue]['note']*UEs[ue]['ects']/coeff for ue in list_note] );
                 data_pv[missing_ue] = {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': None, 'note': note, 'annee_val': None, 'UE': 'GrosSac'};
                 if parcours in ['MAJ']:
                     if grossac[0] in GrosSac.keys() and missing_ue == GrosSac[grossac[0]][-1]: used_ues += grossac;
                     elif grossac[0] in GrosSacP2.keys() and missing_ue == GrosSacP2[grossac[0]][-1]: used_ues += grossac;
                     elif grossac[0] in GrosSac2.keys() and missing_ue == GrosSac2[grossac[0]][-1]: used_ues += grossac;
                     elif grossac[0] in GrosSac3.keys() and missing_ue == GrosSac3[grossac[0]][-1]: used_ues += grossac;

             # On a vraiment une UE manquante -> COVID
             elif not missing_ue+'_GS' in data_pv.keys():
                 logger.debug("  > Ajout de l'UE "+ missing_ue);
                 data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': 'AJ', 'note': 'COVID', 'annee_val': None, 'UE': None};
             else:
                 logger.debug("  > Ajout de l'UE "+ missing_ue);
                 data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': 'GS', 'note':'DIS', 'annee_val': None, 'UE': None};


    # Verification des moyennes (blocs)
    moyenne_tot  = 0.; coeff_tot    = 0.;
    no120 = False
    for bloc in blocs_pv:
        ## Checking whether all UEs are present
        missings = [  [x for x in z if not x in list(data_pv.keys()) ] for z in GetUEsMaquette(blocs_pv) ];
        missings = [x for x in missings if len(x)==min([len(y) for y in missings]) ][0];
        used_ues = [];
        for missing_ue in missings:
            logger.debug("  > Ajout de l'UE manquante "+ missing_ue);

            # est-ce que l'UE est dans le premier gros sac ?
            grossac = [x for x in data_pv.keys() if x in GrosSac.keys() and missing_ue in GrosSac[x] and not x in used_ues] + \
                [x for x in data_pv.keys() if x in GrosSacP2.keys() and missing_ue in GrosSacP2[x] and not x in used_ues];
            if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac2.keys() and missing_ue in GrosSac2[x] ];
            if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac3.keys() and missing_ue in GrosSac3[x] ];

            # test si l'UE fait partie du 1er gros sac
            if len(grossac)>0:
                annee = data_pv[grossac[0]]['note'];
                coeff = sum([UEs[ue]['ects'] for ue in grossac if not parcours in ['DM', 'SPRINT'] or not 'SX' in UEs[ue].keys()]);
                list_note = [ ue for ue in grossac if not data_pv[ue]['note'] in ['U VAC', 'DIS', 'ENCO'] ];
                if [data_pv[ue]['note'] for ue in grossac] == ['DIS']: note = 'DIS';
                else: note = sum( [ data_pv[ue]['note']*UEs[ue]['ects']/coeff for ue in list_note] );
                data_pv[missing_ue] = {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': None, 'note': note, 'annee_val': None, 'UE': 'GrosSac'};
                if parcours in ['MAJ']:
                     if grossac[0] in GrosSac.keys() and missing_ue == GrosSac[grossac[0]][-1]: used_ues += grossac;
                     elif grossac[0] in GrosSacP2.keys() and missing_ue == GrosSacP2[grossac[0]][-1]: used_ues += grossac;
                     elif grossac[0] in GrosSac2.keys() and missing_ue == GrosSac2[grossac[0]][-1]: used_ues += grossac;
                     elif grossac[0] in GrosSac3.keys() and missing_ue == GrosSac3[grossac[0]][-1]: used_ues += grossac;
            else:
                val = 'ADM' if float(data_pv[bloc]['note'])>=50. else 'AJ';
                data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': val, 'note':data_pv[bloc]['note'],\
                   'annee_val': None, 'UE': None};

        ## Calcul de la moyenne du bloc
        bloc_ues = [x for x in Maquette[bloc]['UE'] if set(x).issubset(set(data_pv.keys())) ][0];
        moyenne_bloc = 0.; coeff_bloc   = 0.;
        for ue in bloc_ues:
            if data_pv[ue]['note'] in ['U VAC', 'DIS', 'ENCO']: continue;
            if ('LK6EED00' in list(data_pv.keys()) or 'LK6STD00' in list(data_pv.keys())) and ue in ['LU3PY105', 'LU3PY122', 'LU3PY124', 'LU3PY125']:
                no120=True;
                continue
            if not parcours in ['DM', 'SPRINT'] or (not 'SX' in UEs[ue].keys() and not (ue=='LU2PY123' and no123)):
                if data_pv[ue]['note'] != 'COVID':
                    moyenne_bloc += float(data_pv[ue]['note'])*UEs[ue]['ects'];
                    moyenne_tot  += float(data_pv[ue]['note'])*UEs[ue]['ects'];
                coeff_tot  += UEs[ue]['ects'];
                coeff_bloc += UEs[ue]['ects'];
        try:    moyenne_bloc = round(moyenne_bloc/coeff_bloc,3);
        except: moyenne_bloc = 0.

        ## Output and save if necessary
        if data_pv[bloc]['note']=='-1':
            if not(parcours=='MONO' and semestre in ['S5', 'S6']):
                if not printed: logger.warning("Problemes de moyenne de blocs dans le PV de "  + etu_nom + " (" + etu_id + "):");
                logger.warning('  > Bloc ' + bloc + ' : moyenne calculee = ' + str(moyenne_bloc));
            data_pv[bloc]['note']=moyenne_bloc;

        ## Verification de la moyenne du bloc
        if abs(moyenne_bloc-float(data_pv[bloc]['note']))>0.002:
            logger.error("Problemes de moyenne de blocs dans le PV de "  + etu_nom + " (" + etu_id + "):");
            logger.error("  *** Moyenne calculee " + bloc + " : " + str(moyenne_bloc));
            logger.error("  *** Moyenne Apogee   " + bloc + " : " + str(data_pv[bloc]['note']));

    # Verification du nombre de credits
    credits = sum([UEs[x]['ects'] for x in data_pv.keys() if x in UEs.keys() and not '_GS' in x and not x.startswith('LK') and not ('UE' in data_pv[x].keys() and data_pv[x]['UE']=='GrosSac') and (not parcours in ['DM', 'SPRINT'] or not 'SX' in UEs[x].keys()) and not (x=='LU2PY123' and no123) ]);
    if no120: credits = credits-6;
    if credits!=30: logger.warning("Problemes de nombre total d'ECTS dans le PV de " + etu_nom + " (" + etu_id + "): " + str(credits) + " ECTS");

    ## Calcul de la moyenne du semestre
    try:    moyenne_tot  = round(moyenne_tot/(5.*coeff_tot),3);
    except: moyenne_tot = -1;
    if data_pv['total']['note'] == 'ENCO': return;
    if data_pv['total']['note'] in [-1]:
        logger.warning("Problemes de moyenne totale non calculee dans le PV de " + etu_nom + " (" + etu_id + ")");
        logger.warning("  > Moyenne calculee = " + str(moyenne_tot));
        data_pv['total']['note'] = moyenne_tot;
    if (moyenne_tot-float(data_pv['total']['note'])) > 0.001:
        logger.error("Problemes de moyenne totale dans le PV de "  + etu_nom + " (" + etu_id + "):");
        logger.error("  *** Moyenne calculee : " + str(moyenne_tot));
        logger.error("  *** Moyenne Apogee   : " + str(data_pv['total']['note']));


    # output
    return;


##########################################################
###                                                    ###
###             Verification blocs disc.               ###
###                                                    ###
##########################################################
from maquette import BlocsDisc;
def CalculBlocsDisc(pv_etu, semestre):
    # list UEs
    ues = [x for x in pv_etu.keys() if 'LU' in x and not 'LV' in x and not 'OIP' in x];
    phys= [x for x in BlocsDisc[semestre]['PY'] if all([y in ues for y in x])][0];
    tag = list(set([x[3:5] for x in [y.replace('SX','') for y in ues] if x[3:5]!='PY']))[0];
    MIN = [x for x in BlocsDisc[semestre][tag] if all([y in ues for y in x])][0];

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

            ## Ici l'element est vide : on l'ignore
            if 'UE' not in data_UE.keys(): continue;

            ## Hack double majeure et MAJ/Min math L2
            if my_label in ['LK3PYDM0', 'LK4PYDM0', 'LY3PYJ10', 'LK4PYJ10', 'LK4PYJ20', 'LK6PY090']: continue;

            ## Patch pour le PV des L2
            if my_label.startswith('LY'):
                my_label =data_UE['UE'];
                data_UE['UE']  = None;

            ## DEBUG :  on print le nom de l'element et ce qu'il contient
            logger.debug('  > label = ' + my_label + "; UE = " + str(data_UE));

            ## Extraction du PV
            if   my_label == 'LY5PY090': new_label = data_UE['UE'];
            elif my_label == 'LY5PY092': new_label = data_UE['UE'] + '_GS';
            else: new_label = my_label;
            if my_label == 'LK3PYJ01': new_label = 'LK3PYJ00';
            if my_label == 'LK4PYJ01': new_label = 'LK4PYJ00';
            if my_label == 'LK5PYJ01' and parcours!='SPRINT': new_label = 'LK5PYJ00';
            if my_label == 'LK5PYJ01' and parcours=='SPRINT': new_label = 'LK5PYJ03';
            if my_label == 'LK4PYJ22': new_label = 'LK4PYJ21';
            if my_label == 'LK4PYJ23': new_label = 'LK4PYJ21';
            if my_label in ['LY5PY090', 'LY5PY092']: data_UE['UE']=None;
            pv_individuel[new_label] = {'note':CheckValidation(new_label, data_UE, str(etudiant), pv[etudiant]['nom']), 'annee_val':data_UE['annee_val']};

        # patch philo
        if 'LU2SXPH2' in pv_individuel.keys(): pv_individuel['LK4PHD00'] = pv_individuel['LU2SXPH2'];
        elif 'LU2SXHI2' in pv_individuel.keys(): pv_individuel['LK4HID00'] = pv_individuel['LU2SXHI2'];
        elif 'LU2EE201' in pv_individuel.keys() and 'LU2PY123' in pv_individuel.keys() and \
            'LU2EE203' in pv_individuel.keys() and 'LU2EE204' in pv_individuel.keys():
            pv_individuel['LK4EED00'] = {'tag': 'Bloc DM EEA S4', 'bareme': '100', 'validation': 'ADM', 'note': '-1', 'annee_val': None, 'UE': None}
        elif 'LU2ST045' in pv_individuel.keys() and 'LU2ST402' in pv_individuel.keys() and \
            'LU2ST403' in pv_individuel.keys() and 'LU2PY123' in pv_individuel.keys():
            pv_individuel['LK4STD00'] = {'tag': 'Bloc DM ST S4', 'bareme': '100', 'validation': 'ADM', 'note': '-1', 'annee_val': None, 'UE': None}


        # Verification des moyennes (blocs et semestre)
        CheckMoyennes(pv_individuel, parcours, semestre.split('_')[0], str(etudiant), pv[etudiant]['nom']);

        # Verification des blocs disciplinaires
        if parcours=='DM': pv_individuel[semestre] = CalculBlocsDisc(pv_individuel, semestre.split('_')[0]);

        # Saving
        new_pv[etudiant] = { 'nom': pv[etudiant]['nom'], 'results':pv_individuel};
        logger.debug('  > saved_pv = ' + str(new_pv[etudiant]));

    # exit
    return new_pv;

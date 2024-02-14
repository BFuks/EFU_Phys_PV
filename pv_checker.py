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
from maquette import GrosSac, GrosSacP2, GrosSac2, GrosSac3, GrosSac3P2;
def CheckMoyennes(data_pv, parcours, semestre, etu_id, etu_nom):

##    # patch SX bizarre
##    no123 = any(key in data_pv.keys() for key in ['LU2SXAL2', 'LU2SXPH2', 'LU2SXHI2', 'LK4EWK00', 'LK4SSK00', 'LK4MED00'])

    # Obtentien des blocs et verification que la liste est complete
    blocs_maquette = GetBlocsMaquette(semestre, parcours)
    blocs_pv       = sorted([x for x in data_pv.keys() if (x.startswith('LK') or not x in UEs) and not x in ['total', '999999']]) # and not x in GrosSac.keys() and not x in GrosSacP2.keys()]);
    blocs_maquette = [x for x in blocs_maquette if not x in [x for x in UEs if x.startswith('LK')] or x in blocs_pv]


##     if 'LK3PYJ10' in data_pv.keys() and 'LK3PYJ10' in blocs_maquette and 'LK3PYJ11' in blocs_maquette: blocs_maquette.remove('LK3PYJ11')
##     if (etu_id=='21104860' or 'LU2PY125' in data_pv.keys()) and ('LK3PYJ05' in blocs_maquette or 'LK3PYJ06' in blocs_maquette) and 'LK3PYJ00' in blocs_maquette:
##         blocs_maquette.remove('LK3PYJ00');
##     elif not 'LU2PY125' in data_pv.keys() and 'LK3PYJ05' in blocs_maquette and 'LK3PYJ00' in blocs_maquette:
##         blocs_maquette.remove('LK3PYJ05');
##         if 'LK3PYJ06' in blocs_maquette: blocs_maquette.remove('LK3PYJ06')
##     elif not 'LU2PY125' in data_pv.keys() and 'LK3PYJ06' in blocs_maquette and 'LK3PYJ00' in blocs_maquette:
##         blocs_maquette.remove('LK3PYJ06');

##     if   'LK3PYJ05' in blocs_maquette and 'LK3PYJ06' in blocs_maquette and 'LK3MAM00' in blocs_pv: blocs_maquette.remove('LK3PYJ05');
##     elif 'LK3PYJ05' in blocs_maquette and 'LK3PYJ06' in blocs_maquette and not 'LK3MAM00' in blocs_pv: blocs_maquette.remove('LK3PYJ06')
##     elif 'LK3PYJ10' in blocs_maquette and 'LK3PYJ11' in blocs_maquette: blocs_maquette.remove('LK3PYJ10')
##     if   'LK3PYJ05' in blocs_pv and 'LK3PYJ11' in blocs_pv: blocs_pv.remove('LK3PYJ05');
##     if 'LK3SSK00' in blocs_pv and not 'LK3SSK00' in blocs_maquette: blocs_maquette.append('LK3SSK00');
##     if 'LK5PHM99' in blocs_pv: blocs_pv.remove('LK5PHM99');
##     if 'LK6ST113' in blocs_pv: blocs_pv.remove('LK6ST113');
##     if 'LK6ST116' in blocs_pv: blocs_pv.remove('LK6ST116');
##     if 'LK6HSM01' in blocs_pv: blocs_pv.remove('LK6HSM01');
##     if '6ZVPYME1' in blocs_pv: blocs_pv.remove('6ZVPYME1');
##    if len(blocs_maquette)==3 and 'LK5HIM00' in blocs_maquette: blocs_maquette.remove('LK5HIM00');

    # Comparaison de la maquette et du pv au niveau des blocs
    logger.debug('  > Comparaison de la maquette et du pv au niveau des blocs')
    logger.debug('     * blocs maq=' + str(blocs_maquette))
    logger.debug('     * blocs pv =' + str(blocs_pv))
    if len(blocs_pv)!=2 and data_pv['total']['note']!='NCAE':
       logger.warning("Problemes de bloc manquant dans le PV de " + etu_nom + " (" + etu_id + "). Blocs detectes : " + ", ".join(blocs_maquette)  );


##     if parcours=='PADMAJ' and len(blocs_maquette)==1 and semestre=='S3': blocs_maquette.append('LK3MEM02');
##     if parcours=='PADMAJ' and len(blocs_maquette)==1 and semestre=='S4': blocs_maquette.append('LK4MEM04');

    # Check all blocs are there

    # Verification qu'en cas d'UE dans le gros sac, les UE correspondent ne sont pas dans le PV
##     for to_del in [x for x in data_pv.keys() if x+'_GS' in data_pv.keys()]:
##        logger.warning("Problemes d'UE a supprimer dans le PV de " + etu_nom + " (" + etu_id + "): " + to_del);
##        del data_pv[to_del];

    # Ajout des blocs manquants
##     if data_pv['total']['note']!='NCAE': logger.warning("Moyenne totale non calculée dans le PV de " + str(etu_nom) + " (" + etu_id + ")")
    for missing_bloc in [x for x in blocs_maquette if not x in blocs_pv]:
        logger.warning("  > Adding block " + missing_bloc  + " dans le PV de " + etu_nom + " (" + etu_id + ")")
        data_pv[missing_bloc] =  {'tag': Maquette[missing_bloc]['nom'], 'bareme': '100', 'validation': 'AJ', 'note': '???', 'annee_val': None, 'UE': None};
        blocs_pv.append(missing_bloc);


    # Ajout des UE manquantes
    missings = [  [x for x in z if not x in list(data_pv.keys()) ] for z in GetUEsMaquette(blocs_maquette) ];
    missings = [x for x in missings if len(x)==min([len(y) for y in missings]) ][0];
    for missing_ue in missings:
        logger.warning("  > Ajout de l'UE manquante " + missing_ue + " dans le PV de " + etu_nom + " (" + etu_id + ")");

##              # est-ce que l'UE est dans le premier gros sac ?
##              grossac = [x for x in data_pv.keys() if x in GrosSac.keys() and missing_ue in GrosSac[x] and not x in used_ues] + \
##                  [x for x in data_pv.keys() if x in GrosSacP2.keys() and missing_ue in GrosSacP2[x] and not x in used_ues];
##              if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac2.keys() and missing_ue in GrosSac2[x] ];
##              if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac3.keys() and missing_ue in GrosSac3[x] ];
##              if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac3P2.keys() and missing_ue in GrosSac3P2[x] ];
##              if missing_ue=='LU3PY122' and not any([ (x in data_pv.keys()) for x in ['LU3PY231', 'LU3PY232', 'LU3PY233', 'LU3PY234', 'LU3PY235']]) and 'LU3PY033' in data_pv.keys(): grossac=['LU3PY033']
## 
##              # specific patch
##              logger.warning("  > grossac = "+ str(grossac));
## 
##              # test si l'UE fait partie du 1er gros sac
##              if len(grossac)>0:
##                  annee = data_pv[grossac[0]]['note'];
##                  coeff = sum([UEs[ue]['ects'] for ue in grossac if not parcours in ['DK', 'DM', 'SPRINT'] or not 'SX' in UEs[ue].keys()]);
##                  list_note = [ ue for ue in grossac if not data_pv[ue]['note'] in ['DIS', 'ENCO', 'COVID'] ];
##                  if   [ data_pv[ue]['note'] for ue in list_note ] in ['DIS']: note = 'DIS';
##                  elif [ data_pv[ue]['note'] for ue in list_note ] in ['U VAC']: note = 'U VAC';
##                  else: note = sum( [ data_pv[ue]['note']*UEs[ue]['ects']/coeff for ue in list_note] );
##                  data_pv[missing_ue] = {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': None, 'note': note, 'annee_val': None, 'UE': 'GrosSac'};
##                  logger.debug('  > Ajout du grossac : ' + missing_ue + " : "  + str(data_pv[missing_ue]) + '(#0)');
##                  if parcours in ['MAJ']:
##                      if grossac[0] in GrosSac.keys() and missing_ue == GrosSac[grossac[0]][-1]: used_ues += grossac;
##                      elif grossac[0] in GrosSacP2.keys() and missing_ue == GrosSacP2[grossac[0]][-1]: used_ues += grossac;
##                      elif grossac[0] in GrosSac2.keys() and missing_ue == GrosSac2[grossac[0]][-1]: used_ues += grossac;
##                      elif grossac[0] in GrosSac3.keys() and missing_ue == GrosSac3[grossac[0]][-1]: used_ues += grossac;
##                      elif grossac[0] in GrosSac3P2.keys() and missing_ue == GrosSac3P2[grossac[0]][-1]: used_ues += grossac;


             # On a vraiment une UE manquante -> COVID
##              elif not missing_ue+'_GS' in data_pv.keys():

        data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': 'AJ', 'note': '???', 'annee_val': None, 'UE': None};
##                  if parcours == 'PADMONO': data_pv[missing_ue]['ancienneUE']=True;
##                  logger.debug("  > Ajout de l'UE "+ missing_ue + " : " + str(data_pv[missing_ue]) + '(#1)');
##               else:
##                  logger.debug("  > Ajout de l'UE "+ missing_ue + '(#2)');
##                  data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': 'GS', 'note':'DIS', 'annee_val': None, 'UE': None};


    # Verification des moyennes (blocs)
    moyenne_tot  = 0.; coeff_tot    = 0.;
    logger.debug('  > Vérification des moyennes des blocs')
    for bloc in blocs_pv:
        moyenne_bloc = 0.; coeff_bloc = 0.; compensated = False;

##         ## Checking whether all UEs are present
##         missings = [  [x for x in z if not x in list(data_pv.keys()) ] for z in GetUEsMaquette(blocs_pv) ];
##         missings = [x for x in missings if len(x)==min([len(y) for y in missings]) ][0];
##         used_ues = [];
##         for missing_ue in missings:
##             logger.debug("  > Ajout de l'UE manquante "+ missing_ue + ' (#moy - bloc ' + bloc + ')');
## 
##             # est-ce que l'UE est dans le premier gros sac ?
##             grossac = [x for x in data_pv.keys() if x in GrosSac.keys() and missing_ue in GrosSac[x] and not x in used_ues] + \
##                 [x for x in data_pv.keys() if x in GrosSacP2.keys() and missing_ue in GrosSacP2[x] and not x in used_ues];
##             if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac2.keys() and missing_ue in GrosSac2[x] ];
##             if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac3.keys() and missing_ue in GrosSac3[x] ];
##             if grossac  == []: grossac = [x for x in data_pv.keys() if x in GrosSac3P2.keys() and missing_ue in GrosSac3P2[x] ];
## 
##             # test si l'UE fait partie du 1er gros sac
##             logger.debug("  > Gros Sac = " + str(grossac))
##             if len(grossac)>0:
##                 annee = data_pv[grossac[0]]['note'];
##                 coeff = sum([UEs[ue]['ects'] for ue in grossac if not parcours in ['DK', 'DM', 'SPRINT'] or not 'SX' in UEs[ue].keys()]);
##                 list_note = [ ue for ue in grossac if not data_pv[ue]['note'] in ['U VAC', 'DIS', 'ENCO'] ];
##                 if [data_pv[ue]['note'] for ue in grossac] == ['DIS']: note = 'DIS';
##                 else: note = sum( [ data_pv[ue]['note']*UEs[ue]['ects']/coeff for ue in list_note] );
##                 data_pv[missing_ue] = {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': None, 'note': note, 'annee_val': None, 'UE': 'GrosSac'};
##                 if parcours in ['MAJ']:
##                      if grossac[0] in GrosSac.keys() and missing_ue == GrosSac[grossac[0]][-1]: used_ues += grossac;
##                      elif grossac[0] in GrosSacP2.keys() and missing_ue == GrosSacP2[grossac[0]][-1]: used_ues += grossac;
##                      elif grossac[0] in GrosSac2.keys() and missing_ue == GrosSac2[grossac[0]][-1]: used_ues += grossac;
##                      elif grossac[0] in GrosSac3.keys() and missing_ue == GrosSac3[grossac[0]][-1]: used_ues += grossac;
##                      elif grossac[0] in GrosSac3P2.keys() and missing_ue == GrosSac3P2[grossac[0]][-1]: used_ues += grossac;
##             elif data_pv['total']['note']=='NCAE':
##                 data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': 'AJ', 'note':-1, 'annee_val': None, 'UE': None};
##             else:
##                 val = 'ADM' if float(data_pv[bloc]['note'])>=50. else 'AJ';
##                 data_pv[missing_ue] =  {'tag': UEs[missing_ue]['nom'], 'bareme': '100', 'validation': val, 'note':data_pv[bloc]['note'],\
##                    'annee_val': None, 'UE': None};

        ## Calcul de la moyenne du bloc
        bloc_ues = [x for x in Maquette[bloc]['UE'] if set(x).issubset(set(data_pv.keys())) ][0];
        logger.debug('     * bloc ' + str(bloc) + " : " + str(bloc_ues))
##         bloc_ues = bloc_ues[1] if sxcmi and bloc=='LK6PYJ00' and len(bloc_ues)>1 else bloc_ues[0];

        for ue in bloc_ues:
            if data_pv[ue]['note'] in ['U VAC', 'DIS', 'ENCO', 'VAC']: continue;
##             if ('LK6EED00' in list(data_pv.keys()) or 'LK6STD00' in list(data_pv.keys())) and ue in ['LU3PY105', 'LU3PY122', 'LU3PY124', 'LU3PY125']:
##                 no120=True;
##                 continue
            if not parcours in ['DM', 'SPRINT', 'CMI'] or (not 'SX' in UEs[ue].keys()):
                if data_pv[ue]['note'] != '???':
                    moyenne_bloc += float(data_pv[ue]['note'])*UEs[ue]['ects'];
                    moyenne_tot  += float(data_pv[ue]['note'])*UEs[ue]['ects'];
                coeff_tot  += UEs[ue]['ects'];
                coeff_bloc += UEs[ue]['ects'];
                if data_pv[ue]['note'] == '???' or float(data_pv[ue]['note']) < 50: compensated = True;
##             if not parcours in ['DK', 'DM', 'SPRINT'] or (not 'SX' in UEs[ue].keys() and not (ue=='LU2PY123' and no123)) or (parcours=='DM' and ue in ['LU2IN003', 'LU2IN009']):
##                 if ue in ['LU2PY102', 'LU2GSG31', 'LU3GSG51', 'LU3PY105', 'LU5SX06E', 'LU3SXCE1'] and sxcmi: continue;
##                 if ue=='LU2PY123' and bloc=='LK4CID00': continue;
##                 if data_pv[ue]['note'] != 'COVID':
##                     moyenne_bloc += float(data_pv[ue]['note'])*UEs[ue]['ects'];
##                     moyenne_tot  += float(data_pv[ue]['note'])*UEs[ue]['ects'];
##                 coeff_tot  += UEs[ue]['ects'];
##                 coeff_bloc += UEs[ue]['ects'];
        try:    moyenne_bloc = round(moyenne_bloc/coeff_bloc,3);
        except: moyenne_bloc = 0.
        logger.debug('       -> moyenne bloc  calculée = ' + str(moyenne_bloc) + ' : ' + str(compensated))
        data_pv[bloc]['compensation']=compensated;

        ## Output and save if necessary
        if data_pv[bloc]['note']=='???' and data_pv['total']['note']!='NCAE':
##             if not(parcours=='MONO' and semestre in ['S5', 'S6']):
            logger.warning("Problemes de moyenne de blocs dans le PV de "  + etu_nom + " (" + etu_id + "):");
            logger.warning('  > Bloc ' + bloc + ' : moyenne calculee = ' + str(moyenne_bloc));
            data_pv[bloc]['note']=moyenne_bloc;

        ## Verification de la moyenne du bloc
        if data_pv['total']['note']!='NCAE' and abs(moyenne_bloc-float(data_pv[bloc]['note']))>0.002:
            logger.error("Problemes de moyenne de blocs dans le PV de "  + etu_nom + " (" + etu_id + "):");
            logger.error("  *** Moyenne calculee " + bloc + " : " + str(moyenne_bloc));
            logger.error("  *** Moyenne Apogee   " + bloc + " : " + str(data_pv[bloc]['note']));

        ## Verification du résultat du bloc
        CheckValidation(bloc, data_pv[bloc], str(etu_id), etu_nom, nobloc=False, parcours=parcours, compensation=compensated)

    # Verification du nombre de credits
    creds = sum([UEs[x]['ects'] for x in data_pv.keys() if x in UEs.keys() and not x.startswith('LK') and (not parcours in ['DM', 'SPRINT', 'CMI'] or not 'SX' in UEs[x].keys())]);
##     if 'LK4IND00' in data_pv.keys(): 
##         creds=sum([UEs[x]['ects'] for x in data_pv.keys() if x in UEs.keys() and not x.startswith('LK') and x != 'LU2IN006'] );
##     if 'LK6IND00' in data_pv.keys(): 
##         creds=sum([UEs[x]['ects'] for x in data_pv.keys() if x in UEs.keys() and not x.startswith('LK') and x != 'LU3IN024'] );

##     if no120: creds = creds-6;
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
##     threshold = 0.1 if 'PAD' in parcours else 0.001;
    if abs(moyenne_tot-float(data_pv['total']['note'])) > 0.001:
        logger.error("Problemes de moyenne totale dans le PV de "  + etu_nom + " (" + etu_id + "):");
        logger.error("  *** Moyenne calculee : " + str(moyenne_tot));
        logger.error("  *** Moyenne Apogee   : " + str(data_pv['total']['note']));

    # output
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

            ## Ici l'element est vide : on l'ignore
            if 'UE' not in data_UE.keys(): continue;

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
            pv_individuel[new_label] = {'note':CheckValidation(new_label, data_UE, str(etudiant), pv[etudiant]['nom']), 'annee_val':data_UE['annee_val'], 'validation':data_UE['validation']};

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

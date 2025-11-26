##########################################################
###                                                    ###
###                New PV Checker                      ###
###                                                    ###
###                Date: 26/11/2025                    ###
###                                                    ###
##########################################################

##########################################################
###                                                    ###
###                       Data                         ###
###                                                    ###
##########################################################
from maquette import Blocs, UEs;


##########################################################
###                                                    ###
###          Vérification des données APOGEE           ###
###                                                    ###
##########################################################
def SanityCheck(pv, logger=None):
    # Boucle sur les étudiants
    for student_id, student_data in pv.items():
        # Init
        pv_data = student_data["pv"]
        tag = f"[{student_data['nom']} ({student_id})]"
        logger.debug(f"PV de {tag[1:-1]}")
        score = 0.0
        maxi  = 0.0
        maj   = 'AJ'
        comp  = False

        # 1) Vérification des blocs et des UEs
        for key in pv_data.keys():
            # Safety : ni un bloc ni une UE
            if key=='Résultat': continue
            # Un bloc : vérification
            elif key in Blocs.keys():
                sc, mx = CheckBlock(key, pv_data, tag, logger=logger)
                score += sc
                maxi  += mx
                if Blocs[key]['nom']=='MAJ': maj = pv_data[key]['resultat']
            # Une UE : vérification
            elif key in UEs.keys():
                CheckUE(key, pv_data[key], tag, logger=logger)
                if pv_data[key].get('note',0)<50: comp = True
            # Problème...
            else: logger.warning(f"{tag} Bloc/UE inconnu dans le PV : {key}")

        # 2) Vérification de la moyenne d'année
        CheckSemestre(score, maxi, maj, comp, pv_data, tag, logger=logger)

        # Exit
        logger.debug("OK")


##########################################################
###                                                    ###
###               Vérification d'un bloc               ###
###                                                    ###
##########################################################
def CheckBlock(bloc, pv, tag, logger=None):
    # Initialisation
    logger.debug(f"  - Bloc {bloc}")

    # 1) Détermination de l’ensemble correct d’UEs pour ce bloc
    #    et si toutes les UE sont là
    possible_sets = Blocs[bloc]["UE"]
    matching_set = None
    for ue_list in possible_sets:
        if all(ue in pv.keys() for ue in ue_list):
            matching_set = ue_list
            break
    if matching_set is None:
        logger.warning(f"{tag} Aucun set d'UE ne correspond au bloc {bloc}")
        return

    # 2) On a un lot d'UEs -> calcul de la moyenne pondérée
    score   = 0.0
    maxi    = 0.0
    moyenne = 0.0
    comp    = False
    for ue in matching_set:
        # Safety: UE manquante
        if ue not in pv.keys():
           logger.warning(f"{tag} UE {ue} manquante dans le PV (attendue pour le bloc {bloc}")
           continue

        # Données de l'UE et check de son encodage dans la maquette
        ue_note = pv[ue]["note"]
        ue_ects = UEs.get(ue, {}).get("ects", None)
        if ue_ects is None:
            logger.error(f"{tag} UE {ue} absente de la maquette)")
            continue

        # SX: on ignore
        if ue in Blocs[bloc].get('SX', []): continue

        # Tout va bien, on calcule la moyenne du bloc
        score += ue_note*ue_ects
        maxi  += ue_ects*pv[ue]['bareme']
        if ue_note<pv[ue]['bareme']/2.:  comp = True
        if maxi==0:
            logger.error(f"{tag} Impossible de calculer la moyenne du bloc {bloc} (ECTS = 0)")
            continue
        moyenne = score/maxi*pv[bloc]['bareme']

    # 3) Comparaison avec la moyenne du PV
    note_pv = pv[bloc].get("note", None)
    if note_pv is None: logger.warning(f"{tag} Note absente dans le PV pour le bloc {bloc}")
    else:
        if abs(moyenne-note_pv)>1e-3:
            logger.error(f"{tag} Différence de moyenne pour le bloc {bloc} : "
               f"calculée={moyenne:.3f}, PV={note_pv}")

    # 4) Test du résultat (validation)
    resultat = "ADM" if note_pv>=50 else "AJ"
    if pv[bloc]["resultat"]!=resultat:
        if resultat=='ADM' and not comp:
          logger.warning(f"{tag} Résultat incorrect pour le bloc {bloc} : "
             f"attendu={resultat}, PV={pv[bloc]['resultat']}")
        elif resultat=='ADM' and comp:
          logger.warning(f"{tag} Refus de compensation pour le bloc {bloc}")

    # Exit (on renvoie le score pour la moyenne semestriel
    logger.debug(f"    > OK")
    return [score, maxi]



##########################################################
###                                                    ###
###         Vérification du résultat d'une UE          ###
###                                                    ###
##########################################################
def CheckUE(ue, data, tag, logger=None):
    # Initialisation
    logger.debug(f"  - UE {ue}")

    # Check
    resultat = "ADM" if data['note']>=50 else "AJ"
    if data["resultat"]!=resultat:
        logger.error(f"{tag} Résultat incorrect pour l'UE {ue} : "
           f"attendu={resultat}, PV={data['resultat']}")
    # Exit
    logger.debug(f"    > OK")


##########################################################
###                                                    ###
###         Vérification du résultat semestriel        ###
###                                                    ###
##########################################################
def CheckSemestre(score, maxi, maj, comp, data, tag, logger=None):
    # Initialisation et safety
    logger.debug(f"  - Vérification de la moyenne semestriel")
    if "Résultat" not in data.keys(): logger.warning(f"{tag} Aucune entrée 'Résultat' dans le PV")
    elif maxi==0: logger.error(f"{tag} Impossible de calculer la moyenne semestrielle (ECTS = 0)")

    # 1) Vérification moyenne
    annee    = score/maxi*data['Résultat']['bareme']
    note_pv  = data["Résultat"]["note"]
    if abs(annee-note_pv)>1e-3:
        logger.error(f"{tag} Différence de moyenne semestrielle : calculée={annee:.3f}, PV={note_pv}")

    # 2) Vérification du résultat semestriel
#    resultat = "ADM" if (note_pv>=10 and maj=='ADM') else "AJ"
    resultat = "ADM" if (note_pv>=10) else "AJ"
    if data["Résultat"]["resultat"]!=resultat:
        if resultat=='ADM' and not comp:
          logger.warning(f"{tag} Résultat incorrect pour l'année : "
             f"attendu={resultat}, PV={data['Résultat']['resultat']}")
        elif resultat=='ADM' and comp:
          logger.warning(f"{tag} Refus de compensation pour le semestre")

    # Exit
    logger.debug(f"    > OK")


### ##########################################################
### ###                                                    ###
### ###             Verification blocs disc.               ###
### ###                                                    ###
### ##########################################################
### from maquette import BlocsDisc;
### def CalculBlocsDisc(pv_etu, semestre):
###     # list UEs
###     ues = [x for x in pv_etu.keys() if x=='LK5EEJ13' or ('LU' in x and not 'LV' in x and not 'OIP' in x)];
###     if ues==['LU3PY403', 'LU3PY411', 'LU3MA120']:
###         ues=['LU3PY403', 'LU3PY411', 'LU3MA120', 'LU3PY124']
###         pv_etu['LU3PY124'] = {'note': '???', 'annee_val': None, 'validation': 'AJ'}
###     phys= [x for x in BlocsDisc[semestre]['PY'] if all([y in ues for y in x])][0];
###     tag = list(set([x[3:5] for x in [y.replace('SX','').replace('XS','') for y in ues] if x[3:5]!='PY']));
###     if len(tag)==0: tag=''; MIN='';
###     else: tag = tag[0];
###     try:    MIN = [x for x in BlocsDisc[semestre][tag] if all([y in ues for y in x])][0];
###     except: MIN = '';
### 
###     # calcul de la moyenne
###     MAJ1 = [ [float(str(pv_etu[x]['note']).replace('???','0')), UEs[x]['ects']] for x in phys if not pv_etu[x]['note'] in ['ENCO', 'DIS'] ];
###     MAJ2 = [ [float(str(pv_etu[x]['note']).replace('???','0')), UEs[x]['ects']] for x in MIN  if not pv_etu[x]['note'] in ['ENCO', 'DIS'] ];
###     logger.debug("  > Bloc Disc Phys = " + str(MAJ1));
###     logger.debug("  > Bloc Disc " + tag+ " = " + str(MAJ2));
### 
###     return {
###      'MAJ1':[sum([x[0]*x[1] for x in MAJ1]), sum([x[1] for x in MAJ1])],
###      'MAJ2':[sum([x[0]*x[1] for x in MAJ2]), sum([x[1] for x in MAJ2])]
###     };
### 


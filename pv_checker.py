##########################################################
###                                                    ###
###                New PV Checker                      ###
###                                                    ###
###                Date: 09/07/2026                    ###
###                                                    ###
##########################################################
from itertools import product
from maquette import Blocs, UEs, Listes

##########################################################
###                                                    ###
###          Vérification des données APOGEE           ###
###                                                    ###
##########################################################
def SanityCheck(pv, logger=None, newmaquette=False, session2=False):
    # Boucle sur les étudiants
    for student_id, student_data in pv.items():
        # Init
        pv_data = student_data["pv"]
        tag = f"[{student_data['nom']} ({student_id})]"
        logger.debug(f"PV de {tag[1:-1]}")
        score = maxi  = 0.0
        maj   = None
        comp  = False
        done = []

        # Safety
        if len( [ [ue, pv_data[ue]] for ue in pv_data.keys() if pv_data[ue].get('active',False) and ue!='Résultat'])==0: continue

        # 1) Vérification des blocs et des UEs
        for key in pv_data.keys():
            # Safety : ni un bloc ni une UE
            if key=='Résultat': continue

            # Un bloc : vérification
            elif key in Blocs.keys():

                # Safety: blocs vides et chapeaux
                if not 'nom' in Blocs[key].keys() or not pv_data[key]['active']: continue

                # calcul de la note
                sc, mx, mtch = CheckBlock(key, pv_data, tag, logger=logger)
                score += sc
                maxi  += mx
                done  += mtch
                if Blocs[key]['nom'] == 'MAJ':
                    note = pv_data[key].get('note')
                    maj = note/pv_data[key].get('bareme',100)*100 if isinstance(note,(int,float)) else None

            # Une UE : vérification
            elif key in UEs.keys():
                CheckUE(key, pv_data[key], tag, logger=logger)
                note_str=pv_data[key].get('note','')
                if not note_str in ['DIS'] and (note_str in ['ABI', 'ABJ'] or pv_data[key].get('note',0)<50): comp = True

            # Problème...
            elif pv_data[key].get('active',False): logger.warning(f"{tag} Bloc/UE inconnu dans le PV : {key}")

        # 2) UEs hors blocs
        from pv_writer import include_alacarte
        for key,vals in pv_data.items():
            if newmaquette and not include_alacarte(vals, flag=newmaquette): continue
            if not newmaquette and not vals.get('active'): continue  # A cause de l'info et des maths -> à vérifier
            if key in done or not key in UEs.keys() or vals.get('note','') in ['DIS']: continue
            if not isinstance(vals.get('note',''),(int, float)) and vals.get('resultat','') in ['VAC']: continue
            if key[:2] in ['L3', 'L4', 'L5', 'L6'] and vals.get('note',None)==None: continue
            ue_note = vals.get("note", 0)
            if ue_note in ['ABI', 'ABJ']: ue_note=0
            ue_ects = UEs.get(key, {}).get("ects", None)
            if ue_ects is None:
                logger.error(f"{tag} UE {key} absente de la maquette)")
                continue
            score+=ue_note*ue_ects/vals.get('bareme',0)
            maxi +=ue_ects

        # 3) Vérification de la moyenne d'année
        CheckSemestre(score, maxi, maj, comp, pv_data, tag, logger=logger, newmaquette=newmaquette, session2=session2)

        # Exit
        logger.debug("OK")


##########################################################
###                                                    ###
###               Vérification d'un bloc               ###
###                                                    ###
##########################################################

# Fonction auxiliaire pour traiter les listes d'UE
def expand_UE_list(ue_list, logger=None):
    expanded = []
    for ue in ue_list:
        if ue.startswith("LY") and ue in Listes.keys(): expanded.append(Listes[ue])
        else:
            if ue.startswith("LY"): logger.error(f"Liste d'options inconnue ({ue})")
            expanded.append([ue])
    return [list(combo) for combo in product(*expanded)]


def CheckBlock(bloc, pv, tag, logger=None):
    # Initialisation
    logger.debug(f"  - Bloc {bloc}")

    # 1) Détermination de l’ensemble correct d’UEs pour ce bloc
    #    et si toutes les UE sont là
    possible_sets = []
    for lst in Blocs[bloc]["UE"]: possible_sets.extend(expand_UE_list(lst, logger=logger))
    matching_set = None
    for ue_list in possible_sets:
        if all(myue in [ue for ue in pv if pv[ue].get('active',True)] for myue in ue_list):
            matching_set = ue_list
            break
    if matching_set is None:
        if not pv['Résultat']['resultat'] in ['ENCO', 'NCAE']: logger.warning(f"{tag} Aucun set d'UE ne correspond au bloc {bloc}")
        return [0,0,[]]

    # Vérification supplémentaire et formattage en cas de liste d'UE
    matching_set = [ pv[x]['ue'] if x.startswith('LY') else x for x in matching_set]

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
        ue_note = pv[ue].get("note", 0)
        if ue_note in ['ABI', 'ABJ']: ue_note=0
        ue_ects = UEs.get(ue, {}).get("ects", None)
        if ue_ects is None:
            logger.error(f"{tag} UE {ue} absente de la maquette)")
            continue

        # SX: on ignore
        if ue in Blocs[bloc].get('SX', []) or ue_note in ['DIS'] or (pv[ue].get('resultat',None) in ['VAC'] and ue_note==0): continue

        # Tout va bien, on calcule la moyenne du bloc
        score += ue_note*ue_ects/pv[ue]['bareme']
        maxi  += ue_ects
        if ue_note<pv[ue]['bareme']/2.:  comp = True
        if maxi==0:
            logger.error(f"{tag} Impossible de calculer la moyenne du bloc {bloc} (ECTS = 0)")
            continue
        moyenne = score/maxi*pv[bloc]['bareme']
        pv[bloc]['ects']=maxi

    # 3) Comparaison avec la moyenne du PV
    note_pv = pv[bloc].get("note", None)
    if note_pv is None:
        logger.warning(f"{tag} Note absente dans le PV pour le bloc {bloc}")
        logger.debug(f"    > OK")
        return [0, 0, []]
    elif note_pv in ['DIS']:
        logger.debug(f"    > OK")
        return [score, maxi, matching_set]
    else:
        if abs(moyenne-note_pv)>1e-1:
            logger.error(f"{tag} Différence de moyenne pour le bloc {bloc} : "
               f"calculée={moyenne:.3f}, PV={note_pv}")

    # 4) Test du résultat (validation)
    resultat = "ADM" if note_pv>=50 else "AJ"
    if pv[bloc]["resultat"]!=resultat and resultat=='ADM' and not comp:
          logger.warning(f"{tag} Résultat incorrect pour le bloc {bloc} : attendu={resultat}, PV={pv[bloc]['resultat']}")

    # Exit (on renvoie le score pour la moyenne semestrielle
    logger.debug(f"    > OK")
    return [score, maxi, matching_set]



##########################################################
###                                                    ###
###         Vérification du résultat d'une UE          ###
###                                                    ###
##########################################################
def CheckUE(ue, data, tag, logger=None):
    # Initialisation and safety
    logger.debug(f"  - UE {ue}")
    if data['resultat'] in [None, 'DIS'] or not 'note' in data.keys():
        logger.debug(f"    > OK")
        return

    # Check
    resultat = "ADM" if (not data['note'] in ['ABI', 'ABJ'] and data['note']>=50) else "AJ"
    if data["resultat"]!=resultat and not data['resultat'] in ['VAC']:
        logger.error(f"{tag} Résultat incorrect pour l'UE {ue} : "
           f"attendu={resultat}, PV={data['resultat']}")
    # Exit
    logger.debug(f"    > OK")


##########################################################
###                                                    ###
###         Vérification du résultat semestriel        ###
###                                                    ###
##########################################################
def CheckSemestre(score, maxi, maj, comp, data, tag, logger=None, newmaquette=False, session2=False):
    # Initialisation et safety
    logger.debug(f"  - Vérification de la moyenne semestrielle")
    if "Résultat" not in data.keys(): logger.warning(f"{tag} Aucune entrée 'Résultat' dans le PV")
    elif data['Résultat']['resultat'] in ['ENCO', 'NCAE']: logger.debug(f"    > NCAE/ENCO - pas nécessaire"); return
    elif maxi==0:
        logger.error(f"{tag} Impossible de calculer la moyenne semestrielle (ECTS = 0)")
        return
    if not 'note' in data["Résultat"].keys():
        logger.error(f"{tag} Absence de note pour le semestre")
        return

    # Enregistrement du résultat de la majeure
    data['Résultat']['maj1_1']=maj

    # 1) Vérification moyenne
    annee = (1 if (score==0 and maxi==0) else score/maxi)*data['Résultat']['bareme']+data["Résultat"].get('pnt_jury',0)
    note_pv  = data["Résultat"]["note"]
    if abs(annee-note_pv)>5e-2: logger.error(f"{tag} Différence de moyenne semestrielle : calculée={annee:.3f}, PV={note_pv}")

    # 2) Vérification du résultat semestriel
    if newmaquette and maj!=None: resultat = "ADM" if (note_pv>=10 and maj>=50) else "AJ"
    elif newmaquette: resultat = "ADM" if note_pv>=10 else "AJ"
    else: resultat = "ADM" if (note_pv>=10) else "AJ"
    if data["Résultat"]["resultat"]!=resultat:
        if resultat=='ADM' and not comp:
          logger.warning(f"{tag} Résultat incorrect pour l'année : "
             f"attendu={resultat}, PV={data['Résultat']['resultat']}")
        elif resultat=='ADM' and comp and not session2:
          logger.warning(f"{tag} Refus de compensation pour le semestre")
        elif newmaquette and resultat=='AJ':
          logger.warning(f"{tag} Le résultat de la VET devrait être AJ")

    # Exit
    logger.debug(f"    > OK")


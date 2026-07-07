##########################################################
###                                                    ###
###               Outils de Fusion de PV               ###
###                                                    ###
###                Date: 07/07/2026                    ###
###                                                    ###
##########################################################



##########################################################
###                                                    ###
###              Fusion de deux sessions               ###
###                                                    ###
##########################################################
def MergeSessions(session1, session2, logger=None):
    # Initialisation et safety
    pv = {}
    if session1['VET'] != session2['VET']:
        logger.error(f"Les VET diffèrent entre les sessions 1 ({session1['VET']} 2 ({session2['VET']})")
        return {}
    if not set(session2['students'].keys()).issubset(set(session1['students'].keys())):
        logger.warning(f"Étudiants présents en session 2 mais pas en session 1: "
            f"{set(session2['students'].keys())-set(session1['students'].keys())}")

    # Fusion et reformatage (une entrée dans le dico par étudiant)
    for etu_id, resu1 in session1['students'].items():

        # Copie des résultats de session1 (et réorganisation)
        pv[etu_id] = { "nom": resu1.get("nom"), "VET": [session1["VET"]], "pv": {session1['VET']: dict(resu1["pv"])} }

        # Update si l'étudiant est en session2
        if etu_id in session2['students'].keys():

            # PV session2
            resu2 = session2['students'][etu_id]["pv"]

            # loop sur les éléments du PV et mise à jour
            for ue, data in resu2.items():
                # Safety
                if ue not in pv[etu_id]["pv"][session1['VET']].keys():
                    logger.error(f"[{pv[etu_id]['nom']} ({etu_id})] UE '{ue}' présente en session2 mais pas en session1")
                    pv[etu_id]['pv'][session1['VET']][ue] = dict(data)
                    continue
                if not 'note' in data.keys(): continue
                sess1=True if 'note' in pv[etu_id]['pv'][session1['VET']][ue].keys() else False

                # UE présente dans les deux sessions
                # 1) Check la note n'a pas diminué
                note1 = 0 if (not sess1 or pv[etu_id]['pv'][session1['VET']][ue]["note"] in ['ABI', 'ABJ']) else pv[etu_id]['pv'][session1['VET']][ue]["note"]
                note2 = 0 if data["note"] in ['ABI', 'ABJ'] else data['note']
                if note1 > note2:
                    logger.error(f"[{pv[etu_id]['nom']} ({etu_id})] note de {ue} en session 2 ({data['note']}) "
                       f"inférieure à la note en session1 ({pv[etu_id]['pv'][session1['VET']][ue]['note']})")
                # 2) Sauvegarde
                if note1 != note2:
                    pv[etu_id]['pv'][session1['VET']][ue]["note2"] = data['note']
                    pv[etu_id]['pv'][session1['VET']][ue]["maj1_2"] = data.get('maj1_1',None)
                if data['resultat'] != pv[etu_id]['pv'][session1['VET']][ue]["resultat"]: pv[etu_id]['pv'][session1['VET']][ue]["resultat2"] = data["resultat"]

    # Output
    return pv

##########################################################
###                                                    ###
###             Fusion de deux semestres               ###
###                                                    ###
##########################################################
def MergeSemesters(data, logger=None):

    # Initialisation 
    pv = {}
    logger.info(f"Fusion des VETS : {', '.join(sorted(data.keys()))}")

    # Boucle sur les semestres
    for sem, sem_data in data.items():
        # boucle sur les étudiants
        for etu_id, etu_data in sem_data.items():
            if etu_id not in pv:
                pv[etu_id] = { 'VET': list(etu_data.get('VET', [])), 'nom': etu_data.get('nom', ''),
                    'pv': dict(etu_data.get('pv', {}))}
            else:
                for vet in etu_data.get('VET', []):
                    if vet not in pv[etu_id]['VET']: pv[etu_id]['VET'].append(vet)
                pv[etu_id]['pv'].update(etu_data.get('pv', {}))

    # Output
    return pv


##########################################################
###                                                    ###
###                Outils  statistiques                ###
###                                                    ###
###                Date: 02/02/2026                    ###
###                                                    ###
##########################################################
from collections import defaultdict
from maquette import Blocs, UEs
from pv_writer import include_alacarte


##########################################################
###                                                    ###
###                     Classements                    ###
###                                                    ###
##########################################################

# Fonction auxiliaire : assigne les classement sous la forme "#/N"
def compute_ranks(note_list):
    sorted_list = sorted(note_list, key=lambda x: x[1], reverse=True)
    ranks = {}
    prev_note = None
    current_rank = 1
    for index, (etu_id, note) in enumerate(sorted_list, start=1):
        if note != prev_note: current_rank = index
        ranks[etu_id] = f"{current_rank}/{len(sorted_list)}"
        prev_note = note
    return ranks



def AddRankings(data, logger=None):
    # Initialisation
    ue_notes1 = {}
    ue_notes2 = {}

    # boucle sur les étudiants
    for etu_id, etu_data in data.items():
        # VET et éléments des VET
        for vet, elements in etu_data['pv'].items():
            for myue, vals in elements.items():
                # init
                ue = myue if myue!='Résultat' else vet

                # notes session1
                note = vals.get('note')
                if isinstance(note, (int, float)): ue_notes1.setdefault(ue, []).append((etu_id, note))
                elif note in ['ABI', 'ABJ']: ue_notes1.setdefault(ue, []).append((etu_id, 0))
                elif note in ['DIS', None]: continue
                else: logger.warning(f"[{etu_data['nom']} ({etu_id})] Type de note inconnue ({note}) dans le pv")

                # notes session2
                note = vals.get('note2', vals.get('note'))
                if isinstance(note, (int, float)): ue_notes2.setdefault(ue, []).append((etu_id, note))
                elif note in ['ABI', 'ABJ']: ue_notes2.setdefault(ue, []).append((etu_id, 0))
                elif note in ['DIS', None]: continue
                else: logger.warning(f"[{etu_data['nom']} ({etu_id})] Type de note inconnue ({note}) dans le pv")


        # Annee
        if 'annee' in etu_data.keys():
            ue_notes1.setdefault('annee', []).append((etu_id, etu_data['annee']['note']))
            ue_notes2.setdefault('annee', []).append((etu_id, etu_data['annee']['note2']))


    # Calcul du classement pour chaque UE
    ue_ranks1 = {ue: compute_ranks(lst) for ue, lst in ue_notes1.items()}
    ue_ranks2 = {ue: compute_ranks(lst) for ue, lst in ue_notes2.items()}

    # Injection dans le PV
    for etu_id, etu_data in data.items():
        for vet, elements in etu_data['pv'].items():
            for myue, vals in elements.items():
                # init
                ue = myue if myue!='Résultat' else vet

                # Classement session 1
                if ue in ue_ranks1.keys() and etu_id in ue_ranks1[ue]: vals["rank"] = ue_ranks1[ue][etu_id]

                # Classement session 2
                if ue in ue_ranks2.keys() and 'note2' in vals.keys(): vals["rank2"] = ue_ranks2[ue][etu_id]

        if 'annee' in etu_data.keys():
            # Classement session 1
            if etu_id in ue_ranks1['annee']: etu_data['annee']["rank"] = ue_ranks1['annee'][etu_id]

            # Classement session 2
            if 'note2' in etu_data['annee'].keys(): etu_data['annee']["rank2"] = ue_ranks2['annee'][etu_id]




##########################################################
###                                                    ###
###                  Moyenne annuelle                  ###
###                                                    ###
##########################################################
def MoyenneAnnuelle(data, logger=None, newmaquette=False):

    # Boucle sur les étudiants
    for etu_id, etu_data in data.items():
        if any(vet_data.get('Résultat', {}).get('resultat')=='NCAE' for vet_data in etu_data.get('pv', {}).values()): continue
        session1 = maj1 = session2 = maj2 = ects = maj_ects = 0

        # Boucle sur les VET
        for vet in etu_data['VET']:
            logger.debug(f"[{etu_data['nom']} ({etu_id})] Calcul de la moyenne pour la VET {vet}")
            # Calcul de moyenne non nécessaire
            if etu_data['pv'][vet]['Résultat']['resultat'] in ['NCAE']: continue

            # Calcul des moyennes annuelles session1 et session2
            for name, resu in etu_data['pv'][vet].items():

                # On ne garde que les blocs
                if not name in Blocs.keys(): continue

                # Notes sessions 1 et 2
                note1 = resu.get('note')
                note2 = resu.get('note2', note1)

                # Calculs
                if note2 not in (None, 'DIS') and resu['ects']!='':
                    session2 += note2*resu['ects']/resu['bareme']*100
                    if 'maj' in resu['libelle'].lower():
                        maj2     += note2*resu['ects']/resu['bareme']*100
                        maj_ects += resu['ects']
                    ects += resu['ects']
                if note1 not in (None, 'DIS') and resu['ects']!='':
                    session1 += note1*resu['ects']/resu['bareme']*100
                    if 'maj' in resu['libelle'].lower(): maj1 += note1*resu['ects']/resu['bareme']*100


            # Parcours à la carte
            if newmaquette and session1==0 and ects==0:
                for name, resu in etu_data['pv'][vet].items():

                    # On ne garde que les UEs
                    if not name in UEs.keys() or not include_alacarte(resu, flag=newmaquette): continue

                    # Notes sessions 1 et 2
                    note1 = 0 if resu.get('note') in ('ABI', 'ABJ') else resu.get('note')
                    note2 = 0 if resu.get('note2', note1) in ('ABI', 'ABJ') else resu.get('note2', note1)

                    # Calculs
                    if note2 not in (None, 'DIS'):
                        session2 += note2*UEs[name]['ects']/resu['bareme']*100
                        ects += UEs[name]['ects']
                    if note1 not in (None, 'DIS'):
                        session1 += note1*UEs[name]['ects']/resu['bareme']*100

        # Résultats
        if ects:
            session1 = session1/(5.*ects)
            session2 = session2/(5.*ects)
            if maj_ects:
                maj1 = maj1/maj_ects
                maj2 = maj2/maj_ects
            if newmaquette and maj_ects:
                resu1 = 'ADM' if (session1>=10 and maj1>=50) else 'AJ'
                resu2 = 'ADM' if (session2>=10 and maj2>=50) else 'AJ'
            else:
                resu1 = 'ADM' if session1>=10 else 'AJ'
                resu2 = 'ADM' if session2>=10 else 'AJ'
            etu_data['annee'] = {'note':session1, 'resultat':resu1, 'note2':session2, 'resultat2':resu2, 'maj1_1':maj1, 'maj1_2':maj2}


##########################################################
###                                                    ###
###                Blocs disciplinaires                ###
###                                                    ###
##########################################################
def BlocsDisciplinaires(data, logger=None):

    # Boucle sur les étudiants
    for etu_id, etu_data in data.items():

        # Initialisation année
        annee_bdisc1 = defaultdict(float)
        annee_bdisc2 = defaultdict(float)
        annee_bects  = defaultdict(float)

        # Boucle sur les VETs
        for vet in etu_data['VET']:
            # Initialisation
            logger.debug(f"[{etu_data['nom']} ({etu_id})] Calcul des blocs disciplinaires pour la VET {vet}")
            pv_vet = etu_data['pv'][vet]

            # Calcul non nécessaire
            if etu_data['pv'][vet]['Résultat']['resultat'] in ['NCAE']: continue

            # Liste disciplines
            blocs = list(dict.fromkeys([ bloc[3:5] for bloc, v in pv_vet.items() if bloc in Blocs and v.get('active') and not 'DK' in bloc]))
            if not blocs: continue

            # Initialisation
            bdisc1 = {b:0 for b in blocs}
            bdisc2 = {b:0 for b in blocs}
            bects  = {b:0 for b in blocs}

            # Calcul de la note
            for ue, resu in pv_vet.items():
                # Safety
                if not ue in UEs or 'OIP' in ue: continue
                ects = UEs[ue].get('ects')
                if not ects: continue

                # Notes sessions 1 et 2 et bloc associé à l'UE
                bloc = next((b for b in blocs if b in ue), None)
                if bloc is None: continue
                note1 = resu.get('note') if not resu.get('note') in ['ABI','ABJ'] else 0
                note2 = resu.get('note2',note1) if not resu.get('note2',note1) in ['ABI','ABJ'] else 0

                # Calculs session 2
                if note2 not in (None, 'DIS'):
                    val = note2*ects/resu['bareme']*100
                    bdisc2[bloc] += val
                    bects[bloc]  += ects
                    annee_bdisc2[bloc] += val
                    annee_bects[bloc]  += ects

                # Calcul session 1
                if note1 not in (None, 'DIS'):
                    val = note1*ects/resu['bareme']*100
                    bdisc1[bloc] += val
                    annee_bdisc1[bloc] += val

            # Normalisation VET et stockage
            for b in blocs:
                if bects[b]:
                    bdisc1[b] /= bects[b]
                    bdisc2[b] /= bects[b]
            pv_vet['Résultat']['bdisc1'] = bdisc1
            pv_vet['Résultat']['bdisc2'] = bdisc2

        # Normalisation année et stockage
        if 'annee' in etu_data:
            bdisc1_annee = {}
            bdisc2_annee = {}
            for b in annee_bects:
                if annee_bects[b]:
                    bdisc1_annee[b] = annee_bdisc1[b] / annee_bects[b]
                    bdisc2_annee[b] = annee_bdisc2[b] / annee_bects[b]
            etu_data['annee']['bdisc1'] = bdisc1_annee
            etu_data['annee']['bdisc2'] = bdisc2_annee



##########################################################
###                                                    ###
###            Données statistiques anonymes           ###
###                                                    ###
##########################################################

# Fonction auxiliaire : pour récupérer les flags de compensation et ajouter les notes à la liste
def collect_notes(elem, key, notes, notes2):
    # Initialisation
    n1 = elem.get('note') if not elem.get('note',100) in ['ABI','ABJ'] else 0
    n2 = elem.get('note2',n1) if not elem.get('note2',n1) in ['ABI','ABJ'] else 0
    comp1 = comp2 = False

    # 1ere session
    if isinstance(n1, (int, float)):
        notes[key].append(n1)
        comp1 = n1 < (elem.get('bareme',20)/2)

    # 2nd session
    if isinstance(n2, (int, float)):
        notes2[key].append(n2)
        comp2 = n2 < (elem.get('bareme',20)/2)

    # Output
    return comp1, comp2


# Fonction auxiliaire : modification du résultat en "COMP" si nécessaire
def update_result(res, comp, maj, note):
    # Ce n'est pas ADM
    if res!='ADM': return 'AJ-MAJ' if note>=10 else 'AJ'

    # Pas de note MAJ
    if not maj: return 'COMP' if comp else 'ADM'

    # note MAJ présente
    if maj>=50: return 'COMP' if comp else 'ADM'
    else: return 'COMP-MAJ' if comp else 'ADM-MAJ'


# Fonction principale
def generate_stats(data, logger=None, filtre='', newmaquette=False):
    # Initialisation
    logger.info(f"Génération des statistiques de réussite globales")
    resultats  = defaultdict(list)   # les 'AJ', 'ADM', ...
    resultats2 = defaultdict(list)   # les 'AJ', 'ADM' après session2
    notes      = defaultdict(list)   # notes session1
    notes2     = defaultdict(list)   # notes après session2

    # Boucle principale sur les PV
    for etu_data in data.values():
        # Filtre
        if 'mineure' in etu_data.keys() and filtre!='' and etu_data['mineure']!=filtre: continue

        # Résultats annuels
        comp1_an = comp2_an = False
        maj1_1 = maj1_2 = None
        if 'annee' in etu_data:
            pv_annee = etu_data['annee']
            collect_notes(pv_annee, 'annee', notes, notes2)
            r1_an = pv_annee.get('resultat')
            r2_an = pv_annee.get('resultat2',r1_an)
            maj1_an = pv_annee.get('bdisc1').get('PY', None) if 'bdisc1' in pv_annee else pv_annee.get('maj1_1', None)
            maj2_an = pv_annee.get('bdisc2').get('PY', maj1_an) if 'bdisc2' in pv_annee else pv_annee.get('maj1_2', maj1_an)

        # Boucle sur les semestres
        for vet, pv in etu_data['pv'].items():
            # Initialisation VET
            comp1_vet = comp2_vet= False
            pv_vet = pv.get('Résultat', {})
            r1_vet=r2_vet=None

            # Résultat semestriel
            collect_notes(pv_vet, vet, notes, notes2)
            n1_vet = pv_vet.get('note', None)
            n2_vet = pv_vet.get('note2', n1_vet)
            maj1_vet = pv_vet.get('bdisc1').get('PY', None) if 'bdisc1' in pv_vet else pv_vet.get('maj1_1', None)
            maj2_vet = pv_vet.get('bdisc2').get('PY', maj1_vet) if 'bdisc2' in pv_vet else pv_vet.get('maj1_2', maj1_vet)
            if n1_vet: r1_vet = 'ADM' if n1_vet>=10 and (not newmaquette or maj1_vet>=50) else 'AJ'
            if n2_vet: r2_vet = 'ADM' if n2_vet>=10 and (not newmaquette or maj2_vet>=50) else 'AJ'

            # Tous les autres éléments du PV : UEs / blocs
            for code, elem in pv.items():
                # Ignore : pas besoin pour les stats
                if code == 'Résultat' or 'PY' not in code: continue

                # Stats UE/Bloc
                c1, c2 = collect_notes(elem, code, notes, notes2)
                comp1_vet |= c1
                comp2_vet |= c2

            # Finalisation résultats semestre
            if r1_vet: resultats[vet].append(update_result(r1_vet, comp1_vet, maj1_vet, n1_vet))
            if r2_vet: resultats2[vet].append(update_result(r2_vet, comp2_vet, maj2_vet, n2_vet))
            comp1_an |= (r1_vet=='AJ')
            comp2_an |= (r2_vet=='AJ')

        # Finalisaton résultats annuels
        if 'annee' in etu_data.keys():
            if r1_an: resultats['annee'].append(update_result(r1_an, comp1_an, maj1_an, etu_data['annee'].get('note',None)))
            if r2_an: resultats2['annee'].append(update_result(r2_an, comp2_an, maj2_an, etu_data['annee'].get('note2',etu_data['annee'].get('note',None))))

    # Output
    return { "resultats": dict(resultats), 'resultats2': dict(resultats2), "notes": dict(notes), "notes2": dict(notes2) }


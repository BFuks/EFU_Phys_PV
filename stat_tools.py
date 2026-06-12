##########################################################
###                                                    ###
###                Outils  statistiques                ###
###                                                    ###
###                Date: 12/06/2026                    ###
###                                                    ###
##########################################################
from collections import defaultdict
from maquette import Blocs, UEs
from pathlib import Path
from pv_writer import include_alacarte
import pandas as pd
import re

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


# Fonction auxiliaire : détermination de la second discipline
def Discipline2(pv, vets):
    # Initialisation
    pattern_maj = re.compile(r"(\dSVPY|S\dVPY)")
    pattern_dm  = re.compile(r"(\dSQPY|S\dQPY|Q2PYDL)")
    if all(pattern_maj.search(vet) for vet in vets):
        return next((k[3:5] for k,v in pv[vets[-1]].items() if k in Blocs and k[3:5]!="PY" and v.get('active',True)),'')
    elif all(pattern_dm.search(vet) for vet in vets):
        MAJ2 = next((k[3:5] for k,v in pv[vets[-1]].items() if k in Blocs and k[3:5]!="PY" and v.get('active',True)),'')
        if not MAJ2: MAJ2 = next((k[3:5] for k,v in pv[vets[0]].items() if k in Blocs and k[3:5]!="PY" and v.get('active',True)),'')
        return MAJ2


def AddRankings(data, logger=None, filtre=None):
    # Initialisation
    ue_notes1 = {}
    ue_notes2 = {}

    # boucle sur les étudiants
    for etu_id, etu_data in data.items():
        # Filtre MAJ/MIN ou DM spécifique
        if filtre and Discipline2(etu_data['pv'], sorted(etu_data['VET']))!=filtre: continue

        # VET et éléments des VET
        for vet, elements in etu_data['pv'].items():
            for myue, vals in elements.items():
                # init and safety
                if myue==vet: continue
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
        # Filtre MAJ/MIN ou DM spécifique
        if filtre and Discipline2(etu_data['pv'], sorted(etu_data['VET']))!=filtre: continue

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
#Bcp de hlpers pour rendre la fonction princnipale claire et compacte
def clean_note(note): return 0 if note in ('ABI', 'ABJ') else note

def is_valid_note(note): return note not in (None, 'DIS', 'VAC')

def get_ue_ects(ue, resu_ue):
    ects = UEs.get(ue, {}).get('ects', resu_ue.get('ects'))
    return None if ects in (None, '') else ects

def get_matching_ue_set(bloc, pv_vet):
    ue_sets = Blocs[bloc].get('UE', [])
    for ue_set in ue_sets:
        if all( ue in pv_vet and pv_vet[ue].get('active', True) for ue in ue_set): return ue_set
    return []

def effective_block_ects(bloc, pv_vet, session=1):
    # Init
    ue_set = get_matching_ue_set(bloc, pv_vet)
    total = 0.0
    used_ues = set()
    for ue in ue_set:
        # Safety
        if ue not in pv_vet: continue
        resu_ue = pv_vet[ue]
        if not resu_ue.get('active', True): continue

        # note
        note = (resu_ue.get('note2', resu_ue.get('note')) if session==2 else resu_ue.get('note'))
        note = clean_note(note)
        if not is_valid_note(note): continue

        # ECTS
        ects = get_ue_ects(ue, resu_ue)
        if ects is None: continue
        total += ects
        used_ues.add(ue)

    # output
    return total, used_ues


def MoyenneAnnuelle(data, logger=None, newmaquette=False):
    # Boucle sur les étudiants
    for etu_id, etu_data in data.items():
        # Si une VET est ENCO/NCAE, on ne calcule pas l'année.
        if any(vet_data.get('Résultat', {}).get('resultat') in ['ENCO', 'NCAE'] for vet_data in etu_data.get('pv', {}).values()): continue

        # Init
        session1 = session2 = ects1 = ects2 = 0
        maj1 = maj2 = maj_ects1 = maj_ects2 = 0

        # Boucle sur les VET
        for vet in etu_data['VET']:
            # Init
            logger.debug(f"[{etu_data['nom']} ({etu_id})] Calcul de la moyenne pour la VET {vet}")
            pv_vet = etu_data['pv'][vet]
            used_ues1 = set()
            used_ues2 = set()

            # Calcul des moyennes annuelles session1 et session2 (blocs)
            for name, resu in pv_vet.items():

                # On ne garde que les blocs
                if name not in Blocs.keys() or not Blocs[name]: continue
                if not resu.get('active',True): continue

                # Notes sessions 1 et 2 + quelques infos
                note1 = clean_note(resu.get('note'))
                note2 = clean_note(resu.get('note2', note1))
                bareme = resu.get('bareme', 100)
                is_maj = (Blocs[name].get('nom') == 'MAJ')

                # ECTS effectifs reconstruits depuis les UE du bloc
                bloc_ects1, bloc_ues1 = effective_block_ects(name, pv_vet, session=1)
                bloc_ects2, bloc_ues2 = effective_block_ects(name, pv_vet, session=2)
                used_ues1.update(bloc_ues1)
                used_ues2.update(bloc_ues2)

                # Calculs session 1
                if is_valid_note(note1) and bloc_ects1:
                    contribution1 = note1 * bloc_ects1 / bareme * 100.0
                    session1 += contribution1
                    ects1 += bloc_ects1
                    if is_maj:
                        maj1 += contribution1
                        maj_ects1 += bloc_ects1

                # Calculs session 2
                if is_valid_note(note2) and bloc_ects2:
                    contribution2 = note2 * bloc_ects2 / bareme * 100.0
                    session2 += contribution2
                    ects2 += bloc_ects2
                    if is_maj:
                        maj2 += contribution2
                        maj_ects2 += bloc_ects2

            # Ajout systématique des UE actives non déjà utilisées par un bloc
            for name, resu in pv_vet.items():
                # On ne garde que les UE actives
                if name not in UEs: continue
                if not resu.get('active', True): continue

                # ECTS, notes et barème
                ects = get_ue_ects(name, resu)
                if ects is None: continue
                bareme = resu.get('bareme', 100)
                note1 = clean_note(resu.get('note'))
                note2 = clean_note(resu.get('note2', note1))

                # Session 1 : seulement si l'UE n'a pas déjà été absorbée par un bloc
                if name not in used_ues1 and is_valid_note(note1):
                    session1 += note1 * ects / bareme * 100.0
                    ects1 += ects
                # Session 2 : idem
                if name not in used_ues2 and is_valid_note(note2):
                    session2 += note2 * ects / bareme * 100.0
                    ects2 += ects

        # Résultats
        if ects1:
            moyenne1 = session1 / (5.0 * ects1)
            moyenne2 = session2 / (5.0 * ects2)
            maj_moy1 = maj1 / maj_ects1 if maj_ects1 else None
            maj_moy2 = maj2 / maj_ects2 if maj_ects2 else None
            if newmaquette and maj_moy1 is not None:
                resu1 = 'ADM' if moyenne1 >= 10 and maj_moy1 >= 50 else 'AJ'
                resu2 = 'ADM' if moyenne2 >= 10 and maj_moy2 >= 50 else 'AJ'
            else:
                resu1 = 'ADM' if moyenne1 >= 10 else 'AJ'
                resu2 = 'ADM' if moyenne2 >= 10 else 'AJ'

            # Output
            etu_data['annee'] = {'note':moyenne1, 'resultat':resu1, 'note2':moyenne2, 'resultat2':resu2, 'maj1_1':maj_moy1, 'maj1_2':maj_moy2}


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
            if etu_data['pv'][vet]['Résultat']['resultat'] in ['NCAE', 'ENCO']: continue

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
                bloc = next((b for b in blocs if b.replace('FL','SX') in ue), None)
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
def generate_stats(data, logger=None, filtre=None, newmaquette=False):
    # Initialisation
    logger.info(f"Génération des statistiques de réussite globales")
    resultats  = defaultdict(list)   # les 'AJ', 'ADM', ...
    resultats2 = defaultdict(list)   # les 'AJ', 'ADM' après session2
    notes      = defaultdict(list)   # notes session1
    notes2     = defaultdict(list)   # notes après session2

    # Boucle principale sur les PV
    for etu_data in data.values():
        # Filtre
        if 'mineure' in etu_data.keys() and filtre and etu_data['mineure']!=filtre: continue
        if 'majeure2' in etu_data.keys() and filtre and etu_data['majeure2']!=filtre: continue

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
            if not maj1_vet: maj1_vet=100
            if not maj2_vet: maj2_vet=100
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




##########################################################
###                                                    ###
###                 Analyse  présences                 ###
###                                                    ###
##########################################################

# Reformattage du dictionnaire des PV pour ne garder que ce qui est pertinent
def reformat_dict(data, parcours):
    # Initialisation
    ue_data = {}

    # Boucle sur le dictionnaire
    for student_id, student_data in data.items():
        for pv in student_data.get('pv', {}).values():
            for code, result in pv.items():

                # Restriction: que les UEs et que si il existe une note
                if code not in UEs: continue
                note = result.get('note')
                if note is None: continue

                # Sauvegarde
                ue_data.setdefault(code, {})[student_id] = { 'note': note, 'parcours': parcours }

    return ue_data

# Fusion de deux dictionnaires
def merge_ue_dicts(target, source):
    for ue, students in source.items():
        target.setdefault(ue, {})
        target[ue].update(students)
    return target

# Nettoyage de l'info d'une colonne de présence
def _extract_status(cell):
    # Safety
    if pd.isna(cell): return None
    s = str(cell).strip()
    if not s: return None

    # Main
    if s.startswith("P"): return "P"
    if s.startswith("A"): return "A"
    if s.startswith("E"): return "E"
    if s.startswith("?"): return "?"

    # Safety again
    return None

# Fonction auxiliaire pour charger un fichier de présences
def load_presence_info(filepath):

    # Initialisation
    filepath = Path(filepath)
    drop_cols = { "Nom de famille", "Prénom", "ID Étudiant", "Adresse de courriel", "P", "R", "E", "A", "Sessions prises", "Points", "Pourcentage"}
    id_col = "Numéro d’identification"

    # Lecture du fichier (entête standardisée) et conversion des cellules
    df = pd.read_excel(filepath, header=3).dropna(how='all').reset_index(drop=True)
    df = df[[c for c in df.columns if c not in drop_cols]]
    simple_df = df.copy()
    session_cols = [c for c in simple_df.columns if c != id_col]
    simple_df.loc[:, session_cols] = simple_df.loc[:, session_cols].apply(lambda col: col.map(_extract_status))

    # Sélection des colonnes fiables : au moins une valeur P ou A
    kept_cols = [ col for col in session_cols if simple_df[col].isin(["P", "A"]).any() ]
    if not kept_cols: return {}

    # On ne garde que l'identifiant + les colonnes retenues
    final_df = simple_df[[id_col] + kept_cols].copy()
    final_df.loc[:, kept_cols] = final_df.loc[:, kept_cols]

    # Calcul par étudiant
    result = {}
    for _, row in final_df.iterrows():
        vals = row[kept_cols].tolist()
        if sum(v in ("P", "A", "E") for v in vals)>0:
            presence_rate = 100.0 * sum(v == "P" for v in vals) / sum(v in ("P", "A", "E") for v in vals)
            sid = row[id_col]
            try: sid = str(int(sid))
            except (TypeError, ValueError): sid = str(sid).strip()
            result[sid] = { "taux_presence": presence_rate }

    # output
    return result


# Fonction principale pour ajouter l'info sur les présences
def add_info_presences(ue_data, annee, logger=None):
    # Initilisation
    attendance_dir = Path("presences/data")

    # Loop sur les pv disponibles
    for ue_code, students in ue_data.items():
        # Path
        filepath = attendance_dir / f"{annee}-{ue_code}.xlsx"

        # Safety
        if not filepath.exists():
            if logger: logger.debug(f"Pas de fichier de présence pour {ue_code}")
            continue

        # Processing
        data_presences = load_presence_info(filepath)
        for student_id in list(students.keys()):
            if student_id in data_presences: students[student_id].update(data_presences[student_id])
            else: del students[student_id]

    # output
    return ue_data




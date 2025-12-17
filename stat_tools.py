##########################################################
###                                                    ###
###                Outils  statistiques                ###
###                                                    ###
###                Date: 15/12/2025                    ###
###                                                    ###
##########################################################
from maquette import Blocs



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
                elif note=='ABI': ue_notes1.setdefault(ue, []).append((etu_id, 0))
                elif note in ['DIS', None]: continue
                else: logger.warning(f"[{etu_data['nom']} ({etu_id})] Type de note inconnue ({note}) dans le pv")

                # notes session2
                note = vals.get('note2', vals.get('note'))
                if isinstance(note, (int, float)): ue_notes2.setdefault(ue, []).append((etu_id, note))
                elif note=='ABI': ue_notes2.setdefault(ue, []).append((etu_id, 0))
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
def MoyenneAnnuelle(data, logger=None):

    # Boucle sur les étudiants
    for etu_id, etu_data in data.items():
        # Initialisation
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
                    session2 += note2*resu['ects']
                    if 'maj' in resu['libelle'].lower():
                        maj2     += note2*resu['ects']
                        maj_ects += resu['ects']
                    ects += resu['ects']
                if note1 not in (None, 'DIS') and resu['ects']!='':
                    session1 += note1*resu['ects']
                    if 'maj' in resu['libelle'].lower(): maj1 += note1*resu['ects']

        # Résultats
        if ects:
            session1 = session1/(5.*ects)
            session2 = session2/(5.*ects)
            maj1 = maj1/maj_ects
            maj2 = maj2/maj_ects
            resu1 = 'ADM' if (session1>=10 and maj1>=50) else 'AJ'
            resu2 = 'ADM' if (session2>=10 and maj2>=50) else 'AJ'
            etu_data['annee'] = {'note':session1, 'resultat':resu1, 'note2':session2, 'resultat2':resu2}


## 
### from misc      import GetBlocsMaquette, GetUEsMaquette;
### from pv_writer import GetList;
### import functools, operator;
### 
### def GetMoyenneAnnuelle(pv):
###     # Init
###     pv["full"]  = {};
###     pv["full2"] = {};
### 
###     for etu in GetList(pv.values()):
###          # initialisation etudiant
###          logger.debug("etudiant = " + str(etu));
###          moyenne_annee = 0.;
###          moyenne_annee2= 0.;
###          nbr_semestres = len([y for y in [etu[0] in pv[x].keys() for x in pv.keys()] if y]);
###          # 1ere session
###          for semestre in [x for x in pv.keys() if not 'full' in x]:
###              if not etu[0] in pv[semestre].keys() or moyenne_annee in ['ENCO', 'NCAE']: continue;
###              if pv[semestre][etu[0]]['results']['total']['note'] == 'ENCO': moyenne_annee = 'ENCO'; continue;
###              if pv[semestre][etu[0]]['results']['total']['note'] == 'NCAE': moyenne_annee = 'NCAE'; continue;
###              moyenne_annee += pv[semestre][etu[0]]['results']['total']['note']/nbr_semestres;
### 
###          #2eme session
###          for semestre in [x for x in pv.keys() if not 'full' in x]:
###              if not etu[0] in pv[semestre].keys() or moyenne_annee2 in ['NCAE', 'ENCO']: continue;
###              if 'note2' in pv[semestre][etu[0]]['results']['total'].keys() and pv[semestre][etu[0]]['results']['total']['note2'] == 'ENCO':
###                  moyenne_annee2 = 'ENCO'; continue;
###              if 'note2' in pv[semestre][etu[0]]['results']['total'].keys() and pv[semestre][etu[0]]['results']['total']['note2'] == 'NCAE':
###                  moyenne_annee2 = 'NCAE'; continue;
###              if 'note2' in pv[semestre][etu[0]]['results']['total'].keys(): moyenne_annee2 += pv[semestre][etu[0]]['results']['total']['note2']/nbr_semestres;
###              elif moyenne_annee not in ['NCAE', 'ENCO']: moyenne_annee2 += pv[semestre][etu[0]]['results']['total']['note']/nbr_semestres;
###              else: moyenne_annee2=moyenne_annee;
### 
###          # Debug messages
###          logger.debug("  -> session1: " + str(moyenne_annee))
###          if moyenne_annee != moyenne_annee2: logger.debug("  -> session2: " + str(moyenne_annee2))
### 
###          # output
###          pv["full"][str(etu[0])]  = moyenne_annee;
###          pv["full2"][str(etu[0])] = moyenne_annee2;
### 
###     # Rankings
###     all_notes  = sorted([x for x in list(pv["full"].values()) if x not in ['NCAE', 'ENCO'] ], reverse=True);
###     all_notes2 = sorted([x for x in list(pv["full2"].values()) if x not in ['ENCO', 'NCAE'] ], reverse=True);
###     for etu in pv["full"].keys():
###         if pv["full"][etu]not in ['NCAE', 'ENCO']:
###             pv["full"][etu] = [pv["full"][etu], str(all_notes.index(pv["full"][etu])+1) + '/' + str(len(all_notes))];
###     for etu in pv["full2"].keys():
###         if pv["full2"][etu] not in ['NCAE', 'ENCO']:
###             pv["full2"][etu] = [pv["full2"][etu], str(all_notes2.index(pv["full2"][etu])+1) + '/' + str(len(all_notes2))];
### 
###     return pv;
### 
### 
### 
### def GetStatistics(pv, parcours, semestre):
### 
###     # UEs
###     blocs = [x for x in GetBlocsMaquette(semestre.split('_')[0], parcours) ];
###     ues = [x for x in list(set(functools.reduce(operator.iconcat, GetUEsMaquette(blocs), []))) if 'PY' in x or 'LVAN' in x or x.startswith('LU1')];
###     blocs = [x for x in blocs if 'PY' in blocs];
### 
###     # Init of the output
###     notes = {}; notes2 = {};
###     for x in (ues+blocs+['total']):
###         notes[x]  = [];
###         notes2[x] = [];
### 
###     # loop over all students
###     for etudiant in [x for x in pv.keys() if isinstance(x, int)]:
###         # adding the notes
###         for label, data_UE in pv[etudiant]['results'].items():
### 
###            # no stats needed
###            key = label.split('-')[-1].strip();
###            if not key in notes.keys(): continue
###            if 'UE' in data_UE.keys() and data_UE['UE']=='GrosSac': continue;
### 
###            # get the notes
###            mynote2 = data_UE['note2'] if ('note2' in data_UE.keys() and data_UE['note2'] not in ['U VAC', 'DIS', '???', 'ENCO', 'NCAE', 'VAC']) else '';
###            if 'note'  in data_UE.keys() and data_UE['note']  not in ['U VAC', 'DIS', '???', 'ENCO', 'NCAE', 'VAC']:
###                notes[key].append(data_UE['note']);
###            if mynote2!='': notes2[key].append(mynote2);
###            elif  'note'  in data_UE.keys() and data_UE['note'] not in ['U VAC', 'DIS', '???', 'ENCO', 'NCAE', 'VAC']: notes2[key].append(data_UE['note']);
### 
###     # formatting
###     for key in notes.keys() : notes[key]  = sorted([float(x) for x in  notes[key]],reverse=True);
###     for key in notes2.keys(): notes2[key] = sorted([float(x) for x in notes2[key]],reverse=True);
### 
###     # adding the ranking information to each PV.
###     for etudiant in [x for x in pv.keys() if isinstance(x, int)]:
###         # adding the notes
###         for label, data_UE in pv[etudiant]['results'].items():
### 
###            # no stats needed
###            key = label.split('-')[-1].strip();
###            if not key in notes.keys(): continue
###            if 'UE' in data_UE.keys() and data_UE['UE']=='GrosSac': continue;
### 
###            # get the notes
###            if 'note' in data_UE.keys() and data_UE['note'] not in ['ENCO', 'VAC', 'U VAC', 'DIS', '???', 'NCAE']:
###                pv[etudiant]['results'][label]['ranking']  =  str(notes[key].index(float(data_UE['note']))+1)+'/'+str(len(notes[key]));
### 
###            if 'note2' in data_UE.keys() and data_UE['note2'] not in ['ENCO', 'U VAC', 'VAC', 'DIS', '???', 'NCAE']:
###                pv[etudiant]['results'][label]['ranking2'] = str(notes2[key].index(float(data_UE['note2']))+1)+'/'+str(len(notes2[key]));
### 
###     # output
###     return pv;
### 
### 
### 

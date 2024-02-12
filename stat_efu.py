##########################################################
###                                                    ###
###                 Statistics module                  ###
###                                                    ###
##########################################################


##########################################################
###                                                    ###
###                       Logger                       ###
###                                                    ###
##########################################################
import logging;
logger = logging.getLogger('mylogger');


##########################################################
###                                                    ###
###                     Classements                    ###
###                                                    ###
##########################################################
from misc      import GetBlocsMaquette, GetUEsMaquette;
from pv_writer import GetList;
import functools, operator;

def GetMoyenneAnnuelle(pv):
    # Init
    pv["full"]  = {};
    pv["full2"] = {};

    for etu in GetList(pv.values()):
         # initialisation etudiant
         logger.debug("etudiant = " + str(etu));
         moyenne_annee = 0.;
         moyenne_annee2= 0.;
         nbr_semestres = len([y for y in [etu[0] in pv[x].keys() for x in pv.keys()] if y]);
         # 1ere session
         for semestre in [x for x in pv.keys() if not 'full' in x]:
             if not etu[0] in pv[semestre].keys() or moyenne_annee in ['ENCO', 'NCAE']: continue;
             if pv[semestre][etu[0]]['results']['total']['note'] == 'ENCO': moyenne_annee = 'ENCO'; continue;
             if pv[semestre][etu[0]]['results']['total']['note'] == 'NCAE': moyenne_annee = 'NCAE'; continue;
             moyenne_annee += pv[semestre][etu[0]]['results']['total']['note']/nbr_semestres;

         #2eme session
         for semestre in [x for x in pv.keys() if not 'full' in x]:
             if not etu[0] in pv[semestre].keys() or moyenne_annee2 in ['NCAE', 'ENCO']: continue;
             if 'note2' in pv[semestre][etu[0]]['results']['total'].keys() and pv[semestre][etu[0]]['results']['total']['note2'] == 'ENCO':
                 moyenne_annee2 = 'ENCO'; continue;
             if 'note2' in pv[semestre][etu[0]]['results']['total'].keys() and pv[semestre][etu[0]]['results']['total']['note2'] == 'NCAE':
                 moyenne_annee2 = 'NCAE'; continue;
             if 'note2' in pv[semestre][etu[0]]['results']['total'].keys(): moyenne_annee2 += pv[semestre][etu[0]]['results']['total']['note2']/nbr_semestres;
             elif moyenne_annee not in ['NCAE', 'ENCO']: moyenne_annee2 += pv[semestre][etu[0]]['results']['total']['note']/nbr_semestres;
             else: moyenne_annee2=moyenne_annee;

         # Debug messages
         logger.debug("  -> session1: " + str(moyenne_annee))
         if moyenne_annee != moyenne_annee2: logger.debug("  -> session2: " + str(moyenne_annee2))

         # output
         pv["full"][str(etu[0])]  = moyenne_annee;
         pv["full2"][str(etu[0])] = moyenne_annee2;

    # Rankings
    all_notes  = sorted([x for x in list(pv["full"].values()) if x not in ['NCAE', 'ENCO'] ], reverse=True);
    all_notes2 = sorted([x for x in list(pv["full2"].values()) if x not in ['ENCO', 'NCAE'] ], reverse=True);
    for etu in pv["full"].keys():
        if pv["full"][etu]not in ['NCAE', 'ENCO']:
            pv["full"][etu] = [pv["full"][etu], str(all_notes.index(pv["full"][etu])+1) + '/' + str(len(all_notes))];
    for etu in pv["full2"].keys():
        if pv["full2"][etu] not in ['NCAE', 'ENCO']:
            pv["full2"][etu] = [pv["full2"][etu], str(all_notes2.index(pv["full2"][etu])+1) + '/' + str(len(all_notes2))];

    return pv;



def GetStatistics(pv, parcours, semestre):

    # UEs
    blocs = [x for x in GetBlocsMaquette(semestre.split('_')[0], parcours) ];
    ues = [x for x in list(set(functools.reduce(operator.iconcat, GetUEsMaquette(blocs), []))) if 'PY' in x or 'LVAN' in x];
    blocs = [x for x in blocs if 'PY' in blocs];

    # Init of the output
    notes = {}; notes2 = {};
    for x in (ues+blocs+['total']):
        notes[x]  = [];
        notes2[x] = [];

    # loop over all students
    for etudiant in [x for x in pv.keys() if isinstance(x, int)]:
        # adding the notes
        for label, data_UE in pv[etudiant]['results'].items():

           # no stats needed
           key = label.split('-')[-1].strip();
           if not key in notes.keys(): continue
           if 'UE' in data_UE.keys() and data_UE['UE']=='GrosSac': continue;

           # get the notes
           mynote2 = data_UE['note2'] if ('note2' in data_UE.keys() and data_UE['note2'] not in ['U VAC', 'DIS', 'COVID', 'ENCO', 'NCAE', 'VAC']) else '';
           if 'note'  in data_UE.keys() and data_UE['note']  not in ['U VAC', 'DIS', 'COVID', 'ENCO', 'NCAE', 'VAC']:
               notes[key].append(data_UE['note']);
           if mynote2!='': notes2[key].append(mynote2);
           elif  'note'  in data_UE.keys() and data_UE['note']  not in ['U VAC', 'DIS', 'COVID', 'ENCO', 'NCAE', 'VAC']: notes2[key].append(data_UE['note']);

    # formatting
    for key in notes.keys() : notes[key]  = sorted([float(x) for x in  notes[key]],reverse=True);
    for key in notes2.keys(): notes2[key] = sorted([float(x) for x in notes2[key]],reverse=True);

    # adding the ranking information to each PV.
    for etudiant in [x for x in pv.keys() if isinstance(x, int)]:
        # adding the notes
        for label, data_UE in pv[etudiant]['results'].items():

           # no stats needed
           key = label.split('-')[-1].strip();
           if not key in notes.keys(): continue
           if 'UE' in data_UE.keys() and data_UE['UE']=='GrosSac': continue;

           # get the notes
           if 'note' in data_UE.keys() and data_UE['note'] not in ['ENCO', 'VAC', 'U VAC', 'DIS', 'COVID', 'NCAE']:
               pv[etudiant]['results'][label]['ranking']  =  str(notes[key].index(float(data_UE['note']))+1)+'/'+str(len(notes[key]));

           if 'note2' in data_UE.keys() and data_UE['note2'] not in ['ENCO', 'U VAC', 'VAC', 'DIS', 'COVID', 'NCAE']:
               pv[etudiant]['results'][label]['ranking2'] = str(notes2[key].index(float(data_UE['note2']))+1)+'/'+str(len(notes2[key]));

    # output
    return pv;




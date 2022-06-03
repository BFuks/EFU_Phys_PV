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
    pv["full"] = {};

    for etu in GetList(pv.values()):
         # initialisation etudiant
         logger.debug("etudiant = " + str(etu));
         moyenne_annee = 0.;
         nbr_semestres = len([y for y in [etu[0] in pv[x].keys() for x in pv.keys()] if y]);
         for semestre in pv.keys():
             if not etu[0] in pv[semestre].keys(): continue;
             moyenne_annee += pv[semestre][etu[0]]['results']['total']['note']/nbr_semestres;
         logger.debug("  -> " + str(moyenne_annee))
         pv["full"][str(etu[0])] = moyenne_annee;

    # Rankings
    all_notes = sorted(list(pv["full"].values()), reverse=True);
    for etu in pv["full"].keys():
        pv["full"][etu] = [pv["full"][etu], str(all_notes.index(pv["full"][etu])+1) + \
            '/' + str(len(all_notes))];

    return pv;

def GetStatistics(pv, parcours, semestre):

    # UEs
    blocs = [x for x in GetBlocsMaquette(semestre.split('_')[0], parcours) if 'PY' in x];
    ues = list(set(functools.reduce(operator.iconcat, GetUEsMaquette(blocs), [])));

    # Init of the output
    notes = {};
    for x in (ues+blocs+['total']):
        notes[x] = [];

    # loop over all students
    for etudiant in [x for x in pv.keys() if isinstance(x, int)]:
        # adding the notes
        for label, data_UE in pv[etudiant]['results'].items():

           # no stats needed
           key = label.split('-')[-1].strip();
           if not key in notes.keys(): continue
           if 'UE' in data_UE.keys() and data_UE['UE']=='GrosSac': continue;

           # get the notes
           if 'note' in data_UE.keys() and data_UE['note'] not in ['DIS', 'COVID']: notes[key].append(data_UE['note']);

    # formatting
    for key in notes.keys():
       notes[key] = sorted([float(x) for x in notes[key]],reverse=True);

    # adding the ranking information to each PV.
    for etudiant in [x for x in pv.keys() if isinstance(x, int)]:
        # adding the notes
        for label, data_UE in pv[etudiant]['results'].items():

           # no stats needed
           key = label.split('-')[-1].strip();
           if not key in notes.keys(): continue
           if 'UE' in data_UE.keys() and data_UE['UE']=='GrosSac': continue;

           # get the notes
           if 'note' in data_UE.keys() and data_UE['note'] not in ['DIS', 'COVID']:
               pv[etudiant]['results'][label]['ranking'] = str(notes[key].index(float(data_UE['note']))+1)+'/'+str(len(notes[key]));

    # output
    return pv;




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
from misc     import GetBlocsMaquette, GetUEsMaquette;
import functools, operator;
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

           # get the notes
           if 'note' in data_UE.keys() and data_UE['note'] not in ['DIS', 'COVID']:
               pv[etudiant]['results'][label]['ranking'] = str(notes[key].index(float(data_UE['note']))+1)+'/'+str(len(notes[key]));

    # output
    return pv;




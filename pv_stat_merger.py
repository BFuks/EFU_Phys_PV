##########################################################
###                                                    ###
###                  Merging PV to stats               ###
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
###                   Relevant UEs                     ###
###                                                    ###
##########################################################
Relevant = {
  'LU2PY103': 'Thermo ',
  'LU2PY104': 'MecaAv ',
  'LU2PY110': 'Math-1 ',
  'LU2PY121': 'OEM    ',
  'LU2PY123': 'Math-3 ',
  'LU2PY124': 'Relat  ',
  'LU2PY212': 'Ph.Ex-1',
  'LU2PY215': 'Ph.Ex-2',
  'LU2PY220': 'Math-2 ',
  'LU2PY222': 'Ph.Num ',
  'LU2PY403': 'Thermo ',
  'LU2PY404': 'MecaAv ',
  'LU2PY410': 'Math-1 ',
  'LU2PY421': 'OEM    ',
  'LU2PY424': 'Relat  ',
  'LU2PY520': 'Math-2 '
}
Irrelevant = ['LU2PY532'];

##########################################################
###                                                    ###
###                       Merger                       ###
###                                                    ###
##########################################################
def PVtoStats(stats, pv, session):

    # init
    results = stats;

    # loop over the students in session1
    for etudiant in pv.keys():

        # no info on the student in this pv
        if not etudiant in stats.keys(): continue;

        # Resultats
        notes =  pv[etudiant]['results'];
        results[etudiant]['notes'] = {};
        for ue, details in notes.items():
            if ue in Relevant:  results[etudiant]['notes'][Relevant[ue]]=details['note'];
            elif ue == 'total': results[etudiant]['notes'][session] = details['note'];
            elif not (ue in Irrelevant or not 'PY' in ue or 'LK' in ue):
                logger.warning('UE a inclure dans les stats ? -> ' + ue);

    # Exit
    return results;

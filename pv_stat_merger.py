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
  'LU2PY103': 'Thermo1',
  'LU2PY104': 'MecaAv ',
  'LU2PY110': 'Math-1 ',
  'LU2PY121': 'OEM-1  ',
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
  'LU2PY423': 'Math-3 ',
  'LU2PY424': 'Relat  ',
  'LU2PY520': 'Math-2 ',
  'LU2PY531': 'Astro  ',
  'LU2PY532': 'ML     ',
  'LU3PY101': 'Ph.Qu-1',
  'LU3PY103': 'Thermo2',
  'LU3PY105': 'Stage  ',
  'LU3PY111': 'Ph.Qu-2',
  'LU3PY121': 'OEM-2  ',
  'LU3PY122': 'PhExNum',
  'LU3PY124': 'PrExNum',
  'LU3PY125': 'ProjInt',
  'LU3PY205': 'Stage  ',
  'LU3PY213': 'Math-4 ',
  'LU3PY214': 'MilCont',
  'LU3PY215': 'Ph.Ex-3',
  'LU3PY231': 'Mat.Mat',
  'LU3PY232': 'Astro  ',
  'LU3PY233': 'Ph.Theo',
  'LU3PY234': 'OcAtRen',
  'LU3PY235': 'MecAnal',
  'LU3PY401': 'Ph.Qu-1',
  'LU3PY403': 'Thermo2',
  'LU3PY411': 'Ph.Qu-2',
  'LU3PY421': 'OEM-2  ',
  'LU3PY513': 'Math-4 ',
  'LU3PY514': 'MilCont',
  'LU3PY536': 'MecaApp',
  'LU3PY537': 'InfoQu '
}
Irrelevant = [
  'LU2PY041', 'LU3PYOIP', 'LU3PY012', 'LU3PY013', 'LU3PY303', 'LU3PY020', 'LU3PY001',
  'LU3PY015', 'LU3PY002', 'LU3PY021', 'LU3PY011', 'LU3PY010', 'LU3PY024', 'LU3PYSO3',
  'LU3PY004', 'LU3PY022', 'LU3PY23X', 'LU3PYSO5', 'LU3PY033', 'LU3PY034', 'LU3PY031',
  'LU3PY014'
];

##########################################################
###                                                    ###
###                       Merger                       ###
###                                                    ###
##########################################################
def PVtoStats(stats, pv, session, parcours):

    # init
    results = stats;

    # loop over the students in session1
    for etudiant in pv.keys():

        # no info on the student in this pv
        if not etudiant in stats.keys(): continue;

        # Fix for SPRINT
        if 'SPRINT' in parcours and 'MONO' in stats[etudiant]['parcours']: results[etudiant]['parcours']=stats[etudiant]['parcours'].replace('MONO','SPRINT');

        # Resultats
        keyword = 'Session1' if 'Session1' in session else 'Session2';
        notes =  pv[etudiant]['results'];
        if not 'notes ' + keyword in results[etudiant].keys(): results[etudiant]['notes ' + keyword] = {};
        for ue, details in notes.items():
            if ue in Relevant:  results[etudiant]['notes ' + keyword][ue]=details['note'];
            elif ue == 'total': results[etudiant]['notes ' + keyword][session] = details['note'];
            elif not (ue in Irrelevant or not 'PY' in ue or 'LK' in ue): logger.warning('UE a inclure dans les stats ? -> ' + ue);

    # Exit
    return results;


##########################################################
###                                                    ###
###        Big dictionary with everything in it        ###
###                                                    ###
##########################################################
def MergeStats(stats):

    # available years
    all_years = stats.keys();

    # liste d'etudiants
    known_ids = [];
    for k in stats.keys(): known_ids =  known_ids + list(stats[k].keys());

    # Combination
    new_stats = {};
    for etu in known_ids:
        new_stats[int(etu)] = {};
        for year in all_years:
            if etu in stats[year].keys():
                new_stats[int(etu)][year] = {};
                for old_key in [kk for kk in stats[year][etu].keys() if not 'notes' in kk and not kk in ['parcours','annees'] ]:
                    if not old_key in new_stats[int(etu)].keys(): new_stats[int(etu)][old_key] = stats[year][etu][old_key];
                for old_key in [kk for kk in stats[year][etu].keys() if 'notes' in kk]: new_stats[int(etu)][year][old_key] = stats[year][etu][old_key];
                if not 'parcours' in new_stats[int(etu)].keys(): new_stats[int(etu)]['parcours'] = {};
                new_stats[int(etu)]['parcours'][year]=stats[year][etu]['parcours'];

    # output
    return new_stats;


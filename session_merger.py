##########################################################
###                                                    ###
###                  Merging 2 sessions                ###
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
###                       Merger                       ###
###                                                    ###
##########################################################
def Merge(session1, session2):

    # init
    results = session1;

    # loop over the students in session1
    for etudiant in session1.keys():

        # no session 2
        if not etudiant in session2.keys(): continue;

        # loop over the UEs
        for ue in session1[etudiant]['results'].keys():

            # no second session
            if session2[etudiant]['results'][ue]['annee_val']!=None: continue;

            # saving information
            results[etudiant]['results'][ue]['note2'] = session2[etudiant]['results'][ue]['note'];

    # Exit
    return results;

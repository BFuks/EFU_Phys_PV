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

            # Safety in case an incorrect UE was recorded in session 1
            to_remove = [x for x in session1[etudiant]['results'].keys() if not x in session2[etudiant]['results'].keys()]
            to_add    = [x for x in session2[etudiant]['results'].keys() if not x in session1[etudiant]['results'].keys()]
            if len(to_remove)==1 and len(to_add)==1:
                logger.debug('Replacing info on ' + to_remove[0] + ' by info from ' + to_add[0]);
                results[etudiant]['results'][to_add[0]] = results[etudiant]['results'][to_remove[0]];
                del results[etudiant]['results'][to_remove[0]];

            # no second session
            if not ue in session2[etudiant]['results'].keys():
                logger.warning(ue + ' manquant dans le PV de ' + results[etudiant]['nom'] + ' (' + str(etudiant) + ')')
                session2[etudiant]['results'][ue] = session1[etudiant]['results'][ue]
            if session2[etudiant]['results'][ue]['annee_val']!=None: continue;

            # saving information
            results[etudiant]['results'][ue]['note2'] = session2[etudiant]['results'][ue]['note'];

    # Exit
    return results;

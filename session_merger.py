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

        # Safety in case an incorrect UE was recorded in session 1
        to_remove = [x for x in session1[etudiant]['results'].keys() if not x in session2[etudiant]['results'].keys()]
        to_add    = [x for x in session2[etudiant]['results'].keys() if not x in session1[etudiant]['results'].keys()]
        if len(to_remove)==1 and len(to_add)==1:
            logger.debug('Replacing info on ' + to_remove[0] + ' by info from ' + to_add[0]);
            results[etudiant]['results'][to_add[0]] = results[etudiant]['results'][to_remove[0]];
            del results[etudiant]['results'][to_remove[0]];

        # Specifique aux DM
        sess = [x for x in results[etudiant]['results'].keys() if 'Session2' in x];
        if len(sess)==1:
            results[etudiant]['results'][sess[0].replace('2','1')] = session2[etudiant]['results'][sess[0]];
            del results[etudiant]['results'][sess[0]];

        # loop over the UEs
        for ue in session1[etudiant]['results'].keys():
            # no second session
            if not ue in session2[etudiant]['results'].keys():
                logger.warning(ue + ' manquant dans le PV de ' + results[etudiant]['nom'] + ' (' + str(etudiant) + ')')
                session2[etudiant]['results'][ue] = session1[etudiant]['results'][ue]

            # Traitement double majeure
            if 'Session' in ue:
                results[etudiant]['results'][ue] = session2[etudiant]['results'][ue];
                continue;

            # UE standard
            if session2[etudiant]['results'][ue]['annee_val']==None and session1[etudiant]['results'][ue]['note']==session2[etudiant]['results'][ue]['note']: continue;

            # saving information
            results[etudiant]['results'][ue]['note2'] = session2[etudiant]['results'][ue]['note'];

    # Exit
    return results;

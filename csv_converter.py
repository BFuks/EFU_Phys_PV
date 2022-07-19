##########################################################
###                                                    ###
###                  CSV converter                     ###
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
###                 Core function                      ###
###                                                    ###
##########################################################
def clean(ue):
    new_ue = {};
    for key in ue.keys():
        if not 'rank' in key: new_ue[key] = ue[key];
    return new_ue;


def merge(pv):

    # Get students
    students = [ list(pv[session].keys()) for session in pv.keys() ];
    students = list(set([x for sess in students for x in sess]));

    # Create new dictionnary
    new_pv = {};
    for student in students:
        for session in pv.keys():
            if not student in pv[session].keys(): continue;
            new_individual_pv = {};
            new_individual_pv['nom'] = pv[session][student]['nom'];
            for ue in  pv[session][student]['results'].keys():
                if ue=='total': new_individual_pv[session.split('_')[0]] = clean(pv[session][student]['results'][ue]);
                else          : new_individual_pv[ue] = clean(pv[session][student]['results'][ue]);
            if student in new_pv.keys(): new_pv[student] = {**new_pv[student], **new_individual_pv};
            else                       : new_pv[student] = new_individual_pv;

    return students;


##########################################################
###                                                    ###
###                Histogram generator                 ###
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
###                    Get data                        ###
###                                                    ###
##########################################################
def GetHistoData(PVs):
    # Initialisation
    stats_session1 = {}; stats_session2 = {};

    # Loop over all semesters
    for semestre in PVs.keys():
        # Initialisation
        stats_session1[semestre.replace('_Session1','')] = []; stats_session2[semestre.replace('_Session1','')] = [];

        # Loop over all students
        for student in PVs[semestre].keys():
            for ue, result in  PVs[semestre][student]['results'].items():
                # semester average
                if ue=='total':
                    stats_session1[semestre.replace('_Session1','')].append(result['note']);
                    if 'note2' in result.keys():  stats_session2[semestre.replace('_Session1','')].append(result['note2']);
                    else:                         stats_session2[semestre.replace('_Session1','')].append(result['note']);

                # ignore
                elif ue.startswith('LK') or 'OIP' in ue or not 'PY' in ue: continue;
                elif ue.startswith('LU2PY4') or ue.startswith('LU2PY2') or ue.startswith('LU2PY0'): continue;
                elif ue.startswith('LU3PY4') or ue.startswith('LU3PY2') or ue.startswith('LU3PY0'): continue;

                # standard UE
                else:
                    if not ue in stats_session1.keys(): stats_session1[ue] = []; stats_session2[ue] = [];
                    stats_session1[ue].append(result['note']);
                    if 'note2' in result.keys():  stats_session2[ue].append(result['note2']);
                    else:                         stats_session2[ue].append(result['note']);

    # Cleaning
    for key in stats_session1.keys():
        stats_session1[key] = [x for x in stats_session1[key] if isinstance(x,float)];
        stats_session2[key] = [x for x in stats_session2[key] if isinstance(x,float)];

    # Output
    return stats_session1, stats_session2;



##########################################################
###                                                    ###
###                      Plotter                       ###
###                                                    ###
##########################################################
import matplotlib.pyplot as plt;
def MakePlot1(variable, data, title, filename):
    # Histograms
    font1 = {'family':'sans-serif', 'color':'darkred',  'size':15};
    font2 = {'family':'sans-serif', 'color':'darkblue', 'size':13};

    # canvas
    fig = plt.figure();
    ax = fig.subplots(1);
    ax.tick_params(axis='x', colors='darkblue');
    ax.tick_params(axis='y', colors='darkblue');

    # data
    maxi  = 100 if variable.startswith('L') else 20;
    ax.hist(data, bins=40, range=[0,maxi], color='teal', label='Session 1');

    # Layout
    ax.set_title(title, fontdict=font1);
    ax.legend(loc='upper right');
    plt.xlabel('Note / ' + str(maxi), fontdict=font2);
    fig.supylabel('# étudiants/étudiantes', fontdict=font2, x=0.05);

    # Saving the file
    plt.savefig(filename);
    plt.close();


def MakePlot2(variable, data, title, filename):
    # Histograms
    font1 = {'family':'sans-serif', 'color':'darkred',  'size':15};
    font2 = {'family':'sans-serif', 'color':'darkblue', 'size':13};

    # canvas
    fig = plt.figure();
    (ax1, ax2) = fig.subplots(2,1);
    ax1.tick_params(axis='x', colors='darkblue');
    ax1.tick_params(axis='y', colors='darkblue');
    ax2.tick_params(axis='x', colors='darkblue');
    ax2.tick_params(axis='y', colors='darkblue');

    # data
    maxi  = 100 if variable.startswith('L') else 20;
    ax1.hist(data[0], bins=40, range=[0,maxi], color='teal', label='Session 1');
    ax2.hist(data[1], bins=40, range=[0,maxi], color='teal', label='Session 2');

    # Layout
    ax1.set_title(title, fontdict=font1);
    ax1.legend(loc='upper right');
    ax2.legend(loc='upper right');
    plt.xlabel('Note / ' + str(maxi), fontdict=font2);
    fig.supylabel('# étudiants/étudiantes', fontdict=font2, x=0.05);

    # Saving the file
    plt.savefig(filename);
    plt.close();


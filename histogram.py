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
def GetHistoData(PVs, DMPM=False):
    # Initialisation
    stats_session1 = {}; stats_session2 = {};

    # Loop over all semesters
    for semestre in PVs.keys():
        # Initialisation
        stats_session1[semestre.replace('_Session1','')] = []; stats_session2[semestre.replace('_Session1','')] = [];

        # Loop over all students
        for student in PVs[semestre].keys():
            if DMPM:
                if len([x for x in PVs[semestre][student]['results'].keys() if x.startswith('L') and 'MA' in x])==0: continue;
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
import numpy             as np;
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

    ax.axvline(np.mean(data),   color='darkred',  linestyle='dashed', linewidth=1);
    ax.axvline(np.median(data), color='darkblue', linestyle='dotted', linewidth=1);
    ax.text(maxi/40, ax.get_ylim()[1]*.90, 'Moy. : {:.2f}'.format(np.mean(data)),   color='darkred');
    ax.text(maxi/40, ax.get_ylim()[1]*.80, 'Med. : {:.2f}'.format(np.median(data)), color='darkblue');

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
    ax1.axvline(np.mean(data[0]),   color='darkred',  linestyle='dashed', linewidth=1);
    ax1.axvline(np.median(data[0]), color='darkblue', linestyle='dotted', linewidth=1);
    ax1.text(maxi/40, ax1.get_ylim()[1]*.90, 'Moy. : {:.2f}'.format(np.mean(data[0])),   color='darkred');
    ax1.text(maxi/40, ax1.get_ylim()[1]*.80, 'Med. : {:.2f}'.format(np.median(data[0])), color='darkblue');

    ax2.axvline(np.mean(data[1]),   color='darkred',  linestyle='dashed', linewidth=1);
    ax2.axvline(np.median(data[1]), color='darkblue', linestyle='dotted', linewidth=1);
    ax2.hist(data[1], bins=40, range=[0,maxi], color='teal', label='Session 2');
    ax2.text(maxi/40, ax2.get_ylim()[1]*.90, 'Moy. : {:.2f}'.format(np.mean(data[1])),   color='darkred');
    ax2.text(maxi/40, ax2.get_ylim()[1]*.80, 'Med. : {:.2f}'.format(np.median(data[1])), color='darkblue');

    # Layout
    ax1.set_title(title, fontdict=font1);
    ax1.legend(loc='upper right');
    ax2.legend(loc='upper right');
    plt.xlabel('Note / ' + str(maxi), fontdict=font2);
    fig.supylabel('# étudiants/étudiantes', fontdict=font2, x=0.05);

    # Saving the file
    plt.savefig(filename);
    plt.close();


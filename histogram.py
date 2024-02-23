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
    all_notes      = {};

    # Loop over all semesters
    for semestre in PVs.keys():
        # Initialisation
        stats_session1[semestre.replace('_Session1','')] = []; stats_session2[semestre.replace('_Session1','')] = [];
        stats_session2[semestre.replace('_Session1','_validation')] = [];

        # Loop over all students
        for student in PVs[semestre].keys():

            # initialisation student
            if DMPM:
                if len([x for x in PVs[semestre][student]['results'].keys() if x.startswith('L') and 'MA' in x])==0: continue;
            logger.debug(str(student) +  ":" + str(PVs[semestre][student]['results']) + '\n');
            if not student in all_notes.keys(): all_notes[student] = {};

            # Compensation
            def getnote(x):
                if 'note2' in x.keys(): return x['note2'];
                else: return x['note'];

            compensated = [getnote(PVs[semestre][student]['results'][x]) for x in PVs[semestre][student]['results'].keys() if x.startswith('LU')];
            compensated = any([ x<50.for x in compensated if isinstance(x, float)]);

            for ue, result in  PVs[semestre][student]['results'].items():
                # semester average
                if ue=='total':
                    stats_session1[semestre.replace('_Session1','')].append(result['note']);
                    if 'note2' in result.keys():  stats_session2[semestre.replace('_Session1','')].append(result['note2']);
                    else:                         stats_session2[semestre.replace('_Session1','')].append(result['note']);

                    # Averages and compensation data
                    all_notes[student][semestre.replace('_Session1','')] = getnote(result);
                    all_notes[student][semestre.replace('_Session1','_compensation')] = compensated;
                    if isinstance(getnote(result), str): continue;
                    if getnote(result) < 10: stats_session2[semestre.replace('_Session1','_validation')].append(-1);
                    elif compensated       : stats_session2[semestre.replace('_Session1','_validation')].append(0);
                    else                   : stats_session2[semestre.replace('_Session1','_validation')].append(1);

                # ignore
                elif ue.startswith('LK') or 'OIP' in ue or not 'PY' in ue: continue;
#                elif ue.startswith('LU2PY4') or ue.startswith('LU2PY2') or ue.startswith('LU2PY0'): continue;
#                elif ue.startswith('LU3PY4') or ue.startswith('LU3PY2') or ue.startswith('LU3PY0'): continue;

                # standard UE
                else:
                    if not ue in stats_session1.keys(): stats_session1[ue] = []; stats_session2[ue] = [];
                    stats_session1[ue].append(result['note']);
                    if 'note2' in result.keys():  stats_session2[ue].append(result['note2']);
                    else:                         stats_session2[ue].append(result['note']);
                    all_notes[student][ue] = getnote(result);

            logger.debug(str(student) +  ":" + str(stats_session2) + '\n');
            logger.debug(str(student) +  ":" + str(all_notes) + '\n');

    # Cleaning
    for key in stats_session1.keys():
        stats_session1[key] = [x for x in stats_session1[key] if isinstance(x,float)];
        stats_session2[key] = [x for x in stats_session2[key] if isinstance(x,float)];

    # Output
    return all_notes, stats_session1, stats_session2;


def GetSuccessData(raw_data):
    # Initialisation
    processed_data = {};
    processed_data['year'] = [];
    processed_data['year_validation'] = [];

    # Loop over all students
    for student, results in raw_data.items():
        # student init
        if results == {}: continue;
        logger.debug(str(student) +":" + str(results) );

        # moyenne generale
        try: total = 0.5*sum([ results[x] for x in results.keys() if len(x)==2 ]);
        except: continue
        compensation = any([ results[x] for x in results.keys() if x.endswith('_compensation')]);

        processed_data['year'].append(total);
        if total < 10    : processed_data['year_validation'].append(-1); continue;
        elif compensation: processed_data['year_validation'].append(0);
        else             : processed_data['year_validation'].append(1);

        # ue par ue
        for ue in results.keys():
            if not ue.startswith('LU'):continue;
            if not ue in processed_data.keys(): processed_data[ue] = [];
            if not ue+'_note' in processed_data.keys(): processed_data[ue+'_note'] = [];
            if isinstance(results[ue],str):continue;
            if results[ue]>=50: processed_data[ue].append(+1);
            else              : processed_data[ue].append(-1);
            processed_data[ue+'_note'].append(results[ue]);

    # output
    return processed_data;





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
    if 'semestre' in title: logger.info('  -->  ' + title.split(';')[0] + ' : ' + str(len(data)) +  ' étudiants');
    maxi  = 100 if variable.startswith('L') and len(variable)>2 else 20;
    label = title[-10:-1] if len(variable)==2 else 'Session 1';
    ax.hist(data, bins=40, range=[0,maxi], color='teal', label=label);

    # Calculate percentiles
    ax.axvline(np.mean(data),   color='darkred',  linestyle='dashed', linewidth=1);
    ax.axvline(np.median(data), color='darkblue', linestyle='dotted', linewidth=1);
    ax.text(maxi/100, ax.get_ylim()[1]*.95, 'Moy. : {:.2f}'.format(np.mean(data)),   color='darkred');
    ax.text(maxi/100, ax.get_ylim()[1]*.90, 'Med. : {:.2f}'.format(np.median(data)), color='darkblue');

    percentiles = [10, 25, 75, 90]
    for percentile in percentiles:
        value = np.percentile(data, percentile)
        ax.axvline(value, color='darkgreen', linestyle='dashdot', linewidth=1, label=f'{percentile}% percentile')
        ax.text(value, 6, f'{percentile}%', rotation=90, verticalalignment='center')

    # Layout
    ax.set_title(title, fontdict=font1);
    plt.xlabel('Note / ' + str(maxi), fontdict=font2);
    fig.supylabel('# étudiants/étudiantes', fontdict=font2, x=0.05);
    ax.set_xlim(0, maxi)

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
    if 'semestre' in title: logger.info(title + ' : ' + str(len(data[0])) +  ' étudiants');
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



def MakePie(variable, raw_data, filename):
    # Layout
    font1  = {'family':'sans-serif', 'color':'darkred',  'size':15};
    font2  = {'family':'sans-serif', 'color':'darkblue', 'size':13};
    colors = ["Brown", "Cornsilk", "DarkSeaGreen"]

    # formatting data
    data   = np.array([raw_data.count(-1), raw_data.count(0), raw_data.count(1)]);
    labels = ['Ajournés', 'Compensés', 'Admis'];

    # Pie chart
    plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%');
    plt.title(variable, fontdict=font1);

    # Saving the file
    plt.savefig(filename);
    plt.close();


def MakePie2(variable, raw_data, filename):
    # Layout
    font1  = {'family':'sans-serif', 'color':'darkred',  'size':15};
    font2  = {'family':'sans-serif', 'color':'darkblue', 'size':11};
    colors = ["Brown", "Cornsilk", "DarkSeaGreen"]

    # formatting data
    data1 = np.array([raw_data[0].count(-1), raw_data[0].count(0), raw_data[0].count(1)]);
    data2 = np.array([raw_data[1].count(-1), raw_data[1].count(0), raw_data[1].count(1)]);
    labels = ['Ajournés', 'Compensés', 'Admis'];

    # canvas
    fig = plt.figure();
    (ax1, ax2) = fig.subplots(1,2);

    # Define a custom function for autopct
    def my_autopct1(pct):
        total = sum(data1)
        val = int(round(pct*total/100.0))
        return f'{val} ({pct:.1f}%)'
    def my_autopct2(pct):
        total = sum(data2)
        val = int(round(pct*total/100.0))
        return f'{val} ({pct:.1f}%)'

    # Pie chart
    ax1.pie(data1, wedgeprops=dict(width=0.6), colors=colors, autopct=my_autopct1);
    ax2.pie(data2, wedgeprops=dict(width=0.6), colors=colors, autopct=my_autopct2);
    ax1.text(-0.275, -0.05, "Session 1", fontdict=font2);
    ax2.text(-0.275, -0.05, "Session 2", fontdict=font2);

    # Layout again
    fig.legend(labels, loc="lower center")
    fig.suptitle(variable, fontdict=font1, y=0.85);
    fig.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)

    # Saving the file
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1);
    plt.close();


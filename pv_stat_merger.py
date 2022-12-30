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
  'LU2PY041': 'PhysAct',
  'LU2PY102': 'Stage',
  'LU2PY105': 'Stage',
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
  'LU3PY126': 'ProjNum',
  'LU3PY205': 'Stage  ',
  'LU3PY206': 'HistMec',
  'LU3PY213': 'Math-4 ',
  'LU3PY214': 'MilCont',
  'LU3PY215': 'Ph.Ex-3',
  'LU3PY231': 'Mat.Mat',
  'LU3PY232': 'Astro  ',
  'LU3PY233': 'Ph.Theo',
  'LU3PY234': 'OcAtRen',
  'LU3PY235': 'MecAnal',
  'LU3PY238': 'MesPhys',
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

        # PAD
        if 'PAD' in parcours: results[etudiant]['parcours']=stats[etudiant]['parcours'][:3]+parcours;

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



##########################################################
###                                                    ###
###        Formatting the stat dictionary -> UFR       ###
###                                                    ###
##########################################################
import datetime;
import pandas
def FormatiseStats(stats, year):
    # Init (results = notes; ACN = admin/compense/non-admis
    results = {}; ACN = {};
    results['session1'] = {}; results['session2'] = {}; results['all'] = {};
    ACN['session1']     = {}; ACN['session2']     = {}; ACN['all']     = {};

    # Loop over all data
    for etu,data in stats.items():

        # Safety
        if len( [ k for k in data.keys() if 'notes' in k and data[k]!={}] ) == 0: continue;

        # loop over all student data
        if isinstance(data['parcours'],list): parcours = data['parcours'][-1].replace('L2 ','').replace('L3 ','');
        else : parcours = data['parcours'].replace('L2 ','').replace('L3 ','');
        all_sessions = {}; all_average = 0;
        for key,info in data.items():

            # Safety
            if not 'notes' in key: continue;

            # session
            if   'Session1' in key: session = 'session1';
            elif 'Session2' in key: session = 'session2';

            # get into the marks
            average=-1;
            for ue, note in info.items():

                # Safety
                if isinstance(note,str): continue;
                if not ue.startswith('L'):
                    average = note;
                    if session=='session1': all_average = note;
                    elif session=='session2' and all_average < note: all_average=note;
                    continue;
                if not ue in results[session].keys(): results[session][ue] = {}; ACN[session][ue] = {};
                if not ue in results['all'].keys():   results['all'][ue] = {}; ACN['all'][ue] = {};
                if not parcours in results[session][ue].keys(): results[session][ue][parcours] = []; ACN[session][ue][parcours] = [0,0,0];
                if not parcours in results['all'][ue].keys():   results['all'][ue][parcours] = [];   ACN['all'][ue][parcours]   = [0,0,0];

                # Saving current session
                results[session][ue][parcours].append(note);
                if note < 50   and average >= 10: ACN[session][ue][parcours][1]+=1;
                elif note < 50 and average < 10: ACN[session][ue][parcours][2]+=1;
                else:  ACN[session][ue][parcours][0]+=1;
                if not ue in all_sessions.keys(): all_sessions[ue] = note;
                elif session=='session2' and all_sessions[ue] < note: all_sessions[ue] = note;

        # All sessions
        for ue,note in all_sessions.items():
            results['all'][ue][parcours].append(note);
            if note < 50   and all_average >= 10: ACN['all'][ue][parcours][1]+=1;
            elif note < 50 and all_average < 10: ACN['all'][ue][parcours][2]+=1;
            else:  ACN['all'][ue][parcours][0]+=1;


    # get the final dictionary
    all_ues = [];
    for data in results.values():
        for ue in data.keys(): all_ues.append(ue);
    all_ues = sorted(set(all_ues));

    data_dict = {};
    for ue in all_ues:
        data_dict[ue] = {};
        ue_sessions = [k for k in results.keys() if ue in results[k].keys()];
        for k in ue_sessions:
            total_ue = 0.; n_ue = 0; acn_ue = [0,0,0]
            if not k in data_dict[ue].keys(): data_dict[ue][k] = {};
            for parc in results[k][ue].keys():
                myparc=parc.replace('Bi-Di','MAJ');
                moyenne = round(sum(results[k][ue][parc])/len(results[k][ue][parc]),2);
                total_ue+=sum(results[k][ue][parc]);
                n_ue+=len(results[k][ue][parc]);
                if len(results[k][ue][parc])==0:continue;
                reussite = ['{:.2f}%'.format(100.*float(x)/sum(ACN[k][ue][parc])) + ' (' + str(x) +'/' + str(sum(ACN[k][ue][parc])) + ')' for x in ACN[k][ue][parc]];
                data_dict[ue][k][myparc + ' / 100'] = moyenne;
                data_dict[ue][k][myparc + ' ADM'] = reussite[0];
                data_dict[ue][k][myparc + ' CMP'] = reussite[1];
                data_dict[ue][k][myparc + ' AJO'] = reussite[2];
                acn_ue[0]+=ACN[k][ue][parc][0];
                acn_ue[1]+=ACN[k][ue][parc][1];
                acn_ue[2]+=ACN[k][ue][parc][2];
            reussite = ['{:.2f}%'.format(100.*float(x)/sum(acn_ue)) + ' (' + str(x) +'/' + str(sum(acn_ue)) + ')' for x in acn_ue];
            data_dict[ue][k]['total / 100'] = round(total_ue/n_ue,2);
            data_dict[ue][k]['total ADM'] = reussite[0];
            data_dict[ue][k]['total CMP'] = reussite[1];
            data_dict[ue][k]['total AJO'] = reussite[2];

    # Convert nest dictionaries into tuples
    reformed_dict = {}
    for outerKey, innerDict in data_dict.items():
        individual = {}
        for innerKey, value in innerDict.items():
            for mykey, myvalue in value.items():
                individual[(innerKey,mykey)] = myvalue
        reformed_dict[outerKey] = individual
    multiIndex_df = pandas.DataFrame(reformed_dict)
    effectifs = multiIndex_df.transpose()

    # ordering 
    heads1 = [x for x in list(effectifs.columns) if x[0]=='all'];
    heads2 = [x for x in list(effectifs.columns) if x[0]=='session1'];
    heads3 = [x for x in list(effectifs.columns) if x[0]=='session2'];
    heads1.sort(key=lambda y:y[1]);
    heads2.sort(key=lambda y:y[1]);
    heads3.sort(key=lambda y:y[1]);
    heads = heads1+heads2+heads3;
    effectifs = effectifs.reindex(columns=heads);

    # From dictionnary to Excel
    date = str(datetime.datetime.now().year*10000+datetime.datetime.now().month*100+datetime.datetime.now().day);
    writer = pandas.ExcelWriter('output/effectifs_'+year+'_v' + date +'.xlsx', engine='xlsxwriter');
    effectifs.to_excel(writer, sheet_name='Effectifs ' + year, index=True, header=True);
    sheet = writer.sheets['Effectifs ' + year];
    sheet.set_column(0,len(effectifs.columns),13);
    writer.close();

    # exit
    return ;


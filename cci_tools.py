##########################################################
###                                                    ###
###                    CCI tools                       ###
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
def GetCCIData(PVs):
    # Initialisation
    stats_session1 = {}; stats_session2 = {}; students = {};

    # Loop over all semesters
    for semestre in PVs.keys():
        # Initialisation
        stats_session1[semestre.replace('_Session1','')] = []; stats_session2[semestre.replace('_Session1','')] = [];
        stats_session1[semestre.replace('_Session1','_validation')] = []; stats_session2[semestre.replace('_Session1','_validation')] = [];

        # Loop over all students
        for student, results  in PVs[semestre].items():
            my_results = results['results'];

            # initialisation student
            logger.debug(str(student) +  ":" + str(my_results) + '\n');

            # Compensation
            def getnote(x, session):
                if session=='session2' and 'note2' in x.keys() : return x['note2'];
                else: return x['note'];
            compensated1 = [getnote(PVs[semestre][student]['results'][x], 'session1') for x in PVs[semestre][student]['results'].keys() if x.startswith('LU')];
            compensated1 = any([ x<50.for x in compensated1 if isinstance(x, float)]);
            compensated2 = [getnote(PVs[semestre][student]['results'][x], 'session2') for x in PVs[semestre][student]['results'].keys() if x.startswith('LU')];
            compensated2 = any([ x<50.for x in compensated2 if isinstance(x, float)]);

            # results
            nue=0;
            for k,v in my_results.items():
                if not 'LU' in k: continue;
                if not 'note2' in v.keys(): continue;
                if v['note'] == v['note2']: continue;
                nue+=1;
            result = my_results['total']; C1_str=''; C2_str='';
            stats_session1[semestre.replace('_Session1','')].append(result['note']);
            if 'note2' in result.keys():  stats_session2[semestre.replace('_Session1','')].append(result['note2']);
            else:                         stats_session2[semestre.replace('_Session1','')].append(result['note']);
            if isinstance(getnote(result, 'session1'), str): continue;
            note = getnote(result, 'session1')
            if note < 10  : stats_session1[semestre.replace('_Session1','_validation')].append(-1); C1_str='AJO';
            elif compensated1 : stats_session1[semestre.replace('_Session1','_validation')].append(0); C1_str = 'CMP';
            elif note>=10 : stats_session1[semestre.replace('_Session1','_validation')].append(1); C1_str = 'ADM'
            if isinstance(getnote(result, 'session2'), str): continue;
            note = getnote(result, 'session2')
            if note < 10  : stats_session2[semestre.replace('_Session1','_validation')].append(-1); C2_str = 'AJO';
            elif compensated2 : stats_session2[semestre.replace('_Session1','_validation')].append(0); C2_str = 'CMP';
            elif note>=10 : stats_session2[semestre.replace('_Session1','_validation')].append(1); C2_str = 'ADM';

            #debug 
            logger.debug(str(student) +  " session1 : " + str(stats_session1) + '\n');
            logger.debug(str(student) +  " session2 : " + str(stats_session2) + '\n');
            if not student in students.keys(): students[student] = {};
            if 'note2' in result.keys():
                students[student][semestre.replace('_Session1','')] = [result['note'], result['note2']];
                students[student][semestre.replace('_Session1','').replace('S','V')] = [C1_str, C2_str];
                students[student][semestre.replace('_Session1','').replace('S','N')] = [nue];
            else:
                students[student][semestre.replace('_Session1','')] = [result['note'],''];
                students[student][semestre.replace('_Session1','').replace('S','V')] = [C1_str, ''];
                students[student][semestre.replace('_Session1','').replace('S','N')] = [''];

    # Cleaning
    for key in stats_session1.keys():
        stats_session1[key] = [x for x in stats_session1[key] if isinstance(x,float) or isinstance(x, int)];
        stats_session2[key] = [x for x in stats_session2[key] if isinstance(x,float) or isinstance(x, int)];

    # Anonymous data
    data = [];
    for my_id, myresults in students.items():
      if 'S3' in myresults.keys() and 'S4' in myresults.keys():
         data.append(myresults['S3']+myresults['S4']+myresults['V3'] + myresults['V4'] + myresults['N3'] + myresults['N4']);
      elif 'S3' in myresults.keys():
         data.append(myresults['S3']+['','']+myresults['V3'] + ['',''] + myresults['N3'] + ['']);
      elif 'S4' in myresults.keys():
         data.append(['',''] + myresults['S4'] + ['',''] + myresults['V4'] + [''] + myresults['N4']);
      elif 'S5' in myresults.keys() and 'S6' in myresults.keys():
         data.append(myresults['S5']+myresults['S6']+myresults['V5'] + myresults['V6'] + myresults['N5'] + myresults['N6']);
      elif 'S5' in myresults.keys():
         data.append(myresults['S5']+['','']+myresults['V5'] + ['',''] + myresults['N5'] + ['']);
      elif 'S6' in myresults.keys():
         data.append(['',''] + myresults['S6'] + ['',''] + myresults['V6'] + [''] + myresults['N6']);

    # Output
    return stats_session1, stats_session2, data;






import pandas
def CCIdataToExcel(data, niveau, annee, prcrs_key):
    # Excelised data
    nums = ['3','4'] if niveau == 'L2' else ['5','6'];
    columns = [
      'S' + nums[0] + ' session1', 'S' + nums[0] + ' session2', 'S' + nums[1] + ' session1', 'S' + nums[1] + ' session2',
      'V' + nums[0] + ' session1', 'V' + nums[0] + ' session2', 'V' + nums[1] + ' session1', 'V' + nums[1] + ' session2',
      '#UE S' + nums[0] + ' session2', '#UE S' + nums[1] + ' session2'
    ];
    df = pandas.DataFrame(data, columns=columns);
    excel_file_path = 'cci/data_'  + prcrs_key.lower() +'_' + niveau + '_' + annee.replace('_','-') + '.xlsx';

    # Create ExcelWriter object
    with pandas.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        # Write the DataFrame to Excel
        df.to_excel(writer, sheet_name='CCI data ' + prcrs_key + '_' + niveau + '_' +annee.replace('_','-') , index=False)

        # Get the xlsxwriter workbook and worksheet objects
        workbook = writer.book;
        worksheet = writer.sheets['CCI data ' + prcrs_key +'_' + niveau + '_' + annee.replace('_','-')];

        # Adjust the column width (adjust as needed)
        for i, col in enumerate(columns):
            max_len = max(df[col].astype(str).apply(len).max(), len(col))
            worksheet.set_column(i, i, max_len + 2)



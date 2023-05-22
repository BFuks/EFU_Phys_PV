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
###                Cleaning and merging                ###
###                                                    ###
##########################################################
def clean(ue):
    new_ue = {};
    for key in ue.keys():
        if key=='note':  new_ue['session1' ]=ue[key];
        elif key=='note2': new_ue['session2' ]=ue[key];
        elif not 'rank' in key: new_ue[key] = ue[key];
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

    return new_pv;



##########################################################
###                                                    ###
###             Main function: dic -> CSV              ###
###                                                    ###
##########################################################
import pandas;
def convert(pv):

    # Convert nest dictionaries into tuples
    reformed_dict = {}
    for outerKey, innerDict in pv.items():
        individual_pv = {}
        for innerKey, value in innerDict.items():
            if innerKey=='nom':
                individual_pv[(innerKey,innerKey)]=value
            else:
                for mykey, myvalue in value.items():
                    individual_pv[(innerKey,mykey)] = myvalue
        reformed_dict[outerKey] = individual_pv

    # To Panda dataframe
    multiIndex_df = pandas.DataFrame(reformed_dict)
    multiIndex_dfT = multiIndex_df.transpose()

    # exit
    return multiIndex_dfT



def StatConverter(stats,year):
    # Convert nest dictionaries into tuples
    reformed_dict = {};
    for outerKey, innerDict in stats.items():
        individual_stats = {};
        for innerKey, value in innerDict.items():
            if not innerKey in ['notes', 'notes Session1', 'notes Session2', 'N-1', 'bourse', 'parcours', 'parcours2']: individual_stats[(innerKey,'')]=value;
            else:
                for mykey, myvalue in value.items(): 
                   if innerKey in ['N-1', 'parcours', 'bourse', 'parcours2']:
                       individual_stats[(innerKey,mykey)] = myvalue;
                       continue;
                   val = 0. if myvalue=='COVID' else myvalue;
                   if val in ['DIS', 'ENCO']: continue;
                   new_key = innerKey.replace('Session1', 'Session1 (' + year + ')').replace('Session2', 'Session2 (' + year + ')');
                   if isinstance(val, float): individual_stats[(new_key,mykey.replace('_Session1','').replace('_Session2',''))] = "{:5.2f}".format(round(val,2));
                   else:                      individual_stats[(new_key,mykey.replace('_Session1','').replace('_Session2',''))] = val;
        reformed_dict[str(outerKey)] = individual_stats;
    multiIndex_df = pandas.DataFrame(reformed_dict);

    # formatting
    if int(year.split('_')[0])<2019:
        try: multiIndex_dfT = multiIndex_df.transpose()[['nom','prenom','sexe','date_naissance', 'annee_bac', 'pays_bac', 'inscr_SU', 'parcours', 'parcours2', 'N-1', 'bourse', 'notes', 'mail']];
        except: logger.error('MISSING METHOD'); sys.exit();

    else:
        try: 
            multiIndex_dfT = multiIndex_df.transpose()[[
              'nom','prenom','sexe','date_naissance', 'annee_bac', 'pays_bac', 'inscr_SU', 'parcours', 'parcours2', 'N-1', 'bourse',
              'notes Session1 (' + year + ')', 'notes Session2 (' + year + ')', 'mail'
            ]];
        except:
            try:
                multiIndex_dfT = multiIndex_df.transpose()[[
                    'nom','prenom','sexe','date_naissance', 'annee_bac', 'pays_bac', 'inscr_SU', 'parcours', 'parcours2', 'N-1', 'bourse',
                    'notes Session1 (' + year + ')', 'mail'
                ]];
            except: multiIndex_dfT = multiIndex_df.transpose()[['nom','prenom','sexe','date_naissance', 'annee_bac', 'pays_bac', 'inscr_SU', 'parcours', 'parcours2', 'N-1', 'bourse', 'mail']];

    # output
    return multiIndex_dfT.sort_index(axis=0)



##########################################################
###                                                    ###
###            Excel sheet generation                  ###
###                                                    ###
##########################################################
def ToExcel(stats, year):
    # Ordering of the notes
    if int(year.split('_')[0])<2019:
        heads0 = [x for x in list(stats.columns) if not ('notes' in x)];
        heads = {};
        heads1 = [x for x in list(stats.columns) if ('notes') in x and len(x[1])==2];
        heads2 = [x for x in list(stats.columns) if ('notes') in x and len(x[1])==5];
        heads1.sort(key=lambda y:y[1]);
        heads2.sort(key=lambda y:y[1]);
        heads = heads1+heads2;
        heads = heads0[:-1] + heads1 + heads2 + [heads0[-1]];
        stats = stats.reindex(columns=heads);
    else:
        heads0 = [x for x in list(stats.columns) if not ('notes Session1' in x[0] or 'notes Session2' in x[0])];
        heads = {};
        for keyword in ['Session1', 'Session2']:
            heads1 = [x for x in list(stats.columns) if ('notes ' + keyword) in x[0] and (len(x[1])==2 or x[1].startswith('Session') )];
            heads2 = [x for x in list(stats.columns) if ('notes ' + keyword) in x[0] and len(x[1])==8 and not x[1].startswith('Session')];
            heads1.sort(key=lambda y:y[1]);
            heads2.sort(key=lambda y:y[1]);
            heads[keyword] = heads1+heads2;
        heads = heads0[:-1] + heads['Session1'] + heads['Session2'] + [heads0[-1]];
        stats = stats.reindex(columns=heads);

    # From dictionnary to Excel
    writer = pandas.ExcelWriter('output/stats_'+year+'.xlsx', engine='xlsxwriter');
    stats.to_excel(writer, sheet_name='Statistiques ' + year, index=True, header=True);

    # Column size and format
    ix = len(stats.columns)-1;
    sheet = writer.sheets['Statistiques ' + year];
    sheet.set_column(0,   0, 12); # ID
    sheet.set_column(1,   2, 25); # Non/prenom
    sheet.set_column(3,   3,  6); # Sexe
    sheet.set_column(4,   4, 12); # Date naissance
    sheet.set_column(5,   5,  9); # annee bac
    sheet.set_column(6,   6,  7); # pays bac
    sheet.set_column(7,   7,  8); # inscription SU
    sheet.set_column(8,   8, 13); # Parcours
    sheet.set_column(9,   9, 13); # Parcours 2
    sheet.set_column(10, 10, 10); # N-1
    sheet.set_column(11, 11, 10); # Bourse
    if ix>11: sheet.set_column(12, ix,  10);   # notes
    sheet.set_column(ix+1,ix+1,30); #mail

    #save and exit
    writer.close();
    return;

import datetime;
def ToExcelPV(pv, year, niveau, parcours):
    # Ordering of the notes
    heads0 = [x for x in list(pv.columns) if x[0][0]=='S'];
    heads1 = [x for x in list(pv.columns) if 'LK' in x[0] and not x[1] in ['bareme', 'UE', 'tag', 'validation', 'annee_val']];
    heads2 = [x for x in list(pv.columns) if not 'LK' in x[0] and x[0][0]!='S' and x[0]!='nom' and not x[1] in ['bareme', 'UE', 'tag', 'validation']];
    heads1.sort(key=lambda y:y[0]);
    heads2.sort(key=lambda y:y[0]);
    heads2 = [ (x[0],x[1].replace('note2','session2').replace('note','session1')) for x in heads2];
    heads = [('nom', 'nom')] + heads0 + heads1 + heads2;
    pv = pv.reindex(columns=heads);
    pv = pv.sort_values(by = ('nom', 'nom'))

    # From dictionnary to Excel
    date = str(datetime.datetime.now().year*10000+datetime.datetime.now().month*100+datetime.datetime.now().day);
    SheetID = 'PV ' + niveau + ' ' + parcours + ' ('+year+')';
    writer = pandas.ExcelWriter('output/' + year + '_' + niveau + '_' + parcours + '_v' + date + '.xlsx', engine='xlsxwriter');
    pv.to_excel(writer, sheet_name=SheetID, index=True, header=True);

    # Column size and format
    ix = len(pv.columns)-1;
    sheet = writer.sheets[SheetID];
    sheet.set_column(0,   0, 12); # ID
    sheet.set_column(1,   1, 35); # Non/prenom

    #save and exit
    writer.close();
    return;




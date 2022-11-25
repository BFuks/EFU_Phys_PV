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


def StatConverter(stats):
    # Convert nest dictionaries into tuples
    reformed_dict = {};
    for outerKey, innerDict in stats.items():
        individual_stats = {};
        for innerKey, value in innerDict.items():
            if not innerKey in ['notes Session1', 'notes Session2']: individual_stats[(innerKey,'')]=value;
            else:
                for mykey, myvalue in value.items(): 
                   val = 0. if myvalue=='COVID' else myvalue;
                   if val in ['DIS', 'ENCO']: continue;
                   individual_stats[(innerKey,mykey.replace('_Session1','').replace('_Session2',''))] = "{:5.2f}".format(round(val,2));
        reformed_dict[str(outerKey)] = individual_stats;

    multiIndex_df = pandas.DataFrame(reformed_dict);
    try: multiIndex_dfT = multiIndex_df.transpose()[['nom','prenom','sexe','date_naissance', 'annee_bac', 'pays_bac', 'inscr_SU', 'parcours', 'N-1', 'bourse', 'notes Session1', 'notes Session2', 'mail']];
    except:
        try: multiIndex_dfT = multiIndex_df.transpose()[['nom','prenom','sexe','date_naissance', 'annee_bac', 'pays_bac', 'inscr_SU', 'parcours', 'N-1', 'bourse', 'notes Session1', 'mail']];
        except: multiIndex_dfT = multiIndex_df.transpose()[['nom','prenom','sexe','date_naissance', 'annee_bac', 'pays_bac', 'inscr_SU', 'parcours', 'N-1', 'bourse', 'mail']];
    return multiIndex_dfT



##########################################################
###                                                    ###
###            Excel sheet generation                  ###
###                                                    ###
##########################################################
def ToExcel(stats, year):
    # Ordering of the notes
    heads0 = [x for x in list(stats.columns) if not ('notes Session1' in x or 'notes Session2' in x)];
    heads = {};
    for keyword in ['Session1', 'Session2']:
        heads1 = [x for x in list(stats.columns) if ('notes ' + keyword) in x and len(x[1])==2];
        heads2 = [x for x in list(stats.columns) if ('notes ' + keyword) in x and len(x[1])==8];
        heads1.sort(key=lambda y:y[1]);
        heads2.sort(key=lambda y:y[1]);
        heads[keyword] = heads1+heads2;
    heads = heads0[:-1] + heads['Session1'] + heads['Session2'] + [heads0[-1]];
    stats = stats.reindex(columns=heads);

    #print(stats);
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
    sheet.set_column(9,   9, 10); # N-1
    sheet.set_column(10, 10,  6); # Boruse
    if ix>10: sheet.set_column(11, ix,  8);   # notes
    sheet.set_column(ix+1,ix+1,30); #mail

    #save and exit
    writer.save();
    return;


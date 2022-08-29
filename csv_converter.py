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
            if innerKey!='notes': individual_stats[(innerKey,'')]=value;
            else:
                for mykey, myvalue in value.items(): individual_stats[(innerKey,mykey.replace('_Session1','').replace('_Session2',''))] = "{:5.2f}".format(round(myvalue,2));
        reformed_dict[str(outerKey)] = individual_stats;

    multiIndex_df = pandas.DataFrame(reformed_dict);
    multiIndex_dfT = multiIndex_df.transpose()[['nom','prenom','sexe','date_naissance', 'annees', 'parcours', 'bourse', 'notes', 'mail']];
    return multiIndex_dfT



##########################################################
###                                                    ###
###            Excel sheet generation                  ###
###                                                    ###
##########################################################
def ToExcel(stats):

    # Ordering of the notes
    heads0 = [x for x in list(stats.columns) if not 'notes' in x];
    heads1 = [x for x in list(stats.columns) if 'notes' in x and len(x[1])==2];
    heads2 = [x for x in list(stats.columns) if 'notes' in x and len(x[1])==7];
    heads1.sort(key=lambda y:y[1]);
    heads2.sort(key=lambda y:y[1]);
    heads = heads0[:-1]+heads1+heads2+[heads0[-1]]
    stats = stats.reindex(columns=heads);

    # print(stats);
    # From dictionnary to Excel
    writer = pandas.ExcelWriter('output/stats_2021_2022.xlsx', engine='xlsxwriter');
    stats.to_excel(writer, sheet_name='Statistiques 2021_2022', index=True, header=True);

    # Column size and format
    ix = 19;
    sheet = writer.sheets['Statistiques 2021_2022'];
    sheet.set_column(0, 0, 12);
    sheet.set_column(1, 2, 25);
    sheet.set_column(3, 3,  6);
    sheet.set_column(4, 4, 12);
    sheet.set_column(5, 5, 11);
    sheet.set_column(6, 6, 13);
    sheet.set_column(7, 7,  6);
    sheet.set_column(8,ix,  7);
    sheet.set_column(ix+1,ix+1,30);

    # Row and column format
    row_format = writer.book.add_format({'bold': 0, 'align': 'center', 'valign': 'vcenter', 'border': 1});
    sheet.set_default_row(17);
    sheet.set_row(0,len(stats)+2,row_format);

    # Header format
    merge_format = writer.book.add_format({'bold': 1, 'align': 'center', 'valign': 'vcenter', 'border': 2, 'fg_color': 'yellow'});
    sheet.set_row(0,3,merge_format);
    names = ['ID', 'Nom','Prenom','Sexe','DateNaissance', 'Annees', 'Parcours', 'Bourse']
    for name in names: sheet.merge_range(0, names.index(name), 1, names.index(name), name, merge_format);
    sheet.set_row(0,20);
    sheet.set_row(1,20);
    sheet.merge_range(0,  8, 0, ix, 'Notes', merge_format);
    sheet.merge_range(0, ix+1, 1, ix+1, 'E-mail', merge_format);

    # Hide row 3
    sheet.set_row(2, None, None, {'hidden': True})

    #save and exit
    writer.save();
    return;


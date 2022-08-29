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
    multiIndex_df = pandas.DataFrame(stats);
    multiIndex_dfT = multiIndex_df.transpose()[['nom','prenom','sexe','date_naissance', 'annees', 'parcours', 'bourse', 'mail']];
    return multiIndex_dfT



##########################################################
###                                                    ###
###            Excel sheet generation                  ###
###                                                    ###
##########################################################
def ToExcel(stats):

    # From dictionnary to Excel
    writer = pandas.ExcelWriter('output/stats_2021_2022.xlsx');
    stats.to_excel(writer, sheet_name='Statistiques 2021_2022', index=True, header=True);

    # Column size
    writer.sheets['Statistiques 2021_2022'].column_dimensions['A'].width = 12;
    writer.sheets['Statistiques 2021_2022'].column_dimensions['B'].width = 25;
    writer.sheets['Statistiques 2021_2022'].column_dimensions['C'].width = 25;
    writer.sheets['Statistiques 2021_2022'].column_dimensions['D'].width =  6;
    writer.sheets['Statistiques 2021_2022'].column_dimensions['E'].width = 12;
    writer.sheets['Statistiques 2021_2022'].column_dimensions['F'].width = 11;
    writer.sheets['Statistiques 2021_2022'].column_dimensions['G'].width = 13;
    writer.sheets['Statistiques 2021_2022'].column_dimensions['H'].width =  6;
    writer.sheets['Statistiques 2021_2022'].column_dimensions['I'].width = 25;

    #save and exit
    writer.save();
    return;


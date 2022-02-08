##########################################################
###                                                    ###
###                    XML Reader                      ###
###                                                    ###
##########################################################
import xml.etree.ElementTree as ET
from misc import Bye

##########################################################
###                                                    ###
###                       Logger                       ###
###                                                    ###
##########################################################
import logging;
logger = logging.getLogger('mylogger');


##########################################################
###                                                    ###
###                Import du fichier XML               ###
###                                                    ###
##########################################################
import os
def GetXML(niveau, annee, semestre, parcours):

    # reading
    data = open(os.path.join(os.getcwd(),'data', niveau+'_'+annee+'_'+semestre+'_'+parcours+'.dat'));
    tree = ET.parse(data).getroot();
    data.close();

    # output
    return tree;


##########################################################
###                                                    ###
###      Decodage de l'information XML  (wrapper)      ###
###                                                    ###
##########################################################
from apogee_config import apogee_structure        as Struct;
from apogee_config import apogee_pvind_structure  as PVStruct;
from apogee_config import apogee_resume_structure as ResumeStruct;
def DecodeXML(xml_data, structure=Struct):
    # Initialisation
    decoded_data = {};

    # Navigation dans l'arbre XML
    for child in xml_data:

        # Elements de structure generaux
        if 'irrelevant' in structure.keys() and child.tag in structure['irrelevant']:
            continue;
        elif not child.tag in structure.keys():
            logger.error("Element d'Apogee inconnu (ajouter dans apogee_structure) : " + child.tag)
            Bye();
        elif child.tag in structure.keys() and structure[child.tag] != {}:
            decoded_data.update(DecodeXML(child, structure[child.tag]));
            continue;

        # PV individuel pour un etudiant
        elif child.tag in ['G_IND']:
            pv_individuel = DecodeBloc(child, PVStruct);
            # cleaning
            id_etudiant = int(pv_individuel['id'].split(':')[-1].strip());
            del pv_individuel['id'];
            if id_etudiant in decoded_data.keys():
                old=len([ k for k in decoded_data[id_etudiant]['results'].keys() if 'note' in decoded_data[id_etudiant]['results'][k]]);
                new=len([ k for k in pv_individuel['results'].keys() if 'note' in pv_individuel['results'][k]]);
                if new>=old: decoded_data[id_etudiant] = pv_individuel;
            else:
                decoded_data[id_etudiant] = pv_individuel;
            continue;

        # resume du PV
        elif child.tag in ['G_TOT']:
            resume = DecodeBloc(child, ResumeStruct);
            decoded_data['resume'] = resume;
            continue;

    #output
    return decoded_data;

##########################################################
###                                                    ###
###          Decodage d'un bloc d'information          ###
###                                                    ###
##########################################################
from apogee_config import apogee_blocpv_structure  as PVindStruct;
def DecodeBloc(xml_data, structure):
    # init
    bloc_individuel = {};

    # decoding the data
    for child in xml_data:
        # elements inutiles
        if 'irrelevant' in structure.keys() and child.tag in structure['irrelevant']:
            continue;

        # element a sauvegarder
        if child.tag in structure['relevant'].keys():
            if child.tag == 'LIST_G_TPW':
                bloc_individuel[structure['relevant'][child.tag]] = DecodePV(child,PVindStruct);
            else:
                bloc_individuel[structure['relevant'][child.tag]] = child.text;
            continue;

        # safety check
        logger.error('Tag XML inconnu (au sein d\'un bloc XML) : ' + child.tag);
        Bye();

    # output
    return bloc_individuel;


##########################################################
###                                                    ###
###         Decodage du PV individuel lui-meme         ###
###                                                    ###
##########################################################
from apogee_config import apogee_notes_structure  as NotesStruct;
def DecodePV(xml_data,structure):
    # init
    resultats = {};

    # run over the different sub-blocs
    for child in xml_data:

        # Bloc interessant
        if child.tag == xml_data.tag.replace('LIST_',''):
            bloc = {};
            for grandchild in child:

                # information inutile
                if grandchild.tag in structure['irrelevant']:
                    continue

                # information a sauvegarder
                if grandchild.tag in structure['relevant'].keys():
                    if grandchild.tag == 'LIST_G_TPW_IND':
                        if structure['relevant'][grandchild.tag] in bloc.keys():
                            bloc[structure['relevant'][grandchild.tag]].update(DecodePV(grandchild,NotesStruct));
                        else:
                            bloc[structure['relevant'][grandchild.tag]] = DecodePV(grandchild,NotesStruct);
                    else:
                        bloc[structure['relevant'][grandchild.tag]] = grandchild.text;
                    continue;

                # safety check
                logger.error('Tag XML inconnu (au sein d\'un bloc XML) : ' + grandchild.tag);
                Bye();

            # cleaning
            if 'bareme' in bloc.keys():
                bloc['bareme'] = bloc['bareme'].split('/')[-1].strip();
            if 'notes' in bloc.keys():
                bloc.update(bloc['notes']);
                del bloc['notes'];
            if 'ABI' in bloc.keys() and bloc['ABI'] in ['VAC', 'DIS', 'ABJ']: bloc['validation'] = bloc['ABI']
            if 'ABI' in bloc.keys() and bloc['ABI'] in [None, 'VAC', 'DIS', 'ABJ']: del bloc['ABI'];
            elif 'ABI' in bloc.keys(): bloc['note']=0.;

            # Bloc ID
            if 'id0' in bloc.keys() and 'id1' in bloc.keys():
               bloc['id'] = (bloc['id0']+bloc['id1']).replace('00','00-total');
               if bloc['code'] != None:
                   bloc['id']=bloc['id']+'-'+bloc['code'];
               for x in ['id0', 'id1', 'code']: del bloc[x];

            # Sauvegarde des donnees
            if 'id' in bloc.keys():
                resultats[bloc['id']] = bloc;
                del resultats[bloc['id']]['id'];
            else:
                resultats.update(bloc);
            continue;

        # safety check
        logger.error('Tag XML inconnu (au sein d\'un bloc de PV) : ' + child.tag);
        Bye();

    # output
    return resultats;


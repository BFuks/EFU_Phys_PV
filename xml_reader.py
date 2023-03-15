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

def GetXMLStats(annee):

    # reading
    data = open(os.path.join(os.getcwd(),'data', 'stats_'+annee+'.dat'), encoding='ISO-8859-1');
    for line in data: tree = ET.parse(data).getroot();
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



from apogee_config import apogee_stats, apogee_bloc_stats;
def DecodeXMLStats(xml_data, structure=apogee_stats):
    # Initialisation
    decoded_data = {};

    # Navigation dans l'arbre XML
    for child in xml_data:

        # Elements de structure generaux
        if 'irrelevant' in structure.keys() and child.tag in structure['irrelevant']: continue;
        elif not child.tag in structure.keys():
            logger.error("Element Apogee inconnu (a ajouter dans apogee_stats) : " + child.tag)
            Bye();
        elif child.tag in structure.keys() and structure[child.tag] != {}:
            decoded_data.update(DecodeXMLStats(child, structure[child.tag]));
            continue;

        # stats individuelles pour un etudiant
        elif child.tag in ['G_COD_ETU']: stats_individuel = DecodeBlocStats(child, apogee_bloc_stats);

        # Boursier ?
        stats_individuel['bourse']='non' if stats_individuel['bourse']==None else 'oui';

        # Parcours
        if   stats_individuel['parcours'] == 'L2PY01(20)': stats_individuel['parcours'] = 'L2 MONO';
        elif stats_individuel['parcours'] == 'L3PY01(21)': stats_individuel['parcours'] = 'L3 MONO';
        elif stats_individuel['parcours'] == 'V2PY01(20)': stats_individuel['parcours'] = 'L2 Bi-Di';
        elif stats_individuel['parcours'] == 'V3PY01(21)': stats_individuel['parcours'] = 'L3 Bi-Di';
        elif stats_individuel['parcours'] == 'Q2PYDM(21)': stats_individuel['parcours'] = 'L2 DM';
        elif stats_individuel['parcours'] == 'Q3PYDM(21)': stats_individuel['parcours'] = 'L3 DM';
        elif stats_individuel['parcours'] in ['Q2PYDK(20)', 'Q2PHSX(19)']: stats_individuel['parcours'] = 'L2 DK';
        elif stats_individuel['parcours'] in ['Q3PYDK(21)', 'Q3PHSX(19)']: stats_individuel['parcours'] = 'L3 DK';
        elif stats_individuel['parcours'] == 'L2PY51(20)': stats_individuel['parcours'] = 'L2 CMI';
        elif stats_individuel['parcours'] == 'L3PY51(21)': stats_individuel['parcours'] = 'L3 CMI';
        elif stats_individuel['parcours'] == 'P3PY01(19)': stats_individuel['parcours'] = 'L3 LIOVIS';
        elif stats_individuel['parcours'] == 'W1SX03(19)': stats_individuel['parcours'] = 'UE isolee';
        else: logger.warning('VET inconnue : ' + stats_individuel['parcours'] + ' (' + stats_individuel['nom'] + ')');

        # Numero etudiant  = key du dico
        id_su = int(stats_individuel['id_su']);
        del stats_individuel['id_su'];

        # Etudiant avec deux inscriptions -> fusion des blocs
        if id_su in decoded_data.keys():
          for k,v in stats_individuel.items():
              if v==decoded_data[id_su][k]: continue;
              decoded_data[id_su][k] = [ decoded_data[id_su][k], v ];

              # cleaning (UE isolees != parcours
              if k=='parcours':
                  decoded_data[id_su][k] = [x for x in decoded_data[id_su][k] if x !='UE isolee'];
                  if any([ 'DM' in x for x in decoded_data[id_su][k] ]) and any([ 'DK' in x for x in decoded_data[id_su][k] ]): decoded_data[id_su][k] = [x for x in decoded_data[id_su][k] if 'DK' in x];
                  if len(decoded_data[id_su][k])==1: decoded_data[id_su][k] = decoded_data[id_su][k][0];

              # cleaning : etre boursier n'est pas une superposition
              if k=='bourse':
                  decoded_data[id_su][k]='oui'if 'oui' in decoded_data[id_su][k] else 'non';

        # Cas standard
        else: decoded_data[id_su] = stats_individuel;

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



def DecodeBlocStats(xml_data, structure):
    # init
    bloc_individuel = {};

    # decoding the data
    for child in xml_data:
        # elements inutiles
        if child.tag in structure['irrelevant']: continue;

        # element a sauvegarder
        elif child.tag in structure['relevant'].keys():
            # name defined through NOM_USUEL -> safety
            if child.tag=='NOM' and 'nom' in bloc_individuel.keys() and not bloc_individuel['nom']!=None: continue;
            if child.tag=='NOM_USUEL' and child.text==None: continue;
            #  general case -> saving information
            bloc_individuel[structure['relevant'][child.tag]] = child.text;

        # safety check
        else:
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
            if 'ABI' in bloc.keys() and bloc['ABI'] in ['U VAC', 'VAC', 'DIS', 'ABJ', 'ENCO']: bloc['validation'] = bloc['ABI']
            if 'ABI' in bloc.keys() and bloc['ABI'] in [None, 'U VAC', 'VAC', 'DIS', 'ABJ', 'ENCO']: del bloc['ABI'];
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



##########################################################
###                                                    ###
###                 Patch pour le S6 DM                ###
###                                                    ###
##########################################################
def Patch_DMS6(pv_in, pv_out):
    # Initialisation
    PV_result = pv_out;

    # Updating the pv_out if necessary
    for key in pv_in.keys():
        # Basic info
        if key=='resume': continue;

        # New info to store
        if not key in PV_result.keys(): PV_result[key] = pv_in[key];

        # Existing entry to maybe store
        else:
            old_keys = [x for x in PV_result[key]['results'].keys() if 'note' in PV_result[key]['results'][x].keys()];
            new_keys = [x for x in pv_in[key]['results'].keys() if 'note' in pv_in[key]['results'][x].keys()];
            if len(new_keys)>len(old_keys): PV_result[key] = pv_in[key];

    # Output
    return PV_result;


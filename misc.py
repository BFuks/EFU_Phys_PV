##########################################################
###                                                    ###
###                Boîte à outils                      ###
###                                                    ###
###                Date: 15/01/2026                    ###
###                                                    ###
##########################################################
import re
from merging_tools import MergeSessions, MergeSemesters
from pathlib import Path
from pv_checker import SanityCheck
from stat_tools import AddRankings, MoyenneAnnuelle, BlocsDisciplinaires
from xml_reader import Parse_xml_to_Dict

##########################################################
###                                                    ###
###              Liste des PV disponibles              ###
###                                                    ###
##########################################################
file_pattern = re.compile( r'(?P<niveau>L\d)_'
    r'(?P<annee>\d{4}_\d{4})_'
    r'(?P<semestre>S\d)_'
    r'Session(?P<session>\d)_'
    r'(?P<parcours>[A-Z0-9]+)\.dat'
)

def scan_pv_files(base):
    # Initialisation
    data = {}

    # Boucle sur la liste des fichiers disponibles
    for path in Path(base).glob("*.dat"):
        m = file_pattern.match(path.name)
        if not m: continue

        # Données PV
        d = m.groupdict()
        annee    = d['annee'].replace('_', '-')
        niveau   = d['niveau']
        parcours = d['parcours']
        semestre = d['semestre']
        session  = f"Session{d['session']}"

        # Safety: script pas testé sur les PVs antérieurs à 2024
        if int(annee.split('-')[0])<2024: continue

        # Sauvegarde
        data.setdefault(annee,{}).setdefault(niveau,{}).setdefault(parcours,{}).setdefault(semestre,{})[session] = path

    # output
    return data


##########################################################
###                                                    ###
###                    Choix du PV                     ###
###                                                    ###
##########################################################
def choose(prompt, options):
    # Safety Liste vide
    if not options: raise ValueError("Aucune option disponible")
    options = sorted(options, reverse=False)

    # Choix de l'utilisateur
    while True:
        print(f"\n{prompt}")
        for i, opt in enumerate(options, 1): print(f"  {i}) {opt}")
        choice = input("> ").strip()

        # Entrée invalide
        if not choice or not choice.isdigit() or not (0<int(choice)<=len(options)):
            print(f"Entrée invalide : veuillez entrer un numéro entre 1 et {len(options)}")
            continue

        # OK
        break

    # Output
    return options[int(choice)-1]


##########################################################
###                                                    ###
###          Fonction principale: choix du PV          ###
###                                                    ###
##########################################################
def build_pv(liste_pvs, logger=None, newmaquette=False, dm=False):
    # Initialsation
    data = {}
    for sem, sem_data in sorted(liste_pvs.items()):
        logger.info(f"Traitement {sem}...")
        data[sem] = load_semester(sem_data, logger=logger, newmaquette=newmaquette)

    logger.info("Fusion des semestres...")
    data = MergeSemesters(data, logger=logger)

    logger.info("Calcul de la moyenne annuelle...")
    MoyenneAnnuelle(data, logger=logger, newmaquette=newmaquette)

    if dm and not newmaquette:
        logger.info("Calcul des Blocs disciplinaires...")
        BlocsDisciplinaires(data, logger=logger)

    logger.info("Calcul des classements...")
    AddRankings(data, logger=logger)


    return data


##########################################################
###                                                    ###
###               Traitement fichier PV                ###
###                                                    ###
##########################################################
def load_semester(sem_data, logger=None, newmaquette=False):
    # Safety
    if 'Session1' not in sem_data: raise ValueError("Session1 absente, impossible de construire le PV")

    # Lecture session 1
    logger.info("  -> Session 1...")
    dic_sess1 = Parse_xml_to_Dict(sem_data['Session1'], logger=logger)
    SanityCheck(dic_sess1['students'], logger=logger, newmaquette=newmaquette)

    # Lecture session 2
    if 'Session2' in sem_data:
        logger.info("  -> Session 2...")
        dic_sess2 = Parse_xml_to_Dict(sem_data['Session2'], logger=logger)
        SanityCheck(dic_sess2['students'], logger=logger)
        return MergeSessions(dic_sess1, dic_sess2, logger=logger)

    # Pas de session 2 => formatage
    return MergeSessions(dic_sess1, dic_sess1, logger=logger)


## ##########################################################
## ###                                                    ###
## ###    Liste des annees disponibles pour les stats     ###
## ###                                                    ###
## ##########################################################
## def GetStatList():
##     # Init
##     dico = [];
## 
##     # liste des ficheirs disponibles
##     for myfile in glob.glob(os.path.join(os.getcwd(), 'data/stat*')):
## 
##         # infos generales sur le PV
##         stat_data = myfile.split('/')[-1].split('.')[0].split('_');
##         year     = stat_data[-2]+'_'+stat_data[-1];
## 
##         # sauvegarde des infos
##         dico.append(year);
## 
##     # Output
##     return dico;
## 
## 
## ##########################################################
## ###                                                    ###
## ###                List flattening                     ###
## ###                                                    ###
## ##########################################################
## from collections.abc import Iterable
## def flatten(l):
##     for el in l:
##         if isinstance(el, Iterable) and not isinstance(el, (str, bytes)): yield from flatten(el)
##         else: yield el
## 
## 
## 
## ##########################################################
## ###                                                    ###
## ###         Get information from the structure         ###
## ###                                                    ###
## ##########################################################
## from maquette import Maquette, UEs;
## def GetBlocsMaquette(semestre,parcours):
##     return sorted([x for x in Maquette.keys() if parcours in Maquette[x]['parcours'] and semestre == Maquette[x]['semestre']]);
## 
## import itertools;
## def GetUEsMaquette(blocs_maquette):
##     length = len( [Maquette[x]['UE'] for x in blocs_maquette ] );
##     UEs_maquette = [Maquette[x]['UE'] for x in blocs_maquette][length-1];
##     while length>1:
##         UEs_maquette = [sorted(list(flatten(x))) for  x in itertools.product(UEs_maquette, [Maquette[x]['UE'] for x in blocs_maquette][length-2])];
##         length-=1;
##     return UEs_maquette;
## 
## 
## 


import getopt, sys, time
from colored_log import Init
from misc import scan_pv_files, choose, build_pv
from stat_tools import reformat_dict, add_info_presences, merge_ue_dicts
from pathlib import Path
from plots import correlations_reussite_presence, save_scatters

# Initialisation et options
logger = Init(level=20)
logger.info('\nDebut du run le ' + time.asctime(time.localtime(time.time())))
try: optlist, arglist = getopt.getopt(sys.argv[1:], "d", ["debug"]);
except getopt.GetoptError as err:
    logger.error(str(err));
    sys.exit()
for o,a in optlist:
    if o in ["-d", "--debug"]: logger.setLevel(10);

# Initialisation et liste des PV
base = Path("data")
catalogue = scan_pv_files(base)

# Choix du PV
annee    = choose("Choisir l'année", catalogue.keys())
logger.info(f"PV sélectionné : {annee}")

# Construction des résultats
ue_data = {}
for niveau in ['L2', 'L3']:
    newmaquette = True if int(annee.split('-')[0])>2024 and niveau=='L2' else False
    for parcours in ['SPRINT', 'MONO', 'MAJ', 'MAJPM', 'CMI', 'DK', 'DM']:
        if parcours not in catalogue[annee][niveau]: continue
        ue_new = build_pv(catalogue[annee][niveau][parcours], logger=logger, newmaquette=newmaquette, dm=(parcours in ('DM', 'DK')))
        ue_new = reformat_dict(ue_new, parcours)
        ue_new = add_info_presences(ue_new, annee.replace('-','_'), logger=logger)
        merge_ue_dicts(ue_data, ue_new)


# Figures
correls = correlations_reussite_presence(ue_data,logger=logger)
save_scatters(correls, annee)

# Bye bye
logger.info('Fin du run le ' + time.asctime(time.localtime(time.time())))


import getopt, sys, time
from colored_log import Init
from misc import scan_pv_files, choose, build_pv
from pv_writer import generate_pv_pdf
from stat_tools import generate_stats
from plots import pies, histos, save_plots

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
base = "/Users/fuks/Documents/sdrive/LicencePhysique/Python_Tools/data"
catalogue = scan_pv_files(base)

# Choix du PV
annee    = choose("Choisir l'année", catalogue.keys())
niveau   = choose("Choisir le niveau", catalogue[annee].keys())
parcours = choose("Choisir le parcours", catalogue[annee][niveau].keys())
logger.info(f"PV sélectionné : {annee} | {niveau} | {parcours}")

# Nouvelle maquette
newmaquette = True if int(annee.split('-')[0])>2024 and niveau=='L2' else False

# Construction du dictionnaire
data = build_pv(catalogue[annee][niveau][parcours], logger=logger, newmaquette=newmaquette, dm=(parcours in ('DM', 'DK')))

# Génération du fichier PDF
generate_pv_pdf(data, annee, niveau, parcours, logger=logger, filtre='')

# Génération des données 'stats' et production des histos et tartes
stat_data = generate_stats(data, logger=logger, newmaquette=newmaquette, filtre='')
pies  = pies(stat_data, title = niveau + ' (' + annee + ') - ' + parcours)
hists = histos(stat_data, title = niveau + ' (' + annee + ') - ' + parcours)
save_plots(pies, hists, annee, niveau, parcours)

# Bye bye
logger.info('Fin du run le ' + time.asctime(time.localtime(time.time())))


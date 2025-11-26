import getopt, sys;
from colored_log import Init
from xml_reader import parse_xml_to_dict
from pv_checker import SanityCheck
import pprint

# Initialisation et options
logger = Init(level=20)
try: optlist, arglist = getopt.getopt(sys.argv[1:], "d", ["debug"]);
except getopt.GetoptError as err:
    logger.error(str(err));
    sys.exit()
for o,a in optlist:
    if o in ["-d", "--debug"]: logger.setLevel(10);

# Reading the PV
data = parse_xml_to_dict("/Users/fuks/Documents/sdrive/LicencePhysique/Python_Tools/data/L3_2025_2026_S5_Session1_MONO.dat", logger=logger)
data = parse_xml_to_dict("/Users/fuks/Documents/sdrive/LicencePhysique/Python_Tools/data/L3_2024_2025_S5_Session1_SPRINT.dat", logger=logger)
# pprint.pprint(data)

# Checking the PV
SanityCheck(data['students'], logger=logger)


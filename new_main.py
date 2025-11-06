from colored_log import Init
from xml_reader import parse_xml_to_dict
import pprint

logger = Init(level=10)
data = parse_xml_to_dict("/Users/fuks/Documents/sdrive/LicencePhysique/Python_Tools/data/L3_2025_2026_S5_Session1_MONO.dat", logger=logger)
data = parse_xml_to_dict("/Users/fuks/Documents/sdrive/LicencePhysique/Python_Tools/data/L3_2024_2025_S5_Session1_SPRINT.dat", logger=logger)
pprint.pprint(data)


##########################################################
###                                                    ###
###                New XML Reader                      ###
###                                                    ###
###                Date: 16/02/2026                    ###
###                                                    ###
##########################################################
import re
import sys
import xml.etree.ElementTree as ET


##########################################################
###                                                    ###
###                Import du fichier XML               ###
###                                                    ###
###        Conversion en un dictionnaire Python        ###
###                                                    ###
##########################################################
def Parse_xml_to_Dict(filename, logger=None):
    # Read the XML
    tree = ET.parse(filename)
    root = tree.getroot()

    # Header : determination de la VET
    header = root.find(".//LIST_G_ENTETE/G_ENTETE")

    # Recehrche du code VET alphanumérique à 8 caractères
    code_pattern = re.compile(r"\b([A-Z0-9]{6,8})\b")
    match_def = code_pattern.search(header.findtext("LIC_LIB_PRV_DEF", ""))
    match_prov = code_pattern.search(header.findtext("LIC_LIB_PRV_PROV", ""))
    VET_def = match_def.group(1) if match_def else None
    VET_prov = match_prov.group(1) if match_prov else None
    if not VET_def or not VET_prov or VET_def != VET_prov:
        logger.error("Impossibilité de déterminer le code de la VET dans le header du fichier " + 
           str(filename).split('/')[-1])
        sys.exit()


    # Boucle sur les étudiants
    students = {}
    for g_ind in root.findall(".//LIST_G_TAB/G_TAB/LIST_G_IND/G_IND"):

        # numero étudiant
        student_id = re.search(r"\d+", g_ind.findtext(".//COD_ETU_TPW_IND", ""))
        student_id = student_id.group(0)
        logger.debug(f"Processing student {student_id}")

        # données génerales
        student_data = {}

        for child in g_ind:
            tag = child.tag
            text = (child.text or "").strip()
            logger.debug(f"  ** processing tag {tag} with value {text}")

            # info inutile
            if not text or tag.startswith("COL"): continue
            if tag in ("NAI_ETU_LI1_TPW_IND", "NAI_ETU_LI2_TPW_IND", "COD_ETU_TPW_IND"): continue

            # nom
            if tag == "LIB_NOM_PAT_IND_TPW_IND": student_data["nom"] = text
            else: student_data[tag] = text

            # PV lui-même
            PV = {}
            for g_tpw in g_ind.findall("LIST_G_TPW/G_TPW"):
                element = {}

                # code UE/bloc ou nom de l'élément si non disponible
                code = g_tpw.findtext("COD_OBJ_MNP_TPW", "").strip()
                if not code: code = g_tpw.findtext("LIB_CMT_TPW", "").strip()
                logger.debug(f"  ** processing code '{code}'")

                # Obtention des données des children elements
                children_data = {}
                for c in g_tpw:
                    if c.tag in ["COD_OBJ_MNP_TPW", "LIST_G_TPW_IND"]: continue
                    val = (c.text or "").strip()
                    if val != "": children_data[c.tag] = val

                # Data dans G_TPW_IND
                list_g_tpw_ind = g_tpw.find("LIST_G_TPW_IND")
                g_tpw_ind = g_tpw.find("LIST_G_TPW_IND/G_TPW_IND")
                element['active'] = False if list_g_tpw_ind is not None and g_tpw_ind is None else True

                if g_tpw_ind:
                    for i_child in g_tpw_ind:
                        itag = i_child.tag
                        itext = (i_child.text or "").strip()
                        logger.debug(f"    ** processing tag '{itag}' with value '{itext}'")
                        if itext!="": children_data[itag] = itext
                elif code.startswith('LU'): continue

                # Formatage
                # 1) Bareme 
                bareme = children_data.get("BAR_SAI_TPW")
                if bareme: match = re.search(r"/\s*(\d+)", bareme)
                element["bareme"] = int(match.group(1)) if match else None

                # 2) resultat
                resu_values = [v.replace('U ','') for k, v in children_data.items() if "COD_TRE" in k]
                if len(set(resu_values)) > 1:
                    logger.warning(f"Multiples valeurs du résultat pour l'étudiant {student_data['nom']} ({student_id}) dans l'élément {code}: {resu_values}")
                element["resultat"] = resu_values[0] if resu_values else None

                # 3) note
                pattern = re.compile(r'^(?=.*NOT)(?=.*TPW)(?!.*ETA)(?!.*MEI)(?!.*CF)')
                note_values = []
                for k, v in children_data.items():
                    if pattern.search(k) and v.strip() not in ["VAC"]:
                        if 'CAL' in k: element['note']=v
                        elif 'PNT' in k: element['pnt_jury']=v
                        else: element['tmp']=v
                for key in ['note', 'pnt_jury', 'tmp']:
                    if key in element.keys():
                        try: element[key] = round(float(element[key].replace(',', '.')), 3)
                        except ValueError: element[key].strip()
                if not 'note' in element.keys() and 'tmp' in element.keys():
                    element['note']=element['tmp']
                if 'note' in element.keys() and 'tmp' in element.keys() and element['note']==element['tmp']:
                    del element['tmp']

                # 4) Libelle
                libelle = children_data.get("LIB_CMT_TPW")
                element["libelle"] = libelle if libelle else ""

                # 5) ECTS
                ects = children_data.get("C_NBR_CRD")
                element["ects"] = int(ects) if ects else ""

                # 6) Liste à choix
                if code.startswith('LY'): code = children_data.get("COD_ELP_LSE_TPW")

                # 7) Output avec le patch double majeure
                if not code: continue
                if code.startswith('S3Q'):
                   if not element['active']: continue
                   else: PV['Résultat'] = element
                elif code is not None and not code in ['Observat.']: PV[code] = element

        student_data["pv"] = PV
        students[student_id] = student_data

    # Output
    return { "VET": VET_def, "students": students }



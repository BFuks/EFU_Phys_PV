##########################################################
###                                                    ###
###                Générateur de PV PDF                ###
###                                                    ###
###                Date: 21/01/2026                    ###
###                                                    ###
##########################################################
import re
from datetime import datetime
from maquette import Blocs, UEs
from pv_checker import expand_UE_list
from reportlab.lib           import colors
from reportlab.lib.enums     import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles    import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units     import cm
from reportlab.platypus      import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


##########################################################
###                                                    ###
###                       Styles                       ###
###                                                    ###
##########################################################
styles = getSampleStyleSheet()
StyleTitle = ParagraphStyle('Title', parent=styles['Heading1'], alignment=TA_CENTER)
StyleHeader = ParagraphStyle('Header', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, alignment=TA_CENTER)
StyleTitleCell = ParagraphStyle('TitleCell', parent=styles['Normal'], fontSize=9, leading=12, alignment=TA_CENTER)
StyleCell = ParagraphStyle('Cell', parent=styles['Normal'], fontSize=7, leading=9, alignment=TA_CENTER)

def lighten(color, alpha=0.8):
    return colors.Color( color.red + (1-color.red)*alpha, color.green + (1-color.green)*alpha, color.blue + (1-color.blue)*alpha)


##########################################################
###                                                    ###
###           Routine principale (squelette)           ###
###                                                    ###
##########################################################
def generate_pv_pdf(data, annee, niveau, parcours, logger=None, filtre=''):
    # Nom du fichier PDF
    date = str(datetime.now().year*10000+datetime.now().month*100+datetime.now().day)
    output = SimpleDocTemplate('output/'+annee.replace('-','_')+'_'+niveau+'_'+parcours + '_v' + date + ".pdf",
       pagesize=landscape(A4), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)

    # Initialisation
    logger.info(f"Génération du PV en PDF")
    story = []
    flag_alacarte = True if niveau=='L2' and int(annee.split('-')[0])>=2025 else False
    num_ues = listes_ues(data, flag_alacarte)

    # Titre
    story.append(Paragraph(f"PV {niveau} - {parcours} ({annee})", StyleTitle))
    story.append(Spacer(1, 12))

    # Données PV
    table_data, cell_styles = build_pv_data(data, num_ues, logger=logger, alacarte=flag_alacarte, filtre=filtre)
    table = Table(table_data, repeatRows=1,  colWidths=[6*cm,4.0*cm]+[2.4*cm]*num_ues)
    table.setStyle(TableStyle([
      ('BACKGROUND', (0,0), (-1,0), colors.khaki),
      ('INNERGRID',  (0,0), (-1,-1), 1, colors.black),
      ('BOX',        (0,0), (-1,-1), 3, colors.black),
      ('BOX',        (0,0), (-1, 0), 3, colors.black),
      ('BOX',        (1,0), ( 1,-1), 3, colors.black),
      ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
      ('ALIGN',      (0,0), (-1,-1), 'CENTER')
    ] + cell_styles))
    story.append(table)

    # Output
    output.build(story)


##########################################################
###                                                    ###
###     Fonction auxiliaire : nombre d'UEs par VET     ###
###                                                    ###
##########################################################
def include_alacarte(ue_info, flag=False):
    if flag and ue_info.get('resultat',None)==None and ue_info.get('ects','')=='': return False
    return True

def listes_ues(data, alacarte=False):
    num_ues = set()
    for etudiant in data.values():
        for pv in etudiant['pv'].values():
            num_ues.add(len([k for k in pv.keys() if k in UEs.keys() and include_alacarte(pv[k], flag=alacarte) and not k.startswith(('L3', 'L4', 'L5', 'L6'))]))
    return max(sorted(num_ues))

##########################################################
###                                                    ###
###                   Headers du PV                    ###
###                                                    ###
##########################################################
def build_pv_headers(num):
    header = [ Paragraph("Étudiant", StyleHeader), Paragraph("Moyennes / Blocs", StyleHeader) ]
    for i in range(num): header.append(Paragraph(f"UE #{i+1}", StyleHeader))
    return header



##########################################################
###                                                    ###
###         Fonction coeur : les données du PV         ###
###                                                    ###
##########################################################

# Fonction auxiliaire : formattage texte
def format_session(label, note, resultat, rank, comp):
    # Couleur
    color = colors.black if resultat=='ADM' and not comp else (colors.orange if resultat=='ADM' else colors.red)

    # Cas spécial - NCAE
    if note == 'NCAE': return f"<b>{label} : {note}</b><br />"

    # Cas standard
    return f"<b>{label} : <font color='{color}'>{note}</font></b><font color='grey'> (#{rank})</font><br />"


# Fonction principale
def build_pv_data(data, num_ues, logger=None, alacarte=False, filtre=''):
    # Initialisation
    table = []
    cell_styles = []

    # Headers
    table.append(build_pv_headers(num_ues))
    current_row = 1

    # Boucle sur les étudiants
    for etu_id, etu_data in sorted(data.items(), key=lambda item: item[1].get('nom', '')):
        # Initialisation
        first_row = current_row
        success = True if etu_data.get('annee',{}).get('resultat')=='ADM' else False
        success2 = True if etu_data.get('annee',{}).get('resultat2')=='ADM' else False
        cell, parcours = build_student_cell(etu_id, etu_data, logger=logger, filtre=filtre)
        if cell==None: continue

        # Colonne moyennes / blocs
        txt = []
        for vet_index, (vet, pv) in enumerate(sorted(etu_data['pv'].items())):
            # Initialisastion (blocs UEs et compensation)
            row = []
            list_blocs = [k for k in pv.keys() if k in Blocs.keys() and 'nom' in Blocs[k].keys()]
            list_ues = [k for k in pv.keys() if k in UEs.keys()]
            matching_ue_set = {}
            for bloc in list_blocs:
                possible_sets = []
                for lst in Blocs[bloc]["UE"]: possible_sets.extend(expand_UE_list(lst, logger=logger))
                for given_set in possible_sets:
                    if all(ue in pv.keys() for ue in given_set):
                        matching_ue_set[bloc] = given_set
                        break
            comp_vet1 = comp_vet2 = False
            for ue, pv_ue in pv.items():
                if not ue in UEs.keys(): continue
                n1 = pv_ue.get('note',100) if not pv_ue.get('note',100) in ['ABI','ABJ'] else 0
                n2 = pv_ue.get('note2',n1) if not pv_ue.get('note2',n1) in ['ABI','ABJ'] else 0
                if not n1 in ['DIS'] and n1<50: comp_vet1=True
                if not n2 in ['DIS'] and n2<50: comp_vet2=True

            # Colonne étudiant
            if vet_index==0: row.append(cell)
            else: row.append('')

            # Moyenne semestrielle
            res = pv.get("Résultat", {})
            txt = f"<b>{''.join(sorted(vet[:2], key=str.isdigit))}</b><br />"
            note1 = f"{res.get('note'):.2f}/{res.get('bareme','')}" if 'note' in res.keys() else res.get('resultat')

            # 1. une seule note
            if res.get('note')==res.get('note2', res.get('note')): txt += format_session("Session1", note1, res.get('resultat2', res.get('resultat')), res.get('rank',''), comp_vet1 and comp_vet2)

            # 2. Deux notes différentes
            else:
                txt += format_session("Session1", note1, res.get('resultat'), res.get('rank',''), comp_vet1)
                note2 = f"{res.get('note2'):.2f}/{res.get('bareme','')}" if 'note2' in res.keys() else res.get('resultat')
                resu2 = res.get('resultat2', res.get('resultat'))
                txt += format_session("Session2", note2, resu2, res.get('rank2',''), comp_vet2)

            # Séparateur
            txt+='<br />'

            # Moyenne blocs
            if parcours.startswith('DM'):
                bdisc2 = pv['Résultat'].get('bdisc2',pv['Résultat'].get('bdisc1',{}))
                bdisc1 = pv['Résultat'].get('bdisc1',{})
                for bloc in ([b for b in bdisc2.keys() if b=='PY']+ sorted([b for b in bdisc2.keys() if b!='PY'])):
                    # Texte des blocs
                    colorname = colors.blue if bloc =='PY' else colors.green
                    txt += f"<font color=\'{colorname}\'>{bloc} : {bdisc1[bloc]:.2f}/100</font>"
                    if pv['Résultat'].get('bdisc2').get(bloc)!=pv['Résultat'].get('bdisc1').get(bloc):
                        txt += f" => <font color=\'{colorname}\'>{bdisc2[bloc]:.2f}/100</font><br />"
                    txt+='<br />'
            else:
                for bloc in list_blocs:
                    colorname = colors.blue if Blocs[bloc]['nom']=='MAJ' else colors.green
                    if pv[bloc].get('resultat') in ('DIS', 'NCAE'): continue
                    if pv[bloc].get('resultat') == None and pv[bloc].get('note2',pv[bloc].get('note',None))==None: continue
                    txt += f"<font color=\'{colorname}\'>{Blocs[bloc]['nom']} : {pv[bloc].get('note2',pv[bloc].get('note')):.2f}/{pv[bloc].get('bareme','')}</font><br />"
            row.append(Paragraph(txt, StyleCell))

            # UEs
            offset=0
            for idx, ue in enumerate(list_ues, start=2):
                # Safety
                res = pv.get(ue)
                if (alacarte and not include_alacarte(res, flag=alacarte)) or (ue.startswith(('L3', 'L4', 'L5', 'L6')) and res.get('note',None)==None):
                    offset+=1
                    continue

                # Texte
                color = colors.black if res['resultat']=='ADM' else (colors.orange if success else colors.red)
                note = res.get('note','')
                txt = f"<b>{ue}</b><font size=\'6\' color=\'grey\'><br />{UEs[ue]['nom']} - {UEs[ue]['ects']} ECTS</font><br /><br />"
                if note in ['DIS']: txt+= f"{note}<br />"
                elif note in ['ABI', 'ABJ']: txt+= f"<font color=\'{color}\'>{note}</font> <font size=\'6\' color=\'grey\'>(#{res.get('rank','')})</font><br />"
                elif note !='': txt+= f"<font color=\'{color}\'>{note}/{res.get('bareme','')}</font> <font size=\'6\' color=\'grey\'>(#{res.get('rank','')})</font><br />"
                if res.get('note')!=res.get('note2', res.get('note')):
                    resu2 = res.get('resultat2', res.get('resultat'))
                    color = colors.black if resu2=='ADM' else (colors.orange if success2 else colors.red)
                    txt+= f"<font color=\'{color}\'>{res.get('note2','')}/{res.get('bareme','')}</font> <font size=\'6\' color=\'grey\'>(#{res.get('rank2','')})</font><br />"
                row.append(Paragraph(txt, StyleCell))

                # Couleur de fond
                bg = colors.white
                for bloc, ues in matching_ue_set.items():
                    if ue in ues:
                        bg = lighten(colors.lightblue) if Blocs[bloc]['nom']=='MAJ' else lighten(colors.lightgreen)
                        if parcours.startswith('DM'):
                            maj2 = [b for b in pv['Résultat'].get('bdisc2',pv['Résultat'].get('bdisc1',{})) if b!='PY']
                            if maj2 and maj2[0] in ue and bg==lighten(colors.lightblue): bg=lighten(colors.lightgreen)
                            elif 'PY' in ue and bg==lighten(colors.lightgreen): bg=lighten(colors.lightblue)
                        break
                cell_styles.append( ('BACKGROUND', (idx-offset, current_row), (idx-offset, current_row), bg) )

            # Fin VET -> nouvelle ligne
            table.append(row)
            current_row+=1

        # Fusion de la cellule 'info étudiante'
        if (current_row-1)>first_row: cell_styles.append( ('SPAN', (0, first_row), (0, current_row-1)) )

    return table, cell_styles


##########################################################
###                                                    ###
###          Formattage des données étudiant           ###
###                                                    ###
##########################################################
mineures = {
   'CH': 'Chinois', 'CI':'Chimie', 'DS':'DataScience', 'EE': 'Elec',
   'EV': 'Environnement', 'GS':'Gestion', 'HN':'HistNat', 'IA':'InnovSanté',
   'IN':'Info', 'MA':'Maths', 'ME':'Meca', 'PH':'Philo', 'PT':'ProfEcole',
   'ST':'SdT'
}

# Fonctions auxiliaires : formattage texte
def format_annee(label, note, maj, resultat, rank, comp):
    color = colors.black if resultat=='ADM' and not comp else (colors.orange if resultat=='ADM' else colors.red)
    color_maj = '\'grey\'' if maj>=50 else colors.red
    return f"<br /><b>{label} : <font color='{color}'>{note:.2f}</font></b><font color='grey' size='7'> (#{rank} ; MAJ : <font color={color_maj}>{maj:.2f}/100</font>)</font>"


def format_annee_bdisc(label, note, resultat, rank, comp, bdisc):
    # Blocs présents dans le dictionnaire
    blocs_presents = [b for b in bdisc if b=='PY']+ sorted([b for b in bdisc if b!='PY'])
    # Texte des blocs
    blocs_txt = ', '.join( f"{b} : <font color='{colors.gray if bdisc[b]>=50 else colors.red}'>{bdisc[b]:.2f}/100</font>" for b in blocs_presents)
    sep = '' if bdisc=={} else " ; "
    # Couleur principale
    color = colors.black if resultat=='ADM' and not comp else (colors.orange if resultat=='ADM' else colors.red)
    # output
    return f"<br /><b>{label} : <font color='{color}'>{note:.2f}</font></b><font color='grey' size='7'><br /> (#{rank}{sep}{blocs_txt})</font>"


# Fonction principale
def build_student_cell(etu_id, data, logger=None, filtre=''):

    # Parcours
    pattern_mono = re.compile(r"(\dSLPY|S\dLPY)")
    pattern_maj  = re.compile(r"(\dSVPY|S\dVPY)")
    pattern_dm   = re.compile(r"(\dSQPY|S\dQPY)")
    if all(pattern_mono.search(vet) for vet in data['VET']): parcours = 'MONO'
    elif all(pattern_maj.search(vet) for vet in data['VET']):
        MIN = next((k[3:5] for k,v in data['pv'][sorted(data['VET'])[-1]].items() if k in Blocs and k[3:5] != "PY" and v.get('note','')!=''), '')
        data['mineure'] = MIN
        parcours = 'MajPhys - Min' + mineures.get(MIN,'') if MIN!='' else 'MajPhys'
        if filtre!='' and MIN!=mineures.get(filtre): return None, None, None
    elif all(pattern_dm.search(vet) for vet in data['VET']):
        MAJ2 = next((k[3:5] for k,v in data['pv'][sorted(data['VET'])[-1]].items() if k in Blocs and k[3:5] != "PY" and v.get('note','')!=''), '')
        if not MAJ2: MAJ2 = next((k[3:5] for k,v in data['pv'][sorted(data['VET'])[0]].items() if k in Blocs and k[3:5] != "PY" and v.get('note','')!=''), '')
        data['majeure2'] = MAJ2
        parcours = 'DMPhys - ' + mineures.get(MAJ2,'') if MAJ2!='' else 'DMPhys'
        if filtre!='' and MAJ2!=mineures.get(filtre): return None, None, None
    else:
        parcours = '???'
        logger.error(f"[{data['nom']} ({etu_id})] Parcours indéfini (pv_writer, {data['VET']})")

    # Initialisation cellule
    txt = f"<b>{data['nom']}</b><br/>({etu_id})<br/><br />{parcours}<br />"


    # Compensation annuelle
    comp1 = any(data['pv'].get(vet).get('Résultat').get('resultat') == 'AJ' for vet in data['VET'])
    comp2 = any(data['pv'].get(vet).get('Résultat').get('resultat2',data['pv'].get(vet).get('Résultat').get('resultat')) == 'AJ' for vet in data['VET'])

    # Moyenne annuelle
    if 'annee' in data.keys():
        # Notes et classement
        # 1. une seule note
        if data['annee']['note']==data['annee']['note2']:
            if parcours.startswith('DM'):
                txt+=format_annee_bdisc('Session1', data['annee']['note'], data['annee']['resultat'], data['annee']['rank'], comp1 and comp2, data['annee']['bdisc1'])
            else:
                txt+=format_annee('Session1', data['annee']['note'], data['annee']['maj1_1'], data['annee']['resultat'], data['annee']['rank'], comp1 and comp2)

        # 2. deux notes différentes
        else:
            if parcours.startswith('DM'):
                txt+=format_annee_bdisc('Session1', data['annee']['note'], data['annee']['resultat'], data['annee']['rank'], comp1, data['annee']['bdisc1'])
                txt+=format_annee_bdisc('Session2', data['annee']['note2'], data['annee']['resultat2'], data['annee']['rank2'], comp2, data['annee']['bdisc2'])
            else:
                txt+=format_annee('Session1', data['annee']['note'], data['annee']['maj1_1'], data['annee']['resultat'], data['annee']['rank'], comp1)
                txt+=format_annee('Session2', data['annee']['note2'], data['annee']['maj1_2'], data['annee']['resultat2'], data['annee']['rank2'], comp2)

        if data['annee']['resultat2']=='AJ' and data['annee']['note2']>10:
            logger.warning(f"[{data['nom']} ({etu_id})] Moyenne annuelle > 10 avec bloc MAJ non validé")

    # Output
    return Paragraph(txt, StyleTitleCell), parcours


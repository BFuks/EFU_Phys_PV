##########################################################
###                                                    ###
###                Générateur de PV PDF                ###
###                                                    ###
###                Date: 17/12/2025                    ###
###                                                    ###
##########################################################
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
def generate_pv_pdf(data, annee, niveau, parcours, logger=None):
    # Nom du fichier PDF
    date = str(datetime.now().year*10000+datetime.now().month*100+datetime.now().day)
    output = SimpleDocTemplate('output/'+annee.replace('-','_')+'_'+niveau+'_'+parcours + '_v' + date + ".pdf",
       pagesize=landscape(A4), rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)

    # Initialisation
    story = []
    num_ues = listes_ues(data)

    # Titre
    story.append(Paragraph(f"PV {niveau} - {parcours} ({annee})", StyleTitle))
    story.append(Spacer(1, 12))

    # Données PV
    table_data, cell_styles = build_pv_data(data, num_ues, logger)
    table = Table(table_data, repeatRows=1,  colWidths=[6*cm,4.0*cm]+[2.5*cm]*num_ues)
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
def listes_ues(data):
    num_ues = set()
    for etudiant in data.values():
        for pv in etudiant['pv'].values():
            num_ues.add(len([k for k in pv.keys() if k.startswith("LU")]))
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
def build_pv_data(data, num_ues, logger=None):
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

        # Colonne moyennes / blocs
        txt = []
        for vet_index, (vet, pv) in enumerate(sorted(etu_data['pv'].items())):
            # Initialisastion (blocs et UEs)
            row = []
            list_blocs = [k for k in pv.keys() if k in Blocs.keys()]
            list_ues = [k for k in pv.keys() if k in UEs.keys()]
            matching_ue_set = {}
            for bloc in list_blocs:
                possible_sets = []
                for lst in Blocs[bloc]["UE"]: possible_sets.extend(expand_UE_list(lst, logger=logger))
                for given_set in possible_sets:
                    if all(ue in pv.keys() for ue in given_set):
                        matching_ue_set[bloc] = given_set
                        break

            # Colonne étudiant
            if vet_index==0: row.append(build_student_cell(etu_id, etu_data, logger))
            else: row.append('')

            # Moyenne semestrielle
            res = pv.get("Résultat", {})
            color = colors.black if res['resultat']=='ADM' else (colors.orange if success else colors.red)
            note = f"{res.get('note'):.2f}/{res.get('bareme','')}" if 'note' in res.keys() else res.get('resultat')
            txt = f"<b>{vet[1]+vet[0]}</b><br />"
            if note in ['NCAE']: txt += f"<b>Session1 : {note}</b><br />"
            else: txt += f"<b>Session1 : <font color=\'{color}\'>{note}</font></b> <font color=\'grey\'>(#{res.get('rank','')})</font><br />"

            if res.get('note')!=res.get('note2', res.get('note')):
                color = colors.black if res['resultat2']=='ADM' else (colors.orange if success2 else colors.red)
                note = f"{res.get('note2'):.2f}/{res.get('bareme','')}" if 'note2' in res.keys() else res.get('resultat')
                txt += f"<b>Session2 : <font color=\'{color}\'>{note}</font></b> <font color=\'grey\'>(#{res.get('rank2','')})</font><br />"

            # Séparateur
            txt+='<br />'

            # Moyenne blocs
            for bloc in list_blocs:
                colorname = colors.blue if Blocs[bloc]['nom']=='MAJ' else colors.green
                if pv[bloc].get('resultat') in (None, 'DIS'): continue
                txt += f"<font color=\'{colorname}\'>{Blocs[bloc]['nom']} : {pv[bloc].get('note2',pv[bloc].get('note')):.2f}/{pv[bloc].get('bareme','')}</font><br />"
            row.append(Paragraph(txt, StyleCell))

            # UEs
            for idx, ue in enumerate(list_ues, start=2):
                # Texte
                res = pv.get(ue)
                color = colors.black if res['resultat']=='ADM' else (colors.orange if success else colors.red)
                note = res.get('note','')
                txt = f"<b>{ue}</b><font size=\'6\' color=\'grey\'><br />[{UEs[ue]['nom']} - {UEs[ue]['ects']} ECTS]</font><br /><br />"
                if note in ['DIS']: txt+= f"{note}<br />"
                elif note in ['ABI', 'ABJ']: txt+= f"<font color=\'{color}\'>{note}</font> <font size=\'6\' color=\'grey\'>(#{res.get('rank','')})</font><br />"
                elif note !='': txt+= f"<font color=\'{color}\'>{note}/{res.get('bareme','')}</font> <font size=\'6\' color=\'grey\'>(#{res.get('rank','')})</font><br />"
                if res.get('note')!=res.get('note2', res.get('note')):
                    color = colors.black if res['resultat2']=='ADM' else (colors.orange if success2 else colors.red)
                    txt+= f"<font color=\'{color}\'>{res.get('note2','')}/{res.get('bareme','')}</font> <font size=\'6\' color=\'grey\'>(#{res.get('rank2','')})</font><br />"
                row.append(Paragraph(txt, StyleCell))

                # Couleur de fond
                bg = lighten(colors.white)
                for bloc, ues in matching_ue_set.items():
                    if ue in ues:
                        bg = lighten(colors.lightblue) if Blocs[bloc]['nom']=='MAJ' else lighten(colors.lightgreen)
                        break
                cell_styles.append( ('BACKGROUND', (idx, current_row), (idx, current_row), bg) )

            # Fin VET -> nouvelle ligne
            table.append(row)
            current_row+=1

        # Fusion de la cellule 'info étudiante'
        if (current_row-1)>first_row: cell_styles.append( ('SPAN', (0, first_row), (0, current_row-1)) )

    return table, cell_styles


##########################################################
###                                                    ###
###          Formattage des données édtudiant          ###
###                                                    ###
##########################################################
def build_student_cell(etu_id, data, logger=None):

    # Parcours
    if all(['SLPY' in x for x in data['VET']]): parcours = 'MONO'
    else:
        parcours = '???'
        logger.error(f"[{etu_data['nom']} ({etu_id})] Parcours indéfini (pv_writer)")

    # Initialisation cellule
    txt = f"<b>{data['nom']}</b><br/>({etu_id})<br/><br />{parcours}<br />"


    # Compensation annuelle
    comp1 = comp2 = False
    for pv in data['pv'].values():
        for ue in [x for x in pv.keys() if x in UEs.keys()]:
            note1 = pv[ue].get('note',100)
            if not note1 in ['DIS']:
                if note1 in ['ABI']: note1=0
                if note1<50: comp1=True
            note2 = pv[ue].get('note2',pv[ue].get('note',100))
            if not note2 in ['DIS']:
                if note2 in ['ABI']: note2=0
                if note2<50: comp2=True

    # Moyenne annuelle
    if 'annee' in data.keys():
        # Notes et classement
        color1 = colors.black if (data['annee']['resultat']=='ADM' and not comp1) else (colors.orange if data['annee']['resultat']=='ADM' else colors.red)
        txt += f"<br/><b>Session1 : <font color='{color1}'>{data['annee']['note']:.3f}</font></b>"
        txt += '<font color=\'grey\' size=\'8\'> (#'+data['annee']['rank']+')</font>'

        if data['annee']['note']!=data['annee']['note2']:
            color2 = colors.black if (data['annee']['resultat2']=='ADM' and not comp2) else (colors.orange if data['annee']['resultat2']=='ADM' else colors.red)
            txt += f"<br/><b>Session2 : <font color='{color2}'>{data['annee']['note2']:.3f}</font></b>"
            txt += '<font color=\'grey\' size=\'8\'> (#'+data['annee']['rank2']+')</font>'

    # Output
    return Paragraph(txt, StyleTitleCell)






### ##########################################################
### ###                                                    ###
### ###                 Header of the file                 ###
### ###                                                    ###
### ##########################################################
### from reportlab.platypus      import Paragraph, SimpleDocTemplate, Spacer
### import datetime
### def MakeTitle(annee, niveau, parcours, semestres):
###     # file
###     date = str(datetime.datetime.now().year*10000+datetime.datetime.now().month*100+datetime.datetime.now().day);
###     pv_file    = SimpleDocTemplate('output/'+annee+'_'+niveau+'_'+parcours + '_v' + date + ".pdf", pagesize=landscape(A4),
###       leftMargin=1.5*cm, rightMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm);
### 
###     # title
###     story = [Paragraph('<para align="center"> PV ' + niveau + ' - ' + parcours + ' (' + \
###        annee.replace('_','-') + ') : ' + ', '.join([x.split('_')[0] for x in semestres]) + '</para>',  getSampleStyleSheet()['Heading1'])];
###     story.append(Spacer(1, 0.5*cm));
### 
###     # output
###     return pv_file, story;
### 
### 
### ##########################################################
### ###                                                    ###
### ###                 Header of the file                 ###
### ###                                                    ###
### ##########################################################
### from maquette                import Maquette, UEs, Irrelevant;
### 
### # Nombre de colonnes du PV
### def GetLength(semestres, parcours):
###     tags_semestre = [x.split('_')[0] for x in semestres];
###     num_ue = [[ x for x in Maquette.keys() if parcours in Maquette[x]['parcours'] and y in Maquette[x]['semestre'] and Maquette[x]['nom']!='MIN'] for y in tags_semestre];
###     return max([ sum([ max([ len(ues) for ues in bloc])  for bloc in sem] ) for sem in [[(Maquette[x]['UE'] if Maquette[x]['nom']!='MIN' else [' ']) for x in z] for z in num_ue]]);
### 
### def MakeHeaders(annee, semestres, parcours):
###     # number of columns in the table
###     num_ue = GetLength(semestres, parcours);
###     if parcours=='CMI': num_ue-=2;
###     if parcours=='CMI' and int(annee.split('_')[0])>=2024 and 'S5_Session1' in semestres: num_ue-=1;
###     if parcours=='CMI' and int(annee.split('_')[0])>=2024 and 'S4_Session1' in semestres: num_ue-=2;
###     if parcours in ['DM', 'MAJ', 'PADMAJ']: num_ue+=1;
### 
###     # The header themselves
###     Headers = [[
###         Paragraph('<para align="center"><b>Etudiant</b></para>', getSampleStyleSheet()["BodyText"]),
###         Paragraph('<para align="center"><b>Moyennes</b></para>', getSampleStyleSheet()["BodyText"])
###     ] + [ Paragraph('<para align="center"><b>UE #'+str(1+x)+'</b></para>', getSampleStyleSheet()["BodyText"]) for x in range(num_ue)]];
### 
###     # output
###     return Table(Headers, colWidths=[7*cm,3.7*cm]+[2.6*cm]*(len(Headers[0])-2), style=[
###             ('BACKGROUND', (0,0), ( len(Headers[0]), 0),   colors.khaki),
###             ('GRID',       (0,0), (-1,-1),1, colors.black),
###             ('BOX',        (0,0), (-1, 0),3, colors.black),
###             ('BOX',        (1,0), ( 1,-1),3, colors.black),
###             ('VALIGN',     (0,0), (-1, -1),  'MIDDLE'),
###             ('ALIGN',      (0,0), (-1, -1),  'CENTER')
###     ]);
### 
### 
### ##########################################################
### ###                                                    ###
### ###          Obtention et formattage des notes         ###
### ###                                                    ###
### ##########################################################
### from pv_checker              import CheckValidation
### # Calcul et formattage des moyennes semestrielles
### def GetAverages(parcours, semestre, notes, blocs_maquette, moyenne_annee, etu_id):
### 
###     ## Formatting session 1(colour)
###     if notes['total']['note'] in ['NCAE', 'ENCO']: my_color='black';
###     elif notes['total']['note']>=10. : my_color='black';
###     elif moyenne_annee[0] > 10.      : my_color='orange'; 
###     else                             : my_color='red'
### 
###     ## Formatting session 2 (colour)
###     if 'note2'in notes['total'].keys():
###         if notes['total']['note2'] in ['NCAE', 'ENCO']: my_color2='black';
###         elif notes['total']['note2']>=10. : my_color2='black';
###         elif moyenne_annee[1] > 10.       : my_color2='orange'; 
###         else                              : my_color2='red'
###     else: my_color2='black';
### 
###     ## Affichage moyennes
###     sess1 = ''; sess2 = '';
###     if notes['total']['note'] not in ['NCAE', 'ENCO']:
###         sess1  = '<b>' + semestre.replace('_Session1','') + ' :<br />  <font color=' + my_color + '>'+ '{:.3f}'.format(notes['total']['note']) + '/20</font></b>';
###         sess1 += '<font color=\'grey\' size=\'8\'> (#'+notes['total']['ranking']+')</font>';
###     else:
###         sess1 = '<b>' + semestre.replace('_Session1','')  + ' :<br />  <font color=' + my_color + '>' + notes['total']['note'] + '</font></b>';
###     if 'note2' in notes['total'].keys() and notes['total']['note2'] != notes['total']['note']:
###         if notes['total']['note2'] not in ['NCAE', 'ENCO']:
###             sess2  = '<br /><b><font color=' + my_color2 + '>'+ '{:.3f}'.format(notes['total']['note2']) + '/20</font></b>';
###             sess2 += '<font color=\'grey\' size=\'8\'> (#'+notes['total']['ranking2']+')</font>';
###         else:
###             sess2 = '<br /><b><font color=' + my_color2 + '>' + notes['total']['note2'] + '</font></b>';
### 
###     moyennes_string = '<para align="center">' + sess1 +  sess2 + '<br />';
###     for bloc in sorted([x for x in list(blocs_maquette)],reverse=True):
###         if not parcours in ['DK', 'DM']:
###             nombloc  = Maquette[bloc]['nom'];
###             notebloc = notes[bloc]['note'];
###             if 'note2' in notes[bloc].keys(): notebloc = notes[bloc]['note2'];
###         else:
###             nombloc  = 'MAJ1' if 'PY' in bloc else 'MAJ2';
###             try:
###                 notebloc = notes[semestre][nombloc][0]/notes[semestre][nombloc][1];
###             except:
###                 notebloc = 0
###                 logger.error('Étudiant ' + str(etu_id) + ' - Problème de maquette pour le bloc ' + nombloc + " : " + str(notes[semestre][nombloc]));
###         if not notes['total']['note'] in ['NCAE', 'ENCO'] and not notebloc in ['NCAE', 'ENCO', 'DIS']:
###             colour = 'red' if float(notebloc)<50 else 'black';
###             moyennes_string += '<br />' + nombloc + ' :  <font color=\'' + colour + '\'>' + '{:.3f}'.format(notebloc) + '/100</font>';
###     moyennes_string += '</para>';
### 
###     ## output
###     return Paragraph(moyennes_string, getSampleStyleSheet()['BodyText']);
### 
### 
### 
### # Formattage des notes
### def GetNotes(notes, ues, ncases, moyenne_annee, etu_id, semestre):
###     ## Initialisation
###     notes_string = [];
###     counter = 0;
###     compensation = ( moyenne_annee[0]>=10. or float(notes['total']['note'])>10.) if notes['total']['note'] not in ['NCAE','ENCO'] else False;
###     compensation2 = False;
###     if 'note2' in notes['total'].keys(): compensation2 = ( moyenne_annee[1]>=10. or float(notes['total']['note2'])>10.) if notes['total']['note2'] not in ['NCAE','ENCO'] else False;
### 
###     ## Boucle sur les UE
###     l1 = True if ('1SLPY001' in notes.keys() or '2SLPY001' in notes.keys() )else False
###     list1 = [x for x in notes.keys() if not x in ues]
###     list2 = [x for x in notes.keys() if x in Maquette.keys() and Maquette[x]['nom']=='MIN' and not x in list1]
###     list3 = [x for x in notes.keys() if x in ['LK3PYC03', 'LK4PYC03', 'LK5PYMI0', 'LK6PYMI0']] 
###     for ue in (ues+list1+list2+list3):
###         ### Enlever les notes de la mineure
###         if ue in ['LK5EEJ13', 'LK5PHM99', 'LK6ST113', 'LK6ST116']: continue
###         if ue.startswith('S'): continue
### 
###         ### Note manquante
###         if not ue in notes.keys():
###             notes_string += [Paragraph('', getSampleStyleSheet()['BodyText'])];
###             continue;
### 
###         # Mineure
###         if ue.startswith('LU') and not ('PY' in ue or 'LV' in ue or l1): continue;
###         if ue.startswith('LK') and 'PY' in ue: continue;
###         if ue.startswith('L5PH') or ue.startswith('L3LACH') or ue.startswith('L4LACH') or ue.startswith('L6PH'): continue;
###         if ue.startswith('L5LACH') or ue.startswith('L6LACH'): continue;
###         if ue.startswith('L3PH') or ue.startswith('L4PH'): continue;
###         if ue in ['total', '1SLPY001', '2SLPY001']: continue
### 
###         ### Redoublant deja valide
###         validation_tag = "<br /><font color='grey' size='8'>("+notes[ue]['annee_val']+')</font>' if notes[ue]['annee_val']!=None else '';
### 
###         ### Note session 2 + formattage
###         current_note2=''; fontcolor2='black';
###         if 'note2' in notes[ue].keys():
###             my_note2 = notes[ue]['note2'];
###             current_note2 = '{:.2f}'.format(my_note2)+'/100' if not my_note2 in ['NCAE', 'ABI', 'DIS', 'ENCO', 'U VAC', 'VAC', '???'] else my_note2;
###             if 'ranking2' in notes[ue].keys(): current_note2 += '<font color=\'grey\' size=\'7\'> [#'+notes[ue]['ranking2']+']</font>';
### 
###             fontcolor2 = 'black' if not my_note2 in ['ABI', '???'] and (my_note2 in ['NCAE', 'ENCO', 'DIS', 'U VAC', 'VAC'] or my_note2>=50.) else 'red';
###             if fontcolor2=='red' and compensation2: fontcolor2='orange';
### 
###         ### Note session 1 + formattage
###         my_note = notes[ue]['note'];
###         if my_note!=-1:
###             current_note = '{:.2f}'.format(my_note)+'/100' if not my_note in ['ABI', 'DIS', 'NCAE', 'ENCO', 'U VAC', 'VAC', '???'] else my_note
###             if 'ranking' in notes[ue].keys(): current_note += '<br /><font color=\'grey\' size=\'8\'>#'+notes[ue]['ranking']+'</font>';
###         else: current_note = '???';
### 
###         fontcolor = 'black' if not my_note in ['ABI', '???'] and (my_note in ['NCAE', 'ENCO', 'DIS', 'U VAC', 'VAC'] or my_note>=50.) else 'red';
###         if fontcolor=='red' and compensation: fontcolor='orange';
###         if (not 'note2' in notes[ue].keys() or current_note.split('<')[0] == current_note2.split('<')[0]) and compensation2 and fontcolor=='red': fontcolor='orange';
### 
###         ### Result
###         tmp_string= '<para align="center"><b>' + ue + '</b><br />' + \
###              '<font color=\'grey\' size=\'8\'><super>[' + UEs[ue]['nom'].replace('0','') + ' - ' + str(UEs[ue]['ects']) + ' ECTS]</super></font><br />';
###         if 'note2' in notes[ue].keys() and current_note.split('<')[0] != current_note2.split('<')[0]:
###             # Check session 2 > session 1
###             if current_note!='???' and not notes[ue]['note2'] in ['ENCO'] and notes[ue]['note2']<notes[ue]['note']:
###                 logger.critical(semestre[:2] + ' - ' + str(etu_id) + " :  Note session 2 < note session1 - " + ue + " (" + str(round(notes[ue]['note'],2)) +  ' > ' +  str(round(notes[ue]['note2'],2)) + ")");
###             current_note =  current_note.replace('<br />',' ').replace('#','[#').replace('</font>',']</font>').replace('8','7');
###             tmp_string = tmp_string + '<font color=' + fontcolor + ' size=\'7\'>' + current_note + '</font><br />';
###             tmp_string = tmp_string + '<font size = \'7\' color=' + fontcolor2 + '>' + current_note2 + '</font>'
###         else:
###             tmp_string = tmp_string + '<font color=' + fontcolor + '>' + current_note + '</font>';
###         tmp_string = tmp_string + validation_tag + '</para>';
### 
###         notes_string+= [ Paragraph(tmp_string, getSampleStyleSheet()['BodyText'])];
###         counter+=1;
### 
###     ## Ajout de cases blanches
###     for i in range(ncases-counter): notes_string += [Paragraph('', getSampleStyleSheet()['BodyText'])];
### 
###     ## output
###     return notes_string;
### 
### 
### ##########################################################
### ###                                                    ###
### ###                   Core  function                   ###
### ###                                                    ###
### ##########################################################
### # Liste des etudiants
### import itertools
### def GetList(pv):
###     liste_etudiants =  [ [ [y, x[y]['nom']] for y in x.keys() if y != 'resume'] for x in pv];
###     liste_etudiants = [x for y in liste_etudiants for x in y];
###     filtered_data = []
###     for item in liste_etudiants:
###          if item[1] != None or all(entry[1] == None for entry in liste_etudiants if entry[0] == item[0]):
###             filtered_data.append(item)
###     liste_etudiants = filtered_data;
###     liste_etudiants.sort(key=lambda elem: elem[1]);
###     return list(liste_etudiants for liste_etudiants, _ in itertools.groupby(liste_etudiants));
### 
### 
### def GetLineStyle(counter, endline):
###     # Common style
###     line_style = [
###        ('LINEBEFORE', (3,  0), ( -1, 0), 1, colors.black),
###        ('LINEBEFORE', (0,  0), ( 2, 0), 3, colors.black),
###        ('LINEAFTER', (-1, 0), (-1, 0), 3, colors.black),
###        ('LINEBELOW', ( counter, 0), (-1, 0), 2-counter, colors.black),
###        ('VALIGN',     (0,0), (-1, -1),  'MIDDLE'),
###        ('ALIGN',      (0,0), (-1, -1),  'CENTER')
###     ];
### 
###     # end of line
###     if endline: line_style.append(('LINEBELOW', ( 0, 0), (-1, 0), 3, colors.black));
### 
###     # output
###     return line_style;
### 
### 
### 
### from misc import GetBlocsMaquette, GetUEsMaquette;
### def PDFWriter(pv, annee, niveau, parcours, semestres, redoublants=False, success=False):
### 
###     # Title and headers
###     pv_file, story =  MakeTitle(annee, niveau, parcours, semestres);
###     story.append(MakeHeaders(annee,semestres, parcours));
### 
###     # Liste des UE et blocs par semestre
###     blocs_maquette = {}; UEs_maquette = {};
###     for semestre in semestres:
###         blocs_maquette[semestre] = GetBlocsMaquette(semestre.split('_')[0], parcours);
### 
###     # Etudiant data
###     full = pv["full"]; del pv["full"];
###     full2= pv["full2"]; del pv["full2"];
###     for etu in GetList(pv.values()):
###          # initialisation etudiant
###          logger.debug("etudiant = " + str(etu));
###          moyenne_annee = 0.; moyenne_annee2= 0.;
### 
###          ## Parcours
###          my_parcours = parcours;
###          if parcours in ['DM', 'MAJ', 'DK']:
###              MIN=[];
###              for sem in semestres:
###                  if not etu[0] in pv[sem].keys():continue;
###                  try:    MIN = MIN + [ x for x in pv[sem][etu[0]]['results'].keys() if x in Maquette.keys() and Maquette[x]['nom']=='MIN'];
###                  except: MIN = [''];
###              logger.debug("  > Parcours " + sem + " = "  + str(MIN))
###              if parcours=='MAJ':
###                  try:    my_parcours = 'MajPhys - ' + UEs[MIN[-1]]['nom'][:-1];
###                  except: my_parcours = 'MajPhys';
###              elif parcours in ['DK', 'DM']:
###                  try:    my_parcours = parcours + ' Phys - ' + UEs[MIN[-1]]['nom'][3:-1];
###                  except: my_parcours = parcours + ' Phys';
###          logger.debug("  > Parcours = " + my_parcours);
### 
###          ## Blocs disciplinaire
###          disc = '';
###          if parcours in ['DK', 'DM']:
###              all_sems = [x for x in pv.keys() if etu[0] in pv[x].keys() and 'Session1' in x];
###              maj1=0; maj2=0;
###              coe1=0; coe2=0;
###              for sem in all_sems:
###                  maj1 = maj1 + pv[sem][etu[0]]['results'][sem]['MAJ1'][0];
###                  maj2 = maj2 + pv[sem][etu[0]]['results'][sem]['MAJ2'][0];
###                  coe1 = coe1 + pv[sem][etu[0]]['results'][sem]['MAJ1'][1];
###                  coe2 = coe2 + pv[sem][etu[0]]['results'][sem]['MAJ2'][1];
###              maj1 = maj1/coe1;
###              maj2 = maj2/coe2 if coe2!=0 else 0;
###              col1 = 'red' if maj1 < 50 else 'black';
###              col2 = 'red' if maj2 < 50 else 'black';
###              if maj1 < 50: logger.warning(etu[1] + " (" + str(etu[0]) + ")] : Bloc Phys non valide [" + '{:.3f}'.format(maj1) + '/100]');
###              if coe2!=0 and maj2 < 50: logger.warning(etu[1] + " (" + str(etu[0]) + ")] : Bloc " +  UEs[MIN[-1]]['nom'][3:-1] + " non valide [" + '{:.3f}'.format(maj2) + '/100]');
### 
###              disc =  '<br />MAJ1 : <font color=' + col1 + '> ' + '{:.3f}'.format(maj1) + '/100</font>' + \
###                      '<br />MAJ2 : <font color=' + col2 + '> ' + '{:.3f}'.format(maj2) + '/100</font>';
### 
###          ## Header etudiant
###          etu_id = Paragraph('<para align="center"><b>' + etu[1] + '<br />' + str(etu[0]) + '</b><br /><br />' + my_parcours + '</para>',getSampleStyleSheet()['BodyText']);
###          nbr_semestres = len([y for y in [etu[0] in pv[x].keys() for x in semestres] if y]);
###          max_semestres = nbr_semestres;
###          logger.debug("  > " + str(nbr_semestres) + ' semestre(s) disponible(s)');
### 
###          ## Calcul de la moyenne annuelle
###          moyennes = {};
###          colour_annee = 'black';
###          if full[str(etu[0])] not in ['NCAE', 'ENCO']:
###              moyenne_annee = full[str(etu[0])][0];
###              colour_annee      = 'red' if moyenne_annee<10 else 'black';
###          logger.debug("  > Session1 : " + str(moyenne_annee) + ' (' + colour_annee + ')');
###          if full2[str(etu[0])] not in ['ENCO', 'NCAE']:
###              moyenne_annee2 = full2[str(etu[0])][0];
###              colour_annee2      = 'red' if moyenne_annee2<10 else 'black';
###          if moyenne_annee!=moyenne_annee2: logger.debug("  Session 2 : > " + str(moyenne_annee2) + ' (' + colour_annee2 + ')');
###          if redoublants:
###              if not (moyenne_annee<10 and moyenne_annee2<10): continue;
###          if success:
###              if (moyenne_annee<10 and moyenne_annee2<10): continue;
### 
###          ## Real loop over the semesters
###          for semestre in semestres:
###             ### safety
###             if not etu[0] in pv[semestre].keys(): continue;
### 
###             ### PV individuel
###             pv_ind = pv[semestre][etu[0]];
###             blocs_maq = [x for x in blocs_maquette[semestre] if not x in [x for x in UEs if x.startswith('LK')] or x in pv_ind['results'].keys()];
### ##             if int(annee.split('_')[0])>2022 and 'LK3PYJ05' in blocs_maq and 'LK3PYJ00' in blocs_maq:
### ##                 blocs_maq.remove('LK3PYJ00');
### ##             elif int(annee.split('_')[0])<2023 and 'LK3PYJ05' in blocs_maq and 'LK3PYJ00' in blocs_maq:
### ##                 blocs_maq.remove('LK3PYJ05');
### ##             if int(annee.split('_')[0])>2022 and 'LK3PYJ06' in blocs_maq and 'LK3PYJ00' in blocs_maq:
### ##                 blocs_maq.remove('LK3PYJ00');
### ##             elif int(annee.split('_')[0])<2023 and 'LK3PYJ06' in blocs_maq and 'LK3PYJ00' in blocs_maq:
### ##                 blocs_maq.remove('LK3PYJ06');
### ##             if   'LK3PYJ05' in blocs_maq and 'LK3PYJ06' in blocs_maq and 'LK3MAM00' in pv_ind['results'].keys(): blocs_maq.remove('LK3PYJ05');
### ##             elif 'LK3PYJ05' in blocs_maq and 'LK3PYJ06' in blocs_maq and not 'LK3MAM00' in pv_ind['results'].keys(): blocs_maq.remove('LK3PYJ06')
### ##             elif 'LK3PYJ10' in blocs_maq and 'LK3PYJ11' in blocs_maq: blocs_maq.remove('LK3PYJ10')
### ##             if 'LK3SSK00' in pv_ind['results'].keys() and not 'LK3SSK00' in blocs_maq: blocs_maq.append('LK3SSK00');
### ##             if 'LK3DRD00' in pv_ind['results'].keys() and not 'LK3DRD00' in blocs_maq: blocs_maq.append('LK3DRD00');
### ## 
### ##             if ('LK5PYJDD' in pv_ind['results'].keys() or 'LK5PYJEE' in  pv_ind['results'].keys()) and 'LK5PYJ00' in blocs_maq: blocs_maq.remove('LK5PYJ00');
### ##             if ('LK6PYJDD' in pv_ind['results'].keys() or 'LK6PYJEE' in  pv_ind['results'].keys()) and 'LK6PYJ00' in blocs_maq: blocs_maq.remove('LK6PYJ00');
### ##             if ('LK6PYJDD' in pv_ind['results'].keys() or 'LK6PYJEE' in  pv_ind['results'].keys()) and 'LK6PYJ20' in blocs_maq: blocs_maq.remove('LK6PYJ20');
### ##             if len(blocs_maq)==3 and 'LK5HIM00' in blocs_maq: blocs_maq.remove('LK5HIM00');
### 
###             UEs_maquette[semestre]   = GetUEsMaquette(blocs_maq);
### 
###             ### First cell of the table
###             dep = 0 if nbr_semestres==1 else 1; nbr_semestres-=1;
###             line_style = GetLineStyle(dep, semestre==semestres[-1] and etu == GetList(pv.values())[-1]);
### 
###             sess1=''; sess2='';
###             if full[str(etu[0])] in ['NCAE', 'ENCO']:
###                 sess1 = '<b>Session1 = <font color=' + colour_annee + '>' + full[str(etu[0])] + '</font></b>';
###             else:
###                 sess1 =  '<b>Session1 = <font color=' + colour_annee + '>' + \
###                      '{:.3f}'.format(moyenne_annee) + '/20</font></b><font color=\'grey\' size=\'9\'> (#' + full[str(etu[0])][1] +\
###                      ')</font>';
### 
###             if moyenne_annee!=moyenne_annee2 and full2[str(etu[0])] in ['NCAE', 'ENCO']:
###                 sess2 = '<b>Session2 = <font color=' + colour_annee + '>' + full2[str(etu[0])]  + '</font></b>';
###             elif moyenne_annee!=moyenne_annee2:
###                 sess2 =  '<b>Session2 = <font color=' + colour_annee2 + '>' + \
###                      '{:.3f}'.format(moyenne_annee2) + '/20</font></b><font color=\'grey\' size=\'9\'> (#' + full2[str(etu[0])][1] +\
###                      ')</font>';
### 
###             if dep==0 and nbr_semestres==(max_semestres-1):
###                 etu_id = [etu_id, Paragraph('<para align="center">' + sess1 + '<br />' + sess2 + disc + '</para>', getSampleStyleSheet()['BodyText'])];
###             elif dep==0:
###                 etu_id = [Paragraph('<para align="center"><br /></para>',getSampleStyleSheet()['BodyText']), \
###                           Paragraph('<para align="center">' + sess1 + '<br />' + sess2 + disc + '</para>', getSampleStyleSheet()['BodyText'])];
### 
### 
###             ### Second cell of the table
###             header_semestre = GetAverages(parcours, semestre, pv_ind['results'], blocs_maq, [moyenne_annee, moyenne_annee2], etu[0]);
### 
###             ### Notes des UE
###             num_ue = GetLength(semestres, parcours);
###             if parcours=='CMI':num_ue-=2;
###             if parcours in ['PADMAJ', 'MAJ', 'DM']: num_ue+=1;
###             if parcours=='CMI' and int(annee.split('_')[0])>=2024 and 'S5_Session1' in semestres: num_ue-=1;
###             if parcours=='CMI' and int(annee.split('_')[0])>=2024 and 'S4_Session1' in semestres: num_ue-=2;
###             list_ues = [ [x for x in z if x in list(pv_ind['results'].keys()) ] for z in UEs_maquette[semestre] ];
###             list_ues = [x for x in list_ues if set(x).issubset(set(pv_ind['results'].keys()))];
###             list_ues = [x for x in list_ues if len(x)==max([len(y) for y in list_ues])][0];
###             logger.debug("  > List UEs = " + str(list_ues));
###             etu_notes = GetNotes(pv_ind['results'], list_ues, num_ue, [moyenne_annee, moyenne_annee2], etu[0], semestre);
### 
###             ### Adding the line to the table
###             line_data = [[etu_id, header_semestre] + etu_notes];
###             t = Table(line_data, colWidths=[7*cm,3.7*cm]+[2.6*cm]*GetLength(semestres, parcours), style=line_style);
###             story.append(t);
### 
###     pv_file.build(story);
### 

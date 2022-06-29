##########################################################
###                                                    ###
###                    PV  Writer                      ###
###                                                    ###
##########################################################


##########################################################
###                                                    ###
###                       Logger                       ###
###                                                    ###
##########################################################
import logging;
logger = logging.getLogger('mylogger');


##########################################################
###                                                    ###
###                 Header of the file                 ###
###                                                    ###
##########################################################
from reportlab.lib.pagesizes import A4, landscape;
from reportlab.lib.units     import cm
from reportlab.platypus      import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles    import getSampleStyleSheet
def MakeTitle(annee, niveau, parcours, semestres):
    # file
    pv_file    = SimpleDocTemplate('output/'+annee+'_'+niveau+'_'+parcours + ".pdf", pagesize=landscape(A4),
      leftMargin=1.5*cm, rightMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm);

    # title
    story = [Paragraph('<para align="center"> PV ' + niveau + ' - ' + parcours + ' (' + \
       annee.replace('_','-') + ') : ' + ', '.join([x.split('_')[0] for x in semestres]) + '</para>',  getSampleStyleSheet()['Heading1'])];
    story.append(Spacer(1, 0.5*cm));

    # output
    return pv_file, story;


##########################################################
###                                                    ###
###                 Header of the file                 ###
###                                                    ###
##########################################################
from maquette                import Maquette, UEs, Irrelevant;
from reportlab.lib           import colors
from reportlab.platypus      import Table

# Nombre de colonnes du PV
def GetLength(semestres, parcours):
    tags_semestre = [x.split('_')[0] for x in semestres];
    num_ue = [[ x for x in Maquette.keys() if parcours in Maquette[x]['parcours'] and y in Maquette[x]['semestre'] and Maquette[x]['nom']!='MIN'] for y in tags_semestre];
    return max([ sum([ max([ len(ues) for ues in bloc])  for bloc in sem] ) for sem in [[(Maquette[x]['UE'] if Maquette[x]['nom']!='MIN' else [' ']) for x in z] for z in num_ue]]);

def MakeHeaders(semestres, parcours):
    # number of columns in the table
    num_ue = GetLength(semestres, parcours);
    if parcours=='MAJ' and semestres[0].startswith('S5'): num_ue+=2;
    if parcours=='MONO' and semestres[0].startswith('S5'): num_ue+=1;
    if parcours in ['DM', 'MAJ', 'DK'] and semestres[0].startswith('S3'): num_ue+=1;
    if parcours in ['DM'] and semestres[0].startswith('S5'): num_ue+=1;

    # The header themselves
    Headers = [[
        Paragraph('<para align="center"><b>Etudiant</b></para>', getSampleStyleSheet()["BodyText"]),
        Paragraph('<para align="center"><b>Moyennes</b></para>', getSampleStyleSheet()["BodyText"])
    ] + [ Paragraph('<para align="center"><b>UE #'+str(1+x)+'</b></para>', getSampleStyleSheet()["BodyText"]) for x in range(num_ue)]];

    # output
    return Table(Headers, colWidths=[7*cm,3.7*cm]+[2.6*cm]*(len(Headers[0])-2), style=[
            ('BACKGROUND', (0,0), ( len(Headers[0]), 0),   colors.khaki),
            ('GRID',       (0,0), (-1,-1),1, colors.black),
            ('BOX',        (0,0), (-1, 0),3, colors.black),
            ('BOX',        (1,0), ( 1,-1),3, colors.black),
            ('VALIGN',     (0,0), (-1, -1),  'MIDDLE'),
            ('ALIGN',      (0,0), (-1, -1),  'CENTER')
    ]);


##########################################################
###                                                    ###
###          Obtention et formattage des notes         ###
###                                                    ###
##########################################################
from pv_checker              import CheckValidation
# Calcul et formattage des moyennes semestrielles
def GetAverages(parcours, semestre, notes, blocs_maquette, moyenne_annee):

    ## Formatting session 1(colour)
    if notes['total']['note']=='ENCO': my_color='black';
    elif notes['total']['note']>=10. : my_color='black';
    elif moyenne_annee[0] > 10.      : my_color='orange'; 
    else                             : my_color='red'

    ## Formatting session 2 (colour)
    if 'note2'in notes['total'].keys():
        if notes['total']['note2']=='ENCO': my_color2='black';
        elif notes['total']['note2']>=10. : my_color2='black';
        elif moyenne_annee[1] > 10.       : my_color2='orange'; 
        else                              : my_color2='red'
    else: my_color2='black';

    ## Affichage moyennes
    sess1 = ''; sess2 = '';
    if notes['total']['note']!='ENCO':
        sess1  = '<b>' + semestre.replace('_Session1','') + ' :<br />  <font color=' + my_color + '>'+ '{:.3f}'.format(notes['total']['note']) + '/20</font></b>';
        sess1 += '<font color=\'grey\' size=\'8\'> (#'+notes['total']['ranking']+')</font>';
    else:
        sess1 = '<b>' + semestre.replace('_Session1','')  + ' :<br />  <font color=' + my_color + '>ENCO</font></b>';
    if 'note2' in notes['total'].keys():
        if notes['total']['note2']!='ENCO':
            sess2  = '<br /><b><font color=' + my_color2 + '>'+ '{:.3f}'.format(notes['total']['note2']) + '/20</font></b>';
            sess2 += '<font color=\'grey\' size=\'8\'> (#'+notes['total']['ranking2']+')</font>';
        else:
            sess2 = '<br /><b><font color=' + my_color2 + '>ENCO</font></b>';

    moyennes_string = '<para align="center">' + sess1 +  sess2 + '<br />';

    for bloc in sorted([x for x in list(blocs_maquette)],reverse=True):
        if parcours!='DM':
            nombloc  = Maquette[bloc]['nom'];
            notebloc = notes[bloc]['note'];
            if 'note2' in notes[bloc].keys(): notebloc = notes[bloc]['note2'];
        else:
            nombloc  = 'MAJ1' if 'PY' in bloc else 'MAJ2';
            notebloc = notes[semestre][nombloc][0]/notes[semestre][nombloc][1];
        colour = 'red' if notebloc<50 else 'black';
        moyennes_string += '<br />' + nombloc + ' :  <font color=\'' + colour + '\'>' + '{:.3f}'.format(notebloc) + '/100</font>';
    moyennes_string += '</para>';

    ## output
    return Paragraph(moyennes_string, getSampleStyleSheet()['BodyText']);



# Formattage des notes
from maquette import GrosSac, GrosSacP2;
def GetNotes(notes, ues, ncases, moyenne_annee):

    ## Initialisation
    notes_string = [];
    counter = 0;
    compensation = ( moyenne_annee>=10. or float(notes['total']['note'])>10.) if notes['total']['note']!= 'ENCO' else False;
    compensation2 = False;
    if 'note2' in notes['total'].keys(): compensation2 = ( moyenne_annee>=10. or float(notes['total']['note2'])>10.) if notes['total']['note']!= 'ENCO' else False;

    ## Boucle sur les UE
    for ue in (ues+[x for x in notes.keys() if (x in GrosSac.keys() or x in GrosSacP2.keys())and not x in ues] + [x for x in notes.keys() if x in Maquette.keys() and Maquette[x]['nom']=='MIN']  ):
        ### Enlever les notes de la mineure
        if ue+'_GS' in notes.keys(): continue
        if 'UE' in notes[ue].keys() and notes[ue]['UE']=='GrosSac': continue

        ### Note manquante
        if not ue in notes.keys():
            notes_string += [Paragraph('', getSampleStyleSheet()['BodyText'])];
            continue;

        # Mineure
        if ue.startswith('LU') and not ('PY' in ue or 'LV' in ue or ue in ['LU3ME010']): continue;
        if ue.startswith('L5PH') or ue.startswith('L3LACH') or ue.startswith('L6PH'): continue;

        ### Redoublant deja valide
        validation_tag = "<br /><font color='grey' size='8'>("+notes[ue]['annee_val']+')</font>' if notes[ue]['annee_val']!=None else '';

        ### Note session 2 + formattage
        current_note2='';
        if 'note2' in notes[ue].keys():
            my_note2 = notes[ue]['note2'];
            current_note2 = '{:.2f}'.format(my_note2)+'/100' if not my_note2 in ['ABI', 'DIS', 'COVID', 'ENCO', 'U VAC'] else my_note2.replace('COVID','???');
            if 'ranking2' in notes[ue].keys(): current_note2 += '<font color=\'grey\' size=\'7\'> [#'+notes[ue]['ranking2']+']</font>';

            fontcolor2 = 'black' if not my_note2 in ['ABI', 'COVID'] and (my_note2 in ['ENCO', 'DIS', 'U VAC'] or my_note2>=50.) else 'red';
            if fontcolor2=='red' and compensation2: fontcolor2='orange';

        ### Note session 1 + formattage
        my_note = notes[ue]['note'];
        current_note = '{:.2f}'.format(my_note)+'/100' if not my_note in ['ABI', 'DIS', 'COVID', 'ENCO', 'U VAC'] else my_note.replace('COVID','???');
        if 'ranking' in notes[ue].keys(): current_note += '<br /><font color=\'grey\' size=\'8\'>#'+notes[ue]['ranking']+'</font>';

        fontcolor = 'black' if not my_note in ['ABI', 'COVID'] and (my_note in ['ENCO', 'DIS', 'U VAC'] or my_note>=50.) else 'red';
        if fontcolor=='red' and compensation: fontcolor='orange';

        ### Result
        tmp_string= '<para align="center"><b>' + ue + '</b><br />' + \
             '<font color=\'grey\' size=\'8\'><super>[' + UEs[ue]['nom'].replace('0','') + ' - ' + str(UEs[ue]['ects']) + ' ECTS]</super></font><br />';
        if 'note2' in notes[ue].keys():
            current_note =  current_note.replace('<br />',' ').replace('#','[#').replace('</font>',']</font>').replace('8','7');
            tmp_string = tmp_string + '<font color=' + fontcolor + ' size=\'7\'>' + current_note + '</font><br />';
            tmp_string = tmp_string + '<font size = \'7\' color=' + fontcolor2 + '>' + current_note2 + '</font>'
        else:
            tmp_string = tmp_string + '<font color=' + fontcolor + '>' + current_note + '</font>';
        tmp_string = tmp_string + validation_tag + '</para>';

        notes_string+= [ Paragraph(tmp_string, getSampleStyleSheet()['BodyText'])];
        counter+=1;

    ## Ajout de cases blanches
    for i in range(ncases-counter): notes_string += [Paragraph('', getSampleStyleSheet()['BodyText'])];

    ## output
    return notes_string;


##########################################################
###                                                    ###
###                   Core  function                   ###
###                                                    ###
##########################################################
# Liste des etudiants
import itertools
def GetList(pv):
    liste_etudiants =  [ [ [y, x[y]['nom']] for y in x.keys() if y != 'resume'] for x in pv];
    liste_etudiants = [x for y in liste_etudiants for x in y];
    liste_etudiants.sort(key=lambda elem: elem[1]);
    return list(liste_etudiants for liste_etudiants, _ in itertools.groupby(liste_etudiants));


def GetLineStyle(counter, endline):
    # Common style
    line_style = [
       ('LINEBEFORE', (3,  0), ( -1, 0), 1, colors.black),
       ('LINEBEFORE', (0,  0), ( 2, 0), 3, colors.black),
       ('LINEAFTER', (-1, 0), (-1, 0), 3, colors.black),
       ('LINEBELOW', ( counter, 0), (-1, 0), 2-counter, colors.black),
       ('VALIGN',     (0,0), (-1, -1),  'MIDDLE'),
       ('ALIGN',      (0,0), (-1, -1),  'CENTER')
    ];

    # end of line
    if endline: line_style.append(('LINEBELOW', ( 0, 0), (-1, 0), 3, colors.black));

    # output
    return line_style;



from misc import GetBlocsMaquette, GetUEsMaquette;
def PDFWriter(pv, annee, niveau, parcours, semestres):

    # Title and headers
    pv_file, story =  MakeTitle(annee, niveau, parcours, semestres);
    story.append(MakeHeaders(semestres, parcours));

    # Liste des UE et blocs par semestre
    blocs_maquette = {}; UEs_maquette = {};
    for semestre in semestres:
        blocs_maquette[semestre] = GetBlocsMaquette(semestre.split('_')[0], parcours);

    # Etudiant data
    full = pv["full"]; del pv["full"];
    full2= pv["full2"]; del pv["full2"];
    for etu in GetList(pv.values()):
         # initialisation etudiant
         logger.debug("etudiant = " + str(etu));
         moyenne_annee = 0.; moyenne_annee2= 0.;

         ## Parcours
         my_parcours = parcours;
         if parcours in ['DM', 'MAJ', 'DK']:
             MIN=[];
             for sem in semestres:
                 if not etu[0] in pv[sem].keys():continue;
                 try:    MIN = MIN + [ x for x in pv[sem][etu[0]]['results'].keys() if x in Maquette.keys() and Maquette[x]['nom']=='MIN'];
                 except: MIN = [''];
             logger.debug("  > Parcours = "  + str(MIN))
             if parcours=='MAJ':
                 try:    my_parcours = 'MajPhys - ' + UEs[MIN[-1]]['nom'][:-1];
                 except: my_parcours = 'MajPhys';
             elif parcours in ['DK', 'DM']:
                 try:    my_parcours = parcours + ' Phys - ' + UEs[MIN[-1]]['nom'][3:-1];
                 except: my_parcours = parcours + ' Phys';
         logger.debug("  > Parcours = " + my_parcours);

         ## Blocs disciplinaire
         disc = '';
         if parcours in 'DM':
             all_sems = [x for x in pv.keys() if etu[0] in pv[x].keys() and 'Session1' in x];
             maj1=0; maj2=0;
             coe1=0; coe2=0;
             for sem in all_sems:
                 maj1 = maj1 + pv[sem][etu[0]]['results'][sem]['MAJ1'][0];
                 maj2 = maj2 + pv[sem][etu[0]]['results'][sem]['MAJ2'][0];
                 coe1 = coe1 + pv[sem][etu[0]]['results'][sem]['MAJ1'][1];
                 coe2 = coe2 + pv[sem][etu[0]]['results'][sem]['MAJ2'][1];
             maj1 = maj1/coe1; maj2 = maj2/coe2;
             col1 = 'red' if maj1 < 50 else 'black';
             col2 = 'red' if maj2 < 50 else 'black';
             if maj1 < 50: logger.warning(etu[1] + " (" + str(etu[0]) + ")] : Bloc Phys non valide [" + '{:.3f}'.format(maj1) + '/100]');
             if maj2 < 50: logger.warning(etu[1] + " (" + str(etu[0]) + ")] : Bloc " +  UEs[MIN[-1]]['nom'][3:-1] + " non valide [" + '{:.3f}'.format(maj2) + '/100]');

             disc =  '<br />MAJ1 : <font color=' + col1 + '> ' + '{:.3f}'.format(maj1) + '/100</font>' + \
                     '<br />MAJ2 : <font color=' + col2 + '> ' + '{:.3f}'.format(maj2) + '/100</font>';


         ## Header etudiant
         etu_id = Paragraph('<para align="center"><b>' + etu[1] + '<br />' + str(etu[0]) + '</b><br /><br />' + my_parcours + '</para>',getSampleStyleSheet()['BodyText']);
         nbr_semestres = len([y for y in [etu[0] in pv[x].keys() for x in semestres] if y]);
         max_semestres = nbr_semestres;
         logger.debug("  > " + str(nbr_semestres) + ' semestre(s) disponible(s)');

         ## Calcul de la moyenne annuelle
         moyennes = {};
         colour_annee = 'black';
         if full[str(etu[0])] !='ENCO':
             moyenne_annee = full[str(etu[0])][0];
             colour_annee      = 'red' if moyenne_annee<10 else 'black';
         logger.debug("  > Session1 : " + str(moyenne_annee) + ' (' + colour_annee + ')');
         if full2[str(etu[0])] !='ENCO':
             moyenne_annee2 = full2[str(etu[0])][0];
             colour_annee2      = 'red' if moyenne_annee2<10 else 'black';
         if moyenne_annee!=moyenne_annee2: logger.debug("  Session 2 : > " + str(moyenne_annee2) + ' (' + colour_annee2 + ')');

         ## Real loop over the semesters
         for semestre in semestres:
            ### safety
            if not etu[0] in pv[semestre].keys(): continue;

            ### PV individuel
            pv_ind = pv[semestre][etu[0]];
            blocs_maq = [x for x in blocs_maquette[semestre] if not x in [x for x in UEs if x.startswith('LK')] or x in pv_ind['results'].keys()];
            UEs_maquette[semestre]   = GetUEsMaquette(blocs_maq);

            ### First cell of the table
            dep = 0 if nbr_semestres==1 else 1; nbr_semestres-=1;
            line_style = GetLineStyle(dep, semestre==semestres[-1] and etu == GetList(pv.values())[-1]);

            sess1=''; sess2='';
            if full[str(etu[0])]=='ENCO':
                sess1 = '<b>Session1 = <font color=' + colour_annee + '>ENCO</font></b>';
            else:
                sess1 =  '<b>Session1 = <font color=' + colour_annee + '>' + \
                     '{:.3f}'.format(moyenne_annee) + '/20</font></b><font color=\'grey\' size=\'9\'> (#' + full[str(etu[0])][1] +\
                     ')</font>';

            if moyenne_annee!=moyenne_annee2 and full2[str(etu[0])]=='ENCO':
                sess2 = '<b>Session2 = <font color=' + colour_annee + '>' + 'ENCO</font></b>';
            elif moyenne_annee!=moyenne_annee2:
                sess2 =  '<b>Session2 = <font color=' + colour_annee2 + '>' + \
                     '{:.3f}'.format(moyenne_annee2) + '/20</font></b><font color=\'grey\' size=\'9\'> (#' + full2[str(etu[0])][1] +\
                     ')</font>';

            if dep==0 and nbr_semestres==(max_semestres-1):
                etu_id = [etu_id, Paragraph('<para align="center">' + sess1 + '<br />' + sess2 + disc + '</para>', getSampleStyleSheet()['BodyText'])];
            elif dep==0:
                etu_id = [Paragraph('<para align="center"><br /></para>',getSampleStyleSheet()['BodyText']), \
                          Paragraph('<para align="center">' + sess1 + '<br />' + sess2 + disc + '</para>', getSampleStyleSheet()['BodyText'])];


            ### Second cell of the table
            header_semestre = GetAverages(parcours, semestre, pv_ind['results'], blocs_maq, [moyenne_annee, moyenne_annee2]);

            ### Notes des UE
            num_ue = GetLength(semestres, parcours);
            if parcours=='MONO' and semestres[0].startswith('S5'): num_ue+=1;
            if parcours=='MAJ' and semestres[0].startswith('S5'): num_ue+=2;
            if parcours in ['MAJ','DM', 'DK'] and semestres[0].startswith('S3'): num_ue+=1;
            if parcours in ['DM'] and semestres[0].startswith('S5'): num_ue+=1;
            list_ues = [ [x for x in z if x in list(pv_ind['results'].keys()) ] for z in UEs_maquette[semestre] ];
            list_ues = [x for x in list_ues if set(x).issubset(set(pv_ind['results'].keys()))];
            list_ues = [x for x in list_ues if len(x)==max([len(y) for y in list_ues])][0];
            logger.debug("  > List UEs = " + str(list_ues));
            etu_notes = GetNotes(pv_ind['results'], list_ues, num_ue, moyenne_annee);

            ### Adding the line to the table
            line_data = [[etu_id, header_semestre] + etu_notes];
            t = Table(line_data, colWidths=[7*cm,3.7*cm]+[2.6*cm]*GetLength(semestres, parcours), style=line_style);
            story.append(t);

    pv_file.build(story);


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
       annee.replace('_','-') + ') : ' + ', '.join(semestres) + '</para>',  getSampleStyleSheet()['Heading1'])];
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
    if parcours in ['DM', 'MAJ'] and semestres[0].startswith('S3'): num_ue+=1;
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
def GetAverages(semestre, notes, blocs_maquette, moyenne_annee):

    ## Formatting (colour)
    if notes['total']['note']=='ENCO': my_color='black';
    elif notes['total']['note']>=10.: my_color='black';
    elif moyenne_annee > 10.    : my_color='orange'; 
    else                        : my_color='red'

    ## Affichage moyennes
    if notes['total']['note']!='ENCO':
        moyennes_string = '<para align="center"><b>' + semestre + ':  <font color=' + my_color + '>'+ '{:.3f}'.format(notes['total']['note']) + '/20</font></b>';
        moyennes_string += '<font color=\'grey\' size=\'8\'> (#'+notes['total']['ranking']+')</font><br />';
    else:
        moyennes_string = '<para align="center"><b>' + semestre + ':  <font color=' + my_color + '>ENCO</font></b><br />';

    for bloc in sorted([x for x in list(blocs_maquette) if 'PY' in x],reverse=True):
        nombloc = Maquette[bloc]['nom'] if Maquette[bloc]['parcours'][0]!='DM' else Maquette[bloc]['nom'].replace("MIN","MAJ2");
        moyennes_string += '<br />' + nombloc + ' :  ' + '{:.3f}'.format(notes[bloc]['note']) + '/100';
    for bloc in sorted([x for x in list(blocs_maquette) if not 'PY' in x],reverse=True):
        nombloc = Maquette[bloc]['nom'] if Maquette[bloc]['parcours'][0]!='DM' else Maquette[bloc]['nom'].replace("MIN","MAJ2");
        moyennes_string += '<br />' + nombloc + ' :  ' + '{:.3f}'.format(notes[bloc]['note']) + '/100';
    moyennes_string += '</para>';

    ## output
    return Paragraph(moyennes_string, getSampleStyleSheet()['BodyText']);



# Formattage des notes
from maquette import GrosSac, GrosSacP2;
def GetNotes(notes, ues, ncases, moyenne_annee):

    ## Initialisation
    notes_string = [];
    counter = 0;
    if notes['total']['note']!= 'ENCO':
        compensation = (moyenne_annee>=10.) or float(notes['total']['note'])>10.;
    else: compensation = False;

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
        if ue.startswith('LU') and not ('PY' in ue or 'LV' in ue): continue;
        if ue.startswith('L5PH') or ue.startswith('L3LACH') or ue.startswith('L6PH'): continue;

        ### Redoublant deja valide
        validation_tag = "<br /><font color='grey' size='8'>("+notes[ue]['annee_val']+')</font>' if notes[ue]['annee_val']!=None else '';

        ### Note elle-meme
        my_note = notes[ue]['note'];
        current_note = '{:.2f}'.format(my_note)+'/100' if not my_note in ['ABI', 'DIS', 'COVID', 'ENCO', 'U VAC'] else my_note.replace('COVID','???');
        if 'ranking' in notes[ue].keys(): current_note += '<br /><font color=\'grey\' size=\'8\'>#'+notes[ue]['ranking']+'</font>';

        ### Formattage
        fontcolor = 'black' if not my_note in ['ABI', 'COVID'] and (my_note in ['ENCO', 'DIS', 'U VAC'] or my_note>=50.) else 'red';
        if fontcolor=='red' and compensation: fontcolor='orange';

        ### Result
        notes_string+= [ Paragraph('<para align="center"><b>' + ue + '</b><br />' + \
             '<font color=\'grey\' size=\'8\'><super>[' + UEs[ue]['nom'].replace('0','') + ' - ' + str(UEs[ue]['ects']) + ' ECTS]</super></font><br />' + \
            '<font color=' + fontcolor + '>' + current_note + '</font>'+validation_tag+'</para>', getSampleStyleSheet()['BodyText'])];
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
    for etu in GetList(pv.values()):
         # initialisation etudiant
         logger.debug("etudiant = " + str(etu));
         moyenne_annee = 0.;

         ## Parcours
         my_parcours = parcours;
         if parcours in ['DM', 'MAJ']:
             MIN=[];
             for sem in semestres:
                 if not etu[0] in pv[sem].keys():continue;
                 try:    MIN = MIN + [ x for x in pv[sem][etu[0]]['results'].keys() if x in Maquette.keys() and Maquette[x]['nom']=='MIN'];
                 except: MIN = [''];
             logger.debug("  > Parcours = "  + str(MIN))
             if parcours=='MAJ':
                 try:    my_parcours = 'MajPhys - ' + UEs[MIN[-1]]['nom'][:-1];
                 except: my_parcours = 'MajPhys';
             elif parcours=='DM':
                 try:    my_parcours = 'DM Phys - ' + UEs[MIN[-1]]['nom'][3:-1];
                 except: my_parcours = 'DM Phys';
         logger.debug("  > Parcours = " + my_parcours);

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
         logger.debug("  > " + str(moyenne_annee) + ' (' + colour_annee + ')');

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
            if full[str(etu[0])] !='ENCO':
                if dep==0 and nbr_semestres==(max_semestres-1):
                    etu_id = [etu_id, Paragraph('<para align="center"><b>Session1 = <font color=' + colour_annee + '>' + '{:.3f}'.format(moyenne_annee) + \
                      '/20</font></b><font color=\'grey\' size=\'9\'> (#' + full[str(etu[0])][1] + ')</font></para>', getSampleStyleSheet()['BodyText'])];
                elif dep==0:
                    etu_id = [Paragraph('<para align="center"><br /></para>',getSampleStyleSheet()['BodyText']), \
                              Paragraph('<para align="center"><b>Session1 = <font color=' + colour_annee + '>' + '{:.3f}'.format(moyenne_annee) + \
                              '/20</font></b><font color=\'grey\' size=\'9\'> (#' + full[str(etu[0])][1] + ')</font></para>', getSampleStyleSheet()['BodyText'])
                    ];
            else:
                if dep==0 and nbr_semestres==(max_semestres-1):
                    etu_id = [etu_id, Paragraph('<para align="center"><b>Session1 = <font color=' + colour_annee + '>ENCO</font></b></para>', getSampleStyleSheet()['BodyText'])];
                elif dep==0:
                    etu_id = [Paragraph('<para align="center"><br /></para>',getSampleStyleSheet()['BodyText']), \
                              Paragraph('<para align="center"><b>Session1 = <font color=' + colour_annee + '>ENCO</font></b></para>', getSampleStyleSheet()['BodyText'])
                    ];

            ### Second cell of the table
            header_semestre = GetAverages(semestre, pv_ind['results'], blocs_maq, moyenne_annee);

            ### Notes des UE
            num_ue = GetLength(semestres, parcours);
            if parcours=='MONO' and semestres[0].startswith('S5'): num_ue+=1;
            if parcours=='MAJ' and semestres[0].startswith('S5'): num_ue+=2;
            if parcours in ['MAJ','DM'] and semestres[0].startswith('S3'): num_ue+=1;
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

    ## # Summary headers
    ## story.append(Spacer(1, 1*cm));
    ## story.append(Paragraph('<u>Statistiques</u>', getSampleStyleSheet()['Heading2']));
    ## Headers = [[ Paragraph('<para align="center"><b>'+ x + '</b></para>', getSampleStyleSheet()["BodyText"]) for x in semestres]];
    ## story.append(Table(Headers, [7.5*cm]*len(semestres), style=[
    ##         ('BACKGROUND', (0,0), (-1, 0),   colors.khaki),
    ##         ('BOX',        (0,0), (-1, 0),2, colors.black),
    ##         ('BOX',        (1,0), ( 1,-1),2, colors.black),
    ##         ('VALIGN',     (0,0), (-1, -1),  'MIDDLE'),
    ##         ('ALIGN',      (0,0), (-1, -1),  'CENTER')
    ## ]));

    ## # getting summary data
    ## sums_str = []; adm_str = []; comp_str = []; fail_str = []; null_str = [];
    ## for s in semestres:
    ##     sums = [[pv[s][x]['results']['00-total']['note'], compensation[s][x] ] for x in pv[s].keys() if isinstance(x, int)];
    ##     adm  = len ([x for x in sums if x[0]!=None and float(x[0])>=10. and not x[1] ]);
    ##     comp = len ([x for x in sums if x[0]!=None and float(x[0])>=10. and x[1] ]);
    ##     fail = len ([x for x in sums if x[0]!=None and float(x[0])<10.]);
    ##     null = len(sums)-adm-comp-fail;

    ##     # formatting
    ##     adm_str.append (Paragraph('  * ' + str(adm) + ' admis ('          + '{:.2f}'.format(100* adm/len(sums))+'%)', getSampleStyleSheet()['Heading4']));
    ##     comp_str.append(Paragraph('  * ' + str(comp)+ ' compenses ('      + '{:.2f}'.format(100*comp/len(sums))+'%)', getSampleStyleSheet()['Heading4']));
    ##     fail_str.append(Paragraph('  * ' + str(fail)+ ' ajournes ('       + '{:.2f}'.format(100*fail/len(sums))+'%)', getSampleStyleSheet()['Heading4']));
    ##     null_str.append(Paragraph('  * ' + str(null)+ ' sans resultats (' + '{:.2f}'.format(100*null/len(sums))+'%)', getSampleStyleSheet()['Heading4']));

    ## # adding the lines to the table
    ## my_style =  [ ('LINEAFTER', (0,0), (-1,-1),2, colors.black), ('LINEBEFORE', (0,0), (-1,-1),2, colors.black) ];
    ## story.append(Table([ adm_str], [7.5*cm]*len(semestres),style=my_style));
    ## story.append(Table([comp_str], [7.5*cm]*len(semestres),style=my_style));
    ## story.append(Table([fail_str], [7.5*cm]*len(semestres),style=my_style));
    ## my_style.append(('LINEBELOW', (0,0), (-1,-1),2, colors.black));
    ## story.append(Table([null_str], [7.5*cm]*len(semestres),style=my_style));

    # printing 
    pv_file.build(story);


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
    num_ue = [[ x for x in Maquette.keys() if parcours in Maquette[x]['parcours'] and y in Maquette[x]['semestre']] for y in tags_semestre];
    return max([ sum([ max([ len(ues) for ues in bloc])  for bloc in sem] ) for sem in [[(Maquette[x]['UE'] if Maquette[x]['nom']!='MIN' else [' ']) for x in z] for z in num_ue]]);

def MakeHeaders(semestres, parcours):
    # number of columns in the table
    num_ue = GetLength(semestres, parcours);

    # The header themselves
    Headers = [[
        Paragraph('<para align="center"><b>Etudiant</b></para>', getSampleStyleSheet()["BodyText"]),
        Paragraph('<para align="center"><b>Moyennes</b></para>', getSampleStyleSheet()["BodyText"])
    ] + [ Paragraph('<para align="center"><b>UE #'+str(1+x)+'</b></para>', getSampleStyleSheet()["BodyText"]) for x in range(num_ue)]];

    # output
    return Table(Headers, colWidths=[7*cm,3.7*cm]+[2.4*cm]*(len(Headers[0])-2), style=[
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
    if notes['total']['note']>=10.: my_color='black';
    elif moyenne_annee > 10.    : my_color='orange'; 
    else                        : my_color='red'

    ## Affichage moyennes
    moyennes_string = '<para align="center"><b>' + semestre + ':  <font color=' + my_color + '>'+ '{:.3f}'.format(notes['total']['note']) + '/20</font></b><br />';
    for bloc in sorted(list(blocs_maquette),reverse=True):
        moyennes_string += '<br />' + Maquette[bloc]['nom'] + ' :  ' + '{:.3f}'.format(notes[bloc]['note']) + '/100';
    moyennes_string += '</para>';

    ## output
    return Paragraph(moyennes_string, getSampleStyleSheet()['BodyText']);



# Formattage des notes
from maquette import Ignore;
def GetNotes(notes, ues, ncases, moyenne_annee):

    ## Initialisation
    notes_string = [];
    counter = 0;
    compensation = (moyenne_annee>=50.) or float(notes['total']['note'])>50.;

    ## Boucle sur les UE
    for ue in ues:

        ### Enlever les notes de la mineure
        if ue in Ignore: continue

        ### Note manquante
        if not ue in notes.keys():
            notes_string += [Paragraph('', getSampleStyleSheet()['BodyText'])];
            continue;

        ### Redoublant deja valide
        validation_tag = "<br /><font color='grey'>("+notes[ue]['annee_val']+')</font>' if notes[ue]['annee_val']!=None else '';

        ### Note elle-meme
        my_note = notes[ue]['note'];
        current_note = str(my_note)+'/100' if not my_note in ['ABI', 'DIS'] else my_note;

        ### Formattage
        fontcolor = 'black' if my_note!='ABI' and (my_note=='DIS' or my_note>=50.) else 'red';
        if fontcolor=='red' and compensation: fontcolor='orange';

        ##  ANCIENNE MAQUETTE - - - SIMPLFICIATION EFFECTUEE - - - A SUPPRIMER A UN MOMENT - - - TAG BENJ
        ## ### Mineure
        ## if 'PYMI0' in ue: my_note = my_note.replace('PYMI0', list(set([x[3:5] for x in maquette if not 'PY' in x and not 'LV' in x]))[0]+'M00').replace('HMM','PHM');

        ### Result
        notes_string+= [ Paragraph('<para align="center"><b>' + ue + '</b><br />' + \
             '<font color=\'grey\' size=\'8\'><super>[' + UEs[ue]['nom'].replace('0','') + ']</super></font><br />' + \
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


from collections.abc import Iterable
def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

import itertools;
def PDFWriter(pv, annee, niveau, parcours, semestres):

    # Title and headers
    pv_file, story =  MakeTitle(annee, niveau, parcours, semestres);
    story.append(MakeHeaders(semestres, parcours));

    # Liste des UE et blocs par semestre
    blocs_maquette = {}; UEs_maquette = {};
    for semestre in semestres:
        blocs_maquette[semestre] = sorted([x for x in Maquette.keys() if parcours in Maquette[x]['parcours'] and semestre.split('_')[0] in Maquette[x]['semestre']]);
        length = len( [Maquette[x]['UE'] for x in blocs_maquette[semestre] ] );
        UEs_maquette[semestre] = [Maquette[x]['UE'] for x in blocs_maquette[semestre] ][length-1];
        while length>1:
            UEs_maquette[semestre] = [sorted(list(flatten(x))) for  x in itertools.product(UEs_maquette[semestre], [Maquette[x]['UE'] for x in blocs_maquette[semestre]][length-2])];
            length-=1;

    # Etudiant data
    for etu in GetList(pv.values()):
         # initialisation etudiant
         logger.debug("etudiant = " + str(etu));
         moyenne_annee = 0.;

         ## Parcours
         my_parcours = parcours;
         if parcours == 'MAJ':
             MIN=[];
             for sem in semestres:
                 try:    MIN = MIN + [UEs[x['UE']]['nom'] for x in pv[sem][etu[0]]['results'].values() if 'UE' in x.keys() and x['UE']!=None];
                 except: MIN = [''];
             my_parcours = 'MajPhys - ' + MIN[-1][:-1];
         logger.debug("  > Parcours = " + my_parcours);

         ## Header etudiant
         etu_id = Paragraph('<para align="center"><b>' + etu[1] + '<br />' + str(etu[0]) + '</b><br /><br />' + my_parcours + '</para>',getSampleStyleSheet()['BodyText']);
         nbr_semestres = len([y for y in [etu[0] in pv[x].keys() for x in semestres] if y]);
         logger.debug("  > " + str(nbr_semestres) + ' semestre(s) disponible(s)');

         ## Calcul de la moyenne annuelle
         moyennes = {};
         for semestre in semestres:
            ### safety
            if not etu[0] in pv[semestre].keys(): continue;

            ### Calcul de la moyenne
            moyenne_annee += pv[semestre][etu[0]]['results']['total']['note']/nbr_semestres;
            colour_annee      = 'red' if moyenne_annee<10 else 'black';
            logger.debug("  > " + str(moyenne_annee) + ' (' + colour_annee + ')');

         ## Real loop over the semesters
         for semestre in semestres:
            ### safety
            if not etu[0] in pv[semestre].keys(): continue;

            ### PV individuel
            pv_ind = pv[semestre][etu[0]];

            ### First cell of the table
            dep = 0 if nbr_semestres==1 else 1; nbr_semestres-=1;
            line_style = GetLineStyle(dep, semestre==semestres[-1] and etu == GetList(pv.values())[-1]);
            if dep==0: etu_id = [etu_id, Paragraph('<para align="center"><b>Session1 = <font color=' + colour_annee + '>' + '{:.3f}'.format(moyenne_annee) + \
                  '/20</font></b></para>', getSampleStyleSheet()['BodyText'])];

            ### Second cell of the table
            header_semestre = GetAverages(semestre, pv_ind['results'], blocs_maquette[semestre], moyenne_annee);

            ### Notes des UE
            etu_notes = GetNotes(pv_ind['results'], UEs_maquette[semestre][0], GetLength(semestres,parcours), moyenne_annee);

            ### Adding the line to the table
            line_data   = [[etu_id, header_semestre] + etu_notes];
            t = Table(line_data, colWidths=[7*cm,3.7*cm]+[2.4*cm]*GetLength(semestres, parcours), style=line_style);
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


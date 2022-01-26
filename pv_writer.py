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
# Obtention des notes
def GetNotes(etudiant, pv, blocs_maquette):

    # initialisation
    notes = {}; validation = {};
    compensation = False;

    # note UEs
    for label, UE in pv['results'].items():
        if not 'UE' in UE.keys():       continue;
        if UE['UE'] == None and label.split('-')[-1] in UEs.keys(): UE['UE']=label.split('-')[-1];
        if UE['UE'] != None:            notes[UE['UE']] = CheckValidation(UE, str(etudiant), pv['nom'], Silent=True);
        if 'ABI' in UE.keys():          notes[UE['UE']]='ABI';
        if UE['validation'] == 'U ADM': validation[UE['UE']] = UE['annee_val'];
        if UE['validation'] == 'VAC'  : validation[UE['UE']] = 'VAC';

    # moyennes par blocs
    moyenne_tot  = 0.; coeff_tot = 0.; color_blocs = {};
    for bloc in blocs_maquette:
        try:
            id_ue  = [ set(x).issubset(set(notes.keys())) for x in Maquette[bloc]['UE']].index(True);
        except:
            id_ue=0
        moyenne_bloc = 0.; coeff_bloc   = 0.;
        color_blocs[bloc] = 'black'
        for ue in Maquette[bloc]['UE'][id_ue]:
            # safety
            if not ue in notes.keys(): continue;

            # Getting the note
            if notes[ue]=='DIS': continue;
            note = notes[ue] if notes[ue]!='ABI' else 0;
            moyenne_bloc += note*UEs[ue]['ects']*(1.-float(ue in Irrelevant));
            coeff_bloc   += UEs[ue]['ects'] * (1.-float(ue in Irrelevant));
            moyenne_tot  += note*UEs[ue]['ects'];
            coeff_tot    += UEs[ue]['ects'];
            if note<50. and not ue in Irrelevant: color_blocs[bloc]  = 'orange';
            if note<50.: compensation = True;
        if coeff_bloc!=0:
            notes[bloc] = round(moyenne_bloc/coeff_bloc,3)

    # moyennes finales
    if coeff_tot!=0 and moyenne_tot!=0:
        notes['total']       = float(pv['results']['00-total']['note']) if notes=={} else round(moyenne_tot/coeff_tot/5.,3);
    else:
        notes['total']=0.;
    color_blocs['total'] = 'red' if notes['total']<10. else 'black';

    # output 
    return compensation, notes, color_blocs, validation;


# Calcul et formattage des moyennes
def GetAverages(semestre, notes, comp_annuelle, blocs_maquette, color_blocs):
    #formatting
    mycolor = color_blocs['total'];
    if mycolor=='red' and comp_annuelle:
        mycolor='orange'
    moyennes_string = '<para align="center"><b>' + semestre + ':  <font color=' + mycolor + '>'+ \
      '{:.3f}'.format(notes['total']) + '/20</font></b><br />';
    for bloc in sorted(list(blocs_maquette[semestre]),reverse=True):
        if not bloc in notes.keys(): continue;
        moyennes_string += '<br />' + Maquette[bloc]['nom'] + ' :  ' + '{:.3f}'.format(notes[bloc]) + '/100';
    moyennes_string += '</para>';
    #output
    return Paragraph(moyennes_string, getSampleStyleSheet()['BodyText']);


# Formattage des notes
from maquette import Ignore;
def Formattage(notes, validations, compensation, maquette, ncases):
    # initialisation
    notes_string = [];
    # Formattage des notes individuelles
    counter = 0;

    for note in maquette:
        # Enlever les notes de la mineure
        if note in Ignore: continue

        if not note in notes.keys():
            notes_string += [Paragraph('', getSampleStyleSheet()['BodyText'])];
            continue;
        # info validation
        validation_tag = "<br /><font color='grey'>("+validations[note]+')</font>' if note in validations.keys() else '';
        # info notes
        current_note = str(notes[note])+'/100' if not notes[note] in ['ABI', 'DIS'] else notes[note];
        # font color
        fontcolor = 'black' if notes[note]!='ABI' and (notes[note]=='DIS' or notes[note]>=50.) else 'red';
        if fontcolor=='red' and compensation:
            fontcolor='orange';
        # Mineure
        if 'PYMI0' in note: note = note.replace('PYMI0', list(set([x[3:5] for x in maquette if not 'PY' in x and not 'LV' in x]))[0]+'M00').replace('HMM','PHM');
        #result
        notes_string+= [ Paragraph('<para align="center"><b>' + note + '</b><br />' + \
             '<font color=\'grey\' size=\'8\'><super>[' + UEs[note]['nom'].replace('0','') + ']</super></font><br />' + \
            '<font color=' + fontcolor + '>' + current_note + '</font>'+validation_tag+'</para>', getSampleStyleSheet()['BodyText'])];
        counter+=1;

    # nombre de cases blanches
    for i in range(ncases-counter):
        notes_string += [Paragraph('', getSampleStyleSheet()['BodyText'])];

    # output
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
    # Initialisation
    compensation = {}; blocs_maquette = {}; UEs_maquette = {};
    for semestre in semestres:
        compensation[semestre]   = {};
        blocs_maquette[semestre] = sorted([x for x in Maquette.keys() \
           if parcours in Maquette[x]['parcours'] and semestre.split('_')[0] in Maquette[x]['semestre']]);
        length = len( [Maquette[x]['UE'] for x in blocs_maquette[semestre] ] );
        UEs_maquette[semestre] = [Maquette[x]['UE'] for x in blocs_maquette[semestre] ][length-1];
        while length>1:
            UEs_maquette[semestre] = [sorted(list(flatten(x))) for  x in itertools.product(UEs_maquette[semestre], [Maquette[x]['UE'] for x in blocs_maquette[semestre]][length-2])];
            length-=1;

    # Title and headers
    pv_file, story =  MakeTitle(annee, niveau, parcours, semestres);
    story.append(MakeHeaders(semestres, parcours));

    # Etudiant data
    for etudiant in GetList(pv.values()):
        # initialisation etudiant
        my_parcours = parcours;
        if parcours == 'MAJ':
            MIN=[];
            for sem in semestres:
                try:
                   MIN = MIN + [UEs[x['UE']]['nom'] for x in pv[sem][etudiant[0]]['results'].values() if 'UE' in x.keys() and x['UE']!=None];
                except: MIN =[''];
            my_parcours = 'MajPhys - ' + MIN[-1][:-1];
        etudiant_id = Paragraph('<para align="center"><b>' + etudiant[1] + '<br />' + \
            str(etudiant[0]) + '</b><br /><br />' + my_parcours + '</para>',getSampleStyleSheet()['BodyText']);
        nbr_semestres = len([y for y in [etudiant[0] in pv[x].keys() for x in semestres] if y]);

        # Calcul de la moyenne annuelle
        moyennes = {};
        for semestre in semestres:
            # safety
            if not etudiant[0] in pv[semestre].keys(): continue;

            # Obtention des notes et des moyennes
            compensation[semestre][etudiant[0]], notes, color_blocs, validations  = \
               GetNotes(etudiant[0], pv[semestre][etudiant[0]], blocs_maquette[semestre]);
            etudiant_moyennes = GetAverages(semestre, notes, False, blocs_maquette, color_blocs);
            moyennes[semestre] = notes['total'];

        # boucle principale sur les semestres
        for semestre in semestres:
            # safety
            if not etudiant[0] in pv[semestre].keys(): continue;

            # Obtention des notes et des moyennes
            compensation[semestre][etudiant[0]], notes, color_blocs, validations  = \
               GetNotes(etudiant[0], pv[semestre][etudiant[0]], blocs_maquette[semestre]);

            # Filling + formatting the line in the table
            comp_annuelle = False;
            dep = 0 if nbr_semestres==1 else 1; nbr_semestres-=1;
            line_style = GetLineStyle(dep, semestre==semestres[-1] and etudiant == GetList(pv.values())[-1]);
            if 'S3_Session1' in moyennes.keys() and 'S4_Session1' in moyennes.keys():
                L2  = (moyennes['S3_Session1']+moyennes['S4_Session1'])/2.;
                if L2>=10.:
                    comp_annuelle=True;
                if dep==0:
                    col = 'red' if L2<10 else 'black';
                    etudiant_id = [etudiant_id, Paragraph('<para align="center"><b>L2 (Session1) = <font color=' + col + '>' + \
                      '{:.3f}'.format(L2) + '/20</font></b></para>', getSampleStyleSheet()['BodyText'])];

            etudiant_moyennes = GetAverages(semestre, notes, comp_annuelle, blocs_maquette, color_blocs);
            try:
                id_ue  = [ set(x).issubset(set(notes.keys())) for x in UEs_maquette[semestre]].index(True);
            except:
                id_ue = -1;
                logger.error('Maquette inconnue pour l\'etudiant ' + str(etudiant[0]) + ' (' + etudiant[1] + ')');
                logger.error('  [  ' + ','.join(notes.keys()) + '  ]');
                continue;

            # Formattage des notes
            all_blocs = sorted([x for x in Maquette.keys() if parcours in Maquette[x]['parcours']]);
            blocs_pv       = [];
            for bloc in all_blocs:
                for set_ue in Maquette[bloc]['UE']:
                    if True in [ set(x).issubset(set(list(notes.keys()))) for x in Maquette[bloc]['UE']] and not bloc in blocs_pv: blocs_pv.append(bloc)
            blocs_pv = sorted( UEs_maquette[semestre][id_ue] +  [x for x in blocs_pv if (Maquette[x]['nom']=='MIN' and semestre.split('_')[0]==Maquette[x]['semestre'])]);
            etudiant_notes = Formattage(notes, validations, (comp_annuelle or notes['total']>=10.), blocs_pv, GetLength(semestres,parcours));
            line_data   = [[etudiant_id, etudiant_moyennes] + etudiant_notes ];
            etudiant_id = Paragraph('', getSampleStyleSheet()['BodyText']);

            # Adding the line
            t = Table(line_data, colWidths=[7*cm,3.7*cm]+[2.4*cm]*GetLength(semestres, parcours), style=line_style);
            story.append(t);

    # Summary headers
    story.append(Spacer(1, 1*cm));
    story.append(Paragraph('<u>Statistiques</u>', getSampleStyleSheet()['Heading2']));
    Headers = [[ Paragraph('<para align="center"><b>'+ x + '</b></para>', getSampleStyleSheet()["BodyText"]) for x in semestres]];
    story.append(Table(Headers, [7.5*cm]*len(semestres), style=[
            ('BACKGROUND', (0,0), (-1, 0),   colors.khaki),
            ('BOX',        (0,0), (-1, 0),2, colors.black),
            ('BOX',        (1,0), ( 1,-1),2, colors.black),
            ('VALIGN',     (0,0), (-1, -1),  'MIDDLE'),
            ('ALIGN',      (0,0), (-1, -1),  'CENTER')
    ]));

    # getting summary data
    sums_str = []; adm_str = []; comp_str = []; fail_str = []; null_str = [];
    for s in semestres:
        sums = [[pv[s][x]['results']['00-total']['note'], compensation[s][x] ] for x in pv[s].keys() if isinstance(x, int)];
        adm  = len ([x for x in sums if x[0]!=None and float(x[0])>=10. and not x[1] ]);
        comp = len ([x for x in sums if x[0]!=None and float(x[0])>=10. and x[1] ]);
        fail = len ([x for x in sums if x[0]!=None and float(x[0])<10.]);
        null = len(sums)-adm-comp-fail;

        # formatting
        adm_str.append (Paragraph('  * ' + str(adm) + ' admis ('          + '{:.2f}'.format(100* adm/len(sums))+'%)', getSampleStyleSheet()['Heading4']));
        comp_str.append(Paragraph('  * ' + str(comp)+ ' compenses ('      + '{:.2f}'.format(100*comp/len(sums))+'%)', getSampleStyleSheet()['Heading4']));
        fail_str.append(Paragraph('  * ' + str(fail)+ ' ajournes ('       + '{:.2f}'.format(100*fail/len(sums))+'%)', getSampleStyleSheet()['Heading4']));
        null_str.append(Paragraph('  * ' + str(null)+ ' sans resultats (' + '{:.2f}'.format(100*null/len(sums))+'%)', getSampleStyleSheet()['Heading4']));

    # adding the lines to the table
    my_style =  [ ('LINEAFTER', (0,0), (-1,-1),2, colors.black), ('LINEBEFORE', (0,0), (-1,-1),2, colors.black) ];
    story.append(Table([ adm_str], [7.5*cm]*len(semestres),style=my_style));
    story.append(Table([comp_str], [7.5*cm]*len(semestres),style=my_style));
    story.append(Table([fail_str], [7.5*cm]*len(semestres),style=my_style));
    my_style.append(('LINEBELOW', (0,0), (-1,-1),2, colors.black));
    story.append(Table([null_str], [7.5*cm]*len(semestres),style=my_style));

    # printing 
    pv_file.build(story);


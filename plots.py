##########################################################
###                                                    ###
###             Pie charts et histogrammes             ###
###                                                    ###
###                Date: 21/01/2026                    ###
###                                                    ###
##########################################################
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from collections import Counter
from datetime import datetime
import numpy as np
import re
from pypdf import PdfReader, PdfWriter
from maquette import UEs, Blocs

##########################################################
###                                                    ###
###                     Pie charts                     ###
###                                                    ###
##########################################################

# Design
Sup_Style = { 'family': 'sans-serif', 'color': 'black', 'fontsize': 15, 'fontweight': 'bold'}
Title_Style = { 'family': 'sans-serif', 'color': 'darkred', 'fontsize': 12, 'fontweight':'bold'}
Label_Style = { 'family': 'sans-serif', 'color':'darkblue', 'fontsize': 11}

# Fonction auxiliaire (single pie chart)
def pie(ax, values, title):
    # Filtrage NCAE
    values = [v for v in values if v != 'NCAE']

    # Safety : pie vide
    if not values:
        ax.axis('off')
        return

    # Initialisation avec définition du mapping couleurs/hatch/label
    counts = Counter(values)
    wedges_map = [
        ('ADM',      'DarkSeaGreen', '',      f"ADM ({counts.get('ADM',0)})"),
        ('ADM-MAJ',  'DarkSeaGreen', '//',    f"({counts.get('ADM-MAJ',0)})"),
        ('COMP',     'Cornsilk',     '',      f"COMP ({counts.get('COMP',0)})"),
        ('COMP-MAJ', 'Cornsilk',     '//',    f"({counts.get('COMP-MAJ',0)})"),
        ('AJ',       'Brown',        '',      f"AJ ({counts.get('AJ',0)})")
    ]

    # Filtre des éléments absents
    wedges_values = []
    wedges_colors = []
    wedges_hatch  = []
    wedges_labels = []
    for key, color, hatch, label in wedges_map:
        val = counts.get(key, 0)
        if val > 0:
            wedges_values.append(val)
            wedges_colors.append(color)
            wedges_hatch.append(hatch)
            wedges_labels.append(label)

    # Création du pie chart
    wedges, texts = ax.pie(wedges_values, labels=wedges_labels, startangle=90, colors=wedges_colors, textprops=Label_Style)

    # Appliquer les hatchs
    for w, h in zip(wedges, wedges_hatch):
        w.set_hatch(h)
        if h: w.set_edgecolor('black')

    # layout
    ax.set_title(title, y=0.93, **Title_Style)

# Fonction principale
def pies(stats, title=None):
    # Initialisation : layout (1 ligne / session et 3 colonnes [VET1, VET2, année]) + stats dispos
    fig, axes = plt.subplots(2, 3, figsize=(11.7, 8.3))
    all_keys = list(stats['resultats'].keys())

    vets = [k for k in all_keys if k != 'annee']
    vet1 = vets[0] if len(vets) > 0 else None
    vet2 = vets[1] if len(vets) > 1 else None
    annee = 'annee' if 'annee' in all_keys else None
    col_keys = [k for k in (vet1, vet2, annee) if k is not None]
    col_labels = {}
    for k in col_keys:
        col_labels[k] = 'Année' if k == 'annee' else (''.join(sorted(k[:2], key=lambda c: c.isdigit())))
#    col_labels = { vet1:(''.join(sorted(vet1[:2], key=lambda c: c.isdigit()))), vet2:(''.join(sorted(vet2[:2], key=lambda c: c.isdigit()))), 'annee':'Année' }
    has_session2 = stats['resultats'] != stats['resultats2']

    # Remplissage des plots
    for col, key in enumerate(col_keys):
        # Session 1 (ligne 0)
        if key and key in stats['resultats']: pie(axes[0, col], sorted(stats['resultats'][key]), f"{col_labels[key]} – Session 1")
        else: axes[0, col].axis('off')

        # Session 2 (ligne 1)
        if has_session2 and key and key in stats['resultats2']: pie(axes[1, col], sorted(stats['resultats2'][key]), f"{col_labels[key]} – Session 2" )
        else: axes[1, col].axis('off')

    # Titre global
    if title: fig.suptitle(title, y=0.95, **Sup_Style)

    # Output
    plt.subplots_adjust(hspace=0.4) 
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig

##########################################################
###                                                    ###
###                     Histograms                     ###
###                                                    ###
##########################################################

# Design - extra
Moy_Style = { 'family': 'sans-serif', 'color':'darkred', 'fontsize': 9}
Med_Style = { 'family': 'sans-serif', 'color':'darkblue', 'fontsize': 9}
Pct_Style = { 'family': 'sans-serif', 'color':'darkgreen', 'fontsize': 9, 'bbox': dict(facecolor='white', edgecolor='none', alpha=0.2)}

# Fonction auxiliaire : histogramme simple
def histo(ax, data, title, maxi=20):
    # Safety : histo vide
    if not data:
        ax.axis('off')
        return

    # Création de l'histogramme
    ax.hist(data, bins=20, range=[0, maxi], color='teal')

    # Moyenne, médiane et percentiles
    ax.axvline(np.mean(data), color='darkred', linestyle='dashed', linewidth=1)
    ax.axvline(np.median(data), color='darkblue', linestyle='dotted', linewidth=1)
    ax.text(maxi/100, ax.get_ylim()[1]*.95, 'Moy. : {:.2f}'.format(np.mean(data)),   **Moy_Style);
    ax.text(maxi/100, ax.get_ylim()[1]*.89, 'Med. : {:.2f}'.format(np.median(data)), **Med_Style);
    for perc in [10, 25, 75, 90]:
        val = np.percentile(data, perc)
        ax.axvline(val, color='darkgreen', linestyle='dashdot', linewidth=1)
        ax.text(val+0.01*maxi, ax.get_ylim()[1]*0.9, f"{perc}%", rotation=90, verticalalignment='center', **Pct_Style)

    ax.set_title(title, fontdict=Title_Style)
    ax.set_xlabel("Note / {}".format(maxi), fontdict=Label_Style)
    ax.set_ylabel("# étudiants", fontdict=Label_Style)
    ax.set_xlim(0, maxi)

# Fonction principale
def histos(stats, title=None):
    # Initialisation
    notes1 = stats['notes']
    notes2 = stats['notes2']
    has_session2 = notes1 != notes2
    plots_per_page = 3
    figures = []

    # Classification
    all_ues = sorted([k for k in notes1.keys() if k != 'annee'])
    annee_keys = ['annee'] if 'annee' in notes1 else []
    vet_keys   = [k for k in all_ues if re.match(r'^(\dS|S\d)', k)]
    ue_keys = [k for k in all_ues if k in UEs.keys()]
    ordered_ues = annee_keys + vet_keys + ue_keys

    # Renplissage des plots
    for page_idx in range(int(np.ceil(len(ordered_ues)/plots_per_page))):

        # Layout général
        fig, axes = plt.subplots(2, plots_per_page, figsize=(11.7, 8.3))
        axes = axes.flatten()

        # Localisation
        start_idx = page_idx*plots_per_page
        end_idx = min(start_idx + plots_per_page, len(ordered_ues))
        ues_page = ordered_ues[start_idx:end_idx]

        # Remplissage des plots
        for i, ue in enumerate(ues_page):
            m = re.match(r'^(\dS|S\d)', ue)
            if ue.lower() == 'annee': title_ue = 'Année'
            if m:
                code = m.group(1)
                if code[0].isdigit(): title_ue = "S" + code[0]
                else: title_ue = code
            elif ue in UEs.keys(): title_ue = ue + " - " + UEs[ue]['nom']
            maxi = 100 if ue in UEs.keys() or ue in Blocs.keys() else 20
            histo(axes[i%plots_per_page], notes1[ue], f"{title_ue} (Session 1)", maxi=maxi)
            if has_session2: histo(axes[(i%plots_per_page) + plots_per_page], notes2[ue], f"{title_ue} (Session 2)", maxi=maxi)

        # Masquage des plots vides
        for j in range(len(ues_page), plots_per_page):
            axes[j].axis('off')
            axes[j+plots_per_page].axis('off')

        # output, page par page
        plt.tight_layout()
        figures.append(fig)

    # output global
    return figures


##########################################################
###                                                    ###
###                     Sauvegarde                     ###
###                                                    ###
##########################################################
def save_plots(pies, histos, annee, niveau, parcours):
    # Noms de fichiers
    date = str(datetime.now().year*10000+datetime.now().month*100+datetime.now().day)
    filename = annee.replace('-', '_') + '_' + niveau + '_' + parcours + '_v' + date + '.pdf'
    pv_pdf    = 'output/' + filename
    stats_pdf = 'histos/' + filename

    # Sauvegarde des pie charts et dfes histos
    with PdfPages(stats_pdf) as pdf:
        if pies: pdf.savefig(pies, bbox_inches='tight', pad_inches=0.15)
        if histos:
            for fig in histos: pdf.savefig(fig, bbox_inches='tight', pad_inches=0.15)

    # Fusion avec le PV pirate
    reader_main  = PdfReader(pv_pdf)
    reader_stats = PdfReader(stats_pdf)
    writer = PdfWriter()
    for page in reader_main.pages: writer.add_page(page)
    for page in reader_stats.pages: writer.add_page(page)
    with open(pv_pdf, 'wb') as f: writer.write(f)




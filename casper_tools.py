##########################################################
###                                                    ###
###                  CSV converter                     ###
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
###                  List of students                  ###
###                                                    ###
##########################################################
import glob, os, pandas;
def ReadCasperLists():
    listes_casper = glob.glob(os.path.join(os.getcwd(), 'data/Casper_Liste*'));
    casper_data = {};
    for casper in sorted(listes_casper):

        # raw data
        casper_infos = pandas.read_excel(casper, index_col=1, header=3)
        casper_dico  = casper_infos.to_dict('index');

        # Niveau
        niveau = 'L2 ' if 'L2' in casper else 'L3 ';

        # year
        myyear = casper.split('_')[-1].split('.')[0];
        year = myyear + '_' + str(int(myyear)+1);
        lastyear = str(int(myyear)-1) + '_' + myyear;

        # Formatting
        print("         *** Extraction de l'année " + niveau + '- ' + str(year));
        for k,v in casper_dico.items():
            # Parcours
            parcours = niveau + v['Parcours - type'].replace('DOUBLE MAJEURE', 'DM').replace('DOUBLE CURSUS', 'DK');
            if v['Parcours - code'] == 'CNED': parcours = niveau + 'PAD' + v['Parcours - type'];
            parcours = parcours.replace('MAJ-MIN','Bi-Di').replace('Mono_DI', 'MONO-Int').replace('P6P4_PHILO','Bi-Di');
            parcours = parcours.replace('Bi-mENV','Bi-Di').replace('PE','MONO').replace('P6P4_CHIN','Bi-Di').replace('P6P4_HIST','Bi-Di');
            if not parcours in ['L2 PADMONO', 'L2 DM', 'L2 DK', 'L2 Bi-Di', 'L2 MONO', 'L2 MONO-Int', 'L3 PADMONO', 'L3 DM', 'L3 DK', 'L3 Bi-Di', 'L3 MONO', 'L3 ENS']:
                print(k,v)
                print(parcours); import sys; sys.exit();

            # Bac
            bac = 'France' if v['BAC série - libellé'] != 'EQUIV. TITRE ETR.' else 'Etranger';

            # L1
            portail = 'univ' if v['Portail L1'] in ['MIPI', 'PCGI', 'BCG'] else 'hors SU';

            # Réussite
            notes = {};
            if niveau == 'L2 ':
                if isinstance(v['Réussite au semestre 3'], str): notes['S3'] = v['Réussite au semestre 3'].replace('Non admis','AJ').replace('Admis','ADM');
                if isinstance(v['Réussite au semestre 4'], str): notes['S4'] = v['Réussite au semestre 4'].replace('Non admis','AJ').replace('Admis','ADM');
            else:
                if isinstance(v['Réussite au semestre 5'], str): notes['S5'] = v['Réussite au semestre 5'].replace('Non admis','AJ').replace('Admis','ADM');
                if isinstance(v['Réussite au semestre 6'], str): notes['S6'] = v['Réussite au semestre 6'].replace('Non admis','AJ').replace('Admis','ADM');

            # Existing student
            if k in casper_data.keys():
                if not year in casper_data[k]['parcours'].keys(): casper_data[k]['parcours'][year] = parcours;
                else : casper_data[k]['parcours'][year] = casper_data[k]['parcours'][year] + ' & ' + parcours
                if lastyear in casper_data[k]['N-1'].keys(): casper_data[k]['N-1'][year] = 'univ';
                else: casper_data[k]['N-1'][year] = portail;
                casper_data[k][year] = notes;
                casper_data[k] = dict(sorted(casper_data[k].items()));

            # new student
            else:
                casper_data[k] = {
                    year            : notes,
                    'sexe'          : v['Sexe - libellé'].replace('Homme', 'M').replace('Femme','F'),
                    'nom'           : '',
                    'prenom'        : '',
                    'date_naissance': '',
                    'mail'          : '',
                    'bourse'        : '',
                    'parcours'      : {year: parcours},
                    'annee_bac'     : '',
                    'pays_bac'      : bac,
                    'inscr_SU'      : '',
                    'N-1'           : {year: portail}
                };

    # exit
    return casper_data;



##########################################################
###                                                    ###
###              Cours autre disciplines               ###
###                                                    ###
##########################################################
CasperIgnore = [
  'Espaces vectoriels euclidiens et hermitiens, isomé',   'Fonctions de plusieurs variables, Analyse vector',    'Séries de fonctions, Séries de Fourier, Intégrales',
  'Arithmétique',                                         'Séries entières, Intégrales dépendant d\'un paramèt', 'Statique et dynamique des solides indéformables',
  'Algèbre linéaire 2, espaces vectoriels euclidiens',    'Statique et dynamique des fluides',                   'Programmation pour le calcul scientifique',
  'Transferts thermiques',                                'Biochimie: Métabolisme',                              'Génétique 1',
  'Organisation Fonctionnelle des Animaux',               'Biologie Cellulaire ',                                'Eléments de programmation par objets avec Java',
  'Structures discrètes',                                 'Introduction aux bases de données relationnelles',    'Machine et représentation',
  'Groupes de permutations et groupes d\'isometries',     'Séries de fonctions, séries de Fourier, intégrales',  'Algèbre linéaire 2, espaces vectoriels euclidiens',
  'Fonctions élémentaires de l\'électronique',            'Sources d\'énergie électrique et capteurs',           'Electronique numérique combinatoire et séquentiell',
  'Matlab applications en électronique',                  'Relations structure - propriétés en chimie inorgan',  'Thermodynamique appliquée à la chimie',
  'Liaison intra-moléculaires et réactivité',             'Relations structure - propriétés en chimie organiq',  'Sociologie des sciences',
  'Analyse vectorielle',                                  'Physiologie des signalisations neuro et hormo',       'Algèbre linéaire 2, espaces affines',
  'Probabilités',                                         'Ingénierie biomédicale',                              'Fondements en microélectronique',
  'Microéconomie',                                        'Comptabilité',                                        'Stratégie d\'entreprise',
  'Histoire des entreprises',                             'Chinois - civilisation 3',                            'Chinois - langue 3',
  'Analyse vectorielle et intégrales multiples',          'Méthodes mathématiques pour la mécanique',            'Spectroscopies et Séparation',
  'Techniques analytiques',                               'Introduction à la philosophie des sciences',          'Introduction à l\'histoire des sciences et techniqu',
  'Histoire des sciences à Paris',                        'Médiation scientifique 1',                            'Sociologie des sciences',
  'Bases de thermodynamique',                             'Bases de sédimentologie',                             'Géophysique Océan - Atmosphère - Climat',
  'Programmation impérative en C',                        'Français techniques d\'expression et de communicati', 'Stage d¿Accompagnateur Scientifique (SACS) ',
  'Numérique et internet',                                'Espagnol Semestre 3',                                 'Histoire de la philosophie antique',
  'Philosophie Générale',                                 'Ethique',                                             'Histoire de la philosophie contemporaine',
  'Chinois - civilisation 4',                             'Chinois - langue 4',                                  'Minéralogie Pétrologie Magmatisme',
  'Outils carthographique - SIG',                         'Terrain 1 / Bibliographie',                           'Espagnol Semestre 4',
  'Chimie : structure et réactivité',                     'Concepts et méthodes de la physique pour PCGI',       'Méthodologie du travail universitaire',
  'UE d\'ouverture Abu Dhabi S3',                         'UE d\'ouverture Abu Dhabi S4',                        'Stage Licence non gratifié hors compensation',
  'Fonctions et intégrales de plusieurs variables ',      'Formes quadratiques, isométries affines ',            'Groupes de permutations et groupes d\'isométries',
  'Séries de fonctions, intégrales généralisées',         'Algèbre linéaire 2, formes quadratiques ',            'Analyse et simulations des mécanismes et structure',
  'Pratiques numériques en mécanique',                    'Stage Licence gratifié hors compensation',            'Russe Semestre 4',
  'Arithmétique et algèbre ',                             'L3 Echange international 3ects',                      'La nature de la connaissance scientifique',
  'Quelques problématiques philosophiques contemporai',   'Introduction aux problématiques de Santé publique',   'L\'Odyssée du médicament',
  'Histoire de la philosophie',                           'Philosophie Générale',                                'Calcul assisté par ordinateur de systèmes mécaniqu',
  'Portugais Semestre 3',                                 'Français Langue Etrangère',                           'L2 Echange international 3ects',
  'La boîte à outils numériques du médiateur scientif',   'Eléments de programmation ',                          'Eléments de programmation 2',
  'Sociologie des organisations',                         'TECHNIQUES ET MÉTHODES D\'INFORMATIQUE',              'Elements d\'algèbre et d\'arithmétique (bi-DI)',
  'Ecologie générale',                                    'INITIATIVE ET ENGAGEMENT ÉTUDIANT',                   'Enjeux, valeurs et gestion des ressources naturell',
  'Histoire de l\'environnement et du concept d\'enviro', 'Le changement climatique et ses enjeux 1',            'Le changement climatique et ses enjeux 2',
  'Préparation du stage ou projet collectif',             'DISPENSE U.E.',                                       'Chinois Semestre 3',
  'APS : SCIENCES & APS L2-1',                            'Allemand Semestre 4',                                 'Allemand Semestre 3',
  'Chinois - Civilisation 3',                             'Chinois - Langue 3',                                  'Histoire de l\'Allemagne S3',
  'Les Européens XVIe-XVIIIe S3',                         'Histoire de l\'Allemagne S4',                         'Les Européens XVIe-XVIIIe S4',
  'ANGLAIS 2',                                            'Probabilités élémentaires',                           'Topologie et calcul différentiel',
  'ANGLAIS 3',                                            'Anglais',                                             'Anglais parcours annuel A',
  'Structures élastiques',                                'U.E. PROGRAMME D\'ECHANGE INTERNATIONAL',             'Médiation scientifique 2',
  'Médiation scientifique 2- Stage',                      'Muséologie',                                          'Projet UniverCités 1',
  'Communiquer en anglais sur un sujet de sciences',      'Développement des idées en géosciences',              'Projet UniverCités 2',
  'Bases de la mécanique des milieux continus',           'Méthodes numériques pour la mécanique',               'Systèmes à base de microcontrôleurs',
  'Techniques et dispositifs pour l\'electronique anal',  'Chimie moléculaire',                                  'Electrochimie',
  'Matériaux inorganiques',                               'Spéctroscopies atomiques et moléculaires',            'Equations différentielles',
  'EQUIVALENCE U.E.',                                     'Introduction aux fluides complexes',                  'Mécanique des fluides',
  'Russe Semestre 6',                                     'Géochimie',                                           'Géodynamique',
  'Terrain 2',                                            'Pétrologie métamorphique',                            'Physique du globe: outils et applications',
  'Initiation à l\'algorithmique',                        'Programmation et structures de données en C',         'Introduction aux systèmes d\'exploitation',
  'Projet (application)',                                 'Algèbre Parcours Bi-disciplinaire intensif',          'Anglais Parcours Bi-disciplinaire intensif',
  'Topologie et calcul différentiel DM',                  'Analyse complexe Parcours Bi-disciplinaire intensi',  'Systèmes robotiques',
  'Mémoire de recherche encadré en HPST',                 'Sujets Choisis 2',                                    'Matériaux et structures du génie civil',
  'Algèbre',                                              'Analyse complexe',                                    'ANGLAIS PRATIQUE ET SCIENTIFIQUE PHYTEM',
  'BASES DE LA MÉCANIQUE QUANTIQUE',                      'ELECTROMAGNÉTISME',                                   'ETATS DE LA MATIÈRE',
  'METHODES MATHEMATIQUES ET NUMERIQUES POUR PHYSIC.',    'PHYSIQUE EXPÉRIMENTALE 1',                            'COHÉSION DE LA MATIÈRE, OPTIQUE ET LASERS',
  'INSTRUMENTATION, ELECTRONIQUE ET TRAIT.DE L\'INFOR.',  'INTRODUCTION À LA PHYSIQUE STATISTIQUE',              'PHYSIQUE EXPÉRIMENTALE 2',
  'STAGE D\'INITIATION À LA RECHERCHE',                   'ANGLAIS COMPLEMENT PHYTEM',                           'CHIMIE COMPLEMENT PHYTEM',
  'Equations aux dérivés partielles 1',                   'UE d\'ouverture Abu Dhabi S5',                        'Français Langue Etrangère ',
  'Acoustique',                                           'Chimie moléculaire Parcours Bi-disciplinaire inten',  'Electrochimie Parcours Bi-disciplinaire intensif',
  'Matériaux inorganiques: Synthèses, propriétés, cri',   'Spéctroscopies atomiques et moléculaires DM',         'Espagnol Semestre 6',
  'Réseaux éléctriques intelligents et gestion de l\'é',  'Signaux et systèmes Parcours Bi-disciplinaire inte',  'Systèmes robotiques Parcours Bi-disciplinaire inte',
  'Techniques et dispositifs pour l\'éléctronique anal',  'Bases de la mécanique des milieux continus DM',       'Du microscopique au macroscopique DM',
  'Equations aux dérivés partielles 1 BiDi',              'Equations aux dérivés partielles 2 BiDi',             'Mécanique des fluides Parcours Bi-disciplinaire in',
  'Structures élastiques DM',                             'Le changement scientifique',                          'Allemand Semestre 5',
  'Allemand Semestre 6',                                  'Chinois Semestre 5',                                  'Chinois Semestre 6',
  'Topologie et calcul différentiel parcours bi-DI',      'Eoliennes, hydroliennes et turbomachines',            'Signaux et systèmes',
  'Finance',                                              'Gestion de l\'innovation',                            'Entrepreunariat',
  'Marketing',                                            'Histoire des techniques',                             'Introduction aux études sur les sciences et techni',
  'L\'atome, le bit, le gène : sciences et société au ',  'Du microscopique au macroscopique',                   'Equations aux dérivés partielles 2',
  'L3 Echange international 6 ects',                      'Chimie industrielle',                                 'Initiation à la programmation scientifique',
  'Philosophie politique',                                'Métaphysique',                                        'Philosophie des sciences',
  'Chinois - Civilisation 5',                             'Chinois - Langue 5',                                  'L3 Echange international 12 ects',
  'Systèmes à base de microcontrôleurs DM',               'Structures en pratique',                              'Environnements sédimentaires Parcours BiDi intensi',
  'Géochimie Parcours Bi-disciplinaire intensif',         'Terrain 2 Parcours Bi-disciplinaire intensif',        'Pétrologie métamorphique Parcours Bi-disciplinaire',
  'Physique du globe : outils et applications parcour',   'Intégration',                                         'Espagnol Semestre 5',
  'Signaux et contrôle des systèmes',                     'Physique du globe',                                   'Stage en laboratoire',
  'Enseignement et didactique des Sciences',              'Introduction à l\'analyse spectrale',                 'Mécanique analytique',
  'Russe Semestre 5',                                     'Duo patient-soignant',                                'Fouille de données, sémantique et aide à la décisi',
  'Statistiques et bioinformatique appliquées à la re'
]



##########################################################
###                                                    ###
###                  Cours physique                    ###
###                                                    ###
##########################################################
CasperPhys = {
  'Histoire et philosophie des sciences'              : '2P002',
  'Energie et entropie'                               : '2P003',
  'Physique du mouvement'                             : '2P004',
  'Méthodes mathématiques 1'                          : '2P010',
  'Ondes'                                             : '2P011',
  'Physique expérimentale 1'                          : '2P012',
  'Outils mathématiques'                              : '2P013',
  'Outils mathématiques 1'                            : '2P013',
  'Mécanique et ondes'                                : '2P014',
  'Méthodes mathématiques 2'                          : '2P020',
  'Electromagnétismes et électrocinétique'            : '2P021',
  'Electromagnétisme et électrocinétique'             : '2P021',
  'Calcul scientifique et modélisation'               : '2P022',
  'Outils mathématiques 2'                            : '2P023',
  'Quanta et relativité'                              : '2P024',
  'Compléments de physique'                           : '2P032',
  'Physique des systèmes dynamiques'                  : '2P032',
  'Physique en action L2'                             : '2P041',
  'Projet Numérique'                                  : '2P042',
  'Orientation et Insertion Professionnelle'          : '2POI1',
  'Mécanique quantique'                               : '3P001',
  'Physique numérique'                                : '3P002',
  'Thermodynamique et aspects statistiques'           : '3P003',
  'Thermodynamique et aspects statistiques DM'        : '3P003',
  'Structure de la Matière'                           : '3P004',
  'Structure de la Matière Parcours Bi-disciplinaire ': '3P004',
  'Stage court'                                       : '3P005',
  'Méthodes mathématiques 3'                          : '3P010',
  'Thermodynamique et thermostatistique'              : '3P011',
  'Thermodynamique et thermostatistique DM'           : '3P011',
  'Physique expérimentale 1 Parcours Bi-disciplinaire': '3P012',
  'Outils mathématiques 3'                            : '3P013',
  'Outils mathématiques 3 Parcours Bi-disciplinaire i': '3P013',
  'Physique expérimentale 2'                          : '3P015',
  'Physique expérimentale 2 Parcours Bi-disciplinaire': '3P015',
  'Physique Quantique Parcours Bi-disciplinaire inten': '3P020',
  'Physique Quantique'                                : '3P020',
  'Electromagnétisme et optique'                      : '3P021',
  'Electromagnétisme et optique DM'                   : '3P021',
  'Projet'                                            : '3P022',
  'Stage Approfondi'                                  : '3P023',
  'PROJET EXPÉRIMENTAL'                               : '3P024',
  'Projet en autonomie'                               : '3P024',
  'Projet Parcours Bi-disciplinaire intensif'         : '3P024',
  'Astrophysique'                                     : '3P031',
  'Océans, Atmosphères et Energies renouvelables'     : '3P033',
  'Physique des Milieux continues'                    : '3P034',
  'Physique théorique'                                : '3P035',
  'Méthodes mathématiques pour physiciens '           : '3P036',
  'Mesures Physiques '                                : '3P040',
  'Physique en action L3'                             : '3P041',
  'Histoire de la mécanique '                         : '3P042',
  'Phénomènes de transport'                           : '3P043',
  'Hydrodynamique'                                    : '3P044'
}



##########################################################
###                                                    ###
###                Extraction des notes                ###
###                                                    ###
##########################################################
import math;
def ReadCasperNotes(data, yearlist):
    # Liste des ficheirs et initialisation
    listes_casper = glob.glob(os.path.join(os.getcwd(), 'data/Casper_Notes*'));
    casper_data = data;
    years = yearlist;

    # Enregistrement des données
    for casper in sorted(listes_casper):

        # raw data
        casper_infos = pandas.read_excel(casper, header=3, index_col=0);
        casper_dico  = casper_infos.to_dict(orient='records');

        # Niveau
        niveau = 'L2 ' if 'L2' in casper else 'L3 ';

        # year
        myyear = casper.split('_')[-1].split('.')[0];
        year = myyear + '_' + str(int(myyear)+1);
        if not year in years: years.append(year);

        # Getting notes
        print("         *** Extraction de l'année " + niveau + '- ' + str(year));
        student_id = None;
        notes      = {};
        for line in casper_dico:
            # new student -> saving and resetting
            if not math.isnan(line['N° Dossier']) and not student_id in [None]:
               if not student_id in casper_data.keys(): logger.warning('Ghost student: ' + str(student_id));
               else:
                   for ue, note in notes.items(): casper_data[student_id][year][ue] = note;
               student_id = None; notes = {};

            # Saving the new student id
            if not math.isnan(line['N° Dossier']): student_id = int(line['N° Dossier']);

            # some UE to save
            ue       = line['U.E. - libellé'];
            note     = line['Note Totale'];

            # Safety
            if isinstance(ue,float) and math.isnan(ue): continue;
            if 'Equivalence' in ue or 'Dispense' in ue or ue in CasperIgnore: continue;

            # Getting the UE code
            if not ue in CasperPhys.keys():
                logger.error("UE Casper  non existante : " + ue); sys.exit();
            notes[CasperPhys[ue]] = note;

    # cleaning
    for k,v in casper_data.items(): casper_data[k] = dict(sorted(v.items()));
    casper_data  = dict(sorted(casper_data.items()));

    # Exit
    return sorted(years), casper_data;



##########################################################
###                                                    ###
###              Fusion des infos Casper               ###
###                                                    ###
##########################################################
def MergeCasper(casper_data, stats):
    # Initialisation
    new_stats = stats;

    # Merging process
    for etu_id, value in casper_data.items():
        # Non existing student
        if not etu_id in new_stats.keys(): new_stats[etu_id] = value;

        # existing student to update
        else:
            for keyword in ['parcours', 'N-1']:
                for year in value[keyword].keys():
                    if not year in new_stats[etu_id][keyword].keys(): new_stats[etu_id][keyword][year] = value[keyword][year]
            for year in [k for k in value.keys() if k.startswith('2')]: new_stats[etu_id][year] = value[year];

        # cleaning
        for keyword in ['parcours', 'N-1']: new_stats[etu_id][keyword] = dict(sorted(new_stats[etu_id][keyword].items()));
        new_stats[etu_id] = dict(sorted(new_stats[etu_id].items()));

    # Exit
    return new_stats;

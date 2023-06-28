##########################################################
###                                                    ###
###   Librarie de gestion des statistiques licence     ###
###                                                    ###
##########################################################



##########################################################
###                                                    ###
###                       Logger                       ###
###                                                    ###
##########################################################
import logging;
logger = logging.getLogger('mylogger');

from misc import Bye

##########################################################
###                                                    ###
###      Extraire données depuis le fichier excel      ###
###                                                    ###
##########################################################
import pandas;
import numpy as np

def GetDictionary(year):
	statsfilename = f"output/stats_{year}_{year+1}.xlsx"
	statsDF = pandas.read_excel(statsfilename, index_col = 0, header=[0,1])
	statsDict = statsDF.to_dict('index')
	return statsDict

### Extraire tous les types de données, triés sous forme de liste

def GetInnerKeys(mondict):
	all_keys = set([key for inner_dict in mondict.values() for key in inner_dict.keys()])
	sorted_keys_list = sorted(list(all_keys))
	return sorted_keys_list

def GetParcours(mondict, makey = 'parcours'):
	parcours = set([inner_dict[key] for inner_dict in mondict.values() for key in inner_dict.keys() if key[0] == makey])
	listparcours = sorted(list(parcours))
	return listparcours

#### Combiner des dictionnaires différents, correspondants à des années différentes par exemple

def safe_isnan(value):
	if isinstance(value, (int, float, np.number)):
		return np.isnan(value)
	else:
		return False

def MergeDicoElements(inner1,inner2):
	flag = False
	for key in inner2.keys():
		if key in inner1:
			if inner1[key] != inner2[key]:
				if safe_isnan(inner1[key]):
					inner1[key] = inner2[key]
				elif not safe_isnan(inner2[key]):
					flag = True
		else:
			inner1[key] = inner2[key]
	return inner1, flag

#### mondico est directement modifié. Attention, les associations de dictionnaires sont faites en reférence
#### donc tout modif ultérieure sur l'un influe les autres
def MergeDictionary(mondico, *args):
	flag = False
	for mondict in args:
		for key in mondict.keys():
			if key in mondico:
				mondico[key], flag = MergeDicoElements(mondico[key],mondict[key])
				if flag:
					print(f"Problème dans les donnés du numéro {key} \n")
			else:
				mondico[key] = mondict[key]
#	return mondico


### Extraire toutes les notes associées à une clé (double) : dans makey
### correspondant à des UEs ou des semestre, moins les "nan". 
### Si FINAL = True, fait le max entre session 1 et session 2
### On peut spécifier des valeurs pour un ensemble de clés complémentaires sous la forme 
### 	de dico avec clé (attention, il faut la clé double) + valeure attendue, exemple [('annee_bac', 'Unnamed: 5_level_1'), 2020]
### 	garde les notes où TOUTES les clés sont vérifiées

def GetGradesKeycomp(mondict, makey, FINAL = False, *args):
	Grades = []
	if FINAL :
		makey2 = (makey[0].replace('Session1','Session2'), makey[1])
	for inner_dict in mondict.values():
		if all(inner_dict[keycomp[0]] == keycomp[1] for keycomp in args):
			if FINAL and makey2 in inner_dict and isinstance(inner_dict[makey2],float) and not np.isnan(inner_dict[makey2]):
				Grades += [inner_dict[makey2]]
			else:
				if makey in inner_dict and isinstance(inner_dict[makey],float) and not np.isnan(inner_dict[makey]):
					Grades += [inner_dict[makey]]
#	Grades = [f for f in Grades_withnan if not np.isnan(f)]
	return Grades

### La même mais en langage naturel
### Session est un INT : 1 Session1, 2 Session2, 3 max (i.e. Session 2 si présente, sinon Session 1)
### year : indique l'année des données
### *args est une liste d'autres clés et de la valeur attendue, ex ('annee_bac', 2020)

def GetGradesKeycompLN(mondict, UEouSem, Session, year, *args):
	FINAL = False
	mescles = GetInnerKeys(mondict)
	Session, FINAL = (1, True) if Session == 3 else (Session, FINAL)
	macle = (f"notes Session{Session} ({year}_{year+1})", UEouSem)
	if macle not in mescles:
		logger.error(f"Attention : nom d'UE ou de Session invalide {macle}");
		Bye();
	keycomps = []
	for keycomp in args:
		for (key, value) in mescles:
			if key == keycomp[0]:
				keycomps += [[(key, value), keycomp[1]]]
				break
	if keycomps == []:
		return GetGradesKeycomp(mondict, macle, FINAL)
	else:
		print(f"clés prises en compte : {keycomps}")
		return GetGradesKeycomp(mondict, macle, FINAL, *keycomps)


### Extraire un dictionnaire dont les étudiants correspondent à un certain nombre de clés
### *args est une liste de clés et de la valeur attendue, ex ('annee_bac', 2020)

def ExtractStudents(mondict, *args):
	dicoEtd = {key : mondict[key] for key in mondict.keys() if all(mondict[key][keycomp[0]] == keycomp[1] for keycomp in args)}
	return dicoEtd


def ExtractStudentsLN(mondict, *args):
	mescles = GetInnerKeys(mondict)
	keycomps = []
	for keycomp in args:
		for (key, value) in mescles:
			if key == keycomp[0]:
				keycomps += [[(key, value), keycomp[1]]]
				break
	print(f"clés prises en compte : {keycomps}")
	return ExtractStudents(mondict, *keycomps)


#### FONCTIONS peut-être finalement inutiles...

### Extraire toutes les notes associées à un (ensemble) de clé (double) : dans *args  
### correspondant à des UEs ou des semestre, moins les "nan" : 
### On peut spécifier le parcours, mettre 'all' pour tous les parcours

def GetGrades(mondict, parcours, *args):
	Grades_withnan = []
	if parcours != 'all' and parcours not in GetParcours(mondict):
		logger.error("Attention : nom de parcours invalide");
#		Bye();
	for makey in args:
		if parcours == 'all':
			Grades_withnan = Grades_withnan + [inner_dict[makey] for inner_dict in mondict.values() if makey in inner_dict if isinstance(inner_dict[makey],float)]
		else:
			for inner_dict in mondict.values():
				for key in inner_dict.keys():
					if key[0] == 'parcours' and inner_dict[key] == parcours and makey in inner_dict and isinstance(inner_dict[makey],float):
						Grades_withnan = Grades_withnan + [inner_dict[makey]]
	Grades = [f for f in Grades_withnan if not np.isnan(f)]
	return Grades


##########################################################
###                                                    ###
###                      Plotter  BF                   ###
###                                                    ###
##########################################################
import matplotlib.pyplot as plt;

### Plot avec mean et mediane
### Filename = 'show' montre la figure plutôt que de l'enregister

def MakePlot1(data, title, label, nbin, maxgrade, filename):
    # Histograms
    font1 = {'family':'sans-serif', 'color':'darkred',  'size':15};
    font2 = {'family':'sans-serif', 'color':'darkblue', 'size':13};

    # canvas
    fig = plt.figure();
    ax = fig.subplots(1);
    ax.tick_params(axis='x', colors='darkblue');
    ax.tick_params(axis='y', colors='darkblue');

    # data
    ax.hist(data, nbin, range=[0,maxgrade], color='teal', label=label);

    ax.axvline(np.mean(data),   color='darkred',  linestyle='dashed', linewidth=1);
    ax.axvline(np.median(data), color='darkblue', linestyle='dotted', linewidth=1);
    ax.text(maxgrade/40, ax.get_ylim()[1]*.90, 'Moy. : {:.2f}'.format(np.mean(data)),   color='darkred');
    ax.text(maxgrade/40, ax.get_ylim()[1]*.80, 'Med. : {:.2f}'.format(np.median(data)), color='darkblue');

    # Layout
    ax.set_title(title, fontdict=font1);
    ax.legend(loc='upper right');
    plt.xlabel('Note / ' + str(maxgrade), fontdict=font2);
    fig.supylabel('# étudiants/étudiantes', fontdict=font2, x=0.05);

    # Saving the file
    if filename == 'show':
        plt.show();
    else:
        plt.savefig(filename);
    plt.close();





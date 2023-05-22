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
###                    CSV reader                      ###
###                                                    ###
##########################################################
import csv;
def DecodeCSVProvenance(myfile):
    # storage space for the results
    data = {};

    # Opening the file to read it line by line
    with open(myfile, 'r') as f:
        reader = csv.reader(f, delimiter=';');

        # checking all lines
        for i, line in enumerate(reader):

            # Check the formation
            if not 'PY' in line[1]: continue;

            # Bac
            bac_place = 'France' if line[4]=='O' else 'Etranger';
            try: annee_bac = int(line[3]);
            except: annee_bac = line[3];

            # Annee N-1
            origine ='';
            if   line[11]=='H': origine='univ';
            elif line[11]=='G': origine='univ-EAD';
            elif line[11]=='M': origine='ESPE-MEEF';
            elif line[11]=='D': origine='CPGE';
            elif line[11] in ['U', 'T']: origine='neant';
            elif line[11] in ['A', 'Q']: origine='secondaire';
            elif line[11] in ['B', 'C']: origine='BTS-IUT';
            elif line[11] in ['E', 'J']: origine='ecole';
            elif line[11] in ['K', 'R']: origine='autre_sup';
            else: logger('  ** Provenance: Origine etudiant inconnue: ' + str(line));

            # we have a student in physics
            data[int(line[0])] = {'parcours':line[1], 'annee_bac':annee_bac, 'pays_bac':bac_place, 'inscr_SU':int(line[10]), 'N-1':origine};

    # Output
    return data;



##########################################################
###                                                    ###
###           Definition du parcours APOGEE            ###
###                                                    ###
##########################################################
import sys;
def ParcoursApogee(my_parcours):

        ##  doctorat, master, prepa agreg, L1, Erasmus, cumulatifs
        for nonLPY in ['D', 'M', 'Y', 'T', 'L2SX81']:
           if my_parcours.startswith(nonLPY): return False, '';
        if my_parcours[1]=='1': return False, '';

        ## MIN de physique
        if my_parcours.startswith('V') and my_parcours.endswith('PY') : return False, '';

        ## Autre MAJ
        for maj in ['CI', 'EE', 'MA', 'ME', 'IN', 'ST', 'SV']:
            if my_parcours[2:4] == maj: return False, '';

        ## DM et MAJ-MIN
        if   my_parcours.startswith('Q'): return True, 'L' + my_parcours[1] + ' DM';
        if my_parcours.startswith('V'): return True, 'L' + my_parcours[1] + ' Bi-Di';

        ## LIOVIS
        if my_parcours == 'P3PY01': return True, 'L3 LIOVIS';

        ## MONO
        if my_parcours in ['L2PY91', 'L2PY01', 'L3PY01']: return True, 'L' + my_parcours[1] + ' MONO';
        if my_parcours in ['L2PY02', 'L3PY02', 'L3PY91']: return True, 'L' + my_parcours[1] + ' PADMONO';
        if my_parcours in ['L2PY11', 'L3PY11']:           return True, 'L' + my_parcours[1] + ' MONO-Int';

        # CMI
        if my_parcours in ['L2PY51','L3PY51']:            return True,  'L' + my_parcours[1] + ' CMI'

        # L3 PHYTEM
        if my_parcours == 'L3PY03':                     return True, 'L3 PHYTEM';

        # ERROR
#        if not v['parcours'].startswith('L'): print(v['parcours']); la;
        logger.error('parcours inconnu : ' + my_parcours);
        sys.exit();





import glob, os;
def MergeProvenance(old_years, old_stats, known_ids):
    # initialisation
    years = old_years;
    results = old_stats;
    lists     = glob.glob(os.path.join(os.getcwd(), 'data/prov*'));
    new_infos   = [ 'annee_bac', 'pays_bac', 'inscr_SU'];
    blank_infos = ['nom', 'prenom', 'mail', 'date_naissance', 'sexe'];

    # Loop over the available file
    for myfile in lists:
        year = myfile.split('/')[-1].split('.')[0].split('_')[1];
        year = year+'_'+str(int(year)+1);
        if not year in years : years = years + [year];
        provenance = DecodeCSVProvenance(myfile);
        for etu,v in provenance.items():
            ok, v['parcours'] = ParcoursApogee(v['parcours']);
            if not ok: continue;

            ## new students
            if not etu in results.keys():
                results[etu] = {};
                known_ids = known_ids + [etu];
                for new in new_infos: results[etu][new] = v[new];
                for new in blank_infos: results[etu][new] = '';
                results[etu]['bourse'] = {};
                results[etu]['parcours'] = {year:v['parcours']};
                results[etu]['N-1'] = {year:v['N-1']};

            ## existing student
            else:
                for new in new_infos: results[etu][new] = v[new];
                if not year in results[etu]['parcours'].keys(): results[etu]['parcours'][year] = v['parcours'];
                if not 'N-1' in results[etu].keys(): results[etu]['N-1'] = {year:v['N-1']};
                if not 'bourse' in results[etu].keys(): results[etu]['bourse'] = {};
                else                                 : results[etu]['N-1'][year] = v['N-1'];

    # cleaning
    for k,v in results.items(): results[k] = dict(sorted(v.items()));
    results = dict(sorted(results.items()));

    ## output
    return years, results;

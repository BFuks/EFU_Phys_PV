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


import glob, os;
def MergeProvenance(old_years, old_stats, known_ids):
    # initialisation
    years = old_years;
    results = old_stats;
    lists     = glob.glob(os.path.join(os.getcwd(), 'data/prov*'));
    new_infos = [ 'annee_bac', 'pays_bac', 'inscr_SU'];

    # Loop over the available file
    for myfile in lists:
        year = myfile.split('/')[-1].split('.')[0].split('_')[1];
        year = year+'_'+str(int(year)+1);
        if not year in years : years = years + [year];
        provenance = DecodeCSVProvenance(myfile);
        for etu,v in provenance.items():
            ## Safety
            if v['parcours'].startswith('M'): continue; # Master
            if v['parcours'].startswith('Y'): continue; # Prepa agreg
            if v['parcours'].startswith('T'): continue; # Erasmus
            if v['parcours'].startswith('V') and v['parcours'].endswith('PY') : continue; # MIN physique
            if v['parcours'].startswith('Q'): v['parcours'] =  'L'+v['parcours'][1] + ' DM'; # double majeure
            elif v['parcours'].startswith('V'): v['parcours'] = 'L'+v['parcours'][1] + ' Bi-Di'; # Maj Phys / Min autre
            elif v['parcours'] == 'P3PY01': v['parcours'] = 'L3 LIOVIS'; # LIOVIS
            elif not v['parcours'].startswith('L'): print(v['parcours']); la;

            ## new students
            if not etu in results.keys():
                results[etu] = {};
                known_ids = known_ids + [etu];
                for new in new_infos: results[etu][new] = v[new];
                results[etu]['parcours'] = {year:v['parcours']};
                results[etu]['N-1'] = {year:v['N-1']};

            ## existing student
            else:
                for new in new_infos: results[etu][new] = v[new]; muf = False;
                if not year in results[etu]['parcours'].keys(): results[etu]['parcours'][year] = v['parcours'];
                if not 'N-1' in results[etu].keys(): results[etu]['N-1'] = {year:v['N-1']};
                else                                 : results[etu]['N-1'][year] = v['N-1'];

    ## output
    return years, results;

##########################################################
###                                                    ###
###                Configuration Apogee                ###
###                                                    ###
##########################################################
apogee_structure = {
   # les tags inutiles
   'irrelevant' : ['LIST_G_TFP', 'LIST_G_VDI_VDT', 'LIST_G_ENTETE', 'LIST_G_VET_VET',
                    'LIST_G_FIN_MATRIX', 'C_COD_ANU', 'C_TIT_HEA', 'C_TFP', 'C_NB_LIGNE',
                    'C_NB_ETU_VDT', 'C_NB_ETU_VET', 'CF_LIB_AST', 'CS_MAX_LIB_AST'],

   # la structure elle-meme, avec les PV
   'LIST_G_TAB' : {
     'G_TAB' : {
       'LIST_G_IND' : { 'G_IND':{} }
     }
   },
   # la structure pour le resume du PV
   'LIST_G_TOT' : { 'G_TOT':{} }
};

apogee_stats = {
   # les tags inutiles
   'irrelevant' : [],

   # la structure elle-meme, avec les PV
   'LIST_G_COD_ETU' : { 'G_COD_ETU' : {} }
};




##########################################################
###                                                    ###
###            Configuration PV individuel             ###
###                                                    ###
##########################################################
apogee_pvind_structure = {
  'irrelevant' : [ 'COL_TRI1', 'COL_TRI2', 'COL_TRI4', 'COL_TRI5', 'COL_TRI6',
                   'TEM_DLV_AUT_VDI_TPW_IND', 'DET_BRS_TPW_IND', 'NBR_INS_CYC_ETP_TPW_IND',
                   'NAI_ETU_LI1_TPW_IND', 'NAI_ETU_LI2_TPW_IND', 'LIB_NAT_TPW_IND' ],
    'relevant' : {
       'LIB_NOM_PAT_IND_TPW_IND': 'nom',
       'COD_ETU_TPW_IND'        : 'id',
       'LIST_G_TPW'             : 'results'
    }
};


##########################################################
###                                                    ###
###             Configuration resume PV                ###
###                                                    ###
##########################################################
apogee_resume_structure = {
  'relevant'   : {
    'NBR_ADM_TPW' : 'ADM',
    'PCT_ADM_TPW' : '%_ADM',
    'NBR_AJN_TPW' : 'AJ',
    'PCT_AJN_TPW' : '%_AJN',
    'NBR_ABS_TPW' : 'ABS',
    'NBR_TOT_TPW' : 'TOT',
    'C_NBR_AUT'   : 'AUT',
    'NBR_AJN_TPW' : 'AJ'
  }
};

##########################################################
###                                                    ###
###             Configuration bloc de PV               ###
###                                                    ###
##########################################################
apogee_blocpv_structure = {
  'irrelevant' : ['OD_OBJ_MNP_TPW', 'PVM_LSE_OPT'],
  'relevant'   : {
     'NUM_RNG_OBJ_MNP'     : 'id0',
     'NUM_OCC_OBJ_OBJ_MNP' : 'id1',
     'LIB_CMT_TPW'         : 'tag',
     'COD_OBJ_MNP_TPW'     : 'code',
     'BAR_SAI_TPW'         : 'bareme',
     'LIST_G_TPW_IND'      : 'notes'
  }
};


##########################################################
###                                                    ###
###           Configuration bloc de notes              ###
###                                                    ###
##########################################################
apogee_notes_structure = {
  'irrelevant' : ['NBR_CRD_OBJ_TPW', 'TEM_CRD_PVM', 'COD_TPW', 'NOT_TPW_U', 'NOT_CAL_TPW',
                  'COD_MEN_TPW', 'NOT_PNT_JUR_TPW', 'COD_TRE_VAQ',
                  'LIC_FEX_TPW', 'NBR_RNG_ETU_TPW', 'ETA_NOT_TPW',
                  'ETA_RES_TPW', 'TEM_RES_MEI_NOT_TPW', 'NB_AST', 'LIB_AST', 'COD_TRE',
                  'NOT_SUB_TPW_VAQ', 'NOT_VAA', 'BAR_NOT_VAA', 'C_NBR_CRD', 'CF_FLAG_MEI_NOT',
                  'CF_NOT_TPW', 'CF_COD_TRE_TPW', 'CF_NOT_SUB_TPW'],
  'relevant'   : {
     'COD_TRE_TPW'    : 'validation',
     'NOT_TPW'        : 'note',
     'COD_ELP_LSE_TPW': 'UE',
     'NOT_SUB_TPW'    : 'ABI',
     'ANU_SES_ADM_TPW': 'annee_val'
  }
};


##########################################################
###                                                    ###
###             Configuration bloc de stats            ###
###                                                    ###
##########################################################
apogee_bloc_stats = {
  'irrelevant' : [ 
     'COD_CGE', 'INE', 'NATIONALITE', 'ADA_LIB_AD1_ADA_LIB_AD2_ADA_LI',
     'DECODE_ADA_COD_PAY_100_ADA_LIB', 'CP', 'VILLE', 'LIB_PAY', 'NUM_TEL_PORT',
     'ADR_MAIL_SU', 'LIB_ETP', 'DECODE_INS_ADM_ETP_TEM_IAE_PRM', 'BOURSE',
     'ETA_PMT_IAE', 'ETA_IAS', 'A_PAYER', 'A_REMBOURSER', 'MNT_PAYE',
     'MNT_REMBOURSE', 'BALANCE', 'MNT_IAS', 'REGIME_INS', 'STATUT',
     'ISTUATION_SOCIALE', 'LIB_PRU', 'CODETBPAR', 'LIBETBPAR', 'CNVETBPAR',
     'DAT_CRE_IAE', 'UTILISATEUR', 'APOGEE_SU_VAL_PJ_INS_ADM_ETP_C',
     'DATE_EDT_CERTIFICAT', 'DATE_DLV_CARTE', 'NUMOPI', 'SITUATION_SOCIALE'
  ],
  'relevant'   : {
     'COD_ETU'                       : 'id_su',
     'NOM'                           : 'nom',
     'NOM_USUEL'                     : 'nom',
     'PRENOM'                        : 'prenom',
     'COD_SEX_ETU'                   : 'sexe',
     'TO_CHAR_INDIVIDU_DATE_NAI_IND_': 'date_naissance',
     'ADR_MAIL'                      : 'mail',
     'LIC_ANU'                       : 'annees',
     'VET'                           : 'parcours',
     'COD_BRS'                       : 'bourse'
  }
};




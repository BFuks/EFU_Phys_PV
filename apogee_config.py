##########################################################
###                                                    ###
###                Configuration Apogee                ###
###                                                    ###
##########################################################
apogee_stats = {
   # les tags inutiles
   'irrelevant' : [],

   # la structure elle-meme, avec les PV
   'LIST_G_COD_ETU' : { 'G_COD_ETU' : {} }
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




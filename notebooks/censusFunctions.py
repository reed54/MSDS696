import requests
import pandas as pd
#import censusdata
from pathlib import Path
import pickle

def load_pickled_df (path):
    with open(path, 'rb') as f:
        df = pickle.load(f)
    return(df)

def dump_pickled_df (df, path):
    with open(path, 'wb') as f:
        df = pickle.dump(df, f)
    return

def get_county(str):
    c = str[0:str.index(' County')]
    return(c)

def get_cong_dist(str):
    c = str[0:str.index(' (')]
    return(c)


def get_filename(name, census):
    fn = census + '-' + name + '.p'
    return fn

def get_population_df(key, year):
    '''
    Name
    P001001 Total Population
    P002001 Total Urban and Rural
    P002002 Total Urban
    P002003 Total Urban inside urbanized areas
    P002004 Total Urban inside urban clusters
    P002005 Total Rural
    P003001 Total Race
    P003002 Total White Alone
    P003003 Total Black or African American alone
    P003004 Total American Indian and Alaska Native alone
    P003005 Total Asian alone
    P003006 Total Native Hawaiian and Other Pacific Islander
    P003007 Total Some Other Race Alone
    P003008 Total Two or More Races
    P004001 Total Hispanic or Latino Origin
    P004002 Total Not Hispanic or Latino Origin
    P004003 Total Hispanic or Latino Origin
    '''
    pop_col_names = ['county', 'total_pop', 'total_urb_rur', 'urban', 'urban_ins_ars', 
                     'urban_ins_cls', 'rural',  'total_race', 'white', 'black', 'american_indian',    
                     'asian', 'nat_hawaiian', 'some_othr_race', 'two_or_more_races','hisp_latino',
                     'not_hisp_latino', 'total_hisp_latino', 'state_id', 'county_id']
    
    
    col_types = {c: int for c in pop_col_names}
    col_types['county'] = str

    HOST, dataset = "https://api.census.gov/data/" + str(year), "dec/sf1"
    get_vars =  ["P001" + str(i + 1).zfill(3) for i in range(1)]
    get_vars += ["P002" + str(i + 1).zfill(3) for i in range(5)]
    get_vars += ["P003" + str(i + 1).zfill(3) for i in range(8)]
    get_vars += ["P004" + str(i + 1).zfill(3) for i in range(3)]
    get_vars = ["NAME"] + get_vars

    predicates = {}
    predicates["get"] = ",".join(get_vars)
    predicates["for"] = "county:*"
    predicates["in"] = "state:08"
    predicates["key"] = key
    #print(f'PREDICATES: {predicates}.')

    # Initialize data frame
    base_url = "/".join([HOST, dataset])
    r = requests.get(base_url, params=predicates)

    df = pd.DataFrame(columns=r.json()[0], data=r.json()[1:])
    df.columns = pop_col_names

    print(f'Population Dataframe shape: {df.shape}')

    # Change Datatype for population variables to int64
    df.iloc[:,1:] = df.iloc[:,1:].apply(lambda x: pd.to_numeric(x)) 
    df['county'] = df['county'].apply((lambda s: get_county(s)))
    df = df.astype(col_types)
    return(df)

def get_gender_df(key, year):

    '''
    Name
    P012001	Total SEX BY AGE
    P012002	Total!!Male	SEX BY AGE
    P012003	Total!!Male!!Under 5 years
    P012004	Total!!Male!!5 to 9 years
    P012005	Total!!Male!!10 to 14 years
    P012006	Total!!Male!!15 to 17 years
    P012007	Total!!Male!!18 and 19 years
    P012008	Total!!Male!!20 years
    P012009	Total!!Male!!21 years
    P012010	Total!!Male!!22 to 24 years
    P012011	Total!!Male!!25 to 29 years
    P012012	Total!!Male!!30 to 34 years
    P012013	Total!!Male!!35 to 39 years
    P012014	Total!!Male!!40 to 44 years
    P012015	Total!!Male!!45 to 49 years
    P012016	Total!!Male!!50 to 54 years
    P012017	Total!!Male!!55 to 59 years
    P012018	Total!!Male!!60 and 61 years
    P012019	Total!!Male!!62 to 64 years
    P012020	Total!!Male!!65 and 66 years
    P012021	Total!!Male!!67 to 69 years
    P012022	Total!!Male!!70 to 74 years
    P012023	Total!!Male!!75 to 79 years
    P012024	Total!!Male!!80 to 84 years
    P012025	Total!!Male!!85 years and over
    P012026	Total!!Female
    P012027	Total!!Female!!Under 5 years
    P012028	Total!!Female!!5 to 9 years
    P012029	Total!!Female!!10 to 14 years
    P012030	Total!!Female!!15 to 17 years
    P012031	Total!!Female!!18 and 19 years
    P012032	Total!!Female!!20 years
    P012033	Total!!Female!!21 years
    P012034	Total!!Female!!22 to 24 years
    P012035	Total!!Female!!25 to 29 years
    P012036	Total!!Female!!30 to 34 years
    P012037	Total!!Female!!35 to 39 years
    P012038	Total!!Female!!40 to 44 years
    P012039	Total!!Female!!45 to 49 years
    P012040	Total!!Female!!50 to 54 years
    P012041	Total!!Female!!55 to 59 years
    P012042	Total!!Female!!60 and 61 years
    P012043	Total!!Female!!62 to 64 years
    P012044	Total!!Female!!65 and 66 years
    P012045	Total!!Female!!67 to 69 years
    P012046	Total!!Female!!70 to 74 years
    P012047	Total!!Female!!75 to 79 years
    P012048	Total!!Female!!80 to 84 years
    P012049	Total!!Female!!85 years and over
    '''
    sex_col_names = ['county',    'total_sex_byage', 
                        'total_male',  'male_u5',     'male_5_9',      'male_10_14', 'male_15_17',   'male_18_19', 
                                       'male_20',     'male_21',       'male_22_24', 'male_25_29',   'male_30_34',   
                                       'male_35_39',  'male_40_44',    'male_45_49', 'male_50_54',   'male_55_59',   
                                       'male_60_61',  'male_62_64',    'male_65_66', 'male_67_69',   'male_70_74', 
                                       'male_75_79',  'male_80_84',    'male_85_over',

                        'total_female', 'female_u5',   'female_5_9',   'female_10_14', 'female_15_17', 'female_18_19', 
                                        'female_20',   'female_21',    'female_22_24', 'female_25_29', 'female_30_34', 
                                        'female_35_39','female_40_44', 'female_45_49', 'female_50_54', 'female_55_59', 
                                        'female_60_61','female_62_64', 'female_65_66', 'female_67_69', 'female_70_74',
                                        'female_75_79','female_80_84', 'female_85_over',
                      'state_id', 'county_id' ]
    
    col_types = {c: int for c in sex_col_names}
    col_types['county'] = str
   
    HOST, dataset = "https://api.census.gov/data/" + str(year), "dec/sf1"
    get_vars =  ["P012" + str(i + 1).zfill(3) for i in range(49)]
    get_vars = ["NAME"] + get_vars
    #print(f'GET_VARS: {get_vars}')
    predicates = {}
    predicates["get"] = ",".join(get_vars)
    predicates["for"] = "county:*"
    predicates["in"] = "state:08"
    predicates["key"] = key

    # Initialize data
    base_url = "/".join([HOST, dataset])
    r = requests.get(base_url, params=predicates)

    df = pd.DataFrame(columns=r.json()[0], data=r.json()[1:])
    df.columns = sex_col_names

    print(f'Gender Dataframe shape: {df.shape}')
    df['county'] = df['county'].apply((lambda s: get_county(s)))

    # Change Datatype for population variables to int64
    df = df.astype(col_types)
    return(df)

def get_housing_df(key, year):

    '''
    Name
    P018001	Total
    P018002	Total!!Family households
    P018003	Total!!Family households!!Husband-wife family
    P018004	Total!!Family households!!Other family
    P018005	Total!!Family households!!Other family!!Male householder, no wife present
    P018006	Total!!Family households!!Other family!!Female householder, no husband present
    P018007	Total!!Nonfamily households
    P018008	Total!!Nonfamily households!!Householder living alone
    P018009	Total!!Nonfamily households!!Householder not living alone
    H017001	Total	TENURE BY AGE OF HOUSEHOLDER
    H017002	Total!!Owner occupied
    H017003	Total!!Owner occupied!!Householder 15 to 24 years
    H017004	Total!!Owner occupied!!Householder 25 to 34 years
    H017005	Total!!Owner occupied!!Householder 35 to 44 years
    H017006	Total!!Owner occupied!!Householder 45 to 54 years
    H017007	Total!!Owner occupied!!Householder 55 to 59 years
    H017008	Total!!Owner occupied!!Householder 60 to 64 years
    H017009	Total!!Owner occupied!!Householder 65 to 74 years
    H017010	Total!!Owner occupied!!Householder 75 to 84 years
    H017011	Total!!Owner occupied!!Householder 85 years and over
    H017012	Total!!Renter occupied	TENURE BY AGE OF HOUSEHOLDER
    H017013	Total!!Renter occupied!!Householder 15 to 24 years
    H017014	Total!!Renter occupied!!Householder 25 to 34 years
    H017015	Total!!Renter occupied!!Householder 35 to 44 years
    H017016	Total!!Renter occupied!!Householder 45 to 54 years
    H017017	Total!!Renter occupied!!Householder 55 to 59 years
    H017018	Total!!Renter occupied!!Householder 60 to 64 years
    H017019	Total!!Renter occupied!!Householder 65 to 74 years
    H017020	Total!!Renter occupied!!Householder 75 to 84 years
    H017021	Total!!Renter occupied!!Householder 85 years and over
    '''

    housing_col_names = ['county',  

             'total_house_tenure', 'total_occupied',# 10
             'households_fam',    'households_husband_wife',  'households_other', 
             'households_other_male', 'households_other_owner', 'households_nonfam',  
             'householder_living_alone', 'householder_not_living_alone', 

             'total_owner', 'owner_15_24', 'owner_25_34', 'owner_35_44', 'owner_45_54',   
             'owner_55_59', 'owner_60_64', 'owner_65_74', 'owner_75_84', 'owner_85_up',

             'total_renter', 'renter_15_24', 'renter_25_34', 'renter_35_44', 'renter_45_54',   
             'renter_55_59',  'renter_60_64', 'renter_65_74', 'renter_75_84', 'renter_85_up',

          'state_id', 'county_id' ]
    
    col_types = {c: int for c in housing_col_names}
    col_types['county'] = str
    
    HOST, dataset = "https://api.census.gov/data/" + str(year), "dec/sf1"
    get_vars  =  ["P018" + str(i + 1).zfill(3) for i in range(9)]
    get_vars +=  ["H017" + str(i + 1).zfill(3) for i in range(21)]
    get_vars  = ["NAME"] + get_vars
    #print(f'GET_VARS: {get_vars}')
    predicates = {}
    predicates["get"] = ",".join(get_vars)
    predicates["for"] = "county:*"
    predicates["in"] = "state:08"
    predicates["key"] = key

    # Initialize data frame
    base_url = "/".join([HOST, dataset])
    r = requests.get(base_url, params=predicates)

    df = pd.DataFrame(columns=r.json()[0], data=r.json()[1:])
    #print(f'df features: {df.columns}')
    df.columns = housing_col_names

    print(f'Housing Dataframe shape: {df.shape}')

    # Change Datatype for population variables to int64
    df = df.astype(col_types)
    
    df['county'] = df['county'].apply((lambda s: get_county(s)))
    return(df)

def get_acs19_pop(key, year):

    '''
    Name
    Supplemental Estimates:
    API Example Call: api.census.gov/data/2019/acs/acsse?get=NAME,K200101_001E&for=state:*&key=YOUR_KEY_GOES_HERE
    K200101_001E	Estimate!!Total:	POPULATION BY SEX	 
    K200101_002E	Estimate!!Total:!!Male	POPULATION BY SEX	 
    K200101_003E	Estimate!!Total:!!Female	POPULATION BY SEX	 
    K200102_001E	Estimate!!Total:	POPULATION UNDER 18 YEARS BY AGE	 
    K200102_002E	Estimate!!Total:!!In households:	POPULATION UNDER 18 YEARS BY AGE	 
    K200102_003E	Estimate!!Total:!!In households:!!Under 3 years	POPULATION UNDER 18 YEARS BY AGE	 
    K200102_004E	Estimate!!Total:!!In households:!!3 to 5 years	POPULATION UNDER 18 YEARS BY AGE	 
    K200102_005E	Estimate!!Total:!!In households:!!6 to 8 years	POPULATION UNDER 18 YEARS BY AGE	 
    K200102_006E	Estimate!!Total:!!In households:!!9 to 11 years	POPULATION UNDER 18 YEARS BY AGE	 
    K200102_007E	Estimate!!Total:!!In households:!!12 to 14 years	POPULATION UNDER 18 YEARS BY AGE	 
    K200102_008E	Estimate!!Total:!!In households:!!15 to 17 years	POPULATION UNDER 18 YEARS BY AGE	 
    K200102_009E	Estimate!!Total:!!In group quarters	POPULATION UNDER 18 YEARS BY AGE	 
    K200103_001E	Estimate!!Median age --!!Total:	MEDIAN AGE BY SEX	 
    K200103_002E	Estimate!!Median age --!!Male	MEDIAN AGE BY SEX	 
    K200103_003E	Estimate!!Median age --!!Female	MEDIAN AGE BY SEX	 
    K200104_001E	Estimate!!Total:	POPULATION BY AGE	 
    K200104_002E	Estimate!!Total:!!Under 18 years	POPULATION BY AGE	 
    K200104_003E	Estimate!!Total:!!18 to 24 years	POPULATION BY AGE	 
    K200104_004E	Estimate!!Total:!!25 to 34 years	POPULATION BY AGE	 
    K200104_005E	Estimate!!Total:!!35 to 44 years	POPULATION BY AGE	 
    K200104_006E	Estimate!!Total:!!45 to 54 years	POPULATION BY AGE	 
    K200104_007E	Estimate!!Total:!!55 to 64 years	POPULATION BY AGE	 
    K200104_008E	Estimate!!Total:!!65 years and over	POPULATION BY AGE	 
    '''
    acs_pop_col_names = ['county',  
              'pop_by_sex', 'pbs_male', 'pbs_female' , 'pop_und18',
              'pop_und18_by_age', 'pop_lt3', 'pop_3_5', 'pop_6_8',
              'pop_9_11', 'pop_12_14', 'pop_15_17', 'pop_gq_und_18',
              'median_age', 'median_age_male', 'median_age_female',
              'total_pop_by_age', 'pop_all_und18', 'pop_all_18_24',
              'pop_all_25_34', 'pop_all_35_44', 'pop_all_45_54',
              'pop_all_55_64', 'pop_all_65_over',
              'state_id', 'county_id' ]

    col_types = {c: int for c in acs_pop_col_names}
    col_types['county'] = str
    col_types['median_age'] = float
    col_types['median_age_male'] = float
    col_types['median_age_female'] = float
    
    HOST, dataset = "https://api.census.gov/data/" + str(year), "acs/acsse"
    get_vars   =  ["K200101_" + str(i + 1).zfill(3) + "E" for i in range(3)]
    get_vars  +=  ["K200102_" + str(i + 1).zfill(3) + "E" for i in range(9)]
    get_vars  +=  ["K200103_" + str(i + 1).zfill(3) + "E" for i in range(3)]
    get_vars  +=  ["K200104_" + str(i + 1).zfill(3) + "E" for i in range(8)]
    get_vars   = ["NAME"] + get_vars
    #print(f'GET_VARS: {get_vars}')
    predicates = {}
    predicates["get"] = ",".join(get_vars)
    predicates["for"] = "county:*"
    predicates["in"] = "state:08"
    predicates["key"] = key

    # Initialize data frame
    base_url = "/".join([HOST, dataset])
    r = requests.get(base_url, params=predicates)

    df = pd.DataFrame(columns=r.json()[0], data=r.json()[1:])
    df.columns = acs_pop_col_names

    print(f'ACS Dataframe shape: {df.shape}')

    # Change Datatype for population variables to int64
    df.fillna(0, inplace = True)
    df = df.astype(col_types)  
    
    df['county'] = df['county'].apply((lambda s: get_county(s)))
    return(df)

def get_acs19_marital(key, year):

    '''
    Name
    Supplemental Estimates:
    API Example Call: api.census.gov/data/2019/acs/acsse?get=NAME,K200101_001E&for=state:*&key=YOUR_KEY_GOES_HERE
    K201001_001E    Estimate!!Total:    MARITAL STATUS FOR THE POPULATION 15 YEARS AND OVER  
    K201001_002E    Estimate!!Total:!!Never married MARITAL STATUS FOR THE POPULATION 15 YEARS AND OVER  
    K201001_003E    Estimate!!Total:!!Now married (except separated)    MARITAL STATUS FOR THE POPULATION 15 YEARS AND OVER  
    K201001_004E    Estimate!!Total:!!Separated MARITAL STATUS FOR THE POPULATION 15 YEARS AND OVER  
    K201001_005E    Estimate!!Total:!!Widowed   MARITAL STATUS FOR THE POPULATION 15 YEARS AND OVER  
    K201001_006E    Estimate!!Total:!!Divorced  MARITAL STATUS FOR THE POPULATION 15 YEARS AND OVER  
    '''
    acs_marital_col_names = ['county',  
              'total_marital', 'never_married', 'now_married', 'separated',
              'widowed', 'divorced','state_id', 'county_id' ]

    HOST, dataset = "https://api.census.gov/data/" + str(year), "acs/acsse"
    get_vars   =  ["K201001_" + str(i + 1).zfill(3) + "E" for i in range(6)]
    get_vars   = ["NAME"] + get_vars
    #print(f'GET_VARS: {get_vars}')
    predicates = {}
    predicates["get"] = ",".join(get_vars)
    predicates["for"] = "county:*"
    predicates["in"] = "state:08"
    predicates["key"] = key

    # Initialize data frame
    base_url = "/".join([HOST, dataset])
    r = requests.get(base_url, params=predicates)

    df = pd.DataFrame(columns=r.json()[0], data=r.json()[1:])
    df.columns = acs_marital_col_names

    print(f'ACS Dataframe shape: {df.shape}')

    # Change Datatype for population variables to int64
    df.fillna(0, inplace = True)
    df = df.astype({'total_marital': int, 'never_married': int, 'now_married': int, 'separated': int,
              'widowed': int, 'divorced': int,'state_id': int, 'county_id': int })
    df['county'] = df['county'].apply((lambda s: get_county(s)))
    return(df)

def get_acs19_poverty(key, year):

    '''
    Name
    
    K201703_001E	Estimate!!Total:	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_002E	Estimate!!Total:!!Income in the past 12 months below poverty level:	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_003E	Estimate!!Total:!!Income in the past 12 months below poverty level:!!Married-couple family	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_004E	Estimate!!Total:!!Income in the past 12 months below poverty level:!!Other families:	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_005E	Estimate!!Total:!!Income in the past 12 months below poverty level:!!Other families:!!Male householder, no wife present	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_006E	Estimate!!Total:!!Income in the past 12 months below poverty level:!!Other families:!!Female householder, no husband present	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_007E	Estimate!!Total:!!Income in the past 12 months at or above poverty level:	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_008E	Estimate!!Total:!!Income in the past 12 months at or above poverty level:!!Married-couple family	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_009E	Estimate!!Total:!!Income in the past 12 months at or above poverty level:!!Other families:	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_010E	Estimate!!Total:!!Income in the past 12 months at or above poverty level:!!Other families:!!Male householder, no wife present	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_011E	Estimate!!Total:!!Income in the past 12 months at or above poverty level:!!Other families:!!Female householder, no husband present	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201801_001E	Estimate!!Total:	DISABILITY STATUS BY AGE	 
    K201801_002E	Estimate!!Total:!!With a disability:	DISABILITY STATUS BY AGE	 
    K201801_003E	Estimate!!Total:!!With a disability:!!Under 18 years	DISABILITY STATUS BY AGE	 
    K201801_004E	Estimate!!Total:!!With a disability:!!18 to 64 years	DISABILITY STATUS BY AGE	 
    K201801_005E	Estimate!!Total:!!With a disability:!!65 years and over	DISABILITY STATUS BY AGE	 
    K201801_006E	Estimate!!Total:!!No disability	DISABILITY STATUS BY AGE	 
    K201802_001E	Estimate!!Total:	WORK EXPERIENCE BY DISABILITY STATUS                                                     'total_dis_by_status'
    K201802_002E	Estimate!!Total:!!Worked full-time, year round:	WORK EXPERIENCE BY DISABILITY STATUS	                     'total_full_yr_by_dis'
    K201802_003E	Estimate!!Total:!!Worked full-time, year round:!!With a disability	WORK EXPERIENCE BY DISABILITY STATUS	 'full_yr_w_dis'
    K201802_004E	Estimate!!Total:!!Worked full-time, year round:!!No disability	WORK EXPERIENCE BY DISABILITY STATUS	     'full_yr_wo_dis'
    K201802_005E	Estimate!!Total:!!Worked less than full-time, year round:	WORK EXPERIENCE BY DISABILITY STATUS	          'total_less_yr_dis_sts'
    K201802_006E	Estimate!!Total:!!Worked less than full-time, year round:!!With a disability	WORK EXPERIENCE BY DISABILITY STATUS	 'less_yr_w_dis'
    K201802_007E	Estimate!!Total:!!Worked less than full-time, year round:!!No disability	WORK EXPERIENCE BY DISABILITY STATUS	      'less_yr_wo_dis'
    K201802_008E	Estimate!!Total:!!Did not work:	WORK EXPERIENCE BY DISABILITY STATUS	                                                  'total_no_work_dis_sts'
    K201802_009E	Estimate!!Total:!!Did not work:!!With a disability	WORK EXPERIENCE BY DISABILITY STATUS	                              'no_work_w_dis' 
    K201802_010E	Estimate!!Total:!!Did not work:!!No disability	WORK EXPERIENCE BY DISABILITY STATUS	                                  'no_work_wo_dis'
    K201803_001E	Estimate!!Total:	TYPES OF DISABILITIES	                                                                              'total_types_dis'
    K201803_002E	Estimate!!Total:!!With a disability:	TYPES OF DISABILITIES	                                                          'total_types_w_dis'
    K201803_003E	Estimate!!Total:!!With a disability:!!With a hearing difficulty	TYPES OF DISABILITIES	                                   'types_hearing'
    K201803_004E	Estimate!!Total:!!With a disability:!!With a vision difficulty	TYPES OF DISABILITIES	                                   'types_vision'
    K201803_005E	Estimate!!Total:!!With a disability:!!With a cognitive difficulty	TYPES OF DISABILITIES	                               'types_cognitive'
    K201803_006E	Estimate!!Total:!!With a disability:!!With an ambulatory difficulty	TYPES OF DISABILITIES	                               'types_ambulatory'
    K201803_007E	Estimate!!Total:!!With a disability:!!With a self-care difficulty	TYPES OF DISABILITIES	                               'types_self_care'
    K201803_008E	Estimate!!Total:!!With a disability:!!With an independent living difficulty	TYPES OF DISABILITIES	                       'types_ind_living'
    K201803_009E	Estimate!!Total:!!No disability	TYPES OF DISABILITIES	                                                                   'types_no_dis'
   
    '''
    acs_poverty_col_names = ['county',   
                                                     
             # POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE (11)             
             'total_pov_hsh_type',
                  'total_below_pov',
                        'pov_below_married_cpl', 'pov_below_other', 'pov_below_other_male', 
                        'pov_below_other_female', 
                  'total_above_pov_hsh_type', 
                        'above_pov_married_cpl', 'above_pov_other', 'above_pov_other_male', 
                        'above_pov_other_female',
     
            # DISABILITY STATUS BY AGE (6)
              'total_disability_status_by_age', 
                    'disability_ubd_18', 'diability_18_64', 'disability_65_over', 'no_disability_by_age', 
                    'pov_above_female_no_hus', 
               
            # WORK EXPERIENCE BY DISABILITY STATUS (10)
             'total_dis_by_status', 'total_full_yr_by_dis', 
                             'full_yr_w_dis', 'full_yr_wo_dis',
             'total_less_yr_dis_sts', 
                             'less_yr_w_dis', 'less_yr_wo_dis', 
             'total_no_work_dis_sts',  
                    'no_work_w_dis' ,  'no_work_wo_dis',    
                             
           # TYPES OF DISABILITIES (9+2)                  
            'total_types_dis', 'total_types_w_dis', 'types_hearing', 'types_vision', 'types_cognitive', 
                             'types_ambulatory', 'types_self_care', 'types_ind_living', 'types_no_dis',
                             'state_id', 'county_id' ]
    
   
    col_types = {c: int for c in acs_poverty_col_names}
    col_types['county'] = str
    

    HOST, dataset = "https://api.census.gov/data/" + str(year), "acs/acsse"
    
    get_vars   =  ["K201703_" + str(i + 1).zfill(3) + "E" for i in range(11)] # POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE
    get_vars  +=  ["K201801_" + str(i + 1).zfill(3) + "E" for i in range(6)]  # DISABILITY STATUS BY AGE	 
    get_vars  +=  ["K201802_" + str(i + 1).zfill(3) + "E" for i in range(10)] # WORK EXPERIENCE BY DISABILITY STATUS
    get_vars  +=  ["K201803_" + str(i + 1).zfill(3) + "E" for i in range(9)]  # TYPES OF DISABILITIES
   
    get_vars   = ["NAME"] + get_vars
    #print(f'GET_VARS: {get_vars}')
    #print(f'len(GET_VARS) {len(get_vars)}')
    #print(f'len(acs_poverty_col_names): {len(acs_poverty_col_names)}')
    predicates = {}
    predicates["get"] = ",".join(get_vars)
    predicates["for"] = "county:*"
    predicates["in"] = "state:08"
    predicates["key"] = key

    # Initialize data frame
    base_url = "/".join([HOST, dataset])
    r = requests.get(base_url, params=predicates)
    #print(f'URL: {r.url}')
    #print(f'JSON Arguments: {r.json()[0]}')
    df = pd.DataFrame(columns=r.json()[0], data=r.json()[1:])
    df.columns = acs_poverty_col_names

    print(f'ACS Poverty Dataframe shape: {df.shape}')
    
    df.fillna(0, inplace = True)
    # Change Datatype for population variables to int64
    df = df.astype(col_types)
    
    df['county'] = df['county'].apply((lambda s: get_county(s)))
    return(df)


def get_acs19_income(key,year = 2019, geo = 'county'):

    '''
    Name
    
    K201703_001E	Estimate!!Total:	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_002E	Estimate!!Total:!!Income in the past 12 months below poverty level:	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_003E	Estimate!!Total:!!Income in the past 12 months below poverty level:!!Married-couple family	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_004E	Estimate!!Total:!!Income in the past 12 months below poverty level:!!Other families:	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_005E	Estimate!!Total:!!Income in the past 12 months below poverty level:!!Other families:!!Male householder, no wife present	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_006E	Estimate!!Total:!!Income in the past 12 months below poverty level:!!Other families:!!Female householder, no husband present	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_007E	Estimate!!Total:!!Income in the past 12 months at or above poverty level:	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_008E	Estimate!!Total:!!Income in the past 12 months at or above poverty level:!!Married-couple family	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_009E	Estimate!!Total:!!Income in the past 12 months at or above poverty level:!!Other families:	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_010E	Estimate!!Total:!!Income in the past 12 months at or above poverty level:!!Other families:!!Male householder, no wife present	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201703_011E	Estimate!!Total:!!Income in the past 12 months at or above poverty level:!!Other families:!!Female householder, no husband present	POVERTY STATUS IN THE PAST 12 MONTHS OF FAMILIES BY HOUSEHOLD TYPE	 
    K201801_001E	Estimate!!Total:	DISABILITY STATUS BY AGE	 
    K201801_002E	Estimate!!Total:!!With a disability:	DISABILITY STATUS BY AGE	 
    K201801_003E	Estimate!!Total:!!With a disability:!!Under 18 years	DISABILITY STATUS BY AGE	 
    K201801_004E	Estimate!!Total:!!With a disability:!!18 to 64 years	DISABILITY STATUS BY AGE	 
    K201801_005E	Estimate!!Total:!!With a disability:!!65 years and over	DISABILITY STATUS BY AGE	 
    K201801_006E	Estimate!!Total:!!No disability	DISABILITY STATUS BY AGE	 
    K201802_001E	Estimate!!Total:	WORK EXPERIENCE BY DISABILITY STATUS	 
    K201802_002E	Estimate!!Total:!!Worked full-time, year round:	WORK EXPERIENCE BY DISABILITY STATUS	 
    K201802_003E	Estimate!!Total:!!Worked full-time, year round:!!With a disability	WORK EXPERIENCE BY DISABILITY STATUS	 
    K201802_004E	Estimate!!Total:!!Worked full-time, year round:!!No disability	WORK EXPERIENCE BY DISABILITY STATUS	 
    K201802_005E	Estimate!!Total:!!Worked less than full-time, year round:	WORK EXPERIENCE BY DISABILITY STATUS	 
    K201802_006E	Estimate!!Total:!!Worked less than full-time, year round:!!With a disability	WORK EXPERIENCE BY DISABILITY STATUS	 
    K201802_007E	Estimate!!Total:!!Worked less than full-time, year round:!!No disability	WORK EXPERIENCE BY DISABILITY STATUS	 
    K201802_008E	Estimate!!Total:!!Did not work:	WORK EXPERIENCE BY DISABILITY STATUS	 
    K201802_009E	Estimate!!Total:!!Did not work:!!With a disability	WORK EXPERIENCE BY DISABILITY STATUS	 
    K201802_010E	Estimate!!Total:!!Did not work:!!No disability	WORK EXPERIENCE BY DISABILITY STATUS	 
    K201803_001E	Estimate!!Total:	TYPES OF DISABILITIES	 
    K201803_002E	Estimate!!Total:!!With a disability:	TYPES OF DISABILITIES	 
    K201803_003E	Estimate!!Total:!!With a disability:!!With a hearing difficulty	TYPES OF DISABILITIES	 
    K201803_004E	Estimate!!Total:!!With a disability:!!With a vision difficulty	TYPES OF DISABILITIES	 
    K201803_005E	Estimate!!Total:!!With a disability:!!With a cognitive difficulty	TYPES OF DISABILITIES	 
    K201803_006E	Estimate!!Total:!!With a disability:!!With an ambulatory difficulty	TYPES OF DISABILITIES	 
    K201803_007E	Estimate!!Total:!!With a disability:!!With a self-care difficulty	TYPES OF DISABILITIES	 
    K201803_008E	Estimate!!Total:!!With a disability:!!With an independent living difficulty	TYPES OF DISABILITIES	 
    K201803_009E	Estimate!!Total:!!No disability	TYPES OF DISABILITIES	 
    K201901_001E	Estimate!!Total:	HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201901_002E	Estimate!!Total:!!Less than $20,000	HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201901_003E	Estimate!!Total:!!$20,000 to $39,999	HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201901_004E	Estimate!!Total:!!$40,000 to $59,999	HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201901_005E	Estimate!!Total:!!$60,000 to $99,999	HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201901_006E	Estimate!!Total:!!$100,000 to $149,999	HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201901_007E	Estimate!!Total:!!$150,000 to $199,999	HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201901_008E	Estimate!!Total:!!$200,000 or more	HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201902_001E	Estimate!!Median household income in the past 12 months (in 2019 inflation-adjusted dollars)	MEDIAN HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201903_001E	Estimate!!Total:	FAMILY INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201903_002E	Estimate!!Total:!!Less than $20,000	FAMILY INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201903_003E	Estimate!!Total:!!$20,000 to $39,999	FAMILY INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201903_004E	Estimate!!Total:!!$40,000 to $59,999	FAMILY INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201903_005E	Estimate!!Total:!!$60,000 to $99,999	FAMILY INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201903_006E	Estimate!!Total:!!$100,000 to $149,999	FAMILY INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201903_007E	Estimate!!Total:!!$150,000 to $199,999	FAMILY INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201903_008E	Estimate!!Total:!!$200,000 or more	FAMILY INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201904_001E	Estimate!!Median family income in the past 12 months (in 2019 inflation-adjusted dollars)	MEDIAN FAMILY INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K201905_001E	Estimate!!Median nonfamily household income in the past 12 months (in 2019 inflation-adjusted dollars)	MEDIAN NONFAMILY HOUSEHOLD INCOME IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS)	 
    K202002_001E	Estimate!!Median earnings in the past 12 months (in 2019 Inflation-adjusted dollars) --!!Total (dollars):	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) BY SEX BY WORK EXPERIENCE IN THE PAST 12 MONTHS FOR THE POPULATION 16 YEARS AND OVER WITH EARNINGS IN THE PAST 12 MONTHS	 
    K202002_002E	Estimate!!Median earnings in the past 12 months (in 2019 Inflation-adjusted dollars) --!!Male --!!Total (dollars)	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) BY SEX BY WORK EXPERIENCE IN THE PAST 12 MONTHS FOR THE POPULATION 16 YEARS AND OVER WITH EARNINGS IN THE PAST 12 MONTHS	 
    K202002_003E	Estimate!!Median earnings in the past 12 months (in 2019 Inflation-adjusted dollars) --!!Male --!!Worked full-time, year-round in the past 12 months (dollars)	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) BY SEX BY WORK EXPERIENCE IN THE PAST 12 MONTHS FOR THE POPULATION 16 YEARS AND OVER WITH EARNINGS IN THE PAST 12 MONTHS	 
    K202002_004E	Estimate!!Median earnings in the past 12 months (in 2019 Inflation-adjusted dollars) --!!Total (dollars)	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) BY SEX BY WORK EXPERIENCE IN THE PAST 12 MONTHS FOR THE POPULATION 16 YEARS AND OVER WITH EARNINGS IN THE PAST 12 MONTHS	 
    K202002_005E	Estimate!!Median earnings in the past 12 months (in 2019 Inflation-adjusted dollars) --!!Worked full-time, year-round in the past 12 months (dollars)	MEDIAN EARNINGS IN THE PAST 12 MONTHS (IN 2019 INFLATION-ADJUSTED DOLLARS) BY SEX BY WORK EXPERIENCE IN THE PAST 12 MONTHS FOR THE POPULATION 16 YEARS AND OVER WITH EARNINGS IN THE PAST 12 MONTHS	 
    '''
    acs_income_col_names = ['county',                       
            
            'total_hsh_inc', 'hsh_inc_lt20', 'hsh_inc_20_40', 'hsh_inc_40_60', 'hsh_inc_60_100', 
                   'hsh_inc_100_150','hsh_inc_150_200', 'hsh_inc_200_plus',
            
            'med_household_inc',

            'total_fam_inc', 'fam_inc_lt20', 'fam_inc_20_40', 'fam_inc_40_60', 'fam_inc_60_100', 
                             'fam_inc_100_150','fam_inc_150_200', 'fam_inc_200_plus',
                
            'med_fam_inc', 
            'med_nf_inc', 
            'med_earn_sex', 'med_earn_male', 'med_earn_male_full', 'med_earn_female', 'med_earn_female_full',
                             'state_id', 'county_id' ]
    
    col_types = {c: int for c in acs_income_col_names}
    col_types['county'] = str
    for col in ['med_fam_inc', 'med_nf_inc', 'med_earn_sex', 'med_earn_male', 
                'med_earn_male_full', 'med_earn_female', 'med_earn_female_full']:
        col_types[col] = float
    
    HOST, dataset = "https://api.census.gov/data/" + str(year), "acs/acsse"
    

    get_vars   =  ["K201901_" + str(i + 1).zfill(3) + "E" for i in range(8)]  # HOUSEHOLD INCOME IN THE PAST 12 MONTHS
    get_vars  +=  ["K201902_" + str(i + 1).zfill(3) + "E" for i in range(1)]  # MEDIAN HOUSEHOLD INCOME IN THE PAST 12 MONTHS
    get_vars  +=  ["K201903_" + str(i + 1).zfill(3) + "E" for i in range(8)]  # $200,000 or more	FAMILY INCOME IN THE PAST 12 MONTHS 
    get_vars  +=  ["K201904_" + str(i + 1).zfill(3) + "E" for i in range(1)]  # Median family income in the past 12 months 
    get_vars  +=  ["K201905_" + str(i + 1).zfill(3) + "E" for i in range(1)]  # Median nonfamily household income in the past 12 months 
    get_vars  +=  ["K202002_" + str(i + 1).zfill(3) + "E" for i in range(5)]  # Median earnings in the past 12 months 
   
    get_vars   = ["NAME"] + get_vars
    #print(f'GET_VARS: {get_vars}')
    #print(f'len(GET_VARS) {len(get_vars)}')
   
    predicates = {}
    predicates["get"] = ",".join(get_vars)
    if (geo == 'county'):
        predicates["for"] = "county:*"
    else:
        predicates["for"] = "congressional district:*"
        acs_income_col_names[0] = 'congressional_dist'
        acs_income_col_names[-1] = 'congdist_id'
        
    predicates["in"] = "state:08"
    predicates["key"] = key

    # Initialize data frame
    base_url = "/".join([HOST, dataset])
    r = requests.get(base_url, params=predicates)
    
    df = pd.DataFrame(columns=r.json()[0], data=r.json()[1:])
    df.columns = acs_income_col_names

    print(f'ACS Income Dataframe shape: {df.shape}')
    if (geo == 'county'):
        df['county'] = df['county'].apply((lambda s: get_county(s)))
    else:
        df['congressional_dist'] = df['congressional_dist'].apply((lambda s: get_cong_dist(s)))
    
    # Change Datatype for population variables to int64
    df.fillna(0, inplace = True)
    #df = df.astype(col_types)

    return(df)

def get_population_cong_df(key, year):
    '''
    Name
    P001001 Total Population
    P002001 Total Urban and Rural
    P002002 Total Urban
    P002003 Total Urban inside urbanized areas
    P002004 Total Urban inside urban clusters
    P002005 Total Rural
    P003001 Total Race
    P003002 Total White Alone
    P003003 Total Black or African American alone
    P003004 Total American Indian and Alaska Native alone
    P003005 Total Asian alone
    P003006 Total Native Hawaiian and Other Pacific Islander
    P003007 Total Some Other Race Alone
    P003008 Total Two or More Races
    P004001 Total Hispanic or Latino Origin
    P004002 Total Not Hispanic or Latino Origin
    P004003 Total Hispanic or Latino Origin
    '''
    pop_col_names = ['county', 'total_pop', 'total_urb_rur', 'urban', 'urban_ins_ars', 
                     'urban_ins_cls', 'rural',  'total_race', 'white', 'black', 'american_indian',    
                     'asian', 'nat_hawaiian', 'some_othr_race', 'two_or_more_races','hisp_latino',
                     'not_hisp_latino', 'total_hisp_latino', 'state_id', 'county_id']
    
    
    col_types = {c: int for c in pop_col_names}
    col_types['county'] = str

    HOST, dataset = "https://api.census.gov/data/" + str(year), "dec/sf1"
    get_vars =  ["P001" + str(i + 1).zfill(3) for i in range(1)]
    get_vars += ["P002" + str(i + 1).zfill(3) for i in range(5)]
    get_vars += ["P003" + str(i + 1).zfill(3) for i in range(8)]
    get_vars += ["P004" + str(i + 1).zfill(3) for i in range(3)]
    get_vars = ["NAME"] + get_vars

    predicates = {}
    predicates["get"] = ",".join(get_vars)
    predicates["for"] = "08:*"
    predicates["in"] = "state:08"
    predicates["key"] = key
    #print(f'PREDICATES: {predicates}.')

    # Initialize data frame
    base_url = "/".join([HOST, dataset])
    r = requests.get(base_url, params=predicates)
    print(f'\n\nURL: {r.url}')

    df = pd.DataFrame(columns=r.json()[0], data=r.json()[1:])
    df.columns = pop_col_names

    print(f'Population Dataframe shape: {df.shape}')

    # Change Datatype for population variables to int64
    df.iloc[:,1:] = df.iloc[:,1:].apply(lambda x: pd.to_numeric(x)) 
    #df['county'] = df['county'].apply((lambda s: get_county(s)))
    df = df.astype(col_types)
    return(df)

import os
os.getcwd()
from os import listdir
import pandas as pd
from os.path import isfile, join
import glob
import plotly.graph_objects as go
import geopandas as gpd
import matplotlib.pyplot as plt

def gen_colo_choropleth(dfi, df_description, var, title, palette = 'RdBu'):
    '''
    gen_colo_choropleth:  Uses baseline geometry of Colorado county map combined with data frame containing county 
            data values and generates a choropleth figure that should plot directly into the Jupyter notebook.  
            Additionally, the figure is saved as a png file in the img directory.
            
    colorscale – Sets the colorscale. The colorscale must be an array containing arrays mapping a normalized value to an 
    rgb, rgba, hex, hsl, hsv, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are 
    required. For example, [[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]. To control the bounds of the colorscale in color space, use`zmin` and zmax. 
    
    Alternatively, colorscale may be a palette name string of the following list: 
    Greys,YlGnBu,Greens,YlOrR d,Bluered,RdBu,Reds,Blues,Picnic,Rainbow,Portland,Jet,H ot,Blackbody,Earth,Electric,Viridis,Cividis.

    
    '''
    # This is the baseline map for all of our choropleth maps - Colorado counties.
    fp =  '../data/shape/Colorado_County_Boundaries.shp'

    map_df = gpd.read_file(fp)
   
    # change the data types of the key index fields to integer so that it matches our census data index
    map_df = map_df.astype({"CNTY_FIPS": int, "US_FIPS": int})

    # Load the data dataframe 
    data_df = dfi.copy(deep = True)

    # Fix up Data 
    data_df = data_df.rename(columns={"state_id": "STATEFP", "county_id": "CNTY_FIPS"})

    # join the geodataframe with the cleaned up census dataframe
    merged = map_df.set_index(['CNTY_FIPS']).join(data_df.set_index(['CNTY_FIPS']))

    # set a variable that will call whatever column we want to visualise on the map
    variable = var  # Majority?

    # set the range for the choropleth
    vmin = min(pd.to_numeric(data_df[var]))
    vmax = max(pd.to_numeric(data_df[var]))
    print(f'vmin: {vmin} vmax: {vmax}')

    # create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(10, 6))

    # create map
    merged.plot(column=variable, cmap=palette, linewidth=0.8, ax=ax, edgecolor='0.8')

    # remove the axis
    ax.axis('off')

    # add a title
    ax.set_title(title, fontdict={'fontsize': '14', 'fontweight' : '3'})

    # data source annotation
    ax.annotate(f'Source: Census.gov & CDPHE Open Data, (color palette: {palette})',xy=(0.1, .08),  xycoords='figure fraction', 
                horizontalalignment='left', verticalalignment='top', fontsize=9, color='#555555')

    # Create colorbar as a legend
    sm = plt.cm.ScalarMappable(cmap= palette, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # empty array for the data range
    sm._A = []
    # add the colorbar to the figure
    cbar = fig.colorbar(sm)

    fn = "../img/" +df_description + '_' + var + '_' + palette + '.png'
    fig.savefig(fn, dpi=600)
    #plt.close()
    return

def gen_colo_redblue(dfi, df_description, var , title, palette = 'RdBu'):
    '''
    gen_colo_choropleth:  Uses baseline geometry of Colorado county map combined with data frame containing county 
            data values and generates a choropleth figure that should plot directly into the Jupyter notebook.  
            Additionally, the figure is saved as a png file in the img directory.
            
    colorscale – Sets the colorscale. The colorscale must be an array containing arrays mapping a normalized value to an 
    rgb, rgba, hex, hsl, hsv, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are 
    required. For example, [[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]. To control the bounds of the colorscale in color space, use`zmin` and zmax. 
    
    Alternatively, colorscale may be a palette name string of the following list: 
    Greys,YlGnBu,Greens,YlOrR d,Bluered,RdBu,Reds,Blues,Picnic,Rainbow,Portland,Jet,H ot,Blackbody,Earth,Electric,Viridis,Cividis.

    
    '''
    # This is the baseline map for all of our choropleth maps - Colorado counties.
    fp =  '../data/shape/Colorado_County_Boundaries.shp'

    map_df = gpd.read_file(fp)
   
    # change the data types of the key index fields to integer so that it matches our census data index
    map_df = map_df.astype({"CNTY_FIPS": int, "US_FIPS": int})

    # Load the data dataframe 
    data_df = dfi.copy(deep = True)

    # Fix up Data 
    data_df = data_df.rename(columns={"state_id": "STATEFP", "county_id": "CNTY_FIPS"})

    # join the geodataframe with the cleaned up census dataframe
    merged = map_df.set_index(['CNTY_FIPS']).join(data_df.set_index(['CNTY_FIPS']))

    # set a variable that will call whatever column we want to visualise on the map
    variable = winner  # Majority?

    # set the range for the choropleth
    vmin = 0
    vmax = 1
    print(f'vmin: {vmin} vmax: {vmax}')

    # create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(10, 6))

    # create map
    merged.plot(column=variable, cmap=palette, linewidth=0.8, ax=ax, edgecolor='0.8')

    # remove the axis
    ax.axis('off')

    # add a title
    ax.set_title(title, fontdict={'fontsize': '14', 'fontweight' : '3'})

    # data source annotation
    ax.annotate(f'Source: Census.gov & CDPHE Open Data, (color palette: {palette})',xy=(0.1, .08),  xycoords='figure fraction', 
                horizontalalignment='left', verticalalignment='top', fontsize=9, color='#555555')

    # Create colorbar as a legend
    sm = plt.cm.ScalarMappable(cmap= palette, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # empty array for the data range
    sm._A = []
    # add the colorbar to the figure
    cbar = fig.colorbar(sm)

    fn = "../img/" +df_description + '_' + var + '_' + palette + '.png'
    #fig.savefig(fn, dpi=600)
    #plt.close()
    return

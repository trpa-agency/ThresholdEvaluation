from utils import *
import pandas as pd
# global variables
# get path to save the file
out_chart = local_path.parents[1] / '2023/SoilConservation/Chart'
# set the template, font, and config for the charts
template = 'plotly_white'
font     = 'Calibri'
config   = {"displayModeBar": False}

# get soil conservation data
def get_soil_conservation_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql('SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_SoilConservation_ImperviousOverlayAnalysis_Change', conn)
    return df

# get soil conservation data from web
def get_soil_conservation_data_web():
    impervious_change_url       = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/81"
    impervious_landcap_2019_url = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/82"
    dfImpChg = get_fs_data(impervious_change_url)
    dfImp2019 = get_fs_data(impervious_landcap_2019_url)
    return dfImpChg, dfImp2019

def transform_soil_conservation_data(dfImpChg, dfImp2019):
    df = dfImpChg.astype({"Land_Capab": str})
    df = df.rename(columns={'Land_Capab':'Land Capability', 'GISAcre':'Total Acres', 'OWNERSHIP_': 'Ownership'})
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df[df['Land Capability'].notna()]
    df.set_index('Land Capability')
    dfLCType = df.groupby("Land Capability")["Total Acres"].sum().reset_index()

    df = dfLCType.replace(to_replace='None', value=np.nan).dropna()

    # 2019 analysis results
    df = dfImp2019.astype({"Land_Capab": str})
    df = df.rename(columns={'Land_Capab':'Land Capability', 'GISAcre':'Acre'})
    df.set_index('Land Capability')

    df.loc[(df['Surface']=='Soft')&(df['Feature']=='Trail'), 'Acre'] = df.Acre * 0.5 

    # pivot land capbility by acres of surface type
    pivotSoilImp = pd.pivot_table(df,index=['Land Capability'],
                                columns='Surface',
                                values=['Acre'], 
                                aggfunc=np.sum,fill_value=0)

    flattened = pd.DataFrame(pivotSoilImp.to_records())

    df = flattened.rename(columns={"('Acre', 'Hard')":'Acres of Hard Surface 2019',
                                "('Acre', 'Soft')":'Acres of Soft Surface 2019'})

    # replace all spaces ond blanks with NaN
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df[df['Land Capability'].notna()]

    # calculate acres of coverage
    df["Acres of Coverage 2019"]= df["Acres of Hard Surface 2019"]+df["Acres of Soft Surface 2019"]

    # merge grouped land capability data frame with impervious pivot data frame
    dfMerge = pd.merge(df, dfLCType, on='Land Capability')

    # rename field
    df = dfMerge.rename(columns={'Acre':'Total Acres'})

    # calculate perent coverage
    df['Percent Hard 2019'] = (df['Acres of Hard Surface 2019']/df['Total Acres'])*100
    df['Percent Soft 2019'] = (df['Acres of Soft Surface 2019']/df['Total Acres'])*100
    df['Percent Impervious 2019'] = ((df['Acres of Hard Surface 2019']+df['Acres of Soft Surface 2019'])/df['Total Acres'])*100

    # record percent allowed field
    df['Threshold Value'] = "0%"
    df.loc[df['Land Capability'].isin(['1A','1B','1C','2']), 'Threshold Value'] = "1%"
    df.loc[df['Land Capability'].isin(['3']), 'Threshold Value'] = "5%"
    df.loc[df['Land Capability'].isin(['4']), 'Threshold Value'] = "20%"
    df.loc[df['Land Capability'].isin(['5']), 'Threshold Value'] = "25%"
    df.loc[df['Land Capability'].isin(['6','7']), 'Threshold Value'] = "30%"

    # determine acres of coverage allowed per land capability
    df['Threshold Acres'] = 0
    df.loc[df['Land Capability'].isin(['1A','1B','1C','2']), 'Threshold Acres'] = df['Total Acres']*0.01
    df.loc[df['Land Capability'].isin(['3']), 'Threshold Acres'] = df['Total Acres']*0.05
    df.loc[df['Land Capability'].isin(['4']), 'Threshold Acres'] = df['Total Acres']*0.2
    df.loc[df['Land Capability'].isin(['5']), 'Threshold Acres'] = df['Total Acres']*0.25
    df.loc[df['Land Capability'].isin(['6','7']), 'Threshold Acres'] = df['Total Acres']*0.3

    df2019 = df.drop(columns=['Threshold Acres', 'Threshold Value', 'Total Acres'])

    df = df[['Land Capability',
            'Acres of Hard Surface 2019',
            'Acres of Soft Surface 2019',
            'Acres of Coverage 2019',
            'Percent Hard 2019',
            'Percent Soft 2019',
            'Percent Impervious 2019',
            'Total Acres',
            'Threshold Value',
            'Threshold Acres']]

    df.dropna(subset=['Land Capability'], inplace=True)

    df['Land Capability']= pd.Categorical(df['Land Capability'], ['1A', '1B', '1C', '2', '3', '4', '5', '6', '7'])

    df.sort_values(by="Land Capability")
    df.set_index('Land Capability')
    return df

# transform new coverage data
def transform_new_coverage_data():
    dfNewImp = pd.read_csv("data/raw_data/FinalCoverageChanges_2020-2023.csv")
    # fill any NaN values with 0
    dfNewImp.fillna(0, inplace=True)
    # drop parcle and jurisdiction columns
    dfNewImp.drop(['Parcel', 'Jurisdiction'], axis=1, inplace=True)
    # group by
    df = dfNewImp.groupby(['Bailey1a', 'Bailey1b', 'Bailey1c', 'Bailey2', 'Bailey3', 'Bailey4', 'Bailey5', 'Bailey6', 'Bailey7']).sum()
    df = df.reset_index()
    # stack the dataframe
    df = df.stack().reset_index()
    # # rename columns
    df.rename(columns={'level_1':'LandCapability', 0:'SqFt'}, inplace=True)
    # # drop columns
    df.drop(['level_0'], axis=1, inplace=True)
    # pivot the dataframe
    pivot = pd.pivot_table(df,index=['LandCapability'],
                                values='SqFt', aggfunc=np.sum)
    # flatten pivot
    flattened = pd.DataFrame(pivot.to_records())
    # create acres column
    flattened['Acres'] = flattened['SqFt']/43560
    # rename values
    landcap_dict = {'Bailey1a':'1A', 
                    'Bailey1b':'1B', 
                    'Bailey1c':'1C', 
                    'Bailey2':'2', 
                    'Bailey3':'3', 
                    'Bailey4':'4', 
                    'Bailey5':'5', 
                    'Bailey6':'6', 
                    'Bailey7':'7'}
    # map values
    flattened['LandCapability'] = flattened['LandCapability'].map(landcap_dict)
    # to csv
    flattened.to_csv(r"data/processed_data/LandCapability_Acres.csv")
    df = flattened
    return df

# add new coverage to existing coverage
def add_new_coverage(dfImpOld, dfImpNew):
    # rename acres to Acres of New Coverage
    dfImpNew.rename(columns={'Acres':'Acres of New Coverage', 'LandCapability':'Land Capability'}, inplace=True)
    # merge old and new data
    dfImp = pd.merge(dfImpOld, dfImpNew, on='Land Capability', how='left')
    dfImp['Acres of Coverage 2023'] = dfImp['Acres of New Coverage'] + dfImp['Acres of Coverage 2019']
    return dfImp

# plot soil conservation data
def plot_soil_conservation(df):
    df = df.sort_values(by='Land Capability')
    # create a bar chart
    
    return None
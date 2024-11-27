from utils import *
# get modules
import arcpy
from pathlib import Path
from great_tables import *
# current working directory
out_chart = local_path.parents[1] / '2023/Cumulative_Accounting'
local_path = pathlib.Path().absolute()
# workspace gdb for stuff that doesnt work in memory
gdb = os.path.join(local_path,'Workspace.gdb')

# get locations
sdeBase = r'F:\GIS\PROJECTS\ResearchAnalysis\ThresholdEvaluation\Vector.sde'
# config, template, and font for the charts
config = {"displayModeBar": False}
template = 'plotly_white'
font     = 'Calibri'


def get_allocations():
    # Get the allocations data
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM SDE.ThresholdEvaluation_CumulativeAccounting_Allocations", conn)
    return df

def get_applications():
    # Get the applications data
    # make sql database connection with pyodbc
    engine = get_conn('tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM SDE.ThresholdEvaluation_CumulativeAccounting_Applications", conn)
    return df

def get_banked_development():
    # Get the banked data
    # make sql database connection with pyodbc
    engine = get_conn('tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM SDE.ThresholdEvaluation_CumulativeAccounting_BankedDevelopment", conn)
    return df

def get_capital_expenditures():
    # Get the capital expenditures data
    # make sql database connection with pyodbc
    engine = get_conn('tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM SDE.ThresholdEvaluation_CumulativeAccounting_CapitalExpenditures", conn)
    return df

def get_cfa_accouting():
    # Get the CFA accounting data
    # make sql database connection with pyodbc
    engine = get_conn('tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM SDE.ThresholdEvaluation_CumulativeAccounting_CFA_Accounting", conn)
    return df

def get_cfa_allocations():
    # Get the CFA allocations data
    # make sql database connection with pyodbc
    engine = get_conn('tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM SDE.ThresholdEvaluation_CumulativeAccounting_CFA_Allocations", conn)
    return df

def get_paot_data():
    # Get the PAOT data
    # make sql database connection with pyodbc
    engine = get_conn('tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM SDE.ThresholdEvaluation_CumulativeAccounting_PAOTAllocations", conn)
    return df

def summarize_landcap_by_parcel(year):
    query = f'"YEAR" = {year}'
    # get paths
    parcelPath  = Path(sdeBase) / 'SDE.Parcels/SDE.Parcel_History_Attributed'
    landcapPath = Path(sdeBase) / 'SDE.Soils/SDE.land_capability_NRCS2007'
    # get parcels where the year is 2023
    parcels = arcpy.management.MakeFeatureLayer(str(parcelPath), 'parcels', query) 
    landcap = arcpy.management.MakeFeatureLayer(str(landcapPath), 'landcap')
    # summarize within
    arcpy.analysis.SummarizeWithin(
        in_polygons=parcels,
        in_sum_features=landcap,
        out_feature_class=fr'C:\\GIS\\Scratch.gdb\\Summarize_ParcelLandCapabalities_{year}',
        keep_all_polygons="KEEP_ALL",
        sum_fields=None,
        sum_shape="ADD_SHAPE_SUM",
        shape_unit="ACRES",
        group_field="Land_Capab",
        add_min_maj="ADD_MIN_MAJ",
        add_group_percent="ADD_PERCENT",
        out_group_table=r"C:\GIS\Scratch.gdb\Land_Capab_Summary"
    )
    arcpy.management.Delete('parcels')
    arcpy.Delete_management("memory")


def get_summary(year):
    # get land cap summary as dataframe
    # parcel development layer polygons
    path = fr'C:\GIS\Scratch.gdb\Summarize_ParcelLandCapabalities_{year}'
    # query 2022 rows
    sdf = pd.DataFrame.spatial.from_featureclass(path)
    sdf.spatial.sr = sr
    # create new field for Land Capability Category as empty string
    sdf['Category'] = ''
    # set values to 'SEZ' if Majority_Land_Capab = '1B'
    sdf.loc[sdf['Majority_Land_Capab'] == '1B', 'Category'] = 'SEZ'
    # set values to 'Sensitive' if Majority_Land_Capab = '1C', 1A, 2, 3
    sdf.loc[sdf['Majority_Land_Capab'].isin(['1C', '1A', '2', '3']), 'Category'] = 'Sensitive'
    # set values to 'Non-Sensitive' if Majority_Land_Capab = '4', 5' or '6' 7
    sdf.loc[sdf['Majority_Land_Capab'].isin(['4', '5', '6', '7']), 'Category'] = 'Non-Sensitive'
    # filter out WITHIN_TRPA_BOUNDARY = 0
    sdf = sdf.loc[sdf['WITHIN_TRPA_BNDY'] == 1]
    # melt by category and sum Residential_Units, TouristAccommodation_Units, and CommercialFloorArea_SqFt
    df = pd.melt(sdf, id_vars=['Category'], value_vars=['Residential_Units', 'TouristAccommodation_Units', 'CommercialFloorArea_SqFt'], var_name='DevelopmentType', value_name='Value')
    df = df.groupby(['Category', 'DevelopmentType'], dropna=False).sum().reset_index()
    return df, sdf

def make_table(df):
    # drop Category is None
    df = df.loc[df['Category'] != '']
    # Create the styled HTML table
    html_table = GT(df).tab_header(title="Table 1. ").tab_spanner(
        label="", columns=['Category', 'DevelopmentType', 'Value']).tab_stub(
            rowname_col='DevelopmentType', groupname_col='Category').tab_style(
                style=style.fill(color="aliceblue"), locations=loc.body()).as_raw_html()
    # savel as html
    out_table = out_chart / 'existingdevelopment_table.html'
    # Output the HTML as .html saved on local drive
    with open(out_table, 'w') as f:
        f.write(html_table)
    
# get the data
def get_old_dev_cap():
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM SDE.ThresholdEvaluation_ExistingDevelopmentRights_By_LandCapability", conn)
    return df
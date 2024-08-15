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
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.soil_conservation_summarized", conn)
    return df

# get soil conservation data from web
def get_soil_conservation_data_web():
    soil_conservation_url = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/97"
    return get_fs_data(soil_conservation_url)

# plot soil conservation data


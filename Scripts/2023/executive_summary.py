#Get Air Quality Data for Threshold
from utils import *
# get path to save the file
out_chart = local_path.parents[1] / '2023/ExecutiveSummary/Chart'
# config, template, and font for the charts
config = {"displayModeBar": False}
template = 'plotly_white'
font     = 'Calibri'
#------------------------------------------#
#Create Air Quality-Fire summary chart correlating Days Exceeding Thresholds for each pollutant type
#------------------------------------------#

#Raw data from DRI excel sheets? maybe delete
def get_air_quality_data_DRI(year):
    file_path = fr"F:\Research and Analysis\Air Quality\Annual Reports DRI\AQ data {year}.xlsx"
    df = pd.read_excel(file_path, sheet_name='daily')
    return df

# get  Air Quality data
def get_airquality_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_AirQuality", conn)
    return df
#Define colors of Bars
colors={'PM2.5 - HIGH 24 HR':'#f4a261',
                    'PM10 - HIGH 24 HR':'#2a9d8f',
                    'CO - HIGH 8 HR':'#e76f51',
                    'O3 - HIGH 1 HR ':'#264653',
                    '3-year mean (90th Percentile, Mm-1)':'#e9c46a'}
# Create Dataframe with Air Quality Data and Exceedances
def plot_AQ_daily_exceedances_per_year(df, draft=False):
    #Process Data
    df_exceedances = df.groupby(['Year', 'Indicator'])['Exceedances'].mean().reset_index()
    #df_exceedances.rename(columns={'Exceedances': 'Avg. Days of Exceedances'}, inplace=True)
    df_exceedances = df_exceedances.pivot(index='Year', columns='Indicator', values='Exceedances')
    #Define Threshold Values?
    #threshold_values = {'PM2.5 - HIGH 24 HR': 35, 'PM10 - HIGH 24 HR': 50,'CO - HIGH 8 HR': 6, 'O3 - HIGH 1 HR ': 0.08, '3-year mean (90th Percentile, Mm-1)': 34 }
    #Create Chart
    #Create Chart
    fig = px.bar(df_exceedances, x=df_exceedances.index, y=df_exceedances.columns, title='Annual Air Quality Exceedances Summary by Pollutant', color_discrete_map=colors)

    # Ensure that all years are displayed, even if there is no data for some
    fig.update_layout(yaxis_title='Days Exceeding Standard',
                  xaxis=dict(type='category', categoryorder='array', categoryarray=['PM2.5 - HIGH 24 HR', 'PM10 - HIGH 24 HR', 'CO - HIGH 8 HR', 'O3 - HIGH 1 HR ', '3-year mean (90th Percentile, Mm-1)']),
                  font_family=font,  # Example font, replace with your font variable
                  template=template,  # Example template, replace with your template variable
                  showlegend=True,
                  legend_title_text=None,
                  dragmode=False,
                  legend=dict(
                orientation="h",
                entrywidth=180,
                yanchor="bottom",
                y=1.05,
                xanchor="right",
                x=0.95,
            ),
                  hovermode="x unified")

     # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/AirQuality_Summary.html",
            # include_plotlyjs="directory",
            div_id="AirQuality_Summary",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/AirQuality_Summary.html",
            # include_plotlyjs="directory",
            div_id="AirQuality_Summary",
            full_html=False
        )


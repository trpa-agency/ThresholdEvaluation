from utils import *
import pandas as pd
# global variables
# get path to save the file
out_chart = local_path.parents[1] / '2023/Vegetation/Chart'
# set the template, font, and config for the charts
template = 'plotly_white'
font     = 'Calibri'
config   = {"displayModeBar": False}
# get tahoe yellowcress  data
def get_TYC_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_TahoeYellowCress", conn)
    return df
#-------------
#Plot Tahoe YellowCress
#-------------
def plot_TYC(df, draft= False):
    #Not enough data/ incomplete survey for year 2021
    df = df[df['Year'] != 2021]
    # Define thresholds based on lake level conditions
    thresholds = {
        'low': {'condition': lambda x: x <= 6224, 'value': 32},
        'mid': {'condition': lambda x: 6224 < x < 6227, 'value': 26},
        'high': {'condition': lambda x: x >= 6227, 'value': 20}
    }

    threshold_values = []
    for index, row in df.iterrows():
        lake_level = row['Lake_Level']
        occupied_sites = row['Occupied_Sites']
        for level, threshold in thresholds.items():
            if threshold['condition'](lake_level):
                threshold_values.append(threshold['value'])
                break

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Bar(name="Occupied Site",x=df['Year'], y=df['Occupied_Sites']))

    fig.update_traces(marker_color='#ffffbf', 
                  marker_line_color="#8a7121",
                  marker_line_width=1.5, 
                  opacity=0.6,
                  hovertemplate='<b>%{y:,.0f}</b> occupied sites<extra></extra>'
                 )
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=threshold_values,
        mode='lines',
        name='Threshold',
        line=dict(color='#333333'),
        hovertemplate='Threshold: %{y}<extra></extra>'
    ))

    # create lake level line
    fig.add_trace(go.Scatter(
        y=df['Lake_Level'],
        x=df['Year'],
        name= "Lake Elevation (ft)",
        line=dict(dash= 'dash', color='#679ab8', width=2),
        mode='lines',
        hovertemplate='Lake Level <b>%{y:,.0f}ft</b><extra></extra>'),
        secondary_y=True)

    # Set y-axes titles
    fig.update_yaxes(secondary_y=False)
    fig.update_yaxes(title_text="Lake Level (ft)", tickformat=",d",secondary_y=True)

    # set layout
    fig.update_layout(title='Tahoe Yellow Cress',
                    font_family=font,
                    template=template,
                    showlegend=False,
                    hovermode="x unified",
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1978,
                        dtick = 5,
                        title_text='Year'
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 5,
                        range=[0, 50],
                        title_text='# Occupied Sites'
                    )
                 )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_TahoeYellowCress.html",
            # include_plotlyjs="directory",
            div_id="Vegetation_TahoeYellowCress",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_TahoeYellowCress.html",
            # include_plotlyjs="directory",
            div_id="Vegetation_TahoeYellowCress",
            full_html=False
        )

# get 2010 Ecobject data
def get_ecobject_2010_data():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.Vegetation_EcObject_2010", conn)
    return df

# get new veg change analysis data
def get_new_veg_change_analysis_data():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_NewVegChangeAnalysis", conn)
    return df

# get the vegetation type summary data from 2019
def get_2019_vegtypesummary_data():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_VegetationTypeSummary", conn)
    return df

# plot Vegetation Type
def plot_veg():
    # get data
    df = get_ecobject_2010_data()
    # create figure
    fig = go.Figure()
    # add trace
    fig.add_trace(go.Bar(
        x=df['Year'],
        y=df['Total_Acres'],
        name='Total Acres',
        marker_color='#b3e2cd',
        hovertemplate='<b>%{y:,.0f}</b> acres<extra></extra>'
    ))
    # set layout
    fig.update_layout(
        title='Vegetation Type',
        font_family=font,
        template=template,
        showlegend=False,
        hovermode="x unified",
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 1978,
            dtick = 5,
            title_text='Year'
        ),
        yaxis = dict(
            tickmode = 'linear',
            tick0 = 0,
            dtick = 100,
            title_text='Total Acres'
        )
    )
    # export chart
    fig.write_html(
        config=config,
        file= out_chart / "Final/Vegetation_Type.html",
        # include_plotlyjs="directory",
        div_id="Vegetation_Type",
        full_html=False
    )
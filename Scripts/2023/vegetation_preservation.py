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

# get forest fuels treatment data
def get_data_forest_fuel_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_FuelsTreatment", conn)
    return df

# get EIP Tracker forest fuels treatment data
def get_data_forest_fuel():
    eipForestTreatments = "https://www.laketahoeinfo.org/WebServices/GetReportedEIPIndicatorProjectAccomplishments/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476/19"
    data = pd.read_json(eipForestTreatments)
    df = data[data["PMSubcategoryName1"] == "Treatment Zone"]
    df = df.rename(
        columns={
            "IndicatorProjectYear": "Year",
            "PMSubcategoryOption1": "Treatment Zone",
            "IndicatorProjectValue": "Acres",
        }
    )
    # change value Community Defense Zone to Defense Zone for consistency
    df["Treatment Zone"] = df["Treatment Zone"].replace("Community Defense Zone", "Defense Zone")
    df["Year"] = df["Year"].astype(str)
    df = df.groupby(["Year", "Treatment Zone"]).agg({"Acres": "sum"}).reset_index()
    df.sort_values(by=['Treatment Zone'], inplace=True)
    return df

# plot forest health data
def plot_forest_fuel(df, draft= True):
    years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
    # data
    df = df[df["Year"].isin(years)]
    # plot settings
    path_html="ForestFuelTreatment.html"
    div_id="ForestFuelTreatment"
    x="Year"
    y="Acres"
    facet=None
    color="Treatment Zone"
    color_sequence=["#E69800", "#ABCD66", "#A87000", "#F5CA7A"]
    orders={
        "Year": [
            "2015",
            "2016",
            "2017",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
            "2023",
        ]
    }
    y_title="Acres Treated"
    x_title="Year"
    custom_data=["Treatment Zone"]
    hovertemplate="<br>".join(
        ["<b>%{y:,.0f} acres</b> of forest health treatment", "in the <i>%{customdata[0]}</i>"]
    ) + "<extra></extra>"
    hovermode="x unified"
    format=",.0f"
    additional_formatting=dict(
        # title = "Forest Health Treatment",
        legend=dict(
            title= "Forest Health Treatment Zone",
            orientation="h",
            entrywidth=85,
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=0.95,
        )
    )
    # plot
    # figure 
    fig = px.bar(df, x=x, y=y, 
                color=color, 
                barmode='stack',
                facet_col=facet,
                # facet_row=facet_row,
                color_discrete_sequence=color_sequence,
                category_orders=orders,
                # orientation=orientation,
                custom_data=custom_data
            )
    
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(
        yaxis=dict(tickformat=format, hoverformat=format, title=y_title),
        xaxis=dict(title=x_title),
        hovermode=hovermode,
        template="plotly_white",
        dragmode=False,
        legend_title=None,
    )
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True, tickformat=format))
    fig.update_yaxes(
        col=2, row=1, showticklabels=False, tickfont=dict(color="rgba(0,0,0,0)"), title=None
    )
    fig.update_yaxes(
        col=3, row=1, showticklabels=False, tickfont=dict(color="rgba(0,0,0,0)"), title=None
    )
    fig.update_xaxes(tickformat=".0f")
    fig.update_traces(hovertemplate=hovertemplate)
    fig.update_layout(additional_formatting)
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft" / path_html,
            div_id=div_id,
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final" / path_html,
            div_id=div_id,
            full_html=False,
        )
      
# get the old growth forest data
def get_old_growth_forest():
    data = get_fs_data(
        "https://maps.trpa.org/server/rest/services/Vegetation_Late_Seral/FeatureServer/0"
    )
    # df = data.groupby(["SeralStage","SpatialVar"]).agg({"Acres": "sum"}).reset_index()
    df = data[["SeralStage", "SpatialVar", "TRPA_VegType", "Acres"]]
    return df


def plot_old_growth_forest(df):
    seral = df.groupby("SeralStage").agg({"Acres": "sum"}).reset_index()
    stackedbar(
        seral,
        path_html="html/2.1.b_OldGrowthForest_SeralStage.html",
        div_id="2.1.b_OldGrowthForest_SeralStage",
        x="SeralStage",
        y="Acres",
        facet=None,
        color=None,
        color_sequence=["#208385"],
        orders=None,
        y_title="Acres",
        x_title="Seral Stage",
        custom_data=["SeralStage"],
        hovertemplate="<br>".join(["<b>%{y:,.0f}</b> acres of", "<i>%{customdata[0]}</i> forest"])
        + "<extra></extra>",
        hovermode="x unified",
        orientation=None,
        format=",.0f",
    )
    structure = df.groupby("SpatialVar").agg({"Acres": "sum"}).reset_index()
    stackedbar(
        structure,
        path_html="html/2.1.b_OldGrowthForest_Structure.html",
        div_id="2.1.b_OldGrowthForest_Structure",
        x="SpatialVar",
        y="Acres",
        facet=None,
        color=None,
        color_sequence=["#208385"],
        orders=None,
        y_title="Acres",
        x_title="Structure",
        custom_data=["SpatialVar"],
        hovertemplate="<br>".join(
            ["<b>%{y:,.0f}</b> acres of", "<i>%{customdata[0]}</i> old growth forest"]
        )
        + "<extra></extra>",
        hovermode="x unified",
        orientation=None,
        format=",.0f",
    )
    species = df.groupby("TRPA_VegType").agg({"Acres": "sum"}).reset_index()
    stackedbar(
        species,
        path_html="html/2.1.b_OldGrowthForest_Species.html",
        div_id="2.1.b_OldGrowthForest_Species",
        x="TRPA_VegType",
        y="Acres",
        facet=None,
        color=None,
        color_sequence=["#208385"],
        orders=None,
        y_title="Acres",
        x_title="Vegetation Type",
        custom_data=["TRPA_VegType"],
        hovertemplate="<br>".join(
            ["<b>%{y:,.0f}</b> acres of", "<i>%{customdata[0]}</i> old growth forest"]
        )
        + "<extra></extra>",
        hovermode="x unified",
        orientation=None,
        format=",.0f",
    )
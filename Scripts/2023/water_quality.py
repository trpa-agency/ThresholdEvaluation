from utils import *
# global variables
# get path to save the file
out_chart = local_path.parents[1] / '2023/WaterQuality/Chart'
# set the template, font, and config for the charts
template = 'plotly_white'
font     = 'Calibri'
config   = {"displayModeBar": False}

# get secchi depth data
def get_secchi_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.secchi_summarized", conn)
    return df

# get secchi depth data
def get_secchi_data_web():
    return get_fs_data(
        "https://maps.trpa.org/server/rest/services/LTinfo_Climate_Resilience_Dashboard/MapServer/128"
    )

# A pretty specific graph
def plot_secchi_depth(df, draft=False):
    # convert everything to feet
    df["annual_average"]  = df["annual_average"]  * 3.28084
    df["F5_year_average"] = df["F5_year_average"] * 3.28084

    fig = px.scatter(
        df, x="year", y="annual_average", color_discrete_sequence=["#023f64"]
    )
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        yaxis=dict(title="Depth (feet)"),
        xaxis=dict(title="Year", showgrid=False),
        template="plotly_white",
        hovermode="x unified",
        dragmode=False,
        margin=dict(t=20),
        # title = "Lake Tahoe Secchi Depth",
        legend=dict(
            title="Lake Tahoe Secchi Depth",
            orientation="h",
            entrywidth=100,
            # entrywidthmode="fraction",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1,
            # xref="container",
            # yref="container"
        ),
    )
    fig.update_yaxes(autorange="reversed", autorangeoptions=dict(include=0))
    fig.add_trace(
        px.line(df, x="year", y="F5_year_average", color_discrete_sequence=["#208385"]).data[0]
    )
    fig.data[0].name = "Annual Average"
    fig.data[0].showlegend = True
    fig.data[1].name = "5-Year Average"
    fig.data[1].showlegend = True
    fig.update_traces(hovertemplate="%{y:.1f}ft")
    
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Secchi_Depth.html",
            include_plotlyjs="directory",
            div_id="Secchi_Depth",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Secchi_Depth.html",
            # include_plotlyjs="directory",
            div_id="Secchi_Depth",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )

# get watercraft inspectin stations data
def get_watercraft_inspection_data_web():
    # watercraft inspection stations data is indicator #16 in the LTinfo Data Center
    url = 'https://www.laketahoeinfo.org/WebServices/GetReportedEIPIndicatorProjectAccomplishments/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476/16'
    # get data from web service on LTinfo
    df = pd.read_json(url)
    # rename columns 
    df.rename(columns={'IndicatorProjectYear': 'Year', 
                        'IndicatorProjectValue': 'Total', 
                        'PMSubcategoryOption1': 'Category'}, inplace=True)
    return df

def get_inspection_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("ELECT * FROM sde_tabular.SDE.ThresholdEvaluation_WatercraftInspections", conn)

    return df

# plot watercraft inspection stations data
def plot_watercraft_inspections(df, draft=False):
    stackedbar(
        df,
        path_html=out_chart / "Final/Watercraft_Inspection_Stations.html",
        div_id="Watercraft Inspections",
        x="Year",
        y="Total",
        facet=None,
        color="Category",
        color_sequence=[ "#5c6d70", "#a37774"],
        orders=None,
        y_title="Total Inspections",
        x_title="Year",
        hovermode="x unified",
        orientation="v",
        format=",.0f",
        custom_data=["Category"],
        hovertemplate="<br>".join(
            ["<b>%{y:,.0f}</b> watercrafts inspected with", "<i>%{customdata[0]}</i>"]
        )
        + "<extra></extra>",
        additional_formatting=dict(
            legend=dict(
                orientation="h",
                entrywidth=180,
                yanchor="bottom",
                y=1.05,
                xanchor="right",
                x=0.95,
            )
        )
    )

# get total nitrogen tributary data
def get_total_nitrogen_annual_data_sql():
    # make sql database connection
    engine = get_conn('sde_tabular')
    # get SQL table
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_TotalNitrogen_Concentration", conn)
    # return dataframe
    return df

# get total nitrogen tributary data daily stats
def get_total_nitrogen_daily_data_sql():
    # make sql database connection
    engine = get_conn('sde_tabular')
    # get SQL table
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_TotalNitrogen_Concentration_DailyStats", conn)
    # return dataframe
    return df

# get total phosphorus tributary data
def get_total_phosphorus_annual_data_sql():
    # make sql database connection
    engine = get_conn('sde_tabular')
    # get SQL table
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_TotalPhosphorus_Concentration", conn)
    # return dataframe
    return df

# get total phosphorus tributary data daily stats
def get_total_phosphorus_daily_data_sql():
    # make sql database connection
    engine = get_conn('sde_tabular')
    # get SQL table
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_TotalPhosphorus_Concentration_DailyStats", conn)
    # return dataframe
    return df

# get suspended sediment tributary data
def get_suspended_sediment_annual_data_sql():
    # make sql database connection
    engine = get_conn('sde_tabular')
    # get SQL table
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_SuspendedSediment_Concentration", conn)
    # return dataframe
    return df

# get suspended sediment tributary data daily stats
def get_suspended_sediment_daily_data_sql():
    # make sql database connection
    engine = get_conn('sde_tabular')
    # get SQL table
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_SuspendedSediment_Concentration_DailyStats", conn)
    # return dataframe
    return df

# get water quality data
def get_waterquality_data():
    # read csv file from data folder or F:\Research and Analysis\Water Quality Monitoring Program\Tributaries_LTIMP\Data and Summaries\WY23\wy23_tribThresholds.xlsx
    xls = local_path.parents[0] / '2023/data/raw_data/wy23_tribThresholds.xlsx'
    df = pd.read_excel(xls, sheet_name='WY_summary_mean')
    # drop columns 'station_nm', 'MonitoringLocationIdentifier'
    df = df.drop(columns=['station_nm', 'MonitoringLocationIdentifier'])

    # get mean of all sites by year
    df = df.groupby('WaterYear').mean().reset_index()
    return df

# plot total nitrogen concentration tributary data
def plot_total_nitrogen(df, draft= True):
    # rename columns
    df.rename(columns={'WaterYear': 'Water Year', 'TN': 'Total Nitrogen (mg/L)'}, inplace=True)

    fig = px.scatter(x=df['Water Year'], y=df['Total Nitrogen (mg/L)'], color_discrete_sequence=["#023f64"])
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        yaxis=dict(title="Total Nitrogen (mg/L)"),
        xaxis=dict(title="Year", showgrid=False),
        template="plotly_white",
        hovermode="x unified",
        dragmode=False,
        margin=dict(t=20),
        # title = "Lake Tahoe Secchi Depth",
        legend=dict(
            title="Total Nitrogen",
            orientation="h",
            entrywidth=100,
            # entrywidthmode="fraction",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1,
            # xref="container",
            # yref="container"
        ),
    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Total_Nitrogen.html",
            include_plotlyjs="directory",
            div_id="Total_Nitrogen",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Total_Nitrogen.html",
            # include_plotlyjs="directory",
            div_id="Total_Nitrogen",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )

def plot_total_phosphorus(df, draft= True):
    df.rename(columns={'WaterYear': 'Water Year', 'TP': 'Total Phosphorus (mg/L)'}, inplace=True)
    fig = px.scatter(x=df['Water Year'], y=df['Total Phosphorus (mg/L)'], color_discrete_sequence=["#023f64"])
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        yaxis=dict(title="Total Phosphorus (mg/L)"),
        xaxis=dict(title="Year", showgrid=False),
        template="plotly_white",
        hovermode="x unified",
        dragmode=False,
        margin=dict(t=20),
        # title = "Lake Tahoe Secchi Depth",
        legend=dict(
            title="Total Phosphorus",
            orientation="h",
            entrywidth=100,
            # entrywidthmode="fraction",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1,
            # xref="container",
            # yref="container"
        ),
    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Total_Phosphorus.html",
            include_plotlyjs="directory",
            div_id="Total_Phosphorus",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Total_Phosphorus.html",
            # include_plotlyjs="directory",
            div_id="Total_Phosphorus",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )

def plot_suspended_sediment(df, draft= True):
    df.rename(columns={'WaterYear': 'Water Year', 'FSP': 'Suspended Sediment (mg/L)'}, inplace=True)
    fig = px.scatter(x=df['Water Year'], y=df['Suspended Sediment (mg/L)'], color_discrete_sequence=["#023f64"])
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        yaxis=dict(title="Suspended Sediment (mg/L)"),
        xaxis=dict(title="Year", showgrid=False),
        template="plotly_white",
        hovermode="x unified",
        dragmode=False,
        margin=dict(t=20),
        # title = "Lake Tahoe Secchi Depth",
        legend=dict(
            title="Suspended Sediment",
            orientation="h",
            entrywidth=100,
            # entrywidthmode="fraction",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1,
            # xref="container",
            # yref="container"
        ),
    )  
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Suspended_Sediment.html",
            div_id="Suspended_Sediment",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Suspended_Sediment.html",
            div_id="Suspended_Sediment",
            full_html=False,
        )

# get phosporus load reduction data
def get_phosphorus_load_reduction():
    phURL = 'https://www.laketahoeinfo.org/WebServices/GetReportedEIPIndicatorProjectAccomplishments/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476/254'
    df = pd.read_json(phURL)
    df.rename(columns={'IndicatorProjectYear': 'Year', 'IndicatorProjectValue': 'lbs/year'}, inplace=True)
    return df

def get_nitrogen_load_reduction():
    nURL = 'https://www.laketahoeinfo.org/WebServices/GetReportedEIPIndicatorProjectAccomplishments/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476/253'
    df = pd.read_json(nURL)
    df.rename(columns={'IndicatorProjectYear': 'Year', 'IndicatorProjectValue': 'lbs/year'}, inplace=True)
    return df

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
    return df
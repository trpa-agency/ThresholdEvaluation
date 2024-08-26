from utils import *
import pandas as pd
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

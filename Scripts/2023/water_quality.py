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
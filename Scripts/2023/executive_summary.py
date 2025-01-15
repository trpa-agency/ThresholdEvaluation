from utils import *
out_chart = local_path.parents[1] / '2023/ExecutiveSummary'
# config, template, and font for the charts
config = {"displayModeBar": False}
template = 'plotly_white'
font     = 'Calibri'

# get caldor data
caldor = Path("Data/2023/caldor.gdb")

def get_data_aquatic_species():
    eipInvasive = "https://www.laketahoeinfo.org/WebServices/GetReportedEIPIndicatorProjectAccomplishments/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476/15"
    data = pd.read_json(eipInvasive)
    data = data.rename(
        columns={
            "IndicatorProjectYear": "Year",
            "PMSubcategoryOption1": "Invasive Species Type",
            "IndicatorProjectValue": "Acres",
        }
    )
    # filter out Terrestrial from Invasive Species Type
    data = data.loc[data["Invasive Species Type"] != "Terrestrial"]
    df = data.groupby(["Year", "Invasive Species Type"])["Acres"].sum().reset_index()
    return df


def plot_aquatic_species(df):
    trendline(
        df,
        path_html="html/2.2.a_Aquatic_Species.html",
        div_id="2.2.a_Aquatic_Species",
        x="Year",
        y="Acres",
        color="Invasive Species Type",
        # color_sequence=["#023f64", "#7ebfb5"],
        sort="Year",
        orders=None,
        x_title="Year",
        y_title="Acres",
        format=",.0f",
        hovertemplate="%{y:,.0f}",
        markers=True,
        hover_data=None,
        tickvals=None,
        ticktext=None,
        tickangle=None,
        hovermode="x unified",
        custom_data=None,
        additional_formatting=dict(
            title="Aquatic Invasive Species Treatment",
            margin=dict(t=20),
            # turn off legend
            showlegend=False,
        ),
    )

def plot_aquatic_species_bar(df):
    stackedbar(
        df,
        path_html="html/2.2.a_Aquatic_Species.html",
        div_id="2.2.a_Aquatic_Species",
        x="Year",
        y="Acres",
        color="Invasive Species Type",
        color_sequence=["#023f64", "#7ebfb5"],
        facet=None,
        orders=None,
        x_title="Year",
        y_title="Acres",
        custom_data=["Invasive Species Type"],
        hovertemplate="<br>".join(
            ["<b>%{y:.0f} acres</b> of", "<i>%{customdata[0]}</i> invasive species treated"]
        )
        + "<extra></extra>",
        hovermode="x unified",
        orientation=None,
        format=",.0f",
        additional_formatting=dict(
            title=dict(text="Aquatic Invasive Species Treatment",
                    x=0.05,
                    y=0.95,
                    xanchor="left",
                    yanchor="top",
                    font=dict(size=16),
                    automargin=True),
            margin=dict(t=20),
            # turn off legend
            showlegend=False,
        ),
    )


# get secchi depth data
def get_data_secchi_depth():
    return get_fs_data(
        "https://maps.trpa.org/server/rest/services/LTinfo_Climate_Resilience_Dashboard/MapServer/128"
    )


# A pretty specific graph
def plot_secchi_depth(df):
    config = {"displayModeBar": False}
    # convert everything to feet
    df["annual_average"] = df["annual_average"] * 3.28084
    df["F5_year_average"] = df["F5_year_average"] * 3.28084

    fig = px.scatter(
        df, x="year", y="annual_average", trendline="ols", color_discrete_sequence=["#023f64"]
    )
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        yaxis=dict(title="Feet"),
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
    fig.data[1].name = "Trendline"
    fig.data[1].showlegend = True
    fig.data[2].name = "5-Year Average"
    fig.data[2].showlegend = True
    fig.update_traces(hovertemplate="%{y:.1f}ft")

    fig.write_html(
        config=config,
        file="html/1.3.c_Secchi_Depth.html",
        include_plotlyjs="directory",
        div_id="1.3.c_Secchi_Depth",
    )

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

# Define colors of Bars
colors = {
    'PM2.5 - HIGH 24 HR': '#f4a261',
    'PM10 - HIGH 24 HR': '#2a9d8f',
    'CO - HIGH 8 HR': '#e76f51',
    'O3 - HIGH 1 HR ': '#264653',
    '3-year mean (90th Percentile, Mm-1)': '#e9c46a'
}

# Create Dataframe with Air Quality Data and Exceedances
def plot_AQ_daily_exceedances_per_year(df, draft=False):
    # Process Data
    df_exceedances = df[df['Indicator'].isin(colors.keys())]
    df_exceedances = df_exceedances.groupby(['Year', 'Indicator'])['Exceedances'].mean().reset_index()
    df_exceedances = df_exceedances.pivot(index='Year', columns='Indicator', values='Exceedances').reset_index()
    
    # Calculate average daily exceedances
    df_exceedances = df_exceedances.melt(id_vars=['Year'], var_name='Indicator', value_name='Average Daily Exceedances')
    print(df_exceedances)
    # Create Chart
    fig = px.bar(df_exceedances, x='Year', y='Average Daily Exceedances', color='Indicator', title='Annual Air Quality Exceedances Summary by Pollutant', barmode='group', color_discrete_map=colors)

    # Ensure that all years are displayed, even if there is no data for some
    fig.update_layout(
        yaxis_title='Days Exceeding Standard',
        xaxis=dict(type='category'),
        font_family=font,
        template=template,
        showlegend=True,
        legend_title_text=None,
        dragmode=False,
        hovermode="x unified"
    )
    # Export chart
    if draft:
        fig.write_html(
            config=config,
            file=out_chart / "AirQuality_Summary_draft.html",
            div_id="AirQuality_Summary_draft",
            full_html=False
        )
    else:
        fig.write_html(
            config=config,
            file=out_chart / "AirQuality_Summary.html",
            div_id="AirQuality_Summary",
            full_html=False
        )

#-------------------------------------------------------------#
# GET FIRE DATA 
#-------------------------------------------------------------#
# get fire data
def get_fire_data():
    # wildfire url CALFIRE
    fireStartTable = "https://services1.arcgis.com/jUJYIo9tSA7EHvfZ/arcgis/rest/services/California_Fire_Perimeters/FeatureServer/0"
    # Purple Air data hosted on TRPA's Enterprise Geodatabase
    purpleAirURL = "https://maps.trpa.org/server/rest/services/LTinfo_Climate_Resilience_Dashboard/MapServer/143"
    # get data from the web service
    dfPurpleAir = get_fs_data(purpleAirURL)
    dfFire = get_fs_data(fireStartTable)
    # remove nulls from ALARM_DATE
    dfFire = dfFire.dropna(subset=["ALARM_DATE"])
    # remove negative numbers in ALARM_DATE
    dfFire = dfFire[dfFire["ALARM_DATE"] > 0]
    # groupby date and get the mean of pm25
    dfAir = dfPurpleAir.groupby("date")["mean_pm25"].mean().reset_index()
    # Apply the function to the column
    dfFire["Date"] = dfFire["ALARM_DATE"].apply(convert_to_utc)
    # convert Date to month day year
    dfFire["Date"] = dfFire["Date"].dt.strftime("%m/%d/%Y")
    # convert date to datetime
    dfFire["Date"] = pd.to_datetime(dfFire["Date"], format="%m/%d/%Y")
    # filter date to 2018 or later
    dfFire = dfFire[dfFire["Date"] >= "01/01/2018"]
    # filter FIRE_NAME is ['CALDOR', 'TAMARACK', 'FERGUSON', 'MOSQUITO', 'LOYALTON']
    dfFire = dfFire.loc[
        dfFire["FIRE_NAME"].isin(["CALDOR", "TAMARACK", "FERGUSON", "MOSQUITO", "LOYALTON", "CREEK"])
    ]
    # only keep FIRE_NAME, GIS_ACRES, and Date
    dfFire = dfFire[["FIRE_NAME", "GIS_ACRES", "Date"]]
    # rename columns
    dfFire = dfFire.rename(columns={"FIRE_NAME": "Fire", "GIS_ACRES": "Acres"})
    # change column name to Date and PM 2.5 (ug/m3)
    dfAir = dfAir.rename(columns={"date": "Date", "mean_pm25": "PM 2.5 (ug/m3)"})
    # Apply the function to the column
    dfAir["Date"] = dfAir["Date"].apply(convert_to_utc)
    # # convert Date to str
    dfAir["Date"] = dfAir["Date"].dt.strftime("%m/%d/%Y")
    # # convert Date to datetime
    dfAir["Date"] = pd.to_datetime(dfAir["Date"], format="%m/%d/%Y")

    # merge with sdfPUrplAir on Date
    dfFire = dfFire.merge(dfAir, on="Date", how="left")
    return dfFire

#Use this code to overlay fire information to Air Quality Exceedances
def plot_purple_air_fire(dfAir,dfFire):
    # creat a plotly express line chart
    fig = px.line(dfAir,
                    x="Date",
                    y="PM 2.5 (ug/m3)",
                    title='Purple Air PM2.5'
                                )

    fig.update_traces(hovertemplate="<br>".join([
                        "<b>%{y:,.0f} AQI</b>",
                        "<i>seven day rolling average</i>"
                            ])+"<extra></extra>"
    )

    # add scatter trace to figure of points of dfMerge by date and mean_pm25
    fig.add_trace(go.Scatter(x=dfFire['Date'],
                            y=dfFire['PM 2.5 (ug/m3)'],
                            mode='markers',
                            name='Fire Start Date',
                            customdata=dfFire[["Fire", "Acres"]],
                            hovertemplate="<br>".join([
                                            "<b>%{customdata[0]} FIRE</b> started",
                                            "<i>%{x}</i> and burned",
                                            "<i>%{customdata[1]:,.0f} acres</i>"
                                                ])+"<extra></extra>"
                                                ))

    # make the scatter plot markers larger
    fig.update_traces(marker=dict(size=12))

    # label points by FIRE_NAME
    for i, txt in enumerate(dfFire['Fire']):
        fig.add_annotation(x=dfFire['Date'].iloc[i], y=dfFire['PM 2.5 (ug/m3)'].iloc[i],
                                text=txt+" FIRE",
                                showarrow=True,
                                align="center",
                                arrowhead=1,
                                # arrowsize=1,
                                # arrowwidth=2,
                                arrowcolor="#636363",
                                ax=10,
                                ay=-20,
                                bordercolor="#c7c7c7",
                                borderwidth=1,
                                borderpad=2,
                                bgcolor="#ff7f0e",
                                opacity=0.8
                                )

    # plot variables
    path_html="html/1.2.a_Purple_Air_v2.html"
    div_id="1.2.a_Purple_Air_v2"
    x="time_stamp"
    y="moving_avg"
    color="#FF5733"
    color_sequence=["#023f64"]
    sort="time_stamp"
    orders=None
    x_title="Date"
    y_title="Air Quality Index"
    format=",.0f"
    # hovertemplate="%{y:,.0f}"
    hovermode="x unified"
    config = {"displayModeBar": False}

    fig.update_layout(
            margin=dict(t=20),
            yaxis=dict(title=y_title),
            xaxis=dict(title=x_title, showgrid=False),
            hovermode=hovermode,
            template="plotly_white",
            dragmode=False,
            showlegend=False,
            # title_font_family="Bell Topo Sans",
            # title_font_color="black",
            title=dict(text="Air Quality Index and Significant Fire Events",
                        x=0.05,
                        y=0.95,
                        xanchor="left",
                        yanchor="top",
                        font=dict(size=16),
                        automargin=True)
        )

def get_restored_sez_data():
    df = get_fs_data("https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/77")
    # dfSEZ = pd.read_sql('SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_SEZRestoration', conn)
    df.loc[df.YearCompleted.isna(),"YearCompleted"]=2019
    # df.at['105', 'YearCompleted']= 2000
    df['Threshold Value'] = 1100
    # sort inplace
    df = df.sort_values('YearCompleted')
    # set the cumulative acres restored
    df['CumulativeAcresRestored'] = df['AcresRestored'].cumsum()
    return df

def plot_restored_sez(df, draft=False):
    # create threshold line
    fig=go.Figure(go.Scatter(
        y=df['Threshold Value'],
        x=df['YearCompleted'],
        name= "Threshold",
        line=dict(color='#333333', width=2),
        mode='lines',
        hovertemplate='Threshold:<br><b>%{y:,.0f}</b> total acres restored<extra></extra>'
    ))


    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['CumulativeAcresRestored'],
        x=df['YearCompleted'],
        name= "Total Area Restored",
        line=dict(color='#679ab8', width=2),
        mode='lines',
        hovertemplate='Area Restored to Date: <br><b>%{y:,.0f}</b> total acres<extra></extra>'))

    # set layout
    fig.update_layout(title='Stream Environment Zone Restoration',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        legend_title_text=None,
                        dragmode=False,
                        hovermode="x unified",
                        xaxis = dict(
                            tickmode = 'linear',
                            tick0 = 1980,
                            dtick = 5,
                            range=[1979,2026],
                            title_text= "Year Completed"
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 100,
                            tickformat= ",.0f",
                            range=[0, 1500],
                            title_text='Acres'
                        )
                    )
    # Export chart
    if draft:
        fig.write_html(
            config=config,
            file=out_chart / "RestoredSEZ.html",
            div_id="RestoredSEZ_2023",
            full_html=False
        )
    else:
        fig.write_html(
            config=config,
            file=out_chart / "RestoredSEZ.html",
            div_id="RestoredSEZ_2023",
            full_html=False
        )
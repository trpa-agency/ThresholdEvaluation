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
            div_id="Total_Nitrogen",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Total_Nitrogen.html",
            div_id="Total_Nitrogen",
            full_html=False
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
            x=1
        ),
    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Total_Phosphorus.html",
            div_id="Total_Phosphorus",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Total_Phosphorus.html",
            div_id="Total_Phosphorus",
            full_html=False
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
    # phURL = 'https://www.laketahoeinfo.org/WebServices/GetReportedEIPIndicatorProjectAccomplishments/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476/254'
    # df = pd.read_json(phURL)
    df = pd.read_excel(local_path.parents[0] / '2023/data/raw_data/Phosphorous Load Reduction Achieved.xlsx')
    # df.rename(columns={'IndicatorProjectYear': 'Year', 'IndicatorProjectValue': 'lbs/year'}, inplace=True)
    return df

def plot_phosphorus_load_reduction(df, draft=True):
    # drop total row
    df = df[df['Year'] != 'Total']
    # setup plot
    fig = px.bar(df, x = 'Year', y= 'Total', color_discrete_sequence=["#023f64"])
    fig.update_traces(hovertemplate='<br>%{y:,.0f}')
    # set layout
    fig.update_layout(title="Phosphorous Load Reduction Achieved",
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        xaxis = dict(
                            title_text='Year'
                        ),   
                        yaxis = dict(
                            title_text='Total (lbs/year)'
                        )               
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Phosphorous_Load_Reduction.html",
            div_id="Phosphorous_Load_Reduction",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Phosphorous_Load_Reduction.html",
            div_id="Phosphorous_Load_Reduction",
            full_html=False,
        )

def get_nitrogen_load_reduction():
    # nURL = 'https://www.laketahoeinfo.org/WebServices/GetReportedEIPIndicatorProjectAccomplishments/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476/253'
    # df = pd.read_json(nURL)
    df = pd.read_excel(local_path.parents[0] / '2023/data/raw_data/Nitrogen Load Reduction Achieved.xlsx')
    # df.rename(columns={'IndicatorProjectYear': 'Year', 'IndicatorProjectValue': 'lbs/year'}, inplace=True)
    return df

# plot nitrogen load reduction data
def plot_nitrogen_load_reduction(df, draft=True):
    # drop total row
    df = df[df['Year'] != 'Total']
    # setup plot
    fig = px.bar(df, x = 'Year', y= 'Total', color_discrete_sequence=["#023f64"])
    fig.update_traces(hovertemplate='<br>%{y:,.0f}')
    # set layout
    fig.update_layout(title="Nitrogen Load Reduction Achieved",
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                                                xaxis = dict(
                            title_text='Year'
                        ),   
                        yaxis = dict(
                            title_text='Total (lbs/year)'
                        )                              
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Nitrogen_Load_Reduction.html",
            div_id="Nitrogen_Load_Reduction",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Nitrogen_Load_Reduction.html",
            div_id="Nitrogen_Load_Reduction",
            full_html=False,
        )

# get fine sediment load reduction data
def get_sediment_load_reduction():
    # sURL = 'https://www.laketahoeinfo.org/WebServices/GetReportedEIPIndicatorProjectAccomplishments/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476/255'
    # df = pd.read_json(sURL)
    df = pd.read_excel(local_path.parents[0] / '2023/data/raw_data/Fine Sediment Load Reduction Achieved.xlsx')
    # df.rename(columns={'IndicatorProjectYear': 'Year', 'IndicatorProjectValue': 'lbs/year'}, inplace=True)
    return df

# plot fine sediment load reduction data
def plot_sediment_load_reduction(df, draft=True):
    # drop total row
    df = df[df['Year'] != 'Total']
    # setup plot
    fig = px.bar(df, x = 'Year', y= 'Total', color_discrete_sequence=["#023f64"])
    fig.update_traces(hovertemplate='<br>%{y:,.0f}')
    # set layout
    fig.update_layout(title="Fine Sediment Load Reduction Achieved",
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        xaxis = dict(
                            title_text='Year'
                        ),   
                        yaxis = dict(
                            title_text='Total (lbs/year)'
                        )           

                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Fine_Sediment_Load_Reduction.html",
            div_id="Fine_Sediment_Load_Reduction",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Fine_Sediment_Load_Reduction.html",
            div_id="Fine_Sediment_Load_Reduction",
            full_html=False,
        )

def get_periphyton_data():
    #Import DAta
    # file_path = r"F:\Research and Analysis\Water Quality Monitoring Program\Nearshore\IntegratedAlgaeMonitoring\data\Peri"
    file_path = local_path.parents[0] / '2023/data/raw_data'
    # Load each CSV file into a DataFrame
    inclinedf = pd.read_csv(os.path.join(file_path, 'InclineWest_Historic.csv'))
    Pinelanddf = pd.read_csv(os.path.join(file_path, 'Pineland_Historic.csv'))
    Rubicondf = pd.read_csv(os.path.join(file_path, 'Rubicon_Historic.csv'))
    Sugarpinedf = pd.read_csv(os.path.join(file_path, 'Sugarpine_Historic.csv'))
    TahoeCitydf = pd.read_csv(os.path.join(file_path, 'TahoeCity_Historic.csv'))
    Zephyrdf = pd.read_csv(os.path.join(file_path, 'Zephyr_Historic.csv'))

    #Combine All Dataframes
    combined_df = pd.concat([inclinedf, Pinelanddf, Rubicondf, Sugarpinedf, TahoeCitydf, Zephyrdf], ignore_index=True)
    # Ensure the Date column is in datetime format
    combined_df['Sample_Date'] = pd.to_datetime(combined_df['Sample_Date'])

    # Extract the year from the Date column and create a new Year column
    combined_df['Year'] = combined_df['Sample_Date'].dt.year

    #Group by 'Year' and 'Site', then calculate the average of the 'chl' column
    df = combined_df.groupby(['Year', 'site'], as_index=False)['Chl'].mean()
    return df

def plot_periphyton(df, draft=True):
    # set colors
    color_discrete_map = {'Incline West': '#008080',
                        'Pineland': '#FF6F61', 
                        'Rubicon Pt.': '#cab2d6',
                        'Sugar Pine Pt.': '#4169E1',
                        'Tahoe City': '#DAA520',
                        'Zephyr Pt.': '#708090'                                
                            }

    # setup plot
    fig = px.line(df, x = 'Year', y= 'Chl', color='site',
                    color_discrete_map = color_discrete_map)

    fig.update_traces(hovertemplate='<br>%{y:.2f}')


    # set layout
    fig.update_layout(title="Nearshore Attached Algae - Average Chlorophyll",
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        xaxis = dict(
                            tickmode = 'linear',
                            tick0 = 1985,
                            dtick = 5
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[0, 110],
                            title_text='Average Chl'
                        )
                    
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Periphyton.html",
            div_id="Periphyton",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Periphyton.html",
            div_id="Periphyton",
            full_html=False,
        )

def get_primary_productivity_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_PrimaryProductivity", conn)
    return df

def plot_primary_productivity(df, draft = False):
        # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Primary_Productivity', 
                    )

    fig.update_traces(hovertemplate='Primary Productivity<br>%{y:.2f} gmC/m2/yr ')

    df['Threshold']=52

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold<br>%{y:.2f} gmC/m2/yr<extra></extra>'
    ))


    # create trendline
    fig2 = px.scatter(df, x = 'Year', y= 'Primary_Productivity', 
                    trendline='ols', trendline_color_override='#8a7121')

    # set up trendline trace
    trendline = fig2.data[1]

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]
    # get beta value
    beta = fit_results.params[1]
    print("Beta = " + str(fit_results.params[1]))
    # add beta value from trend line to data frame
    df['Beta'] = fit_results.params[1]

    # create variable of beta
    slope = df['Beta']

    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=3, 
                    customdata=slope, hovertemplate='Trend<br>%{customdata:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title='Primary Productivity',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        xaxis = dict(
                            tickmode = 'linear',
                            tick0 = 1960,
                            dtick = 5,
                            title_text='Year'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 50,
                            range=[0, 300],
                            title_text='Value (gmC/m2/yr)'
                        )
                    )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Primary_Productivity.html",
            #include_plotlyjs="directory",
            div_id="Primary_Productivity",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Primary_Productivity.html",
            # include_plotlyjs="directory",
            div_id="Primary_Productivity",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )

# get nearshore turbidity data
def get_nearshore_turbidity_data():
    engine = get_conn('sde_tabular')
    with engine.begin() as conn:
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.Nearshore_NTU", conn)
        # df = df.loc[df['Location'].isin(['Camp Richardson', 'Rubicon'])]
        # drop objectid
        df = df.drop(columns=['OBJECTID'])
        # # unstack so we have Location, Year, Value
        df = df.set_index(['Location']).unstack()
        # flatten to dataframe
        df = df.reset_index()
        # create year column = to level_0[:4]
        df['Year'] = df['level_0'].apply(lambda x: x[3:])
        # drop level_0
        df = df.drop(columns=['level_0'])
        # rename columns 0 to Value
        df = df.rename(columns={0: 'Value'})
    return df

# plot nearshore turbidity data
def plot_nearshore_turbidity(df, draft=True):
    df.rename(columns={'Value': 'Turbidity (NTU)'}, inplace=True)
    fig = px.scatter(df, x='Year', y='Turbidity (NTU)', color="Location")
    # add threshold line
    fig.add_trace(go.Scatter(
        y=[1, 1],
        x=[2015, 2023],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold<br>%{y:.2f} NTU<extra></extra>'
    ))
    # add threshold line equal to 3 NTU
    fig.add_trace(go.Scatter(
        y=[3, 3],
        x=[2015, 2023],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold<br>%{y:.2f} NTU<extra></extra>'
    ))
    fig.update_traces(marker=dict(size=8), mode = 'markers')
    fig.update_layout(
        yaxis=dict(title="Turbidity (NTU)"),
        xaxis=dict(title="Year", showgrid=False),
        template="plotly_white",
        hovermode="x unified",
        dragmode=False,
        margin=dict(t=20),
        # title = "Lake Tahoe Secchi Depth",
        legend=dict(
            title="Turbidity",
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
            file= out_chart / "Draft/Nearshore_Turbidity.html",
            div_id="Nearshore_Turbidity",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Nearshore_Turbidity.html",
            div_id="Nearshore_Turbidity",
            full_html=False
        )

def get_ais_infestation_data_web():
    url = 'https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/114'
    df = get_fs_data(url)
    return df
def get_ais_infestation_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT Site_Name, Infest_Status_2023, Infest_Status_2022, Infest_Status_2021, Infest_Status_2020, Infest_Status_2019, Infest_Status_2018 FROM sde.SDE.AquaticInvasivePlants_ControlSites", conn)
    df_melt = pd.melt(df, id_vars=['Site_Name'], value_vars=['Infest_Status_2023', 'Infest_Status_2022', 'Infest_Status_2021', 'Infest_Status_2020', 
                                                             'Infest_Status_2019', 'Infest_Status_2018'],
                                                            var_name='Year', value_name='Infestation_Status')

    df_melt['Year'] = df_melt['Year'].str[-4:]
    df_melt['Year'] = df_melt['Year'].astype(int)
    df_melt['Infestation_Status'] = df_melt['Infestation_Status'].replace('n/a',None)
    df_melt['Infestation_Status'] = df_melt['Infestation_Status'].str[0]
    df_plot = df_melt.groupby(['Year','Infestation_Status']).size().reset_index(name='count')
    AIS_Status = {'C':'Control', 'S':'Surveillance', 'P':'Planning'}
    df_plot['Infestation_Status'] = df_plot['Infestation_Status'].replace(AIS_Status)
    # calculate percentage of each infestation status by year
    df_plot['total'] = df_plot.groupby('Year')['count'].transform('sum')

    df_plot['percentage'] = round(df_plot['count']/df_plot['total']*100,2)
    return df_plot

def plot_ais_infestation(df, draft=True):
    # setup plot
    color_map = {'Control':"#a37774", 'Surveillance':"#5c6d70", 'Planning':"#015B3D"}
    fig = px.bar(df, x='Year', y='percentage', color='Infestation_Status', barmode='stack', title='AIS site status percentage',
             labels={ 'Infestation_Status': 'Status', 'percentage':'Percentage of Sites'}, color_discrete_map=color_map,
        template="plotly_white",opacity=0.9)

    fig.update_traces(
        hovertemplate='<b>Year: %{x}</b><br>Status: %{fullData.name}<br>Percentage: %{y:.0f}%<extra></extra>'
    )
    # set layout
    fig.update_layout(
                        font_family=font,
                        template=template,
                        showlegend=True,
                        xaxis = dict(
                            tickmode = 'linear',
                            tick0 = 2018,
                            dtick = 1,
                            title_text='Year'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 10,
                            range=[0, 100],
                            title_text='Percentage (%)'
                        )
                    
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/AIS_Infestation.html",
            div_id="AIS_Infestation",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/AIS_Infestation.html",
            div_id="AIS_Infestation",
            full_html=False,
        )

def plot_tahoe_keys(draft=True):
    # setup plot
    data = {
    'Year': [2020, 2020, 2020],
    'Species': ['Eurasian Watermilfoil', 'Coontail', 'Curlyleaf Pondweed'],
    'Square_Feet': [131729, 181720, 188664]
    }
    df = pd.DataFrame(data)
    color_map = {'Eurasian Watermilfoil':"#a37774", 'Coontail':"#5c6d70", 'Curlyleaf Pondweed':"#015B3D"}
    fig = px.bar(df, x='Species', y='Square_Feet', color='Species', title='Volume of Aquatic Invasive Species',
                labels={ 'Species': 'Species', 'Square_Feet':'Square Feet'}, color_discrete_map=color_map,
            template="plotly_white",opacity=0.9)

    
    # set layout
    fig.update_layout(
                        font_family=font,
                        template=template,
                        showlegend=True,
                        xaxis = dict(
                            title_text='Species'
                        ),
                        yaxis = dict(
                            title_text='Cubic Yards',
                            range=[0, 200000]
                        )

                    
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Tahoe_Keys_Infestation.html",
            div_id="Tahoe_Keys_Infestation",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Tahoe_Keys_Infestation.html",
            div_id="Tahoe_Keys_Infestation",
            full_html=False,
        )
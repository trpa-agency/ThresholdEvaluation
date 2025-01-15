from utils import *
# get path to save the file
out_chart = local_path.parents[1] / '2023/AirQuality/Chart'
# config, template, and font for the charts
config = {"displayModeBar": False}
template = 'plotly_white'
font     = 'Calibri'
# set colors
color_discrete_map = {'Cave Rock': '#33a02c',
                      'DL Bliss State Park': '#1f78b4', 
                      'Incline Village/Crystal Bay': '#fb9a99',
                      'Kings Beach': '#e31a1c',
                      'Lake Tahoe Basin': '#ff7f00',
                      'Lake Tahoe CC': '#ff7f00',
                      'LTCC': '#ff7f00',
                      'SOLA': '#a6cee3', 
                      'South Lake Tahoe port': '#b2df8a', 
                      'South Lake Tahoe Sandy Way': '#b2df8a',
                      'South Lake Tahoe Tahoe Blvd': '#b2df8a',
                      'Stateline Harveys':'#cab2d6',
                      'Stateline Horizon': '#cab2d6',
                      'Stateline TRPA': '#cab2d6',
                      'Tahoe City': '#fdbf6f'                    
                        }
# get winter traffic  data
def get_wintertraffic_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_WinterTrafficVolume", conn)
    return df
# get  NOX data
def get_NOX_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_NOX_Emissions", conn)
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

# plot PM 2.5 annual data These colors highlight Lake Tahoe CC and SOLA which our trendline is based off of
PM_discrete_map= {'Cave Rock': '#cab2d6', #lavendar#33a02c',
                      'DL Bliss State Park': '#b2df8a', #mint'#1f78b4'blue close to threhsold blue, 
                      'Incline Village/Crystal Bay': '#c1854b', #(earthy brown),
                      'Kings Beach': '#B0B0B0', #medium gray'#cab2d6', #lavendar
                      'Lake Tahoe CC': '#337ab7', #Threshold darker blue
                      'SOLA': '#337ab7', #Threshold darker blue, 
                      'South Lake Tahoe Sandy Way': '#337ab7', #Threshold darker blue
                      'Stateline TRPA': '#87CEEB', #sky blue
                      'Tahoe City': '#fdbf6f' #peach                    
                        }
def plot_pm2_5_annual(df, draft= False):
    # set indicator
    indicator = 'PM2.5 - ANNUAL AVG.'
    # filter data
    df = df.loc[df['Indicator'] == indicator]

    # correct threshold value errors
    df['Threshold Value'] = 9
# Define the desired order
    site_order = [
        'Lake Tahoe CC'
        'South Lake Tahoe Sandy Way',
        'SOLA',
        'Cave Rock',
        'DL Bliss State Park',
        'Incline Village/Crystal Bay',
        'Kings Beach',
        'Stateline TRPA',
        'Tahoe City'
    ]

    # Reorder the Site column
    df['Site'] = pd.Categorical(df['Site'], categories=site_order, ordered=True)
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', color='Site',
                    color_discrete_map = PM_discrete_map,
                    category_orders={"Site": site_order})

    fig.update_traces(hovertemplate='<b>%{y:.2f}</b> ppm')

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:.0f} ppm<extra></extra>'
    ))

    # Using boolean indexing with case-insensitive comparison includes SOLA and LTCC sites for trend
    dfTrend = df[df['Include_in_Trend_Analysis'].str.lower() == 'yes']

    # create trendline
    fig2 = px.scatter(dfTrend, x = 'Year', y= 'Value', 
                    trendline='ols', trendline_color_override='#8a7121')

    # set up trendline trace
    trendline = fig2.data[1]

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]

    # add beta value from trend line to data frame
    df.loc[df['Indicator'] == indicator, 'Beta'] = fit_results.params[1]

    # create variable of beta
    slope = df.loc[df['Indicator'] == indicator, 'Beta']

    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                    customdata=slope, hovertemplate='Trend: %{customdata:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title="PM 2.5 - Annual Average Concentration",
                        font_family=font,
                        template=template,
                        showlegend=True,
                        dragmode=False,
                        legend_title_text=None, #Remove legend title
                        hovermode="x unified",
                        xaxis = dict(
                            tickmode = 'linear',
                            tick0 = 1985,
                            dtick = 5
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 2,
                            range=[0, 12],
                            title_text='Parts per Million'
                        )
                    
                    )
   # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/AirQuality_AnnualPM25.html",
            # include_plotlyjs="directory",
            div_id="AirQuality_AnnualPM25",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/AirQuality_AnnualPM25.html",
            # include_plotlyjs="directory",
            div_id="AirQuality_AnnualPM25",
            full_html=False
        )
#---------------------------
#24 Hour PM2.5 Concentration
#----------------------------
# plot PM 2.5 24hour data
def plot_pm2_5_24hour(df, draft= False):
    # set indicator
    indicator = 'PM2.5 - 3 YR AVG. 98% 24 HR'
    # limit rows to indicator
    df = df.loc[df['Indicator'] == indicator]
    # correct threshold value errors
    df['Threshold Value'] = 35

    fig = px.scatter(df, x = 'Year', y= 'Value', color='Site', 
                 color_discrete_map = color_discrete_map)

    fig.update_traces(hovertemplate='<br>3-Year Mean of 98th Percentile:<br><b>%{y:.2f}</b> ppm')

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:.0f} ppm<extra></extra>'
    ))

    # filter trend analysis
    #dfTrend = df[df['Include_in_Trend_Analysis'].str.lower() == 'yes']

    # create trendline
    fig2 = px.scatter(df, x = 'Year', y= 'Value', 
                 trendline='ols', trendline_color_override='#8a7121')

    # set up trendline trace
    trendline = fig2.data[1]

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]
    # get beta value
    beta = fit_results.params[1]

    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                 hovertemplate=f'Trend: {beta:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title="PM 2.5 - Highest 24 hour Concentration",
                    font_family=font,
                    template=template,
                    showlegend=True,
                    dragmode=False,
                    hovermode="x unified",
                    legend_title_text=None, #Remove legend title
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1980,
                        dtick = 5
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 10,
                        range=[0, 80],
                        title_text='Parts per Million'
                    )
                  
                 )

    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/AirQuality_24hrPM25.html",
            # include_plotlyjs="directory",
            div_id="AirQuality_24hrPM25",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/AirQuality_24hrPM25.html",
            # include_plotlyjs="directory",
            div_id="AirQuality_24hrPM25",
            full_html=False
        )

#---------------------------
#Annual Average PM10 Concentration
#----------------------------

# plot PM pm annual  data
def plot_pm10_annual(df, draft= False):
    PM_discrete_map= {'Cave Rock': '#33a02c',
                      'DL Bliss State Park': '#b2df8a', 
                      'Incline Village/Crystal Bay': '#c1854b', #(earthy brown),
                      'Kings Beach': '#e31a1c',
                      'Lake Tahoe Basin': '#ff7f00',
                      'Lake Tahoe CC': '#fdbf6f', #peach,
                      'LTCC': '#ff7f00',
                      'SOLA': '#a6cee3', 
                      'South Lake Tahoe port': '#b2df8a', 
                      'South Lake Tahoe Sandy Way': '#337ab7', #Threshold darker blue
                      'South Lake Tahoe Tahoe Blvd': '#b2df8a',
                      'Stateline Harveys':'#cab2d6',
                      'Stateline Horizon': '#cab2d6',
                      'Stateline TRPA': '#cab2d6',
                      'Tahoe City': '#fdbf6f'                    
                        }
    # set indicator
    indicator = 'PM10 - ANNUAL AVG.'

    # limit rows to indicator
    df = df.loc[df['Indicator'] == indicator]
    # correct threshold value errors- CA 
    df['Threshold Value'] = 20
    # Define the desired order
    site_order = ['South Lake Tahoe Sandy Way',
                  'Stateline Horizon',
                  'Stateline TRPA',
                  'SOLA',
                  'Cave Rock',
                  'DL Bliss State Park',
                  'Incline Village/Crystal Bay',
                'Lake Tahoe CC'
    ]

    # Reorder the Site column
    df['Site'] = pd.Categorical(df['Site'], categories=site_order, ordered=True)

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', color='Site',
                 color_discrete_map = PM_discrete_map,
                 category_orders={"Site": site_order})

    fig.update_traces(hovertemplate='<b>%{y:.2f}</b> ppm')

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:.0f} ppm<extra></extra>'
    ))


    # filter trend analysis
    dfTrend = df[df['Include_in_Trend_Analysis'].str.lower() == 'yes']

    # create trendline
    fig2 = px.scatter(dfTrend, x = 'Year', y= 'Value', 
                 trendline='ols', trendline_color_override='#8a7121')

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]

    # create variable of beta
     # Get beta value
    beta = fit_results.params[1]

    # Extract the trendline trace
    trendline = fig2.data[1]
    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                 hovertemplate=f'Trend: {beta:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title="PM 10 - Average Annual Concentration",
                    font_family=font,
                    template=template,
                    showlegend=True,
                    legend_title_text=None, #Remove legend title
                    hovermode="x unified",
                    dragmode=False,
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1985,
                        dtick = 5
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 5,
                        range=[0, 30],
                        title_text='Parts per Million'
                    )
                  
                 )
     # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/AirQuality_AnnualPM10.html",
            # include_plotlyjs="directory",
            div_id="AirQuality_AnnualPM10",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/AirQuality_AnnualPM10.html",
            # include_plotlyjs="directory",
            div_id="AirQuality_AnnualPM10",
            full_html=False
        )

#---------------------------
# PM10 24hr High Concentration
#----------------------------

# plot PM pm annual  data
def plot_pm10_24hr(df, draft= False):

    # set indicator
    indicator = 'PM10 - HIGH 24 HR'

    # limit rows to indicator
    df = df.loc[df['Indicator'] == indicator]
    df['Threshold Value CA'] = 50
    df['Threshold Value NV'] = 150

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', color='Site', 
                 color_discrete_map = color_discrete_map)
         

    fig.update_traces(hovertemplate='<br> Highest 24-hr Concentration: <b>%{y:.2f}</b> ppm')


    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value CA'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='CARB Threshold: %{y:.0f} ppm<extra></extra>'
    ))

     # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value NV'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#337ab7', width=2, dash='dash'),
        mode='lines',
        hovertemplate='EPA NAAQS Threshold: %{y:.0f} ppm<extra></extra>'
    ))

    # create trendline
    fig2 = px.scatter(df, x = 'Year', y= 'Value', 
                 trendline='ols', trendline_color_override='#8a7121')

    # set up trendline trace
    trendline = fig2.data[1]

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]

    # create variable of beta
     # Get beta value
    beta = fit_results.params[1]

    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                 hovertemplate=f'Trend: {beta:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title="PM 10 - Highest 24 hour Concentration",
                    font_family=font,
                    template=template,
                    showlegend=True,
                    hovermode="x unified",
                    legend_title_text=None, #Remove legend title
                    dragmode=False,
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1985,
                        dtick = 5
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 50,
                        range=[0, 500],
                        title_text='Parts per Million'
                    )
                  
                 )
    # export chart
    if draft == True:
        fig.write_html(
        config=config,
        file= out_chart / "Draft/AirQuality_24hrPM10.html",
        # include_plotlyjs="directory",
        div_id="AirQuality_24hrPM10",
        full_html=False
        )   
    elif draft == False: 
        fig.write_html(
           config=config,
           file= out_chart / "Final/AirQuality_24hrPM10.html",
           # include_plotlyjs="directory",
           div_id="AirQuality_24hrPM10",
           full_html=False
       )
#---------------------------
#O3 1- Hour High
#----------------------------
O3_discrete_map={'Cave Rock': '#337ab7', #Threshold darker blue
                      'DL Bliss State Park': '#279bdc', #Threshold light blue 
                      'Incline Village/Crystal Bay': '#c1854b', #(earthy brown),
                      'Kings Beach': '#cab2d6', #lavendar
                      'Lake Tahoe Basin': '#6c9c7b', #medium pine green,
                      'Lake Tahoe CC': '#b2df8a', #mint
                      'LTCC': '#b2df8a', #mint,
                      'SOLA': '#b2df8a', #mint
                      'South Lake Tahoe Airport': '#b2df8a', #mint
                      'South Lake Tahoe Sandy Way': '#b2df8a', #mint
                      'South Lake Tahoe Tahoe Blvd': '#b2df8a', #mint
                      'Stateline Harveys':'#87CEEB', #sky blue
                      'Stateline Horizon': '#87CEEB', #sky blue
                      'Stateline TRPA': '#87CEEB', #sky blue
                      'Tahoe City': '#fdbf6f', #peach#'#fb9a99', #pink                    
                        }
# plot 03 1hour data
def plot_o3_1hour_high(df, draft= False):        

    # set indicator
    indicator = 'O3 - HIGH 1 HR'

    # limit rows to indicator
    df = df.loc[df['Indicator'] == indicator]
    df['Threshold Value'] = .08


    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', color='Site', color_discrete_map = O3_discrete_map) 
                
    fig.update_traces(hovertemplate='<b>%{y:.2f}</b> ppm')


    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:.2f} ppm<extra></extra>'
    ))


    # create trendline
    fig2 = px.scatter(df, x = 'Year', y= 'Value', 
                 trendline='ols', trendline_color_override='#8a7121')

    # set up trendline trace
    trendline = fig2.data[1]

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]
    # get beta value
    beta = fit_results.params[1]

    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                 hovertemplate=f'Trend: {beta:.4f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title="Ozone - 1 hour Average Concentration",
                    font_family=font,
                    template=template,
                    showlegend=True,
                    legend_title_text=None, #Remove legend title
                    dragmode=False,
                    hovermode="x unified",
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1985,
                        dtick = 5
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 0.01,
                        range=[0.06, 0.11],
                        title_text='Parts per Million'
                    )
                  
                 )
    # export chart
    if draft == True:
        fig.write_html(
        config=config,
        file= out_chart / "Draft/AirQuality_1hrOzone.html",
        # include_plotlyjs="directory",
        div_id="AirQuality_1hrOzone",
        full_html=False
        )   
    elif draft == False: 
        fig.write_html(
           config=config,
           file= out_chart / "Final/AirQuality_1hrOzone.html",
           # include_plotlyjs="directory",
           div_id="AirQuality_1hrOzone",
           full_html=False
       )
        
#---------------------------
# CO 8- Hour Average
#----------------------------
# set colors
CO_discrete_map = {   'South Lake Tahoe Tahoe Blvd': '#b2df8a', #mint          
                      'South Lake Tahoe Sandy Way': '#b2df8a', #mint
                      #'South Lake Tahoe Tahoe Blvd': '#279bdc', #Threshold lighter blue         
                      #'South Lake Tahoe Sandy Way': '#279bdc', #Threshold lighter blue#'#6495ED', # cornflower Light Sky Blue
                      #'South Lake Tahoe Sandy Way': '#808080' , #medium gray
                      #'South Lake Tahoe Tahoe Blvd': '#808080' , #medium gray
                      #'Stateline Harveys':'#cab2d6', #lavendar
                      #'Stateline Horizon': '#cab2d6', #lavendar
                      'Stateline Harveys':'#87CEEB', #sky blue
                      'Stateline Horizon': '#87CEEB', #sky blue
                      #'Stateline Harveys':'#B0B0B0', #medium gray
                      #'Stateline Horizon': '#B0B0B0', #medium gray
                      'Stateline TRPA': '#337ab7', #Threshold darker blue
                      #'Stateline TRPA': '#279bdc', #Threshold lighter blue
                      'Tahoe City': '#D3D3D3', #light gray#6495ED', # cornflower#              
                        }
# plot CO 8hour data
def plot_co_8hour_avg(df, draft= False):
    # Set indicator
    indicator = 'CO - HIGH 8 HR'

    # Limit rows to the indicator
    df = df.loc[df['Indicator'] == indicator]

    # Set threshold value
    df['Threshold Value'] = 6

    # Filter the data for years 2013-2023 for the trendline
    df_trendline = df[(df['Year'] >= 2013) & (df['Year'] <= 2023)]

    # Define the desired order
    site_order = [
        'Stateline TRPA',
        'Stateline Harveys',
        'Stateline Horizon',
        'South Lake Tahoe Sandy Way',
        'South Lake Tahoe Tahoe Blvd',
        'Tahoe City'
    ]

    # Reorder the Site column
    df['Site'] = pd.Categorical(df['Site'], categories=site_order, ordered=True)
    # Setup main plot
    fig = px.scatter(df, x='Year', y='Value', color='Site', color_discrete_map= CO_discrete_map,category_orders={"Site": site_order}  # Ensure the legend order
    )
    fig.update_traces(hovertemplate='<b>%{y:.2f}</b> ppm')

    # Create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Year'],
        name="Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:.0f} ppm<extra></extra>'
    ))


    # All data trendline
    #----------------------#

    # Create trendline using the full data
    fig_full_trendline = px.scatter(df, x='Year', y='Value', 
                                color_discrete_map=color_discrete_map,
                                trendline='ols', trendline_color_override='#808080') #B0B0B0') #medium gray

    # Set up trendline trace
    trendline_full = fig_full_trendline.data[1]

    # Get OLS results from full data
    fit_results_full = px.get_trendline_results(fig_full_trendline).px_fit_results.iloc[0]

    # Get beta value
    beta_full = fit_results_full.params[1]

    # Update trendline with slope information
    trendline_full.update(showlegend=True, name="Trend (All)", line_width=2,  
                      hovertemplate=f'Trend (All): {beta_full:.2f}<extra></extra>')

    # Add trendline to the main figure
    fig.add_trace(trendline_full)


    # Filtered data trendline (2013-2023/TRPA Stateline)
    # Create trendline using the filtered data
    fig_filtered_trendline = px.scatter(df_trendline, x='Year', y='Value', 
                                    color_discrete_map=color_discrete_map,
                                    trendline='ols', trendline_color_override='#8a7121')

    # Set up trendline trace
    trendline_filtered = fig_filtered_trendline.data[1]

    # Get OLS results from filtered data
    fit_results_filtered = px.get_trendline_results(fig_filtered_trendline).px_fit_results.iloc[0]

    # Get beta value
    beta_filtered = fit_results_filtered.params[1]

    trendline_filtered.update(showlegend=True, name="Trend (Stateline TRPA)", line_width=2,
                          hovertemplate=f'Trend (Stateline TRPA): {beta_filtered:.2f}<extra></extra>')

    # Add trendline to the main figure
    fig.add_trace(trendline_filtered)

    # Set layout
    fig.update_layout(title="Carbon Monoxide - 8 hour Average Concentration",
                  font_family=font,
                  template=template,
                  showlegend=True,
                  legend_title_text=None, #Remove legend title
                  hovermode="x unified",
                  dragmode=False,
                  xaxis=dict(
                      tickmode='linear',
                      tick0=1985,
                      dtick=5
                  ),
                  yaxis=dict(
                      tickmode='linear',
                      tick0=0,
                      dtick=1,
                      range=[0, 10],
                      title_text='Parts per Million'
                  )
                 )


    # export chart
    if draft == True:
            fig.write_html(
            config=config,
            file= out_chart / "Draft/AirQuality_8hrCO.html",
            # include_plotlyjs="directory",
             div_id="AirQuality_8hrCO",
            full_html=False
            )   
    elif draft == False: 
        fig.write_html(
           config=config,
           file= out_chart / "Final/AirQuality_8hrCO.html",
           # include_plotlyjs="directory",
           div_id="AirQuality_8hrCO",
           full_html=False
       )

#---------------------------
# Regional Visibility 50th Percentile Blis State Park
#----------------------------

# plot 03 1hour data
def plot_50_Bliss_vis(df, draft= False):

    # set indicator
    #indicator = '3-year mean (50th Percentile, Mm-1)'

    # limit rows to indicator
    df = df.loc[(df['Indicator'] == ('3-year mean (50th Percentile, Mm-1)'))&
                      (df['Pollutant'] == 'Regional Visibility')]

    # correct threshold value errors
    df['Threshold Value'] = 25
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', 
                 #color_discrete_map=color_discrete_map,
                 hover_data={'Year':False, # remove year from hover data
                             'Value':':.2f'
                             })

    fig.update_traces(hovertemplate='3-Year Mean: <b>%{y:.1f}</b> Mm-1',
                      name= '3-Year Mean',
                      marker=dict(color='#337ab7'),
                      showlegend=True) #Threshold darker blue)))


    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:.0f} Mm-1<extra></extra>'
    ))


    dfTrend = df[df['Include_in_Trend_Analysis'].str.lower() == 'yes']

    # create trendline
    fig2 = px.scatter(dfTrend, x = 'Year', y= 'Value', 
                 trendline='ols', trendline_color_override='#8a7121')

    # set up trendline trace
    trendline = fig2.data[1]

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]
    # get beta value
    beta = fit_results.params[1]
    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                  hovertemplate=f'Trend: {beta:.1f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title='Regional Visibility 50th Percentile DL Bliss State Park',
                    font_family=font,
                    template=template,
                    showlegend=True,
                    legend_title_text=None, #Remove legend title
                    hovermode="x unified",
                    dragmode=False,
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1985,
                        dtick = 5
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 2,
                        range=[15, 26],
                        title_text='Light Extinction (Mm-1)'
                    )
                 )

    # export chart
    if draft == True:
        fig.write_html(
        config=config,
        file= out_chart / "Draft/AirQuality_RegVis50th_Bliss.html",
        # include_plotlyjs="directory",
        div_id="AirQuality_RegVis50th_Bliss",
        full_html=False
        )   
    elif draft == False: 
        fig.write_html(
           config=config,
           file= out_chart / "Final/AirQuality_RegVis50th_Bliss.html",
           # include_plotlyjs="directory",
           div_id="AirQuality_RegVis50th_Bliss",
           full_html=False
       )
        
#---------------------------
# Regional Visibility 90th Percentile Blis State Park
#----------------------------

# plot 03 1hour data
def plot_90_Bliss_vis(df, draft= False):

    # limit rows to indicator
    df = df.loc[(df['Indicator'] == '3-year mean (90th Percentile, Mm-1)')&
                      (df['Pollutant'] == 'Regional Visibility')]

    # correct threshold value errors
    df['Threshold Value'] = 34
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', 
                 color_discrete_map=color_discrete_map,
                 hover_data={'Year':False, # remove year from hover data
                             'Value':':.2f'
                             })

    fig.update_traces(hovertemplate='3-Year Mean: <b>%{y:.2f}</b> Mm-1',name= '3-Year Mean',
                      marker=dict(color='#337ab7'),
                      showlegend=True)


    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:d} Mm-1<extra></extra>'
    ))


    # create trendline
    fig2 = px.scatter(df, x = 'Year', y= 'Value', 
                 trendline='ols', trendline_color_override='#8a7121')

    # set up trendline trace
    trendline = fig2.data[1]

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]
    # get beta value
    beta = fit_results.params[1]

    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                 hovertemplate=f'Trend: {beta:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title='Regional Visibility 90th Percentile DL Bliss State Park',
                    font_family=font,
                    template=template,
                    showlegend=True,
                    legend_title_text=None, #Remove legend title
                    hovermode="x unified",
                    dragmode=False,
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1985,
                        dtick = 5
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 5,
                        range=[20, 60],
                        title_text='Light Extinction (Mm-1)'
                    )
                 )

    # export chart
    if draft == True:
        fig.write_html(
        config=config,
        file= out_chart / "Draft/AirQuality_RegVis90th_Bliss.html",
        # include_plotlyjs="directory",
        div_id="AirQuality_RegVis90th_Bliss",
        full_html=False
        )   
    elif draft == False: 
        fig.write_html(
           config=config,
           file= out_chart / "Final/AirQuality_RegVis90th_Bliss.html",
           # include_plotlyjs="directory",
           div_id="AirQuality_RegVis90th_Bliss",
           full_html=False
       )
        
#---------------------------
# SubRegional Visibility 50th Percentile SLT
#----------------------------
colors={'LTCC': '#337ab7', #Threshold darker blue,
        'SOLA': '#87CEEB'}#'#a6cee3' also a nice blue...}
# plot 03 1hour data
def plot_50_SLT_vis(df, draft= False):
     #limit rows to indicator
    df = df.loc[(df['Indicator'] == '3-year mean (50th Percentile, Mm-1)')&
                      (df['Pollutant'] == 'Sub-Regional Visibility')]


    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', 
                 color_discrete_map=colors, color='Site',
                 hover_data={'Year':True, # remove year from hover data
                             'Value':':.2f'
                             })

    fig.update_traces(hovertemplate='3-Year Mean: <b>%{y:.2f}</b> Mm-1')


    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:,.0f} Mm-1<extra></extra>'
    ))
    
    #Filter for new data /newest site only
    dfTrend = df[df['Site'] == 'LTCC']
   
   # create trendline
    fig2 = px.scatter(dfTrend, x = 'Year', y= 'Value', 
                     trendline='ols', trendline_color_override='#8a7121')

    # set up trendline trace
    trendline = fig2.data[1]

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]
    # get beta value
    beta = fit_results.params[1]
    #print("Beta = " + str(fit_results.params[1]))
    # add beta value from trend line to data frame
    dfTrend['Beta'] = fit_results.params[1]

    # create variable of beta
    slope = dfTrend['Beta']

    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                     customdata=slope, hovertemplate='Trend: %{customdata:,.2f} Mm-1<extra></extra>')
    # add to figure
    fig.add_trace(trendline)
    # set layout
    # set layout
    fig.update_layout(title='Sub-Regional Visibility 50th Percentile South Lake Tahoe',
                    font_family=font,
                    template=template,
                    showlegend=True,
                    legend_title_text=None, #Remove legend title
                    hovermode="x unified",
                    dragmode=False,
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1985,
                        dtick = 5
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 5,
                        range=[20, 60],
                        title_text='Light Extinction (Mm-1)'
                    )
                 )
    # export chart
    if draft == True:
        fig.write_html(
        config=config,
        file= out_chart / "Draft/AirQuality_SubRegVis50th_SouthLake.html",
        # include_plotlyjs="directory",
        div_id="AirQuality_SubRegVis50th_SouthLake",
        full_html=False
        )   
    elif draft == False: 
        fig.write_html(
           config=config,
           file= out_chart / "Final/AirQuality_SubRegVis50th_SouthLake.html",
           # include_plotlyjs="directory",
           div_id="AirQuality_SubRegVis50th_SouthLake",
           full_html=False
       )

#---------------------------
# SubRegional Visibility 90th Percentile SLT
#----------------------------
colors={'LTCC': '#337ab7', #Threshold darker blue,
        'SOLA': '#87CEEB'}#'#a6cee3' also a nice blue...}
# plot 90th percentiledata
def plot_90_SLT_vis(df, draft= False):
    # limit rows to indicator
    df = df.loc[(df['Indicator'] == '3-year mean (90th Percentile, Mm-1)')&
                      (df['Pollutant'] == 'Sub-Regional Visibility')]


    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', color='Site', 
                 color_discrete_map=colors,
                 hover_data={'Year':True,
                             'Value':':.2f'
                             })

    fig.update_traces(hovertemplate='3-Year Mean: <b>%{y:,.2f}</b> Mm-1')


    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:,.0f} Mm-1<extra></extra>'
    ))

    dfTrend = df[df['Site'] == 'LTCC']
   
   # create trendline
    fig2 = px.scatter(dfTrend, x = 'Year', y= 'Value', 
                     trendline='ols', trendline_color_override='#8a7121')

    # set up trendline trace
    trendline = fig2.data[1]

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]
    # get beta value
    beta = fit_results.params[1]
    #print("Beta = " + str(fit_results.params[1]))
    # add beta value from trend line to data frame
    dfTrend['Beta'] = fit_results.params[1]

    # create variable of beta
    slope = dfTrend['Beta']

    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                     customdata=slope, hovertemplate='Trend: %{customdata:,.2f} Mm-1<extra></extra>')

    # add to figure
    fig.add_trace(trendline)
    # set layout
    fig.update_layout(title='Sub-Regional Visibility 90th Percentile South Lake Tahoe',
                    font_family=font,
                    template=template,
                    showlegend=True,
                    legend_title_text=None, #Remove legend title
                    hovermode="x unified",
                    dragmode=False,
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1985,
                        dtick = 5
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 20,
                        range=[0, 180],
                        title_text='Light Extinction (Mm-1)'
                    )
                 )
    # export chart
    if draft == True:
        fig.write_html(
        config=config,
        file= out_chart / "Draft/AirQuality_SubRegVis90th_SouthLake.html",
        # include_plotlyjs="directory",
        div_id="AirQuality_SubRegVis90th_SouthLake",
        full_html=False
        )   
    elif draft == False: 
        fig.write_html(
           config=config,
           file= out_chart / "Final/AirQuality_SubRegVis90th_SouthLake.html",
           # include_plotlyjs="directory",
           div_id="AirQuality_SubRegVis90th_SouthLake",
           full_html=False
       )

#---------------------------
# NOx
#----------------------------

# plot NOX data
def plot_NOx(df, draft= False):
    df.Value.dropna()

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')

    fig.update_traces(hovertemplate='<b>%{y: .2f}</b> tons per day<extra></extra>',
                      marker=dict(color='#337ab7')) #Threshold darker blue


    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:.0f} <extra></extra>'
    ))


    # create trendline
    fig2 = px.scatter(df, x = 'Year', y= 'Value', 
                 trendline='ols', trendline_color_override='#8a7121')

  

    # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]
    # get beta value
    beta = fit_results.params[1]
    # set up trendline trace
    trendline = fig2.data[1]
    
    # update trendline
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                  hovertemplate=f'Trend: {beta:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title='NOx Emissions',
                    font_family=font,
                    template=template,
                    showlegend=True,
                    legend_title_text=None, #Remove legend title
                    dragmode=False,
                    hovermode="x unified",
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1975,
                        dtick = 5
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 1,
                        range=[0, 8],
                        title_text='Tons per Day'
                    )
                 )
   # export chart
    if draft == True:
        fig.write_html(
        config=config,
        file= out_chart / "Draft/AirQuality_NOx_Emissions.html",
        # include_plotlyjs="directory",
        div_id="AirQuality_NOx_Emissions",
        full_html=False
        )   
    elif draft == False: 
        fig.write_html(
           config=config,
           file= out_chart / "Final/AirQuality_NOx_Emissions.html",
           # include_plotlyjs="directory",
           div_id="AirQuality_NOx_Emissions",
           full_html=False
       )
#---------------------------
# Winter Traffic
#----------------------------

# plot winter traffic data
def plot_winter_traffic(df, draft= False):
    df.dropna()
    # set indicator

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', 
                 hover_data={'Year':True, # remove year from hover data
                             'Value':':,.0f'}
                             )

    fig.update_traces(hovertemplate='Traffic Count: <b>%{y:,.0f}</b> cars',
                      marker=dict(color='#337ab7'))


    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
    hovertemplate='Threshold: %{y:,.0f} cars<extra></extra>'
    ))

    # set layout
    fig.update_layout(title='Winter Traffic Volume',
                    font_family=font,
                    template=template,
                    showlegend=True,
                    legend_title_text=None, #Remove legend title
                    dragmode=False,
                    hovermode="x unified",
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1980,
                        dtick = 5
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 5000,
                        range=[0, 30000],
                        title_text='Number of Cars'
                    )
                )
    # export chart
    if draft == True:
        fig.write_html(
        config=config,
        file= out_chart / "Draft/AirQuality_WinterTrafficVolume.html",
        # include_plotlyjs="directory",
        div_id="AirQuality_WinterTrafficVolume",
        full_html=False
        )   
    elif draft == False: 
        fig.write_html(
           config=config,
           file= out_chart / "Final/AirQuality_WinterTrafficVolume.html",
           # include_plotlyjs="directory",
           div_id="AirQuality_WinterTrafficVolume",
           full_html=False
       )

# get midlake dissolved nitrogen data
def get_midlake_dissolved_nitrogen_data():
    engine = get_conn('sde_tabular')
    with engine.begin() as conn:
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_MidLake_DissolvedNitrogen", conn)
    return df

# plot midlake dissolved nitrogen data
def plot_midlake_dissolved_nitrogen(df, draft=False):
    # df.rename(columns={'Value': 'Dissolved Nitrogen (mg/L)'}, inplace=True)
    fig = px.scatter(df, x='Year', y='Value', color_discrete_sequence=["#023f64"])
    # add threshold line
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', 
    #                  hover_data={'Year':False, # remove year from hover data
    #                              'Value':'y:.2f'
    #                             }
                    )

    fig.update_traces(hovertemplate='Dissolved Nitrogen: <b>%{y:,.0f}</b> g ha-1 yr-1',
                      marker=dict(color='#337ab7'))

    df['Threshold']=1

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold : %{y} <extra></extra>'
    ))
    
    # create trendline
    fig2 = px.scatter(df, x = 'Year', y= 'Value', 
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
    trendline.update(showlegend=True, name="Trend", line_width=2, 
                     customdata=slope, hovertemplate='Trend: %{customdata:,.2f} g/ha/year<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title='Mid Lake Dissolved Nitrogen',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        legend_title_text=None, #Remove legend title
                        dragmode=False,
                        hovermode="x unified",
                        xaxis = dict(
                            tickmode = 'linear',
                            tick0 = 1990,
                            dtick = 5,
                            title_text='Year'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 500,
                            range=[0, 3500],
                            title_text='Grams per Hectare per Year'
                        )
                    )
    # remove threhold from legend?
    #?fig.for_each_trace(lambda t: t.update(showlegend=False) if t.name == 'Threshold' else ())
    
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Midlake_Dissolved_Nitrogen.html",
            div_id="Midlake_Dissolved_Nitrogen",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Midlake_Dissolved_Nitrogen.html",
            div_id="Midlake_Dissolved_Nitrogen",
            full_html=False
        )

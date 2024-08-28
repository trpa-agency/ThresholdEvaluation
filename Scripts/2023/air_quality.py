from utils import *
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
                      'South Lake Tahoe Airport': '#b2df8a', 
                      'South Lake Tahoe Sandy Way': '#b2df8a',
                      'South Lake Tahoe Tahoe Blvd': '#b2df8a',
                      'Stateline Harveys':'#cab2d6',
                      'Stateline Horizon': '#cab2d6',
                      'Stateline TRPA': '#cab2d6',
                      'Tahoe City': '#fdbf6f'                    
                        }
# get bald eagle data
def get_airquality_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_AirQuality", conn)
    return df

# plot PM 2.5 annual data
def plot_pm2_5_annual(df, draft= False):
    # set indicator
    indicator = 'PM2.5 - ANNUAL AVG.'
    # filter data
    df = df.loc[df['Indicator'] == indicator]

    # correct threshold value errors
    df['Threshold Value'] = 12

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value', color='Site',
                    color_discrete_map = color_discrete_map)

    fig.update_traces(hovertemplate='<br>%{y:.2f} ppm')

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold :<br>%{y:.2f} ppm<extra></extra>'
    ))

    # Using boolean indexing with case-insensitive comparison
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
    trendline.update(showlegend=True, name="Trend", line_width=3, 
                    customdata=slope, hovertemplate='Trend :<br>%{customdata:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title="PM 2.5 - Annual Average Concentration",
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
                            range=[0, 15],
                            title_text='Value (ppm)'
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
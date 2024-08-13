from utils import *
out_chart = local_path.parents[1] / '2023/Wildlife/Chart'
template = 'plotly_white'
font     = 'Calibri'

# get bald eagle data
def get_bald_eagle_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.bald_eagle_summarized", conn)
    return df

def get_wildlife_data_web():
    wildlife_url = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/96"
    return get_fs_data(wildlife_url)

def get_waterford_data_web():
    waterfowl_url = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/94"
    return get_fs_data(waterfowl_url)

# plot bald eagle data
def plot_bald_eagle(df, draft=False):
    # filter df for bald eagle
    df = df.loc[df['Wildlife_Species'] == 'Bald Eagle - winter']
    # add threshold value
    df['Threshold Value'] = 2
    # config
    config = {"displayModeBar": False}
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Total', color='Wildlife_Species')

    # update popup
    fig.update_traces(customdata=df['Wildlife_Species'],
                    hovertemplate='%{y:.0f} Bald Eagles Observed<extra></extra>')
    # # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold: %{y:.0f}<extra></extra>'
    ))
    # create trendline
    fig2 = px.scatter(df, x = 'Year', y= 'Total', 
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

    # update trendline legend and popup
    trendline.update(showlegend=True, name="Trend", line_width=3,
                    customdata=slope, 
                    hovertemplate='Trend: %{customdata:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title='Wintering Bald Eagle',
                        legend_title_text='',
                        font_family=font,
                        template=template,
                        hovermode="x unified",
                        showlegend=True,
                        xaxis = dict(
                            tickmode = 'linear',
                            dtick = 5
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[0, 45],
                            title_text='Number of Eagles'
                        )       
                    )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Wildlife_BaldEagle_Winter_NestSites.html",
            include_plotlyjs="directory",
            div_id="Bald Eagle",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Wildlife_BaldEagle_Winter_NestSites.html",
            # include_plotlyjs="directory",
            div_id="Bald_Eagle",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )
from utils import *
out_chart = local_path.parents[1] / '2023/Wildlife/Chart'
# config, template, and font for the charts
config = {"displayModeBar": False}
template = 'plotly_white'
font     = 'Calibri'

def get_primary_productivity_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.PrimaryProductivity", conn)
    return df

def plot_primary_productivity(df, draft = False):
        # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Primary_Productivity', 
    #                  hover_data={'Year':False, # remove year from hover data
    #                              'Value':'y:.2f'
    #                             }
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
            include_plotlyjs="directory",
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

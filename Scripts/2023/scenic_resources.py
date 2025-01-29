from utils import *
import pandas as pd
# global variables
# get path to save the file
out_chart = local_path.parents[1] / '2023/Scenic/Chart'
# set the template, font, and config for the charts
template = 'plotly_white'
font     = 'Calibri'
config   = {"displayModeBar": False}

# get corridor rating data
def get_scenic_corridor_rating():
    # make sql database connection with pyodbc
    engine = get_conn('sde')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde.SDE.Scenic_Corridor_Rating", conn)
    return df

# get scenic viewpoint rating data
def get_scenic_viewpoint_rating():
    # make sql database connection with pyodbc
    engine = get_conn('sde')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde.SDE.Scenic_Viewpoint_Rating", conn)
    return df

# plot scenic attainment
def plot_scenic_corridor_attainment_roadway(df, draft=False):
    # setup data
    df = df.loc[(df['CATEGORY'] == 'Roadway')]
    df = df.groupby(['YEAR','STATUS']).size()
    df = df.to_frame().reset_index()
    df.rename(columns={0:'Count', 'STATUS':'Status', 'YEAR':'Year'}, inplace=True)
    pivotScenic = pd.pivot_table(df,index=['Year'],
                                columns='Status',
                                values='Count')
    df = pd.DataFrame(pivotScenic.to_records())
    # setup plot
    fig = px.bar(df, x="Year", y=["Attainment","Non-Attainment"], 
                color_discrete_sequence=['#A7BEAE','#B85042'])
    # update hover template
    fig.update_traces(hovertemplate='<br> %{y:.0f} units')
    # set layout
    fig.update_layout(
                        # title='Roadway Units in Attainment', 
                        legend_title_text="Roadway Units in Attainment",
                        legend=dict(
                        orientation="h",
                        entrywidth=90,
                        yanchor="bottom",
                        y=1.05,
                        xanchor="right",
                        x=1
                        ),
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        xaxis = dict(
                            tickmode = 'linear',
                            type='category'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[0, 60],
                            title_text='Units'
                        )
                    )
    # show the chart
    fig.show()
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Scenic_Roadway_Attainment.html",
            div_id="Scenic_Roadway_Attainment",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Scenic_Roadway_Attainment.html",
            div_id="Scenic_Roadway_Attainment",
            full_html=False
        )

def plot_scenic_corridor_attainment_shoreline(df, draft=False):
    # setup data
    df = df.loc[(df['CATEGORY'] == 'Shoreline')]
    df = df.groupby(['YEAR','STATUS']).size()
    df = df.to_frame().reset_index()
    df.rename(columns={0:'Count', 'STATUS':'Status', 'YEAR':'Year'}, inplace=True)
    pivotScenic = pd.pivot_table(df,index=['Year'],
                                columns='Status',
                                values='Count')
    df = pd.DataFrame(pivotScenic.to_records())
    # setup plot
    fig = px.bar(df, x="Year", y=["Attainment","Non-Attainment"], 
                color_discrete_sequence=['#A7BEAE', '#B85042'])
    # udpate hover template
    fig.update_traces(hovertemplate='<br> %{y:.0f} units')
    # set layout
    fig.update_layout(
                        # title='Shoreline Units in Attainment', 
                        legend_title_text="Shoreline Units in Attainment",
                        legend=dict(
                        orientation="h",
                        entrywidth=90,
                        yanchor="bottom",
                        y=1.05,
                        xanchor="right",
                        x=1
                        ),
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        xaxis = dict(
                            tickmode = 'linear',
                            type='category'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[0, 35],
                            title_text='Units'
                        )
                    )
    # show the chart
    fig.show()
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Scenic_Shoreline_Attainment.html",
            div_id="Scenic_Shoreline_Attainment",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Scenic_Shoreline_Attainment.html",
            div_id="Scenic_Shoreline_Attainment",
            full_html=False
        )
# plot scenic viewpoint rating
def plot_scenic_viewpoint_roadway_rating(df, draft=False):
    # setup dataframe
    df = df.loc[(df['CATEGORY'] == 'Roadway')]
    df = df.groupby('YEAR')['THRESHOLD_RATING'].mean()
    df = df.to_frame().reset_index()
    df.rename(columns={'YEAR':'Year', 'THRESHOLD_RATING':'Value'}, inplace=True)
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')

    fig.update_traces(hovertemplate='Average Rating (all sites):<br> %{y:.2f}')

    # # create threshold line
    # fig.add_trace(go.Scatter(
    #     y=df['Threshold Value'],
    #     x=df['Year'],
    #     name= "Threshold",
    #     line=dict(color='#333333', width=3),
    #     mode='lines',
    #     hovertemplate='Threshold :<br>%{y:.2f} ppm<extra></extra>'
    # ))


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
    trendline.update(showlegend=True, name="Trend", line_width=3, 
                    customdata=slope, hovertemplate='Trend:<br>%{customdata:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title="Scenic Roadway Resource Ratings",
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
                            range=[0, 10],
                            title_text='Average Scenic Resource Rating'
                        )
                    
                    )


    # show figure
    fig.show()
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Scenic_Roadway_Rating.html",
            div_id="Scenic_Roadway_Rating",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Scenic_Roadway_Rating.html",
            div_id="Scenic_Roadway_Rating",
            full_html=False
        )

# plot scenic shoreline viewpoint rating
def plot_scenic_viewpoint_shoreline_rating(df, draft=False):
    # setup dataframe
    df = df.loc[(df['CATEGORY'] == 'Shoreline')]
    df = df.groupby('YEAR')['THRESHOLD_RATING'].mean()
    df = df.to_frame().reset_index()
    df.rename(columns={'YEAR':'Year', 'THRESHOLD_RATING':'Value'}, inplace=True)
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')

    fig.update_traces(hovertemplate='Average Rating (all sites):<br> %{y:.2f}')

    # # create threshold line
    # fig.add_trace(go.Scatter(
    #     y=df['Threshold Value'],
    #     x=df['Year'],
    #     name= "Threshold",
    #     line=dict(color='#333333', width=3),
    #     mode='lines',
    #     hovertemplate='Threshold :<br>%{y:.2f} ppm<extra></extra>'
    # ))


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
    trendline.update(showlegend=True, name="Trend", line_width=3, 
                    customdata=slope, hovertemplate='Trend:<br>%{customdata:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title="Scenic Shoreline Resource Ratings",
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
                            range=[0, 10],
                            title_text='Average Scenic Resource Rating'
                        )
                    
                    )


    # show figure
    fig.show()
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Scenic_Shoreline_Rating.html",
            div_id="Scenic_Shoreline_Rating",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Scenic_Shoreline_Rating.html",
            div_id="Scenic_Shoreline_Rating",
            full_html=False
        )


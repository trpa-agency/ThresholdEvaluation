from utils import *
out_chart = local_path.parents[1] / '2023/Wildlife/Chart'
# config, template, and font for the charts
config = {"displayModeBar": False}
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
def calculate_estimated_population(df_observed, df_estimated, parameter='EGPN'):
    # Extract growth rates from df_estimated
    growth_rate_row = df_estimated[df_estimated['Parameter'] == parameter]
    
    if not growth_rate_row.empty:
        growth_rate = growth_rate_row['growth_rate'].values[0]
        growth_rate_lower = growth_rate_row['growth_rate_low'].values[0]
        growth_rate_upper = growth_rate_row['growth_rate_upper'].values[0]
    else:
        raise ValueError(f"No {parameter} parameter found in df_estimated")

    # Ensure growth rates are numeric
    growth_rate = float(growth_rate)
    growth_rate_lower = float(growth_rate_lower)
    growth_rate_upper = float(growth_rate_upper)

    # Sort df_observed by 'Year' and reset index
    df_observed = df_observed.sort_values(by='Year').reset_index(drop=True)
    
    # Initialize estimated population columns
    df_observed['estimated_population'] = df_observed['Total']
    df_observed['estimated_population_lower'] = df_observed['Total']
    df_observed['estimated_population_upper'] = df_observed['Total']
    
    # Calculate estimated populations with growth rates
    for i in range(1, len(df_observed)):
        df_observed.loc[i, 'estimated_population'] = df_observed.loc[i-1, 'estimated_population'] * growth_rate
        df_observed.loc[i, 'estimated_population_lower'] = df_observed.loc[i-1, 'estimated_population_lower'] * growth_rate_lower
        df_observed.loc[i, 'estimated_population_upper'] = df_observed.loc[i-1, 'estimated_population_upper'] * growth_rate_upper
    
    return df_observed

def get_bald_eagle_data_wt_estimate_sql():
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df_observed = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_Wildlife", conn)
        df_estimated = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_Wildlife_Estimates", conn)
    df_observed = df_observed.loc[df_observed['Wildlife_Species'] == 'Bald Eagle - winter']
    df_estimated = df_estimated.loc[df_estimated['Species'] == 'Bald Eagle - winter']
    df_observed = calculate_estimated_population(df_observed, df_estimated)
    return df_observed

def get_osprey_data_wt_estimate_sql():
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df_observed = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_Wildlife", conn)
        df_estimated = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_Wildlife_Estimates", conn)
    df_observed = df_observed.loc[df_observed['Wildlife_Species'] == 'Osprey']
    df_estimated = df_estimated.loc[df_estimated['Species'] == 'Osprey']
    df_observed = calculate_estimated_population(df_observed, df_estimated)
    return df_observed

def get_peregrine_falcon_data_wt_estimate_sql():
    engine = get_conn('sde_tabular')

    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df_observed = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_Wildlife", conn)
        df_estimated = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_Wildlife_Estimates", conn)
    df_observed = df_observed.loc[df_observed['Wildlife_Species'] == 'Peregrine Falcon']
    df_observed = df_observed.loc[df_observed['Year'] > 2008]
    df_estimated = df_estimated.loc[df_estimated['Species'] == 'Peregrine Falcon']
    
    df_observed = calculate_estimated_population(df_observed, df_estimated)
    return df_observed

def plot_osprey_data_wt_estimate(df, draft=False):
    df = df.loc[df['Wildlife_Species'] == 'Osprey']
    # add threshold value
    df['Threshold Value'] = 4

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Total', color='Wildlife_Species')

    # update popup
    fig.update_traces(customdata=df['Wildlife_Species'],
                    hovertemplate='<b>%{y:.0f}</b> Osprey Nests Observed<extra></extra>')
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
    fig2 = px.scatter(df, x = 'Year', y= 'estimated_population', 
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
    fig.update_layout(title='Osprey Nests',
                    font_family=font,
                        template=template,
                        hovermode="x unified",
                        showlegend=True,
                        dragmode=False,
                        legend_title_text=None, #Remove legend title
                        xaxis = dict(
                            tickmode = 'linear',
                            dtick = 5
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[0, 35],
                            title_text='Number of Osprey Nests'
                        )       
                    )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Wildlife_Osprey_NestSites.html",
            include_plotlyjs="directory",
            div_id="Osprey",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Wildlife_Osprey_NestSites.html",
            # include_plotlyjs="directory",
            div_id="Osprey",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )


def plot_pfalcon_data_wt_estimate(df, draft=False):
    df = df.loc[df['Wildlife_Species'] == 'Peregrine Falcon']
    # add threshold value
    df['Threshold Value'] = 2

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Total', color='Wildlife_Species')

    # update popup
    fig.update_traces(customdata=df['Wildlife_Species'],
                    hovertemplate='<b>%{y:.0f}</b> Peregrine Falcon Nests Observed<extra></extra>')
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
    fig2 = px.scatter(df, x = 'Year', y= 'estimated_population', 
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
    fig.update_layout(title='Peregrine Falcon Nests',
                        legend_title_text='',
                        font_family=font,
                        template=template,
                        hovermode="x unified",
                        showlegend=True,
                        dragmode=False,
                        xaxis = dict(
                            tickmode = 'linear',
                            dtick = 5
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[0, 10],
                            title_text='Number of Peregrine Falcon Nests'
                        )       
                    )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Wildlife_PeregrineFalcon_NestSites.html",
            #include_plotlyjs="directory",
            div_id="Peregrine Falcon",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Wildlife_PeregrineFalcon_NestSites.html",
            # include_plotlyjs="directory",
            div_id="Peregrine Falcon",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )


def plot_bald_eagle_winter_est(df, draft=False):
    # filter df for bald eagle
    df = df.loc[df['Wildlife_Species'] == 'Bald Eagle - winter']
    # add threshold value
    df['Threshold Value'] = 2

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Total', color='Wildlife_Species')

    # update popup
    fig.update_traces(customdata=df['Wildlife_Species'],
                    hovertemplate='<b>%{y:.0f}</b> Bald Eagles Observed<extra></extra>')
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
    fig2 = px.scatter(df, x = 'Year', y= 'estimated_population', 
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
                        dragmode=False,
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
            file= out_chart / "Draft/Wildlife_BaldEagle_Winter.html",
            div_id="Bald Eagle",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Wildlife_BaldEagle_Winter.html",
            div_id="Bald Eagle",
            full_html=False
        )





def get_wildlife_data_web():
    wildlife_url = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/96"
    return get_fs_data(wildlife_url)

def get_waterford_data_web():
    waterfowl_url = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/94"
    return get_fs_data(waterfowl_url)

# plot bald eagle data
def plot_bald_eagle_winter(df, draft=False):
    # filter df for bald eagle
    df = df.loc[df['Wildlife_Species'] == 'Bald Eagle - winter']
    # add threshold value
    df['Threshold Value'] = 2

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Total', color='Wildlife_Species')

    # update popup
    fig.update_traces(customdata=df['Wildlife_Species'],
                    hovertemplate='<b>%{y:.0f}</b> Bald Eagles Observed<extra></extra>',
                    name='Winter Bald Eagle Count',
                    marker=dict(color='#337ab7'))
    # # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
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
                        dragmode=False,
                        xaxis = dict(
                            tickmode = 'linear',
                            dtick = 1
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
            file= out_chart / "Draft/Wildlife_BaldEagle_Winter.html",
            include_plotlyjs="directory",
            div_id="Bald Eagle",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Wildlife_BaldEagle_Winter.html",
            # include_plotlyjs="directory",
            div_id="Bald_Eagle",
            full_html=False,
            # default_height=500,
            # default_width=800,
        )

# plot bald eagle data
def plot_bald_eagle_summer(df, draft=False):
    # filter df for bald eagle
    df= df.loc[df['Wildlife_Species'] == 'Bald Eagle - nesting']
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Total', color='Wildlife_Species')
    # update popup
    fig.update_traces(customdata=df['Wildlife_Species'],
                    hovertemplate='<b>%{y:.0f}</b> Active Bald Eagle Nests<extra></extra>',
                    name="Active Bald Eagle Nests",
                    marker=dict(color='#337ab7'))
    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:.0f}<extra></extra>'
    ))

    # # create trendline
    fig2 = px.scatter(df, x = 'Year', y= 'Total', 
                    trendline='ols', trendline_color_override='#8a7121')

    # # set up trendline trace
    trendline = fig2.data[1]

    # # get ols results
    fit_results = px.get_trendline_results(fig2).px_fit_results.iloc[0]
    # # get beta value
    beta = fit_results.params[1]
    # # add beta value from trend line to data frame
    df['Beta'] = fit_results.params[1]

    # # create variable of beta
    slope = df['Beta']

    # # update trendline legend and popup
    trendline.update(showlegend=True, name="Trend", line_width=3,
                    customdata=slope, 
                    hovertemplate='Trend: %{customdata:.2f}<extra></extra>')

    # # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(title='Bald Eagle Nesting Pairs',
                        font_family=font,
                        template=template,
                        hovermode="x unified",
                        showlegend=True,
                        dragmode=False,
                        legend_title_text=None, #Remove legend title
                        legend=dict(
                        title=""),
                        xaxis = dict(
                            tickmode = 'linear',
                            dtick = 1
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 1,
                            range=[0, 5],
                            title_text='Number of Active Nests'
                        )       
                    )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Wildlife_BaldEagle_NestSites.html",
            include_plotlyjs="directory",
            div_id="Bald Eagle",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Wildlife_BaldEagle_NestSites.html",
            # include_plotlyjs="directory",
            div_id="Bald_Eagle",
            full_html=False
        )

# plot gosehawk data
def plot_goshawk_data(df, draft=False):
    # get goshawk data
    df = df.loc[df['Wildlife_Species'] == 'Northern Goshawk']
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Total', color='Wildlife_Species')

    # update popup
    fig.update_traces(customdata=df['Wildlife_Species'],
                    hovertemplate='<b>%{y:.0f}</b> Active %{customdata} Nesting Territories<extra></extra>',
                    name='Goshawk Nesting Territories',
                    marker=dict(color='#337ab7'))

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold: %{y:.0f}<extra></extra>'
    ))

    # set layout
    fig.update_layout(
        title='Northern Goshawk Nesting',
        font_family=font,
        template=template,
        hovermode="x unified",
        showlegend=True,
        dragmode=False,
        legend_title_text=None, #Remove legend title
        legend=dict(
            title=""  # Set legend title to an empty string
        ),
        xaxis=dict(
            tickmode='linear',
            tick0= 1997,
            dtick=1
        ),
        yaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=2,
            range=[0, 15],
            title_text='Active Nesting Territories'
        )
    )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Wildlife_Goshawk_NestSites.html",
            include_plotlyjs="directory",
            div_id="Bald Eagle",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Wildlife_Goshawk_NestSites.html",
            # include_plotlyjs="directory",
            div_id="Bald_Eagle",
            full_html=False
        )

# plot perigrine falcon data
def plot_falcon_data(df, draft=False):
    # setup dataframe
    df = df.loc[df['Wildlife_Species'] == 'Peregrine Falcon']

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Total', color='Wildlife_Species')

    # update popup
    fig.update_traces(customdata=df['Wildlife_Species'],
                    hovertemplate='<b>%{y:.0f}</b> Active <b>%{customdata}</b> Nest Sites<extra></extra>',
                    name="Peregrin Falcon Nests", marker=dict(color='#337ab7'))

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
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
    trendline.update(showlegend=True, name="Trend", line_width=2,
                    customdata=slope, 
                    hovertemplate='Trend: %{customdata:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)
    # set layout
    fig.update_layout(title='Peregrine Falcon Nesting',
                        font_family=font,
                        template=template,
                        hovermode="x unified",
                        showlegend=True,
                        dragmode=False,
                        legend_title_text=None, #Remove legend title
                        legend=dict(
                        title=""),
                        xaxis = dict(
                            tickmode = 'linear',
                            tick0=2008,
                            dtick = 1
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 1,
                            range=[0, 6],
                            title_text='Number of Active Nests'
                        )       
                    )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Wildlife_PeregrineFalcon_NestSites.html",
            include_plotlyjs="directory",
            div_id="Bald Eagle",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Wildlife_PeregrineFalcon_NestSites.html",
            # include_plotlyjs="directory",
            div_id="Bald_Eagle",
            full_html=False
        )

# plot osprey chart
def plot_osprey_data(df, draft=False):
    # setup dataframe
    df = df.loc[df['Wildlife_Species'] == 'Osprey']

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Total', color='Wildlife_Species')

    # update popup
    fig.update_traces(customdata=df['Wildlife_Species'],
                    hovertemplate='<b>%{y:.0f}</b> Active <b>%{customdata}</b> Nests<extra></extra>',
                    marker=dict(color='#337ab7'),name='Osprey Nesting')

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
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
    #add beta value from trend line to data frame
    df['Beta'] = fit_results.params[1]

    # create variable of beta
    slope = df['Beta']

    # update trendline legend and popup
    trendline.update(showlegend=True, name="Trend", line_width=2,
                    customdata=slope, 
                    hovertemplate='Trend: %{customdata:.2f}<extra></extra>')

    # add to figure
    fig.add_trace(trendline)

    # set layout
    fig.update_layout(font=font,
                        template=template,
                        hovermode="x unified",
                        showlegend=True,
                        dragmode=False,
                        legend_title_text=None, #Remove legend title
                        legend=dict(
                        title=""
                        ),
                        xaxis = dict(
                            tickmode = 'linear',
                            dtick = 1
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[0, 35],
                            title_text='Number of Active Nests'
                        )       
                    )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Wildlife_Osprey_NestSites.html",
            include_plotlyjs="directory",
            div_id="Bald Eagle",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Wildlife_Osprey_NestSites.html",
            # include_plotlyjs="directory",
            div_id="Bald_Eagle",
            full_html=False
        )

# get waterfowl data from web
def get_waterfowl_data_web():
    waterfowl_url = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/94"
    df = get_fs_data(waterfowl_url)
        # df manipulation
    df = df.drop(['OBJECTID', 'ID', 'Comments'], axis=1)
    df = df.melt(id_vars= 'Name')
    df['variable'] = df['variable'].map(lambda x: x.lstrip('F'))
    df = df.groupby('variable') \
        .agg({'Name':'size', 'value':'mean'}) \
        .rename(columns={'Name':'count','value':'mean_sent'}) \
        .reset_index()
    df.rename(columns={'variable': 'Year', 
                    'mean_sent': 'Human Activity Rating'},
            inplace=True)
    return df

# plot waterfowl data
def plot_waterfowl_data(df, draft=False):
    # Set up plot
    fig = px.line(df, x='Year', y='Human Activity Rating', title="Human Activity in Waterfowl Population Sites")
    # Update traces to show legend
    fig.update_traces(showlegend=True, 
                      name="Average Rating for All Sites", 
                      hovertemplate='Average Rating: <b>%{y:.2f}</b><extra></extra>',
                      line=dict(color='#337ab7', width=3)
                      )
    #Set the range of the x-axis
    fig.update_layout(font_family=font,
                        template=template,
                        hovermode="x unified",
                        showlegend=True,
                        dragmode=False,
                        legend_title_text=None, #Remove legend title
                        xaxis = dict(
                            tickmode = 'linear',
                            dtick = 1
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 0.5,
                            range=[0, 4],
                            title_text='Human Disturbance Rating'
                        ),
                        legend=dict( 
                        orientation="h", 
                        entrywidth=180, 
                        yanchor="bottom", 
                        y=1.05, 
                        xanchor="right", 
                        x=0.95 
                        )  
                        )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Wildlife_Waterfowl.html",
            include_plotlyjs="directory",
            div_id="Bald Eagle",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Wildlife_Waterfowl.html",
            # include_plotlyjs="directory",
            div_id="Bald_Eagle",
            full_html=False
        )
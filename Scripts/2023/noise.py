from utils import *
# global variables
# get path to save the file
out_chart = local_path.parents[1] / '2023/Noise/Chart'
# set the template, font, and config for the charts
template = 'plotly_white'
font     = 'Calibri'
config   = {"displayModeBar": False}

# get plan noise data
def get_plannoise_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_PlanAreaNoise", conn)
    return df

# get shore noise data
def get_shorenoise_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_ShoreNoise", conn)
    return df

# plot Hotel/Motel Noise
def plot_hotelmotel(df, draft = False):
    # filter data
    df = df.loc[df['Category'] == 'Hotel / Motel Areas']
    df.astype({'Year': 'str'}).dtypes
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')
    # update popup
    fig.update_traces(hovertemplate='%{y:.0f} decibels<extra></extra>')
    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.0f} decibels<extra></extra>'
    ))
    # update layout
    fig.update_layout(title='Hotel/Motel Areas Noise',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[40, 80],
                            title_text='Value (average decibels)'
                        )  
                    )
    # generate figure
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Noise_Hotel.html",
            div_id="Noise_Hotel",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Noise_Hotel.html",
            div_id="Noise_Hotel",
            full_html=False
        )    

# plot commercial noise
def plot_commercial(df, draft=True):
    # get commercial area records
    df = df.loc[df['Category'] == 'Commercial Areas']
    df.astype({'Year': 'str'}).dtypes
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')
    # update popup
    fig.update_traces(hovertemplate='%{y:.0f} decibels<extra></extra>')
    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.0f} decibels<extra></extra>'
    ))
    # update layout
    fig.update_layout(title='Commercial Area Noise',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[40, 80],
                            title_text='Value (average decibels)'
                        )  
                    )
    # generate figure
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Noise_Commercial.html",
            div_id="Noise_Commercial",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Noise_Commercial.html",
            div_id="Noise_Commercial",
            full_html=False
        )

# plot residential noise
def plot_highdensityresidential(df, draft=True):
    # get high density residential area records
    df = df.loc[df['Category'] == 'High Density Residential']
    df.astype({'Year': 'str'}).dtypes
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')
    # update popup
    fig.update_traces(hovertemplate='%{y:.0f} decibels<extra></extra>')
    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.0f} decibels<extra></extra>'
    ))
    # update layout
    fig.update_layout(title='High Density Residential Areas Noise',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[40, 80],
                            title_text='Value (average decibels)'
                        )  
                    )
    # generate figure
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Noise_HighDensityResidential.html",
            div_id="Noise_HighDensityResidential",
            full_html=False
        )  
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Noise_HighDensityResidential.html",
            div_id="Noise_HighDensityResidential",
            full_html=False
        )

# plot industrial noise
def plot_industrial(df, draft=True):
    # get industrial area records
    df = df.loc[df['Category'] == 'Industrial Areas']
    df.astype({'Year': 'str'}).dtypes
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')
    # update popup
    fig.update_traces(hovertemplate='%{y:.0f} decibels<extra></extra>')

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.0f} decibels<extra></extra>'
    ))
    # update layout
    fig.update_layout(title='Industrial Areas Noise',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[40, 80],
                            title_text='Value (average decibels)'
                        )  
                    )
    # generate figure
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Noise_Industrial.html",
            div_id="Noise_Industrial",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Noise_Industrial.html",
            div_id="Noise_Industrial",
            full_html=False
        )

# plot low density residential noise
def plot_lowdensity(df, draft=True):
    # get critical wildlife habitat area records
    df = df.loc[df['Category'] == 'Low Density Residential']
    df.astype({'Year': 'str'}).dtypes
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')
    # update popup
    fig.update_traces(hovertemplate='%{y:.0f} decibels<extra></extra>')
    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.0f} decibels<extra></extra>'
    ))
    # update layout
    fig.update_layout(title='Low Density Residential Areas Noise',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[40, 60],
                            title_text='Value (average decibels)'
                        )  
                    )
    # generate figure
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Noise_LowDensityResidential.html",
            div_id="Noise_LowDensityResidential",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Noise_LowDensityResidential.html",
            div_id="Noise_LowDensityResidential",
            full_html=False
        )

# plot rural noise
def plot_rural(df, draft=False):
    # get Rural Outdoor Rec area records
    df = df.loc[df['Category'] == 'Rural Outdoor Recreation Areas']
    df.astype({'Year': 'str'}).dtypes
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')
    # update popup
    fig.update_traces(hovertemplate='%{y:.0f} decibels<extra></extra>')
    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.0f} decibels<extra></extra>'
    ))
    # update layout
    fig.update_layout(title='Rural Outdoor Recreation Areas Noise',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[40, 80],
                            title_text='Value (average decibels)'
                        )  
                    )
    # generate figure
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Noise_RuralOutdoorRecreation.html",
            div_id="Noise_RuralOutdoorRecreation",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Noise_RuralOutdoorRecreation.html",
            div_id="Noise_RuralOutdoorRecreation",
            full_html=False
        )

# plot outdoor recreation noise
def plot_rec(df,draft=False):
    # get urban outdoor rec area records
    df = df.loc[df['Category'] == 'Urban Outdoor Recreation Areas']
    df.astype({'Year': 'str'}).dtypes
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')
    # update popup
    fig.update_traces(hovertemplate='%{y:.0f} decibels<extra></extra>')
    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.0f} decibels<extra></extra>'
    ))
    # update layout
    fig.update_layout(title='Urban Outdoor Recreation Areas Noise',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[40, 80],
                            title_text='Value (average decibels)'
                        )  
                    )
    # generate figure
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Noise_UrbanOutdoorRecreation.html",
            div_id="Noise_UrbanOutdoorRecreation",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Noise_UrbanOutdoorRecreation.html",
            div_id="Noise_UrbanOutdoorRecreation",
            full_html=False
        )

# plot wilderness and roadless area noise
def plot_wilderness(df, draft=False):
    # get Wilderness and Roadless area records
    df = df.loc[df['Category'] == 'Wilderness and Roadless']
    df.astype({'Year': 'str'}).dtypes
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')
    # update popup
    fig.update_traces(hovertemplate='%{y:.0f} decibels<extra></extra>')
    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.0f} decibels<extra></extra>'
    ))
    # update layout
    fig.update_layout(title='Wilderness and Roadless Areas Noise',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[30, 70],
                            title_text='Value (average decibels)'
                        )  
                    )
    # generate figure
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Noise_WildernessRoadless.html",
            div_id="Noise_WildernessRoadless",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Noise_WildernessRoadless.html",
            div_id="Noise_WildernessRoadless",
            full_html=False
        )
    
# plot watercraft noise
def plot_watercraft(df, draft=False):
    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')

    # update popup
    fig.update_traces(hovertemplate='%{y:.2f} exceedances per day<extra></extra>')

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.0f} exceedances per day<extra></extra>'
    ))
    # update layout
    fig.update_layout(title= 'Shoreline Noise',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 0.1,
                            range=[-0.1, 1],
                            title_text='Average Exceedances per Day across all sites'
                        )  
                    )
    # generate figure
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Noise_Watercraft.html",
            div_id="Noise_Watercraft",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Noise_Watercraft.html",
            div_id="Noise_Watercraft",
            full_html=False
        )

# plot wildlife noise
def plot_wildlife(draft=False):
    ##Outdated chart... didn't want to delete this until the other chart is approved
    #dfCriticalNoise = dfPlanNoise.loc[dfPlanNoise['Category'] == 'Critical Wildlife Habitat']
    #dfCriticalNoise.astype({'Year': 'str'}).dtypes
    #df = dfCriticalNoise 

    area = ['Baldwin','Blackwood','Camp Richardson','East Shore','Emerald Bay',
            'Freel Peak','Genoa Peak','Marlette Lake','Martis Peak','Truckee Marsh']

    vals = [46.5, 58.6, np.nan, 56.2,49.2, 47.5, np.nan, np.nan, 45.0, 48.0]

    df = {'Plan Area':area, 'CNEL':vals}

    df= pd.DataFrame(d)
    df['Threshold Value']=45
    df['Average']=50.2

    fig = px.bar(df, x='Plan Area',y='CNEL')

    fig.update_traces(hovertemplate='%{y:,.1f} dB',
                        marker_color='rgb(188,202,200)', 
                        marker_line_color='rgb(88,48,10)',
                        opacity=0.6)


    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Plan Area'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.1f} dB<extra></extra>'
    ))

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Average'],
        x=df['Plan Area'],
        name= "Average CNEL",
        line=dict(color='#8a7121', width=3),
        mode='lines',
        hovertemplate='Average CNEL:<br>%{y:.1f} dB<extra></extra>'
    ))
    
    # set layout
    fig.update_layout(title='Average CNEL Values in Critical Wildlife Habitat Areas',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        xaxis = dict(
                            tickmode = 'linear',
                            dtick = 1,
                            title_text='Plan Area'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 20,
                            range=[0, 80],
                            title_text='A-weighted decibels'
                        )
                    )

    fig.show()

    # THIS IS WRONG---SEE BELOW
    #get critical wildlife habitat area records
    dfWildNoise = dfPlanNoise.loc[dfPlanNoise['Category'] == 'Critical Wildlife Habitat']
    dfWildNoise.astype({'Year': 'str'}).dtypes
    df = dfWildNoise 

    # setup plot
    fig = px.scatter(df, x = 'Year', y= 'Value')

    # update popup
    fig.update_traces(hovertemplate='%{y:.0f} decibels<extra></extra>')

    # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold_Value'],
        x=df['Year'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='lines',
        hovertemplate='Threshold:<br>%{y:.0f} decibels<extra></extra>'
    ))


    # update layout
    fig.update_layout(title='Critical Wildlife Habitat Areas Noise',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 5,
                            range=[40, 80],
                            title_text='Value (average decibels)'
                        )  
                    )
                    


    # generate figure
    fig.show()

from utils import *
import pandas as pd
# global variables
# get path to save the file
out_chart = local_path.parents[1] / '2023/SoilConservation/Chart'
# set the template, font, and config for the charts
template = 'plotly_white'
font     = 'Calibri'
config   = {"displayModeBar": False}

#get SEZ Data
def get_SEZ_data_web():
    SEZ_url = "https://maps.trpa.org/server/rest/services/SEZ_Assessment_Unit/FeatureServer/0"
    df = get_fs_data_spatial(SEZ_url)
    return df
# get soil conservation data
def get_sez_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df  = pd.read_sql('SELECT Threshold_Year, Final_Percent, Final_Points_Possible, Final_Total_Points, Acres FROM sde.SDE.SEZ_Assessment_Unit_evw', conn)
    return df
def get_soil_conservation_data_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        dfImpChg  = pd.read_sql('SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_SoilConservation_ImperviousOverlayAnalysis_Change', conn)
        dfImp2019 = pd.read_sql('SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_SoilConservation_ImperviousOverlayAnalysis_2019', conn)
    return dfImpChg, dfImp2019

# get soil conservation data from web
def get_soil_conservation_data_web():
    impervious_change_url       = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/81"
    impervious_landcap_2019_url = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/82"
    dfImpChg = get_fs_data(impervious_change_url)
    dfImp2019 = get_fs_data(impervious_landcap_2019_url)
    return dfImpChg, dfImp2019

def transform_soil_conservation_data(dfImpChg, dfImp2019):
    df = dfImpChg.astype({"Land_Capab": str})
    df = df.rename(columns={'Land_Capab':'Land Capability', 'GISAcre':'Total Acres', 'OWNERSHIP_': 'Ownership'})
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df[df['Land Capability'].notna()]
    df.set_index('Land Capability')
    dfLCType = df.groupby("Land Capability")["Total Acres"].sum().reset_index()

    df = dfLCType.replace(to_replace='None', value=np.nan).dropna()

    # 2019 analysis results
    df = dfImp2019.astype({"Land_Capab": str})
    df = df.rename(columns={'Land_Capab':'Land Capability', 'GISAcre':'Acre'})
    df.set_index('Land Capability')

    df.loc[(df['Surface']=='Soft')&(df['Feature']=='Trail'), 'Acre'] = df.Acre * 0.5 

    # pivot land capbility by acres of surface type
    pivotSoilImp = pd.pivot_table(df,index=['Land Capability'],
                                columns='Surface',
                                values=['Acre'], 
                                aggfunc=np.sum,fill_value=0)

    flattened = pd.DataFrame(pivotSoilImp.to_records())

    df = flattened.rename(columns={"('Acre', 'Hard')":'Acres of Hard Surface 2019',
                                "('Acre', 'Soft')":'Acres of Soft Surface 2019'})

    # replace all spaces ond blanks with NaN
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df[df['Land Capability'].notna()]

    # calculate acres of coverage
    df["Acres of Coverage 2019"]= df["Acres of Hard Surface 2019"]+df["Acres of Soft Surface 2019"]

    # merge grouped land capability data frame with impervious pivot data frame
    dfMerge = pd.merge(df, dfLCType, on='Land Capability')

    # rename field
    df = dfMerge.rename(columns={'Acre':'Total Acres'})

    # calculate perent coverage
    df['Percent Hard 2019'] = (df['Acres of Hard Surface 2019']/df['Total Acres'])*100
    df['Percent Soft 2019'] = (df['Acres of Soft Surface 2019']/df['Total Acres'])*100
    df['Percent Impervious 2019'] = ((df['Acres of Hard Surface 2019']+df['Acres of Soft Surface 2019'])/df['Total Acres'])*100

    # record percent allowed field
    df['Threshold Value'] = "0%"
    df.loc[df['Land Capability'].isin(['1A','1B','1C','2']), 'Threshold Value'] = "1%"
    df.loc[df['Land Capability'].isin(['3']), 'Threshold Value'] = "5%"
    df.loc[df['Land Capability'].isin(['4']), 'Threshold Value'] = "20%"
    df.loc[df['Land Capability'].isin(['5']), 'Threshold Value'] = "25%"
    df.loc[df['Land Capability'].isin(['6','7']), 'Threshold Value'] = "30%"

    # determine acres of coverage allowed per land capability
    df['Threshold Acres'] = 0
    df.loc[df['Land Capability'].isin(['1A','1B','1C','2']), 'Threshold Acres'] = df['Total Acres']*0.01
    df.loc[df['Land Capability'].isin(['3']), 'Threshold Acres'] = df['Total Acres']*0.05
    df.loc[df['Land Capability'].isin(['4']), 'Threshold Acres'] = df['Total Acres']*0.2
    df.loc[df['Land Capability'].isin(['5']), 'Threshold Acres'] = df['Total Acres']*0.25
    df.loc[df['Land Capability'].isin(['6','7']), 'Threshold Acres'] = df['Total Acres']*0.3

    # df2019 = df.drop(columns=['Threshold Acres', 'Threshold Value', 'Total Acres'])

    df = df[['Land Capability',
            'Acres of Hard Surface 2019',
            'Acres of Soft Surface 2019',
            'Acres of Coverage 2019',
            'Percent Hard 2019',
            'Percent Soft 2019',
            'Percent Impervious 2019',
            'Total Acres',
            'Threshold Value',
            'Threshold Acres']]

    df.dropna(subset=['Land Capability'], inplace=True)

    df['Land Capability']= pd.Categorical(df['Land Capability'], ['1A', '1B', '1C', '2', '3', '4', '5', '6', '7'])

    df.sort_values(by="Land Capability")
    df.set_index('Land Capability')
    return df

# transform new coverage data
def transform_new_coverage_data():
    dfNewImp = pd.read_csv("data/raw_data/FinalCoverageChanges_2020-2023.csv")
    # fill any NaN values with 0
    dfNewImp.fillna(0, inplace=True)
    # drop parcle and jurisdiction columns
    dfNewImp.drop(['Parcel', 'Jurisdiction'], axis=1, inplace=True)
    # melt
    df_melt = dfNewImp.melt(value_vars=['Bailey1a', 'Bailey1b', 'Bailey1c', 'Bailey2', 'Bailey3', 'Bailey4', 'Bailey5', 'Bailey6', 'Bailey7'], var_name='LandCapability', value_name='SqFt')
    # # group by Bailey Type
    df = df_melt.groupby(['LandCapability']).sum()
    # # reset index
    df.reset_index(inplace=True)
    # create acres column
    df['Acres'] = df['SqFt']/43560
    # rename values
    landcap_dict = {'Bailey1a':'1A', 
                    'Bailey1b':'1B', 
                    'Bailey1c':'1C', 
                    'Bailey2':'2', 
                    'Bailey3':'3', 
                    'Bailey4':'4', 
                    'Bailey5':'5', 
                    'Bailey6':'6', 
                    'Bailey7':'7'}
    # map values
    df['LandCapability'] = df['LandCapability'].map(landcap_dict)
    # rename columns
    df.rename(columns={'LandCapability':'Land Capability'}, inplace=True)
    # to csv
    df.to_csv(r"data/processed_data/LandCapability_Acres.csv")
    return df

# add new coverage to existing coverage
def add_new_coverage(dfImpOld, dfImpNew):
    # rename acres to Acres of New Coverage
    dfImpNew.rename(columns={'Acres':'Acres of New Coverage', 'LandCapability':'Land Capability'}, inplace=True)
    # merge old and new data
    dfImp = pd.merge(dfImpOld, dfImpNew, on='Land Capability', how='left')
    dfImp['Acres of Coverage 2023'] = dfImp['Acres of New Coverage'] + dfImp['Acres of Coverage 2019']
    return dfImp

# plot soil conservation data
def plot_soil_conservation(df, landcap = None, draft=True):
    df = df.sort_values(by='Land Capability')

    # create a bar chart
    # create a dictionary of bar colors based on landcap
    colordict = {'1A': 0,
                 '1B': 1,
                 '1C': 2,
                 '2': 3,
                 '3': 4,
                 '4': 5,
                 '5': 6,
                 '6': 7,
                 '7': 8}
    
    # set color map
    colors = ['lightslategray',] * 9
    # update color based on land capability
    colors[colordict[landcap]] = '#279bdc'

    # create threshold lines
    fig = go.Figure(go.Scatter(
        y=df['Threshold Acres'],
        x=df['Land Capability'],
        name= "Threshold",
        line=dict(color='#333333', width=3),
        mode='markers',
        marker_symbol='line-ew',
        marker_line_color="midnightblue", 
        marker_color="lightskyblue", 
        marker_line_width=2, 
        marker_size = 36,
        customdata=df['Threshold Value'],
        hovertemplate='Threshold:<br>%{customdata} coverage allowed<br>or %{y:,.0f} acres<extra></extra>'
    ))

    # create coverage bars
    fig.add_trace(go.Bar(
        y=df['Acres of Coverage 2023'],
        x=df['Land Capability'],
        name= "Coverage 2023",
        marker_color=colors,
    #     marker_color='rgb(188,202,200)', 
        marker_line_color='rgb(88,48,10)',
        opacity=0.6,
        hovertemplate='<b>%{y:,.0f} acres</b> covered<extra></extra>'
    ))

    # set layout
    fig.update_layout(title=f'Impervious Cover in Land Capability Class {landcap}',
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=True,
                        hovermode="x unified",
                        barmode='overlay',
                        xaxis = dict(
                            tickmode = 'linear',
                            title_text=f'Land Capability Class',
                        ),
                        yaxis = dict(
                            title_text='Acres',
                            tickmode = 'linear',
                            rangemode="tozero",
                            range= [0,7000],
                            tick0 = 0,
                            dtick = 1000,
                            tickformat=","
                        )
                    )

    fig.show()
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / f"Draft/SoilConservation_{landcap}.html",
            div_id=f"SoilConservatin_{landcap}",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / f"Final/SoilConservation_{landcap}.html",
            div_id=f"SoilConservation_{landcap}",
            full_html=False,
        )
#def plot_SEZ_scores(df,draft=True):
    
    # Calculate total acres per year
 #   total_acres_per_year = df.groupby('Threshold_Year')['Acres'].sum().reset_index()
  #  total_acres_per_year.rename(columns={'Acres': 'Total_Acres'}, inplace=True)
    # Calculate acres per Final_Rating per year
   # acres_per_rating = df.groupby(['Threshold_Year', 'Final_Rating'])['Acres'].sum().reset_index()
    # Merge total acres with acres per rating
    #merged_df = pd.merge(acres_per_rating, total_acres_per_year, on='Threshold_Year')
    # Calculate percentage
    #merged_df['Percentage'] = (merged_df['Acres'] / merged_df['Total_Acres']) * 100
    # Pivot the data
    #pivot_df = merged_df.pivot(index='Threshold_Year', columns='Final_Rating', values='Percentage').reset_index()
    # Fill NaN with 0 (in case any ratings are missing for a year)
    #pivot_df.fillna(0, inplace=True)
    
    # Create the figure
    #fig = go.Figure()
    # List of ratings
    #ratings = ['D', 'C', 'B', 'A']
    #colors = {'D': '#963b3c', 'C': '#C28025', 'B': '#D4b746', 'A': '#3e8c43'}
   
    #Addbarfor each rating
    #for rating in ratings:
     #   fig.add_trace(go.Bar(
      #      x=pivot_df['Threshold_Year'],
       #     y=pivot_df[rating],
        #    name=f'Rating {rating}',
         #   marker_color=colors[rating]  # Assign color here
        #))

# Update layout to stack the bars
    #fig.update_layout(
     #   barmode='stack',
      #  title='Regional SEZ Condition Index Per Year',
       # xaxis_title='Year',
        #yaxis_title='Percentage of Acres',
        #yaxis=dict(ticksuffix='%'),
        #legend_title='Final Rating'
    #)
    #if draft == True:
     #   fig.write_html(
      #      config=config,
       #     file= out_chart / f"Draft/SoilConservation_SEZ_Scores.html",
        #    div_id=f"SoilConservatin_SEZ_Scores",
      #      full_html=False,
       # )
    #elif draft == False:
     #   fig.write_html(
      #      config=config,
       #     file= out_chart / f"Final/SoilConservation_SEZ_Scores.html",
        #    div_id=f"SoilConservation_SEZ_Scores",
         #   full_html=False,
        #)

def plot_BasinwideSEZ_scores(df, draft=False):
    #BasinwideScore= df[['Acres', 'SEZ_ID','Assessment_Unit_Name','Threshold Year', 'Final_Percent', 'SEZ_Type']]

    # Calculate SEZ_Quality
    df['SEZ_Quality'] = df['Final_Percent']

    # Calculate SEZ_Condition Index
    df['SEZ_Condition_Index'] = df['Acres'] * df['SEZ_Quality']
    # Group by 'Threshold Year' and calculate the sums for each year
    grouped = df.groupby('Threshold_Year').agg(
    total_sez_ci=('SEZ_Condition_Index', 'sum'),
    total_acres=('Acres', 'sum')
    )

    # Calculate the final number for each year
    grouped['BasinwideSEZ_Quality'] = grouped['total_sez_ci'] / grouped['total_acres']
    # Reset index to convert 'Threshold_Year' from index to column
    grouped = grouped.reset_index()
    #Set Threshold Value
    Threshold_Value = 88
    # setup plot
    fig = px.bar(grouped, x = 'Threshold_Year', y= 'BasinwideSEZ_Quality', color_discrete_sequence=['rgba(119, 129, 92, 0.5)'])
                   
    fig.update_traces(texttemplate='%{y:.2f}',  # Format the text labels
        textposition='inside',  # Position the labels inside 
        marker=dict(
            line=dict(color='#77815c', width=2)  # Proper string format for color
        ),
        hovertemplate='SEZ Quality:<br><b>%{y:.2f}</b>')

    # set layout
    fig.update_layout(title='Regional SEZ Quality',
                    font_family=font,
                    template=template,
                    legend_title_text='',
                    showlegend=True,
                    #legend=dict(
                    #orientation="h",
                    #entrywidth=180,
                    #yanchor="bottom",
                    #y=1.05,
                    #xanchor="right",
                    #x=0.95,
                    #),
                    hovermode="x unified",
                    xaxis = dict(
                        tickmode = 'linear',
                        dtick = grouped["Threshold_Year"].unique(),
                        #dtick = 2,
                        #range= [2019, 2024],
                        title_text='Year'
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 25,
                        range=[0, 100],
                        title_text='Acre-weighted SEZ Quality'
                    )
                 )

    # create threshold line
    fig.add_trace(go.Scatter(
        y=[Threshold_Value] * len(df),  # Create a constant line at 88
        x=df['Threshold_Year'],
        #x=[2019,2024],
        name= "Threshold",
        line=dict(color='#333333', width=2, dash='dash'),
        mode='lines',
        hovertemplate='Threshold :<br>%{y:.0f}<extra></extra>'
    ))
    # show figure
    fig.show()
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / f"Draft/SoilConservation_BasinwideSEZScores.html",
            div_id=f"SoilConservatin_BasinwideSEZScores",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / f"Final/SoilConservation_BasinwideSEZScores.html",
            div_id=f"SoilConservation_BasinwideSEZScores",
            full_html=False,
        )
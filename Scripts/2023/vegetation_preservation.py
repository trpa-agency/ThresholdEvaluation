from utils import *
import pandas as pd
# global variables
# get path to save the file
out_chart = local_path.parents[1] / '2023/Vegetation/Chart'
# set the template, font, and config for the charts
template = 'plotly_white'
font     = 'Calibri'
config   = {"displayModeBar": False}
# 
local_path = Path(__file__).parent
#Get Sensitive Plant Data
def get_TDraba_xslx():
    # Set the path to SEnsitive plant Excel files
    path = r'F:\Research and Analysis\Threshold reporting\ThresholdData\Vegetation\Sensitve Plants'
    # Load the data from different sheets
    df = pd.read_excel(f"{path}\DrabaData_2022_USFS.xlsx", sheet_name="Tahoe Draba subpopulations", skiprows=3 )
    return df
def get_CDraba_xslx():
    # Set the path to SEnsitive plant Excel files
    path = r'F:\Research and Analysis\Threshold reporting\ThresholdData\Vegetation\Sensitve Plants'
    # Load the data from different sheets
    df = pd.read_excel(f"{path}\DrabaData_2022_USFS.xlsx", sheet_name="Cup subpopulations", skiprows=2)
    return df
def get_lewisia_xslx():   
    # Set the path to SEnsitive plant Excel files
    path = r'F:\Research and Analysis\Threshold reporting\ThresholdData\Vegetation\Sensitve Plants'
    # Load the data from different sheets
    df = pd.read_excel(f"{path}\LELODataUpdated2022_USFS.xlsx", sheet_name="Long Petaled subpopulations", skiprows=2)
    return df

#-------------
# Plot Sensitive Plants
#----------------
def plot_TDraba(df, draft=False):
    Threshold_Value= 5
    #Tahoe Draba data
    fig = px.bar(df, x='Year', y='subpopulations', title='Tahoe Draba Subpopulations', color_discrete_sequence=['rgba(31, 119, 180, 0.5)'])
        
    # Customize hover template for cleaner display
    fig.update_traces(
        marker=dict(
            line=dict(color='#1f77b4', width=2)  # Proper string format for color
        ),
        hovertemplate='<b>Subpopulations:</b> %{y}<extra></extra>'
    )

    # Ensure that all years are displayed, even if there is no data for some
    fig.update_layout(
                yaxis_title='Subpopulations',
                yaxis=dict(
                range=[0, 50],  # Adjust the range to stay above 0 and slightly above the max value
                tickmode='linear',
                tick0=0,  
                dtick=10   
                ),
                  xaxis=dict(type='category'),
                  font_family=font,  # Example font, replace with your font variable
                  template=template,  # Example template, replace with your template variable
                  showlegend=True,
                  legend=dict(
                orientation="h",
                entrywidth=180,
                yanchor="bottom",
                y=1.05,
                xanchor="right",
                x=0.95,
            ),
                  hovermode="x unified")
    # create threshold line
    fig.add_trace(go.Scatter(
        y=[Threshold_Value] * len(df['Year']),  # Create a constant line
        x=df['Year'],
        name= "Threshold",
        hovertemplate='Threshold : %{y:.0f}<extra></extra>',
        mode='lines',
        line=dict(
        color='#333333',
        width=2,
        dash='dash'  # Apply dashed line style
    )   
    ))
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_TahoeDraba.html",
            # include_plotlyjs="directory",
            div_id="Vegetation_TahoeDraba",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_TahoeDraba.html",
            # include_plotlyjs="directory",
            div_id="Vegetation_TahoeDraba",
            full_html=False
        )    

def plot_CDraba(df, draft=False):
    #Tahoe Draba data
    fig = px.bar(df, x='Year', y='subpopulations', title='Cup Draba Subpopulations', color_discrete_sequence=['rgba(138, 113, 33, 0.5)'])
        
    # Customize hover template for cleaner display
    fig.update_traces(
        marker=dict(
            line=dict(color='#8A7121', width=2)  # Proper string format for color
        ),
        hovertemplate='<b>Subpopulations:</b> %{y}<extra></extra>'
    )

    # Ensure that all years are displayed, even if there is no data for some
    fig.update_layout(yaxis_title='Subpopulations',
                      xaxis_title='Year',
                  xaxis=dict(type='category'),
                  font_family=font,  # Example font, replace with your font variable
                  template=template,  # Example template, replace with your template variable
                  showlegend=True,
                  legend=dict(
                orientation="h",
                entrywidth=180,
                yanchor="bottom",
                y=1.05,
                xanchor="right",
                x=0.95,
            ),
                  hovermode="x unified")
    # create threshold line
    Threshold_Value= 2
    # create threshold line
    fig.add_trace(go.Scatter(
        y=[Threshold_Value] * len(df['Year']),  # Create a constant line
        x=df['Year'],
        name= "Threshold",
        hovertemplate='Threshold : %{y:.0f}<extra></extra>',
        mode='lines',
        line=dict(
        color='#333333',
        width=2,
        dash='dash'  # Apply dashed line style
    )
))
# export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_CupDraba.html",
            # include_plotlyjs="directory",
            div_id="Vegetation_CupDraba",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_CupDraba.html",
            # include_plotlyjs="directory",
            div_id="Vegetation_CupDraba",
            full_html=False
        )    

def plot_lewisia(df, draft=False):
    #Tahoe Draba data
    fig = px.bar(df, x='year', y='subpopulations', title='Long-Petaled Lewisia Subpopulations', color_discrete_sequence=['rgba(119, 129, 92, 0.5)'])
        
    # Customize hover template for cleaner display
    fig.update_traces(
        marker=dict(
            line=dict(color='#77815c', width=2)  # Proper string format for color
        ),
        hovertemplate='<b>Subpopulations:</b> %{y}<extra></extra>'
    )

    # Ensure that all years are displayed, even if there is no data for some
    fig.update_layout(yaxis_title='Subpopulations',
                  xaxis=dict(type='category'),
                  font_family=font,  # Example font, replace with your font variable
                  template=template,  # Example template, replace with your template variable
                  showlegend=True,
                  legend=dict(
                orientation="h",
                entrywidth=180,
                yanchor="bottom",
                y=1.05,
                xanchor="right",
                x=0.95,
            ),
                  hovermode="x unified")
    # create threshold line
    Threshold_Value= 2
    # create threshold line
    fig.add_trace(go.Scatter(
        y=[Threshold_Value] * len(df['year']),  # Create a constant line
        x=df['year'],
        name= "Threshold",
        hovertemplate='Threshold : %{y:.0f}<extra></extra>',
        mode='lines',
        line=dict(
        color='#333333',
        width=2,
        dash='dash'  # Apply dashed line style
    )  
    ))
# export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_Lewisia.html",
            # include_plotlyjs="directory",
            div_id="Vegetation_Lewisia",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_Lewisia.html",
            # include_plotlyjs="directory",
            div_id="Vegetation_Lewisia",
            full_html=False
        )    
#--------------------------------------------------------------------------------         
# get tahoe yellowcress  data
def get_TYC_data_sql():
    # make sql database connection
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_TahoeYellowCress", conn)
    return df
#-------------
#Plot Tahoe YellowCress
#-------------
def plot_TYC(df, draft= False):
    #Not enough data/ incomplete survey for year 2021
    df = df[df['Year'] != 2021]
    # Define thresholds based on lake level conditions
    thresholds = {
        'low': {'condition': lambda x: x < 6225, 'value': 36},
        'mid': {'condition': lambda x: 6225 <= x < 6227, 'value': 26},
        'high': {'condition': lambda x: x >= 6227, 'value': 20}
    }

    threshold_values = []
    for index, row in df.iterrows():
        lake_level = row['Lake_Level']
        occupied_sites = row['Occupied_Sites']
        for level, threshold in thresholds.items():
            if threshold['condition'](lake_level):
                threshold_values.append(threshold['value'])
                break

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

     # create lake level line
    fig.add_trace(go.Scatter(
        y=df['Lake_Level'],
        x=df['Year'],
        name= "Lake Elevation (ft)",
        line=dict(color='rgba(103, 154, 184,.6)'),#color='#679ab8', width=2, opacity=0),
        fill='tonexty',  # Fills under the line only
        fillcolor='rgba(103, 154, 184, 0.2)',  # Sets the fill color and opacity  
        mode= 'lines',
        hovertemplate='Lake Level was %{y:,.0f}ft<extra></extra>',
        legendgroup = 'background'
        ), 
        secondary_y=False)
    
   
    #Add Yellow Cress Data as bar chart
    # Bar chart for Occupied Sites
    fig.add_trace(go.Bar(
    x=df['Year'],
    y=df['Occupied_Sites'],
    name="Total Occupied Sites",
    marker=dict(color='#ffffbf', line=dict(color="#8a7121", width=1.5)),
    #opacity=.6,
    hovertemplate='<b>%{y:,.0f}</b> sites had Tahoe Yellow Cress<extra></extra>',
    legendgroup='foreground'
    ), secondary_y=True)
    
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=threshold_values,
        mode='lines',
        name='Threshold',
        line=dict(color='#333333', dash='dash', width=2),
        hovertemplate='Threshold: %{y}<extra></extra>'
    ), secondary_y=True)
   
    # set layout
    fig.update_layout(title='Tahoe Yellow Cress',
                    font_family=font,
                    template= template,
                    showlegend=True,
                    dragmode=False,
                    hovermode="x unified",
                    xaxis = dict(
                        tickmode = 'linear',
                        tick0 = 1978,
                        dtick = 5,
                        title_text='Year',
                        showgrid=False
                    ),
                    yaxis = dict(
                        tickmode = 'linear',
                        tick0 = 0,
                        dtick = 5,
                        range=[0, 50],
                        title_text='Total Occupied Sites',
                        showgrid=False
                    )
                 )
   
    # Set y-axes titles
    fig.update_yaxes(title_text="Lake Elevation (ft)", tickformat=",d",dtick= 2, 
    range=[df['Lake_Level'].min() - 5, df['Lake_Level'].max() + 5],
    showgrid=False, 
    secondary_y=False)
    # Set layout for the primary (left) y-axis
    fig.update_yaxes(
        title_text="Total Occupied Sites",  # Left Y-axis title
        tickformat=",d",
        range=[0, 45],  # Adjust range for Occupied Sites
        showgrid=False,
        secondary_y=True  # Ensure this is the secondary y-axis (bar chart)
        )
    #fig.update_yaxes(title_text="Lake Level (ft)", tickformat=",d",secondary_y=False)
    # export chart
    fig.update_layout(dict(yaxis2={'anchor': 'x', 'overlaying': 'y', 'side': 'left'},
                  yaxis={'anchor': 'x', 'domain': [0.0, 1.0], 'side':'right'}))

    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_TahoeYellowCress.html",
            # include_plotlyjs="directory",
            div_id="Vegetation_TahoeYellowCress",
            full_html=False
        )   
    elif draft == False: 
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_TahoeYellowCress.html",
            # include_plotlyjs="directory",
            div_id="Vegetation_TahoeYellowCress",
            full_html=False
        )

# get 2010 Ecobject data
def get_ecobject_2010_data():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.Vegetation_EcObject_2010", conn)
    return df

# get 2010 Ecobject data overlaid with Caldor Veg Burn Severity
def get_ecobject_caldor_identity_data():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_Vegetation_ID_Ecobejct2010_CaldorVegBurnSeverity", conn)
    # columns to keep
    columns_to_keep = ['SpatialVar', 'Ownership', 'Development',
                    'WHRTYPE', 'Acres','QMD','Elev_Ft', 'SeralStage', 
                    'TRPA_VegType','gridcode','FID_CaldorBurnSeverity']
    # filter out columns
    df = df[columns_to_keep]
    # filter out Development
    df = df[df['Development'] =='Undeveloped']
    # # drop nan values
    df = df[df['TRPA_VegType'] != '']
    # set SeralStage = N/A to Not Classified
    df['SeralStage'] = df['SeralStage'].replace('N/A', 'Not Classified')
    return df

# get new veg change analysis data
def get_new_veg_change_analysis_data():
    # make sql database connection
    engine = get_conn('sde_tabular')
    # get dataframe from SQL view
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_NewVegChangeAnalysis", conn)
    return df

# get the vegetation type summary data from 2019
def get_2019_vegtypesummary_data():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_VegetationTypeSummary", conn)
    return df

# plot Vegetation Type
def plot_veg_abundance(df, draft=True):
    # dfVegSum = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_VegetationTypeSummary", conn)
    colors = ['#9ed7c2','#cdf57a','#b4d79e', 
            '#ff0000', '#a5f57a','#00a820','#df73ff', 
            '#3e72b0','#2f3f56', '#a8a800']

    # df= df.loc[(df['Development']=='Undeveloped')&(df['QMD']<11)]
    df= df.loc[(df['Development']=='Undeveloped')]

    table = pd.pivot_table(df, values=['Acres'], index=['TRPA_VegType'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened
    df['TRPA_VegType'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=['TRPA_VegType'])

    df['TotalAcres']= 171438.19
    df['VegPercent'] = (df['Acres']/df['TotalAcres'])*100

    # setup chart
    fig = px.bar(df, x="TRPA_VegType", y='VegPercent',  color='TRPA_VegType', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'])

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{y:.1f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br>of undisturbed vegetation"
        ])
    )


    # set layout
    fig.update_layout(title="Vegetation Type % Abundance",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="x unified",
                        barmode = 'overlay',
                        xaxis = dict(
                            tickmode = 'linear',
                            title_text='Vegetation Type'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 10,
                            ticksuffix='%',
                            range=[0, 60],
                            title_text='% of undisturbed vegetation'
                        )
                    )

    fig.show()
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_Abundance.html",
            div_id="Vegetation_Abundance",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_Abundance.html",
            div_id="Vegetation_Abundance",
            full_html=False
        )
        
# get forest fuels treatment data
def get_data_forest_fuel_sql():
    # make sql database connection with pyodbc
    engine = get_conn('sde_tabular')
    # get dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("SELECT * FROM sde_tabular.SDE.ThresholdEvaluation_FuelsTreatment", conn)
    return df

# get EIP Tracker forest fuels treatment data
def get_data_forest_fuel():
    eipForestTreatments = "https://www.laketahoeinfo.org/WebServices/GetReportedEIPIndicatorProjectAccomplishments/JSON/e17aeb86-85e3-4260-83fd-a2b32501c476/19"
    data = pd.read_json(eipForestTreatments)
    df = data[data["PMSubcategoryName1"] == "Treatment Zone"]
    df = df.rename(
        columns={
            "IndicatorProjectYear": "Year",
            "PMSubcategoryOption1": "Treatment Zone",
            "IndicatorProjectValue": "Acres",
        }
    )
    # change value Community Defense Zone to Defense Zone for consistency
    df["Treatment Zone"] = df["Treatment Zone"].replace("Community Defense Zone", "Defense Zone")
    df["Year"] = df["Year"].astype(str)
    df = df.groupby(["Year", "Treatment Zone"]).agg({"Acres": "sum"}).reset_index()
    df.sort_values(by=['Treatment Zone'], inplace=True)
    return df

# plot forest health data
def plot_forest_fuel(df, draft= True):
    years = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"]
    # data
    df = df[df["Year"].isin(years)]
    # plot settings
    path_html="ForestFuelTreatment.html"
    div_id="ForestFuelTreatment"
    x="Year"
    y="Acres"
    facet=None
    color="Treatment Zone"
    color_sequence=["#E69800", "#ABCD66", "#A87000", "#F5CA7A"]
    orders={
        "Year": [
            "2015",
            "2016",
            "2017",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
            "2023",
        ]
    }
    y_title="Acres Treated"
    x_title="Year"
    custom_data=["Treatment Zone"]
    hovertemplate="<br>".join(
        ["<b>%{y:,.0f} acres</b> of forest health treatment", "in the <i>%{customdata[0]}</i>"]
    ) + "<extra></extra>"
    hovermode="x unified"
    format=",.0f"
    additional_formatting=dict(
        # title = "Forest Health Treatment",
        legend=dict(
            title= "Forest Health Treatment Zone",
            orientation="h",
            entrywidth=85,
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=0.95,
        )
    )
    # plot
    # figure 
    fig = px.bar(df, x=x, y=y, 
                color=color, 
                barmode='stack',
                facet_col=facet,
                # facet_row=facet_row,
                color_discrete_sequence=color_sequence,
                category_orders=orders,
                # orientation=orientation,
                custom_data=custom_data
            )
    
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(
        yaxis=dict(tickformat=format, hoverformat=format, title=y_title),
        xaxis=dict(title=x_title),
        hovermode=hovermode,
        template="plotly_white",
        dragmode=False,
        legend_title=None,
    )
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True, tickformat=format))
    fig.update_yaxes(
        col=2, row=1, showticklabels=False, tickfont=dict(color="rgba(0,0,0,0)"), title=None
    )
    fig.update_yaxes(
        col=3, row=1, showticklabels=False, tickfont=dict(color="rgba(0,0,0,0)"), title=None
    )
    fig.update_xaxes(tickformat=".0f")
    fig.update_traces(hovertemplate=hovertemplate)
    fig.update_layout(additional_formatting)
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft" / path_html,
            div_id=div_id,
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final" / path_html,
            div_id=div_id,
            full_html=False,
        )

# get the old growth forest data
def get_old_growth():
    data = get_fs_data(
        "https://maps.trpa.org/server/rest/services/Vegetation_Late_Seral/FeatureServer/0"
    )
    # df = data.groupby(["SeralStage","SpatialVar"]).agg({"Acres": "sum"}).reset_index()
    df = data[["SeralStage", "SpatialVar", "TRPA_VegType", "Acres"]]
    return df

# plot old growth forest data
def plot_old_growth(df, draft=True):
    df = df.groupby("SeralStage").agg({"Acres": "sum"}).reset_index()
    # plot settings
    path_html="Total_Old_Growth.html"
    div_id="OldGrowthForest_SeralStage"
    x="SeralStage"
    y="Acres"
    color_sequence=["#208385"]
    y_title="Acres"
    x_title="Seral Stage"
    custom_data=["SeralStage"]
    hovertemplate="<br>".join(["<b>%{y:,.0f}</b> acres of", "<i>%{customdata[0]}</i> forest"]) + "<extra></extra>"
    hovermode="x unified"
    format=",.0f"
    # plot
    # figure 
    fig = px.bar(df, x=x, y=y,  
                color_discrete_sequence=color_sequence,
                custom_data=custom_data
            )
    
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(
        yaxis=dict(tickformat=format, hoverformat=format, title=y_title),
        xaxis=dict(title=x_title),
        hovermode=hovermode,
        template="plotly_white",
        dragmode=False,
        legend_title=None,
    )
    fig.for_each_yaxis(lambda yaxis: yaxis.update(showticklabels=True, tickformat=format))
    fig.update_yaxes(
        col=2, row=1, showticklabels=False, tickfont=dict(color="rgba(0,0,0,0)"), title=None
    )
    fig.update_yaxes(
        col=3, row=1, showticklabels=False, tickfont=dict(color="rgba(0,0,0,0)"), title=None
    )
    fig.update_xaxes(tickformat=".0f")
    fig.update_traces(hovertemplate=hovertemplate)
    # fig.update_layout(additional_formatting)

    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft" / path_html,
            div_id=div_id,
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final" / path_html,
            div_id=div_id,
            full_html=False,
        )

# plot Red Fir forest abundance
def plot_redfir(df, draft=True):
    colors = ['lightslategray',] * 10
    colors[1] = '#ff0000'

    table = pd.pivot_table(df, values=['Acres'], index=['TRPA_VegType'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened
    df['TRPA_VegType'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=['TRPA_VegType'])

    df['TotalAcres']= 171438.19
    df['VegPercent'] = (df['Acres']/df['TotalAcres'])*100

    df = df.sort_values('Acres', ascending=False)

    # setup chart
    fig = px.bar(df, y="TRPA_VegType", x='VegPercent',  color='TRPA_VegType', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'], orientation='h',)

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{x:.1f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br>of undisturbed vegetation"
        ])
    )

    # create coverage bars
    fig.add_trace(go.Bar(
        x=[6.23],
        y=['Red Fir Forest'],
        name= "Red Fir Forest - QMD<11",
        marker_color='#FF7F7F', 
    #     marker_line_color='rgb(88,48,10)',
    #     opacity=0.6,
        orientation='h',
        hovertemplate='<b>%{x:,.1f}%</b><br>or <b>10,673</b> acres<br>of total undisturbed vegetation <br>is immature Red Fir forest<br>(QMD<11")<extra></extra>'
    ))

    # create coverage bars
    fig.add_trace(go.Bar(
        x=[0.5],
        y=['Red Fir Forest'],
        name= "Red Fir Forest - Burned in Caldor Fire",
        marker_color='#000000', 
    #     marker_line_color='rgb(88,48,10)',
    #     opacity=0.6,
        orientation='h',
        hovertemplate='<b>%{x:,.1f}%</b><br>or <b>862</b> acres<br>of total undisturbed vegetation<br>was Red Fir forest that burned in the Caldor Fire<extra></extra>'
    ))

    # set layout
    fig.update_layout(title="Relative Abundance of Red Fir Forest In Seral Stages Other Than Mature",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="y unified",
                        barmode = 'overlay',
                        yaxis = dict(
                            tickmode = 'linear',
                            title_text='Vegetation Type'
                        ),
                        xaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 10,
                            ticksuffix='%',
                            range=[0, 60],
                            title_text='% of undisturbed vegetation'
                        )
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_RedFir.html",
            div_id="Vegetation_RedFir",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_RedFir.html",
            div_id="Vegetation_RedFir",
            full_html=False
        )

# plot yellow pine abundance
def plot_yellowpine(df, draft=True):
    colors = ['lightslategray',] * 10
    colors[0] = '#a8a800'

    table = pd.pivot_table(df, values=['Acres'], index=['TRPA_VegType'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened
    df['TRPA_VegType'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=['TRPA_VegType'])

    df['TotalAcres']= 171438.19
    df['VegPercent'] = (df['Acres']/df['TotalAcres'])*100

    df = df.sort_values('Acres', ascending=False)

    # setup chart
    fig = px.bar(df, y="TRPA_VegType", x='VegPercent',  color='TRPA_VegType', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'], orientation='h',)

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{x:.1f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br>of undisturbed vegetation"
        ])
    )

    # create coverage bars
    fig.add_trace(go.Bar(
        x=[13.9],
        y=['Yellow Pine Forest'],
        name= "Yellow Pine Forest - QMD<11",
        marker_color='#ffffbf', 
    #     marker_line_color='rgb(88,48,10)',
    #     opacity=0.6,
        orientation='h',
        hovertemplate='<b>%{x:,.1f}%</b><br>or <b>23,836</b> acres<br>of total undisturbed vegetation <br>is immature Yellow Pine Forest<br>(QMD<11")<extra></extra>'
    ))

    # create coverage bars
    fig.add_trace(go.Bar(
        x=[2.6],
        y=['Yellow Pine Forest'],
        name= "Yellow Pine Forest - Burned in Caldor Fire",
        marker_color='#000000', 
    #     marker_line_color='rgb(88,48,10)',
    #     opacity=0.6,
        orientation='h',
        hovertemplate='<b>%{x:,.1f}%</b><br>or <b>4,536</b> acres<br>of total undisturbed vegetation<br>was Yellow Pine forest that burned in the Caldor Fire<extra></extra>'
    ))

    # set layout
    fig.update_layout(title="Relative Abundance of Yellow Pine Forest In Seral Stages Other Than Mature",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="y unified",
                        barmode = 'overlay',
                        yaxis = dict(
                            tickmode = 'linear',
                            title_text='Vegetation Type'
                        ),
                        xaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 10,
                            ticksuffix='%',
                            range=[0, 60],
                            title_text='% of undisturbed vegetation'
                        )
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_YellowPine.html",
            div_id="Vegetation_YellowPine",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_YellowPine.html",
            div_id="Vegetation_YellowPine",
            full_html=False
        )

def plot_veg_composition_canopy(df, draft=True):
    colors = ['#448970','#BEFFE8','#448970','#BEFFE8','#448970','#BEFFE8','grey']

    table = pd.pivot_table(df, values=['Acres'], index=['SeralStage'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened

    df['TotalAcres']= 171438.19
    df['SeralPercent'] = (df['Acres']/df['TotalAcres'])*100

    # setup chart
    fig = px.bar(df, x="SeralStage", y='SeralPercent',  color='SeralStage', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'])

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{y:.2f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br> of undisturbed vegetation"
        ])
    )
    # set layout
    fig.update_layout(title="Stand Composition and Age - Seral Stage by Canopy Classification",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="x unified",
                        xaxis = dict(
                            categoryorder= 'array',
                            categoryarray= ['Early Seral Closed', 'Early Seral Open', 
                                            'Mid Seral Closed', 'Mid Seral Open','Late Seral Closed','Late Seral Open', 'Not Classified'],
                            tickmode = 'linear',
                            title_text='Seral Stage'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 10,
                            range=[0, 50],
                            title_text='% of undisturbed vegetation'
                        )
                    )

    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_Composition_Canopy.html",
            div_id="Vegetation_Composition",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_Composition_Canopy.html",
            div_id="Vegetation_Composition Canopy",
            full_html=False
        )

# plot seral stage
def plot_seral_stage(df, draft=True):
    colors = ['#BEFFE8','#448970','#66CDAB','grey']

    df['SeralClass'] = ''

    df.loc[df['SeralStage'] =='N/A', 'SeralClass'] = 'N/A'
    df.loc[(df['SeralStage']=='Early Seral Closed')|(df['SeralStage']=='Early Seral Open'), 'SeralClass'] = 'Early Seral' 
    df.loc[(df['SeralStage']=='Mid Seral Closed')|(df['SeralStage']=='Mid Seral Open'), 'SeralClass'] = 'Mid Seral' 
    df.loc[(df['SeralStage']=='Late Seral Closed')|(df['SeralStage']=='Late Seral Open'), 'SeralClass'] = 'Late Seral'
    df.loc[df['SeralStage'] =='Not Classified', 'SeralClass'] = 'Not Classified' 

    table = pd.pivot_table(df, values=['Acres'], index=['SeralClass'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened

    df['TotalAcres']= 171438.19
    df['SeralPercent'] = (df['Acres']/df['TotalAcres'])*100

    # setup chart
    fig = px.bar(df, x="SeralClass", y='SeralPercent',  color='SeralClass', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'])

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{y:.2f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br> of undisturbed vegetation"
        ])
    )
    # set layout
    fig.update_layout(title="Seral Stage",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="x unified",
                        xaxis = dict(
                            categoryorder= 'array',
                            categoryarray= ['Early Seral', 'Mid Seral', 'Late Seral', 'Not Classified'],
                            tickmode = 'linear',
                            title_text='Seral Stage'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 50,
                            range=[0, 100],
                            title_text='% of undisturbed vegetation'
                        )
                    )

    fig.show()
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_SeralStage.html",
            div_id="Vegetation_SeralStage",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_SeralStage.html",
            div_id="Vegetation_SeralStage",
            full_html=False
        )


def plot_veg_composition(df, draft=True):
    colors = ['#448970','#BEFFE8','#448970','grey']

    table = pd.pivot_table(df, values=['Acres'], index=['SeralStage'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened

    # combine early open and early closed, mid open and mid closed, late open and late closed
    df['SeralStage'] = df.loc[:, 'SeralStage'].replace({'Early Seral Closed':'Early Seral',
                                                        'Early Seral Open':'Early Seral',
                                                        'Mid Seral Open':'Mid Seral',
                                                        'Mid Seral Closed':'Mid Seral',
                                                        'Late Seral Open':'Late Seral',
                                                        'Late Seral Closed':'Late Seral'})
 
    df['TotalAcres']= 171438.19
    df['SeralPercent'] = (df['Acres']/df['TotalAcres'])*100

    # setup chart
    fig = px.bar(df, x="SeralStage", y='SeralPercent',  color='SeralStage', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'])

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{y:.2f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br> of undisturbed vegetation"
        ])
    )
    # set layout
    fig.update_layout(title="Stand Composition and Age - Seral Stage by Canopy Classification",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="x unified",
                        xaxis = dict(
                            categoryorder= 'array',
                            categoryarray= ['Early Seral Closed', 'Early Seral Open', 
                                            'Mid Seral Closed', 'Mid Seral Open','Late Seral Closed','Late Seral Open', 'Not Classified'],
                            tickmode = 'linear',
                            title_text='Seral Stage'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 10,
                            range=[0, 50],
                            title_text='% of undisturbed vegetation'
                        )
                    )

    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_Composition.html",
            div_id="Vegetation_Composition",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_Composition.html",
            div_id="Vegetation_Composition",
            full_html=False
        )
# plot deciduous forest abundance
def plot_deciduous(df, draft=True):
    colors = ['lightslategray',] * 10
    colors[1] = '#cdf57a'
    table = pd.pivot_table(df, values=['Acres'], index=['TRPA_VegType'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened
    df['TRPA_VegType'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=['TRPA_VegType'])

    df['TotalAcres']= 171438.19
    df['VegPercent'] = (df['Acres']/df['TotalAcres'])*100


    # df2 = {'TRPA_VegType': 'Yellow Pine Forest', 'Acres': 23836.14, 'VegPercent': 13.9} 
    # df = df.append(df2, ignore_index = True) 

    # setup chart
    fig = px.bar(df, x="TRPA_VegType", y='VegPercent',  color='TRPA_VegType', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'])

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{y:.1f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br>of undisturbed vegetation"
        ])
    )

    # set layout
    fig.update_layout(title="Relative Abundance of Deciduous Riparian Vegetation Types",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="x unified",
                        barmode = 'overlay',
                        xaxis = dict(
                            tickmode = 'linear',
                            title_text='Vegetation Type'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 10,
                            ticksuffix='%',
                            range=[0, 60],
                            title_text='% of undisturbed vegetation'
                        )
                    )
    # export chart
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_Deciduous.html",
            div_id="Vegetation_Deciduous",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_Deciduous.html",
            div_id="Vegetation_Deciduous",
            full_html=False
        )

# plot wetland vegetation abundance
def plot_wetland(df, draft=True):
    colors = ['lightslategray',] * 10
    colors[2] = '#b4d79e'
    colors[8] ='#2f3f56'

    # df= df.loc[(df['Development']=='Undeveloped')&(df['QMD']<11)]
    df= df.loc[(df['Development']=='Undeveloped')]


    table = pd.pivot_table(df, values=['Acres'], index=['TRPA_VegType'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened
    df['TRPA_VegType'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=['TRPA_VegType'])

    df['TotalAcres']= 171438.19
    df['VegPercent'] = (df['Acres']/df['TotalAcres'])*100

    # setup chart
    fig = px.bar(df, x="TRPA_VegType", y='VegPercent',  color='TRPA_VegType', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'])

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{y:.1f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br>of undisturbed vegetation"
        ])
    )

    # set layout
    fig.update_layout(title="Relative Abundance of Meadow and Wetland Vegetation Types",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="x unified",
                        barmode = 'overlay',
                        xaxis = dict(
                            tickmode = 'linear',
                            title_text='Vegetation Type'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 10,
                            ticksuffix='%',
                            range=[0, 60],
                            title_text='% of undisturbed vegetation'
                        )
                    )

    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_Wetland.html",
            div_id="Vegetation_Wetland",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_Wetland.html",
            div_id="Vegetation_Wetland",
            full_html=False
        )

# plot shrub abundance
def plot_shrub(df, draft=True):
    colors = ['lightslategray',] * 10
    colors[5] = '#00a820'

    # df= df.loc[(df['Development']=='Undeveloped')&(df['QMD']<11)]
    df= df.loc[(df['Development']=='Undeveloped')]


    table = pd.pivot_table(df, values=['Acres'], index=['TRPA_VegType'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened
    df['TRPA_VegType'].replace('', np.nan, inplace=True)
    df = df.dropna(subset=['TRPA_VegType'])

    df['TotalAcres']= 171438.19
    df['VegPercent'] = (df['Acres']/df['TotalAcres'])*100

    # setup chart
    fig = px.bar(df, x="TRPA_VegType", y='VegPercent',  color='TRPA_VegType', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'])

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{y:.1f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br>of undisturbed vegetation"
        ])
    )

    # set layout
    fig.update_layout(title="Relative Abundance of Shrub Vegetation Types",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="x unified",
                        barmode = 'overlay',
                        xaxis = dict(
                            tickmode = 'linear',
                            title_text='Vegetation Type'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 10,
                            ticksuffix='%',
                            range=[0, 60],
                            title_text='% of undisturbed vegetation'
                        )
                    )

    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_Shrub.html",
            div_id="Vegetation_Shrub",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_Shrub.html",
            div_id="Vegetation_Shrub",
            full_html=False
        )

# plot subalpine seral stage
def plot_seral_subalpine(df,draft=True):
    colors = ['#BEFFE8','#448970','#66CDAB','grey']
    # status dataframe
    df= df.loc[(df.Elev_Ft>8500)]

    df['SeralClass'] = ''

    df.loc[df['SeralStage'] =='N/A', 'SeralClass'] = 'N/A'
    df.loc[(df['SeralStage']=='Early Seral Closed')|(df['SeralStage']=='Early Seral Open'), 'SeralClass'] = 'Early Seral' 
    df.loc[(df['SeralStage']=='Mid Seral Closed')|(df['SeralStage']=='Mid Seral Open'), 'SeralClass'] = 'Mid Seral' 
    df.loc[(df['SeralStage']=='Late Seral Closed')|(df['SeralStage']=='Late Seral Open'), 'SeralClass'] = 'Late Seral' 
    df.loc[df['SeralStage'] =='Not Classified', 'SeralClass'] = 'Not Classified' 
    table = pd.pivot_table(df, values=['Acres'], index=['SeralClass'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened

    df['TotalAcres']= 25619.50
    df['SeralPercent'] = (df['Acres']/df['TotalAcres'])*100

    # setup chart
    fig = px.bar(df, x="SeralClass", y='SeralPercent',  color='SeralClass', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'])

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{y:.2f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br>of undisturbed vegetation<br>above 8,500ft"
        ])
    )
    # set layout
    fig.update_layout(title="Sub-Alpine Zone Seral Stage",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="x unified",
                        xaxis = dict(
                            categoryorder= 'array',
                            categoryarray= ['Early Seral', 'Mid Seral', 'Late Seral', 'Not Classified'],
                            tickmode = 'linear',
                            title_text='Seral Stage'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 50,
                            range=[0, 100],
                            title_text='% of undisturbed vegetation'
                        )
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_Seral_Subalpine.html",
            div_id="Vegetation_SeralSubalpine",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_Seral_Subalpine.html",
            div_id="Vegetation_SeralSubalpine",
            full_html=False
        )

# plot seral in the montane zone
def plot_seral_upper_montane(df,draft=True):
    colors = ['#BEFFE8','#448970','#66CDAB','grey']
    # status dataframe
    df= df.loc[((df.Elev_Ft>7000)&(df.Elev_Ft<=8500))]

    df['SeralClass'] = ''

    df.loc[df['SeralStage'] =='N/A', 'SeralClass'] = 'N/A'
    df.loc[(df['SeralStage']=='Early Seral Closed')|(df['SeralStage']=='Early Seral Open'), 'SeralClass'] = 'Early Seral' 
    df.loc[(df['SeralStage']=='Mid Seral Closed')|(df['SeralStage']=='Mid Seral Open'), 'SeralClass'] = 'Mid Seral' 
    df.loc[(df['SeralStage']=='Late Seral Closed')|(df['SeralStage']=='Late Seral Open'), 'SeralClass'] = 'Late Seral' 
    df.loc[df['SeralStage'] =='Not Classified', 'SeralClass'] = 'Not Classified' 

    table = pd.pivot_table(df, values=['Acres'], index=['SeralClass'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened

    df['TotalAcres']= 93894.92
    df['SeralPercent'] = (df['Acres']/df['TotalAcres'])*100

    # setup chart
    fig = px.bar(df, x="SeralClass", y='SeralPercent',  color='SeralClass', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'])

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{y:.2f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br>of undisturbed vegetation<br>between 7,000 & 8,500ft"
        ])
    )
    # set layout
    fig.update_layout(title="Upper Montane Zone Seral Stage",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="x unified",
                        xaxis = dict(
                            categoryorder= 'array',
                            categoryarray= ['Early Seral', 'Mid Seral', 'Late Seral', 'Not Classified'],
                            tickmode = 'linear',
                            title_text='Seral Stage'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 50,
                            range=[0, 100],
                            title_text='% of undisturbed vegetation'
                        )
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_Seral_UpperMontane.html",
            div_id="Vegetation_SeralUpperMontane",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_Seral_UpperMontane.html",
            div_id="Vegetation_SeralUpperMontane",
            full_html=False
        )

# plot seral in the montane zone
def plot_seral_montane(df,draft=True):
    colors = ['#BEFFE8','#448970','#66CDAB','grey']

    # status dataframe
    df= df.loc[(df.Elev_Ft<=7000)]

    df['SeralClass'] = ''

    df.loc[df['SeralStage'] =='N/A', 'SeralClass'] = 'N/A'
    df.loc[(df['SeralStage']=='Early Seral Closed')|(df['SeralStage']=='Early Seral Open'), 'SeralClass'] = 'Early Seral' 
    df.loc[(df['SeralStage']=='Mid Seral Closed')|(df['SeralStage']=='Mid Seral Open'), 'SeralClass'] = 'Mid Seral' 
    df.loc[(df['SeralStage']=='Late Seral Closed')|(df['SeralStage']=='Late Seral Open'), 'SeralClass'] = 'Late Seral' 
    df.loc[df['SeralStage'] =='Not Classified', 'SeralClass'] = 'Not Classified' 
    table = pd.pivot_table(df, values=['Acres'], index=['SeralClass'],
                            aggfunc=np.sum)

    flattened = pd.DataFrame(table.to_records())

    flattened.columns = [hdr.replace("('Acres', '", '').replace("')", "") \
                        for hdr in flattened.columns]

    df = flattened

    df['TotalAcres']= 51923.77
    df['SeralPercent'] = (df['Acres']/df['TotalAcres'])*100

    # setup chart
    fig = px.bar(df, x="SeralClass", y='SeralPercent',  color='SeralClass', color_discrete_sequence=colors,
                custom_data=['Acres','TotalAcres'])

    fig.update_traces(
        name='',
    #     hoverinfo = "y",  
        hovertemplate="<br>".join([
            "<b>%{y:.2f}%</b>",
            "or <b>%{customdata[0]:,.0f}</b> acres<br>of the %{customdata[1]:,.0f} total acres<br> of undisturbed vegetation<br>below 7,000ft"
        ])
    )
    # set layout
    fig.update_layout(title="Montane Zone Seral Stage",
                        font_family=font,
                        template=template,
                        legend_title_text='',
                        showlegend=False,
                        hovermode="x unified",
                        xaxis = dict(
                            categoryorder= 'array',
                            categoryarray= ['Early Seral', 'Mid Seral', 'Late Seral', 'Not Classified'],
                            tickmode = 'linear',
                            title_text='Seral Stage'
                        ),
                        yaxis = dict(
                            tickmode = 'linear',
                            tick0 = 0,
                            dtick = 50,
                            range=[0, 100],
                            title_text='% of undisturbed vegetation'
                        )
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Vegetation_Seral_Montane.html",
            div_id="Vegetation_SeralMontane",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Vegetation_Seral_Montane.html",
            div_id="Vegetation_SeralMontane",
            full_html=False
        )

# plot land capability
def plot_landcapability(df, draft=True):
    df = df.astype({"Land_Capab": str})
    df = df.rename(columns={'Land_Capab':'Land Capability', 'GISAcre':'Total Acres', 'OWNERSHIP_': 'Ownership'})
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df[df['Land Capability'].notna()]
    df.set_index('Land Capability')
    dfLCType = df.groupby("Land Capability")["Total Acres"].sum().reset_index()
    df = dfLCType
    df = df.dropna()
    df = df.replace(r'^\s*$', np.nan, regex=True)
    df = df.replace(to_replace='None', value=np.nan).dropna()

    df['Land Capability']= pd.Categorical(df['Land Capability'], ['1A', '1B', '1C', '2', '3', '4', '5', '6', '7', ])

    df.sort_values(by="Land Capability")

    colors = ['#D1FF73','#FFFF00','#4CE600','#4C7300', 
            '#0084A8', '#FFD37F','#FFAA00','#CD8966', '#734C00']

    fig = px.bar(df, y="Land Capability", x="Total Acres", color="Land Capability", 
                orientation="h", hover_name="Land Capability",
                color_discrete_sequence=colors ,
                title="Land Capability"
                )

    fig.update_traces(hovertemplate='%{y}<br>%{x:,.0f} acres<extra></extra>')

    fig.update_layout(font_family=font, template=template, showlegend=True)
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Land_Capability.html",
            div_id="LandCapability",
            full_html=False
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Land_Capability.html",
            div_id="LandCapability",
            full_html=False
        )


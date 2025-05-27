from utils import *
out_chart = local_path.parents[1] / '2023/Fisheries/Chart'
# config, template, and font for the charts
config = {"displayModeBar": False}
template = 'plotly_white'
font     = 'Calibri'

# get fish habitat dataS
def get_fishhab():
    # Lake fish hab data
    engine = get_conn('sde')
    # get BMP Status data as dataframe from BMP SQL Database
    with engine.begin() as conn:
        # create dataframe from sql query
        df = pd.read_sql("Select Habitat2015, Acres FROM sde.SDE.Fish_Habitat_2016", conn)

    # set field to string
    
    df['Condition'] = df['Habitat2015'].astype(str)
    # change domain values to text
    df.Condition = df.Condition.replace({"1": "Marginal",
                                         "2": "Feed-Cover",
                                         "3": "Spawning" })
    
    # combine Feed-Cover and Spawning into one category
    df.Condition = df.Condition.replace({"Feed-Cover": "Excellent Habitat",
                                         "Spawning"  : "Excellent Habitat" })
    # group by habitat values and acres
    df = df.groupby(['Condition'])['Acres'].sum().reset_index()
    df['Threshold Value'] = 5948
    # set marginal habitat to NaN for threshold line
    df.loc[df['Condition'] == 'Marginal', 'Threshold Value'] = np.nan
    return df

# plot fish habitat data
def plot_fishhab(df,  draft=False):
    # set colors for bars
    # colors = ['#CDCD66','#00A884','#8400A8']
    # drop index
    # df = df.drop(df.index[0])
    colors = ['#00A884','#CDCD66']

    fig = px.bar(df, x='Condition', y='Acres',  color='Condition', color_discrete_sequence=colors)

    # add threhold line chart
    # fig.add_trace(go.Scatter(x=df['Condition'], y=[1000, 1000], mode='lines', name='Threshold', line=dict(color='red', width=2)))
    fig.update_xaxes(title= 'Condition',tickfont=dict(family='Calibri', size=14))
    fig.update_yaxes(title= 'Acres',  tickfont=dict(family='Calibri', size=14))
    fig.update_xaxes(
        tickvals=["Marginal", "Excellent Habitat"],
        ticktext=["Marginal Habitat", "Excellent Habitat"]  # New labels
    )
    fig.update_traces(hovertemplate='<b>%{y:,.0f}</b> acres<br> of %{x}<extra></extra>',
                      opacity=0.6,
                    showlegend=False)
    fig.update_layout(font=dict(family=font, size=14))
    
    # create threshold line
      
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Condition'],
        name='Threshold',
        showlegend=True,
        line=dict(color='#333333', width=2, dash='dash'),
        mode='markers',
        marker=dict(size=6, color='#333333'),
        marker_symbol='line-ew',
        #marker_line_color="midnightblue", 
        #marker_color="lightskyblue", 
        marker_line_width=2, 
        marker_size = 240,
        customdata=df['Threshold Value'],
        hovertemplate='Threshold target<br>of %{y:,.0f} acres of Excellent Habitat<extra></extra>',
        #showlegend=True
    ))

    # set layout
    fig.update_layout(title="Fish Habitat - Nearshore Lake Tahoe",
                        xaxis_type='category',
                        font_family=font,
                        template=template,
                        showlegend=True,
                        hovermode="x unified",
                        legend=dict(
                orientation="h",
                entrywidth=180,
                yanchor="bottom",
                y=1.05,
                xanchor="right",
                x=0.95,
                title=None
            ),                    
                    )
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Fisheries_Habitat.html",
            div_id="Fish_Habitat",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Fisheries_Habitat.html",
            div_id="Fish_Habitat",
            full_html=False,
        )
#Get Stream HAbitat Condition Data (CSCI Scores
# get stream condition index scores dataS
def get_CSCI():
    #Get data from REST service
    CSCIAverages_url = "https://maps.trpa.org/server/rest/services/LTInfo_Monitoring/MapServer/84"
    df = get_fs_data(CSCIAverages_url)
    return df
    # Lake fish hab data
    #engine = get_conn('sde')
    # get BMP Status data as dataframe from BMP SQL Database
    #with engine.begin() as conn:
        # create dataframe from sql query
       # df = pd.read_sql("sde.SDE.Stream?6", conn)
#Plot Stream Habitat Condition
def plot_avgCSCI(df,  draft=False):
    # match colors to map features
    #colors = ['#E6E600','#E69800','#38A800']
    # Sort DataFrame by 'Year'
    df = df.sort_values(by='Year')
# setup plot if only using average for all trend sites
#fig = px.scatter(dfStreamStatus, x = 'Year', y= 'Value')
#Update Pop up for average of all trend sites.. not per panel
#fig.update_traces(hovertemplate='%{y:.2f} Average CSCI Score<extra></extra>')
    #setup plot
    fig = go.Figure()
    # -- Calculate slope for each panel --
    def calc_slope(y):
        y = y.dropna()
        if len(y) < 2:
            return np.nan  # Not enough data
        x = np.arange(len(y))
        slope, intercept = np.polyfit(x, y, 1)
        return slope

    # Filter data for Test A and Test B
    df_trend_a = df[df['Trend_Panel'] == 'A']
    df_trend_b = df[df['Trend_Panel'] == 'B']

    
    slope_a = calc_slope(df_trend_a['Value'])
    slope_b = calc_slope(df_trend_b['Value'])
    # Add traces for Test A and Test B
    fig.add_trace(go.Scatter(x=df_trend_a['Year'], y=df_trend_a['Value'], mode='markers',
                          marker=dict(color='#87CEEB'), name='Trend Panel A',
                         hovertemplate='Trend Panel A: <b>%{y:.2f}</b> Averaged CSCI<extra></extra>'))
    fig.add_trace(go.Scatter(x=df_trend_b['Year'], y=df_trend_b['Value'], mode='markers',
                         marker=dict(color='#337ab7'), name='Trend Panel B',
                         hovertemplate='Trend Panel B: <b>%{y:.2f}</b> Averaged CSCI</b><extra></extra>'))
    # update layout
    fig.update_layout(title='Stream Bioassessment',
                  xaxis_title= 'Year',
                  hovermode="x unified",
                  font_family=font,
                  template=template,
                  legend=dict(
                #orientation="h",
                entrywidth=180,
                yanchor="bottom",
                y=1.05,
                xanchor="right",
                x=0.95
                ),
                  yaxis=dict(
                      tickmode='linear',
                      tick0=0,
                      dtick=0.05,
                      range=[0.8, 1.05],
                      title_text='Average California Stream Condition Index'
                  ))
    if draft == True:
        fig.write_html(
            config=config,
            file= out_chart / "Draft/Fisheries_StreamStatus.html",
            div_id="Fisheries_StreamStatus",
            full_html=False,
        )
    elif draft == False:
        fig.write_html(
            config=config,
            file= out_chart / "Final/Fisheries_StreamStatus.html",
            div_id="Fisheries_StreamStatus",
            full_html=False,
        )
    return slope_a, slope_b

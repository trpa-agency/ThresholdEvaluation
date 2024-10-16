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
    fig.update_xaxes(title= 'Habitat',tickfont=dict(family='Calibri', size=14))
    fig.update_yaxes(title= 'Acres',  tickfont=dict(family='Calibri', size=14))
    fig.update_xaxes(
        tickvals=["Marginal", "Excellent Habitat"],
    )
    fig.update_traces(hovertemplate='%{x}<br>%{y:,.0f} acres<extra></extra>')
    fig.update_layout(font=dict(family=font, size=14))
        # create threshold line
    fig.add_trace(go.Scatter(
        y=df['Threshold Value'],
        x=df['Condition'],
        line=dict(color='#333333', width=3),
        mode='markers',
        marker_symbol='line-ew',
        marker_line_color="midnightblue", 
        marker_color="lightskyblue", 
        marker_line_width=2, 
        marker_size = 240,
        customdata=df['Threshold Value'],
        hovertemplate='Threshold target<br>of %{y:,.0f} acres<extra></extra>'
    ))
    # set layout
    fig.update_layout(title="Fish Habitat - Nearshore Lake Tahoe",
                        xaxis_type='category',
                        font_family=font,
                        template=template,
                        showlegend=False,
                        hovermode="x unified"                    
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

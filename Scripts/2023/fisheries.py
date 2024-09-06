from utils import *
out_chart = local_path.parents[1] / '2023/Fisheries/Chart'
# config, template, and font for the charts
config = {"displayModeBar": False}
template = 'plotly_white'
font     = 'Calibri'

# get fish habitat data
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
    # group by habitat values and acres
    df = df.groupby(['Condition'])['Acres'].sum().reset_index()

    return df

# plot fish habitat data
def plot_fishhab(df,  draft=False):
    # set colors for bars
    colors = ['#CDCD66','#00A884','#8400A8']
    fig = px.bar(df,  color='Condition', color_discrete_sequence=colors)
    fig.update_layout(xaxis_type='category',
                    title_text='Fish Habitat - Nearshore Lake Tahoe',
                    showlegend = False,
                    template=template
                    )

    fig.update_xaxes(title= 'Habitat',tickfont=dict(family='Calibri', size=14))
    fig.update_yaxes(title= 'Acres', tickfont=dict(family='Calibri', size=14))
    fig.update_xaxes(
        ticktext=["Marginal", "Feed-Cover", "Spawning"],
        tickvals=["0", "1", "2", df.index.max()],
    )
    fig.update_traces(hovertemplate='%{x}<br>%{y:,.0f} acres<extra></extra>')
    fig.update_layout(font=dict(family=font, size=14))
    fig.update_layout(margin=dict(l=0, r=0, t=50, b=0))
    fig.update_layout(autosize=True)
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

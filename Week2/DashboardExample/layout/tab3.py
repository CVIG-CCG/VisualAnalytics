import dash_html_components as html
import dash_core_components as dcc
from mydatabase import transform
from app import app
from dash.dependencies import Output, Input
import plotly.graph_objs as go

df = transform.get_data()

layout = html.Div([
        html.Div([html.H3('Visualize:')], style={'textAlign': 'left'}),
        html.Div([
            dcc.Dropdown(
                id='selected-feature',
                options=[{"label": i, "value": i} for i in ['price', 'rating']],
                value='price',
                style={"display": "black", "width": "80%"}
            )
        ]),
        html.Div([
            dcc.Graph(
                id="ru-my-heatmap",
                style={"margin-right": "auto", "margin-left": "auto", "width": "70%", "height": "600px"}
            )
        ])
])


@app.callback(Output("ru-my-heatmap", "figure"),
            [
                Input("country-drop", "value"),
                Input("province-drop", "value"),
                Input("selected-feature", "value"),
                Input("variety-drop", "value")
            ]
            )
def update_figure(country, province, feature, variety):
    dff = df
    dff.groupby(['country', 'province', 'variety']).mean().reset_index()
    dff = dff.loc[dff['country'].isin(country)]

    if province is None:
        province = []
    if variety is None:
        variety = []

    if len(country) > 0 and len(province) > 0 and len(variety) > 0:
        dff = dff.loc[dff['country'].isin(country) & dff['province'].isin(province) & dff['variety'].isin(variety)]
    elif len(country) > 0 and len(province) > 0 and len(variety) == 0:
        dff = dff.loc[dff['country'].isin(country) & dff['province'].isin(province)]
    elif len(country) > 0 and len(province) == 0 and len(variety) > 0:
        dff.loc[dff['country'].isin(country) & dff['variety'].isin(variety)]
    elif len(country) > 0 and len(province) == 0 and len(variety) == 0:
        dff.loc[dff['country'].isin(country)]
    else:
        dff

    trace = go.Heatmap(
        z=dff[feature],
        x=dff['variety'],
        y=dff['province'],
        hoverongaps= True,
        colorscale='rdylgn',
        colorbar={'title': 'Average', 'x':-0.9}, showscale=True
    )

    return {
        'data':[trace],
        'layout':{
            'xaxis': {'automargin': False},
            'yaxis': {'automargin': True, 'side': 'right'},
            'margin': {'t': 10, 'l': 30, 'r': 100, 'b': 230}
        }
    }
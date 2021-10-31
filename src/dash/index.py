import dash
from dash.dependencies import Input, Output, State
from dash import html
from dash import dcc

import plotly.express as px
px.set_mapbox_access_token(open(".mapbox_token").read())
import pandas as pd
from datetime import date

from helpers import generate_table, generate_table_pics, get_activity_df, get_arrival_df, get_return_df, get_trips_df, render_map

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

app.enable_dev_tools(debug=True, dev_tools_props_check=False)

app.layout = html.Div([
        html.H1('Dash Tabs component demo'),

        html.Div([ 
            html.Table(
            [
                html.Tr([
                    html.Td([
                        html.H3('Trip data'),
                        dcc.Input(id="start_loc", type="text", placeholder="start location", style={'marginRight':'10px'}),
                        dcc.Input(id="dest_loc", type="text", placeholder="destination", style={'marginRight':'10px'}),
                        dcc.DatePickerSingle(
                            id='start_date',
                            date=date.today()
                        ),
                        dcc.Input(
                            id="start_time",
                            type="text",
                            placeholder="HH:MM",
                        ),
                        html.Button(children='Submit', id='submit-val', n_clicks=0),
                        html.Div([
                            html.Div([])
                        ], id='trips')
                    ], style={'width': '50%', 'verticalAlign': 'top'}),
                    html.Td([
                        html.H3('Tab content 2'),
                        html.Div([
                            dcc.Graph(
                                id='map-graph',
                                figure=render_map(pd.DataFrame(columns=['lat', 'lon', 'route_type']))
                            )
                        ], id='map'),
                        html.H3('Arrival'),
                        html.Div([
                            generate_table(get_arrival_df())
                        ]),
                        html.H3('Outdoor activity'),
                        html.Div([
                            generate_table(get_activity_df())
                        ]),
                        html.H3('Return'),
                        html.Div([
                            generate_table(get_return_df())
                        ])
                    ])
                ])
            ], style={"width": "100%", "align-items": "top", "justify-content": "center", 'verticalAlign': 'top'}),
        ])

])



@app.callback(
    Output("trips", "children"),
    Input("submit-val", 'n_clicks'),
    Input("start_date", "date"),
    State("start_loc", "value"),
    State("dest_loc", "value"),
    State("start_time", "value")
)
def update_output(n_clicks, start_date, start_loc, dest_loc, start_time):
    new_df = get_trips_df(n_clicks, start_loc, dest_loc, start_date, start_time)
    return generate_table_pics(new_df)


if __name__ == '__main__':
    app.run_server(debug=True)
import numpy as np
from dash_canvas import DashCanvas
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_daq as daq
import pprint
import json
from dash.exceptions import PreventUpdate
from dash_canvas.utils import array_to_data_url, parse_jsonstring
import dash_bootstrap_components as dbc

import util

dimension = (500, 500)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.NavbarSimple(brand='Christmas with Fourier', dark=True, color='dark', className='mb-3'),
    html.Div(
        ['inspired from ',
         html.A('this', href='https://youtu.be/ds0cmAV-Yek', target='_blank')],
        className='mb-3'
    ),
    dbc.Row([
        dbc.Col(
            DashCanvas(
                id='christmas-canvas',
                lineWidth=2,
                filename='./assets/bg.png',
                hide_buttons=['zoom', 'pan', 'select', 'rectangle', 'line'],
                goButtonTitle='Fourier Series Aggregation'
            )),
        dbc.Col(
            dcc.Loading(
                html.Div(
                    'Draw on the left side'
                    , style={'width': dimension[0], 'height': dimension[1], 'color': 'gray'},className='border'),
                id='fft-output',
            )
        )
    ], justify='center'),
    dbc.Row([
        dbc.Col(
            daq.ColorPicker(
                id='color-picker',
                label='Brush color',
                value=dict(hex='#119DFF')
            ),
        ),
    ], justify='center')
])


@app.callback(Output('christmas-canvas', 'lineColor'),
              Input('color-picker', 'value'),
              )
def update_canvas_linecolor(value):
    if isinstance(value, dict):
        return value['hex']
    else:
        return value


@app.callback(Output('fft-output', 'children'),
              Input('christmas-canvas', 'json_data'),
              prevent_initial_call=True)
def update_data(string):
    if string:
        data = json.loads(string)
        # with open('data.json', 'w') as f:
        #     f.write(string)
        ttl = util.get_line_cords(data, dimension)
        if not ttl:
            raise PreventUpdate
        frames = util.get_frames(ttl, dimension)
        return dcc.Graph(figure=util.get_figure(frames, dimension))

    else:
        raise PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True)

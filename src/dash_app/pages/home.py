import time

import dash
from dash import html, Input, Output, callback

dash.register_page(__name__, path='/')

layout = html.Div(
    [
        html.Div([html.P(id="paragraph_id", children=["Button not clicked"])]),
        html.Button(id="button_id", children="Run Job!"),
    ]
)


@callback(
    Output("paragraph_id", "children"),
    Input("button_id", "n_clicks"),
    running=[
        (Output("button_id", "disabled"), True, False),
        (Output("button_id", "children"), "Running...", "Run Job!")
    ],
    background=True,
    prevent_initial_call=True
)
def update_clicks(n_clicks):
    time.sleep(2.0)
    return [f"Clicked {n_clicks} times"]

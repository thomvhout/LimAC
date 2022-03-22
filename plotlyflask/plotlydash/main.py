import os

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from . import ac
from . import client
from . import utils

"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
"""

# BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css"
# app = dash.Dash(external_stylesheets=[BS])
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


def init_dashboard(server):
    app = dash.Dash(__name__,
                    server=server,
                    routes_pathname_prefix='/dashapp/',
                    )
    """
        external_stylesheets=[
           '/static/dist/css/styles.css',
        ]
        """
    navbar = dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(width=3),  # spacer
                        dbc.Col(html.Img(src=app.get_asset_url(
                            './logo.png'), height="65px")),
                        dbc.Col(html.Div([
                            dbc.NavbarBrand(
                                html.H3("Beste Racecrew Limbo!"), className="ml-2, navbar-dark", href="https://www.youtube.com/watch?v=dQw4w9WgXcQ")],
                            style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})),
                        # Restart Button
                        dbc.Col(
                            dbc.Button(
                                [dbc.Spinner(size="sm"), " Save Settings"],
                                id="btnServerSaveSettings",
                                color="light",
                                # disabled=True,
                                disabled=False,
                            ), width="auto"
                        ),
                        dbc.Col(
                            dbc.Button(
                                ["Stop Server"],
                                id="btnServerStop",
                                color="danger",
                                # disabled=True,
                                disabled=False,
                            ), width="auto"
                        ),
                        dbc.Col(
                            dbc.Button(
                                [dbc.Spinner(size="sm"), " Start Server"],
                                id="btnServerStart",
                                color="success",
                                # disabled=True,
                                disabled=False,
                            ), width="auto"
                        ),
                    ],
                    align="center",
                    # no_gutters=True,
                    className="navbar navbar-expand-lg navbar-dark bg-primary",
                )
            ),
            # dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        ],
        color="primary",
        dark=True,
        sticky="top",
        className="navbar navbar-expand-lg navbar-dark bg-primary",
    )

    def genMapThumbUrl():
        mapImgs = utils.searchFiles(utils.getpwd() + "/assets/img/", "*.png")
        mapImgs.sort()
        mapImgUrl = []
        for img in mapImgs:
            mapImgUrl.append(dbc.Col(dbc.Card(
                [
                    dbc.CardImg(src=app.get_asset_url("./img/" + img)),
                    dbc.CardBody([html.H4(img)])
                ], className="bg-dark"), width="auto",

                style={'width': '25%',
                       'align-items': 'center', 'justify-content': 'center'}
            ))
        return mapImgUrl

    # mapImages = dbc.Row(children=genMapThumbUrl(),
    #                    no_gutters=True, id="tracks")
    mapImages = dbc.Row(children=genMapThumbUrl(), id="tracks")

    trackButtons = html.Div(
        [
            dbc.RadioItems(
                id="radioTrack",
                options=[
                    {"label": "Track 1", "value": 1},
                    {"label": "Track 2", "value": 2},
                    {"label": "Track 3", "value": 3},
                ]
            ), html.Div(
                id="radioOutput"
            )
        ], className="radio-group"
    )

    def genTrackSelectOptions():
        available = []
        tracks = ac.getTracks()
        for layout in tracks:
            available.append({"label": layout[0], "value": layout[0]})
        return available

    def genLayoutSelectOptions(track):
        print("track gotten:" + track)
        available = []
        tracks = ac.getTracks()
        # TODO fix bug: check only top level tracks => track="drag1000" returns the full match
        matchTracks = [mTrack for mTrack in tracks if track in mTrack]
        if len(matchTracks) == 0 or len(matchTracks[0]) == 1:
            # The track has no extra layouts or no track match was found
            return [{"label": "default", "value": "default"}]
        i = 1
        # Loop through layouts, skipping track name at index 1
        matchTracks[0].sort()
        for j in range(1, len(matchTracks[0])):
            available.append(
                {"label": matchTracks[0][i], "value": i})
            i += 1
        return available

    tab_tracks_content = dbc.Card(
        dbc.CardBody(
            [
                html.H3("Select Track"),
                dbc.InputGroup([
                    # TODO replace w/ dbc.DropdownMenu for pretty type search support
                    # dbc.InputGroupAddon("Track"),
                    dbc.InputGroupText("Track"),
                    dbc.Select(options=genTrackSelectOptions(),
                               id="selectTrack"),
                    # dbc.InputGroupAddon("Layout"),
                    dbc.InputGroupText("Layout"),
                    dbc.Select(options=genLayoutSelectOptions("default"),
                               id="selectLayout"),
                    dbc.Button("Confirm", id="btnTrackConfirm"),
                ], id="trackSelectGroup"
                ),
                trackButtons,
                mapImages,
                # html.P("This is tab 1!", className="card-text"),
            ]
        ),
        className="mt-3",

        style={'width': '100%', 'display': 'flex',
               'align-items': 'center', 'justify-content': 'center'}
    )

    tab_cars_content = dbc.Card(
        dbc.CardBody(
            [
                html.Img(src=app.get_asset_url("./carLoop.gif")),
                dcc.Dropdown(
                    options=[
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'Montreal', 'value': 'MTL'},
                        {'label': 'San Francisco', 'value': 'SF'}
                    ],
                    value=['MTL', 'NYC'],
                    multi=True)
            ],
            style={'width': '100%', 'display': 'flex',
                   'align-items': 'center', 'justify-content': 'center'}
        ), className="mt-3")

    tabs = html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(label="Tracks", tab_id="tab-tracks"),
                    # label_style={"color": "#FFFFFF"}),
                    dbc.Tab(label="Cars", tab_id="tab-cars"),
                ],
                id="tabs",
                active_tab="tab-tracks",
            ),
            html.Div(id="content"),
        ]
    )

    app.layout = dbc.Container([
        #    html.Div([
        #        dbc.Navbar(
        #            [navbar]),
        #        tabs,
        #    ], className="navbar navbar-expand-lg fixed-top navbar-dark bg-primary"),
        navbar,
        tabs,
    ], fluid=True, className="p-0")
    #               className controls padding (+more?)

    # TODO Fix example dynamic content (https://community.plotly.com/t/add-dynamic-content-to-a-div/22233)

    @app.callback(Output("content", "children"), [Input("tabs", "active_tab")])
    def switch_tab(at):
        if at == "tab-tracks":
            return tab_tracks_content
        elif at == "tab-cars":
            return tab_cars_content
        return html.P("This shouldn't ever be displayed...")

    @ app.callback(
        [
            Output("selectLayout", "options"),
            Output("selectLayout", "value"),
        ],
        [
            Input("selectTrack", "value"),
            Input("selectLayout", "value"),
            Input("btnTrackConfirm", "n_clicks"),
        ],
    )
    def update_trackSelect(track, layout, confirm):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dash.no_update
        else:
            elem_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if elem_id == "selectTrack":
            return genLayoutSelectOptions(track), 1
        elif elem_id == "selectLayout":
            return dash.no_update
        elif elem_id == "btnTrackConfirm":
            # TODO send to server
            client.sendToServer(f"t;{track};{layout}")
            return dash.no_update
        return [{"label": "default", "value": "default"}]

    # Buttons

    @ app.callback(
        Output('btnServerStart', 'children'),
        Input('btnServerStart', 'n_clicks'),
    )
    def update_btnServerStart(n_clicks):
        if n_clicks == None:
            n_clicks = " "
        else:
            ret = client.sendToServer("start")
            return ret
        return "Server Start {}".format(n_clicks)

    # TODO Move to function, in order to obstruct the command passed to the AC server
    # Buttons

    @ app.callback(
        Output('btnServerStop', 'children'),
        Input('btnServerStop', 'n_clicks'),
    )
    def update_btnServerStop(n_clicks):
        if n_clicks == None:
            n_clicks = " "
        else:
            # TODO put client's server response in `popover` when failing
            ret = client.sendToServer("stop")
            return ret
        return "Server Stop {}".format(n_clicks)

    @ app.callback(
        Output('btnServerSaveSettings', 'children'),
        Input('btnServerSaveSettings', 'n_clicks'),
    )
    def update_btnServerSave(n_clicks):
        if n_clicks == None:
            n_clicks = " "
        return "Saving Settings {}".format(n_clicks)

    @ app.callback(
        Output('radioOutput', 'children'),
        Input('radioTrack', 'id')
    )
    def update_radio(value):
        return "Selected: {}".format(value)

    return app.server


if __name__ == "__main__":
    app.run_server(debug=True, port=8050, host="0.0.0.0")

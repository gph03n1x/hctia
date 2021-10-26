import pandas as pd
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State

from hctia.app import app
from hctia.connection import execute_at_remote_host
from hctia.hosts import read_ssh_config
from hctia.settings import DISPLAY_COLUMNS, EXCLUDED_HOSTS, SSH_CONFIG

host_list = read_ssh_config(SSH_CONFIG, excluded_hosts=EXCLUDED_HOSTS)
dataframe = pd.DataFrame(host_list)

layout = html.Div(
    [
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Textarea(id="bash-commands"),
                    ],
                    className="field",
                ),
                html.Div(
                    children=[
                        html.Button(
                            "Execute @ VMs",
                            id="execute-at-vms",
                            className="ui button info",
                            n_clicks=0,
                        )
                    ],
                    className="field",
                ),
            ],
            className="ui form",
        ),
        html.Hr(),
        html.Div(
            children=[
                html.Div(
                    html.Div(
                        children=[
                            html.Div(
                                children=[],
                                className="ui fluid vertical steps",
                                id="progress-commands",
                            ),
                            html.Div(
                                children=[],
                                className="ui fluid vertical steps",
                                id="final-commands",
                            ),
                        ],
                        className="ui segment box",
                    ),
                    className="column",
                ),
                html.Div(
                    children=[
                        html.Div(
                            dash_table.DataTable(
                                id="hosts-table",
                                columns=[
                                    {"name": column, "id": column}
                                    for column in dataframe.columns
                                    if column in DISPLAY_COLUMNS
                                ],
                                data=dataframe.to_dict("records"),
                                filter_action="native",
                                row_selectable="multi",
                                style_cell={"textAlign": "left"},
                            ),
                            className="ui segment box",
                        ),
                    ],
                    className="column",
                ),
            ],
            className="ui two column grid",
        ),
    ]
)


@app.long_callback(
    Output("final-commands", "children"),
    Input("execute-at-vms", "n_clicks"),
    State("bash-commands", "value"),
    State("hosts-table", "selected_rows"),
    prevent_initial_call=True,
    running=[
        (Output("execute-at-vms", "disabled"), True, False),
        (
            Output("progress-commands", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"},
        ),
        (
            Output("final-commands", "style"),
            {"visibility": "hidden"},
            {"visibility": "visible"},
        ),
    ],
    progress=Output("progress-commands", "children"),
    interval=1000,
)
def handle_button(set_progress, _add_button, ssh_value, selected_hosts):
    statuses = []
    if selected_hosts and ssh_value:
        selected_host_list = dataframe.iloc[selected_hosts].to_dict("records")
        for host in selected_host_list:
            statuses.append(execute_at_remote_host(host, ssh_value))
            set_progress(statuses)
    return statuses

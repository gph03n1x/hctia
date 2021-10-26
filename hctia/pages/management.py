import dash
import pandas as pd
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output, State

from hctia.app import app
from hctia.connection import add_to_remote_host, rm_from_remote_host
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
                        html.Div(
                            children=[
                                html.I(className="certificate icon"),
                                dcc.Input(
                                    id="ssh-public",
                                    placeholder="ssh-rsa rsa/yaba/daba/dou= email@example.com",
                                ),
                            ],
                            className="ui left icon input",
                        ),
                    ],
                    className="item",
                    style={"flex-grow": "1"},
                ),
                html.Div(
                    children=[
                        html.Button(
                            "Add to VMs",
                            id="add-to-vms",
                            className="ui button positive",
                            n_clicks=0,
                        )
                    ],
                    className="item",
                ),
                html.Div(
                    children=[
                        html.Button(
                            "Remove from VMs",
                            id="rm-from-vms",
                            className="ui button negative",
                            n_clicks=0,
                        )
                    ],
                    className="item",
                ),
            ],
            className="ui menu",
        ),
        html.Div(
            children=[
                html.Div(
                    html.Div(
                        children=[
                            html.Div(
                                children=[],
                                className="ui fluid vertical steps",
                                id="progress-logs",
                            ),
                            html.Div(
                                children=[],
                                className="ui fluid vertical steps",
                                id="final-logs",
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
    Output("final-logs", "children"),
    Input("add-to-vms", "n_clicks"),
    Input("rm-from-vms", "n_clicks"),
    State("ssh-public", "value"),
    State("hosts-table", "selected_rows"),
    prevent_initial_call=True,
    running=[
        (Output("add-to-vms", "disabled"), True, False),
        (Output("rm-from-vms", "disabled"), True, False),
        (
            Output("progress-logs", "style"),
            {"visibility": "visible"},
            {"visibility": "hidden"},
        ),
        (
            Output("final-logs", "style"),
            {"visibility": "hidden"},
            {"visibility": "visible"},
        ),
    ],
    progress=Output("progress-logs", "children"),
    interval=1000,
)
def handle_button(set_progress, _add_button, _rm_button, ssh_value, selected_hosts):
    changed_id = [p["prop_id"] for p in dash.callback_context.triggered][0]
    statuses = []
    action = add_to_remote_host if "add-to-vms" in changed_id else rm_from_remote_host

    if selected_hosts and ssh_value:
        selected_host_list = dataframe.iloc[selected_hosts].to_dict("records")
        for host in selected_host_list:
            statuses.append(action(host, ssh_value))
            set_progress(statuses)

    return statuses

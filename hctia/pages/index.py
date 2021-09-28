from dash import dash_table, dcc, html

from hctia.settings import DISPLAY_COLUMNS


def construct_index_layout(dataframe):
    return html.Div(
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

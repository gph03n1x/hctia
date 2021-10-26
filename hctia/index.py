from dash import dcc, html
from dash.dependencies import Input, Output

from hctia.app import app
from hctia.pages import execution, management
from hctia.utils import generate_menu_classes

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            children=[
                dcc.Link(
                    children=[html.I(className="lock icon"), "Key management"],
                    href="/",
                    className="item",
                    id="menu-link-0",
                ),
                dcc.Link(
                    children=[
                        html.I(className="terminal icon"),
                        "Multiple command execution",
                    ],
                    href="/execute",
                    className="item",
                    id="menu-link-1",
                ),
            ],
            className="ui menu",
        ),
        html.Div(id="page-content"),
    ]
)


@app.callback(
    Output("page-content", "children"),
    Output("menu-link-0", "className"),
    Output("menu-link-1", "className"),
    Input("url", "pathname"),
)
def display_page(pathname):
    mapping = {"/": management.layout, "/execute": execution.layout}
    total = len(mapping.keys())
    for index, path in enumerate(mapping):
        if pathname == path:
            return mapping[path], *generate_menu_classes(index, total)
    else:
        return "404", *generate_menu_classes(-1, total)


if __name__ == "__main__":
    app.run_server(debug=True)

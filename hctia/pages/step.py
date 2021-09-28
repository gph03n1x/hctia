from dash import html


def construct_step(host, status, icon, color=""):
    return html.Div(
        children=[
            html.I(className=f"{icon} icon"),
            html.Div(
                children=[
                    html.Div(host, className=f"ui {color} title header"),
                    html.Div(status, className="description"),
                ],
                className="content",
            ),
        ],
        className="step",
    )

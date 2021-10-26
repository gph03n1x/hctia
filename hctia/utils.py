from dash import html


def generate_step_message(host, status, icon, color=""):
    return html.Div(
        children=[
            html.I(className=f"{icon} icon"),
            html.Div(
                children=[
                    html.Div(host, className=f"ui {color} title header"),
                    html.Div(children=status, className="description"),
                ],
                className="content",
            ),
        ],
        className="step",
    )


def generate_menu_classes(active, total):
    return ["active item" if index == active else "item" for index in range(total)]

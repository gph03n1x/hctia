import dash
import diskcache
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.long_callback import DiskcacheLongCallbackManager

from hctia.connection import add_to_remote_host, rm_from_remote_host
from hctia.hosts import read_ssh_config
from hctia.pages.index import construct_index_layout
from hctia.settings import EXCLUDED_HOSTS, SSH_CONFIG

host_list = read_ssh_config(SSH_CONFIG, excluded_hosts=EXCLUDED_HOSTS)

cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)

dataframe = pd.DataFrame(host_list)

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    {
        "href": "https://cdn.jsdelivr.net/npm/semantic-ui@2.4.2/dist/semantic.min.css",
        "rel": "stylesheet",
    },
]
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
    long_callback_manager=long_callback_manager,
)
app.title = "HCTIA"
server = app.server

app.layout = construct_index_layout(dataframe)


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


if __name__ == "__main__":
    app.run_server(debug=True)

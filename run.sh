#!/bin/bash

python -c "import time, webbrowser;time.sleep(2);webbrowser.open_new_tab('http://127.0.0.1:8050')" &
gunicorn hctia.index:server --bind 127.0.0.1:8050

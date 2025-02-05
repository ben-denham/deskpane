"""
Based on:

* https://github.com/r0x0r/pywebview/blob/master/examples/flask_app/src/backend/server.py
* https://panel.holoviz.org/how_to/integrations/FastAPI_Tornado.html
"""
import os
from pathlib import Path
import sys

from bokeh.embed import server_document
from flask import Flask, render_template
import panel as pn
import webview

from app import build_app

base_dir = Path('.')
if hasattr(sys, '_MEIPASS'):
    base_dir = Path(sys._MEIPASS)
server = Flask(__name__, template_folder=base_dir / 'templates')
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # disable caching


@server.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


def main():
    panel_port = webview.http._get_random_port()
    webview_port = webview.http._get_random_port()

    panel_server = pn.serve(
        {'/app': build_app},
        port=panel_port,
        allow_websocket_origin=[f'127.0.0.1:{webview_port}'],
        address='127.0.0.1',
        show=False,
        threaded=True,
    )

    @server.route('/')
    def landing():
        script = server_document(f'http://127.0.0.1:{panel_port}/app')
        return render_template('embed.html', script=script, template='Flask')

    try:
        webview.create_window(
            'Deskpane',
            server,
            http_port=webview_port,
        )
        webview.start(
            # TODO: Could we enable ssl for both the webview and panel app?
            ssl=False,
            # Use debug flag to open devtools
            debug=False,
            gui='qt',
        )
    finally:
        panel_server.stop()


if __name__ == '__main__':
    main()

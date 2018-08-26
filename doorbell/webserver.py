import os
from os.path import dirname, abspath

from flask import (
    Flask,
    render_template
)
from flask import jsonify

# Create the application instance
web = Flask(__name__, root_path=os.path.join(dirname(dirname(abspath(__file__))), "web"))


# Create a URL route in our application for "/"
@web.route('/')
def home():
    return render_template('index.html')


@web.route('/api/config.json')
def summary():
    d = dict(some='thing')
    return jsonify(d)


class WebServer:

    @staticmethod
    def run():
        web.run(debug=False)
        return web

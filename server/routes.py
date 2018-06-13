import os
import flask
from server import app


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
        return flask.send_from_directory(app.static_folder, path)
    else:
        return flask.send_from_directory(app.static_folder, 'index.html')


@app.route('/api')
def api():
    return flask.jsonify({'message': 'hello'})

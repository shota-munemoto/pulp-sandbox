import os
import sys
import tornado.wsgi
import flask
import flask_sqlalchemy
import scheduling
import utils

if utils.frozen():
    static_folder = os.path.join(sys._MEIPASS, 'static/build')
else:
    static_folder = 'static/build'
app = flask.Flask(__name__, static_folder=static_folder)

db_path = os.path.join(os.getcwd(), 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    if path != '' and os.path.exists(os.path.join('static/build', path)):
        return flask.send_from_directory('static/build', path)
    else:
        return flask.send_from_directory('static/build', 'index.html')


@app.route('/api')
def api():
    return flask.jsonify({'message': 'hello'})


def run(host, port):
    db.create_all()
    container = tornado.wsgi.WSGIContainer(app)
    http_server = tornado.httpserver.HTTPServer(container)
    http_server.listen(port, address=host)
    tornado.ioloop.IOLoop.current().start()

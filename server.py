import scheduling
import flask

app = flask.Flask(__name__)


@app.route('/')
def index():
    url = flask.url_for('schedule')
    return f'<a href="{url}">勤務表を作成する。</a>'


@app.route('/schedule')
def schedule():
    if scheduling.solve():
        return '<p>勤務表を作成しscheduling.txtに出力しました。</p>'
    else:
        return '<p>勤務表を作成できませんでした。</p>'


def run(host, port):
    app.run(host=host, port=port)

from base64 import encodebytes as eb, decodebytes as db
from sqlite3 import connect
import os

from base62 import encode as enc, decode as dec
from flask import *

app = Flask(__name__)
os.chdir("/Users/della/url_sht")


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/statics/<filename>', methods=['GET'])
def statics(filename):
    try:
        return open("./statics/{}".format(filename)).read()
    except FileNotFoundError:
        return abort(404)

@app.route('/gen', methods=['POST'])
def gen():
    co = connect("DB.sqlite")
    c = co.cursor()
    data = request.form
    try:
        x = data['crypting']
    except KeyError:
        return {'errorCode': '1', 'errMSG': 'No way!'}
    c.execute("SELECT * FROM urls;")
    a = c.fetchall()
    sur = -1
    for x in a:
        if x[1] == data['toshorten']:
            sur = x[0]
    if sur == -1:
        sur = len(a)
        c.execute("INSERT INTO urls VALUES({}, '{}')".format(str(sur), data['toshorten']))
        co.commit()
    sur = 'http://localhost/sur/' + eb(enc(sur).encode()).decode()
    return {'data': sur, 'errorCode': '0', 'errMSG': ''}


@app.route('/sur/<b64>', methods=['GET'])
def gonow(b64):
    try:
        l = db(b64.encode())
        l = dec(l.decode())
    except:
        return redirect("http://localhost", code=301)
    co = connect("DB.sqlite")
    c = co.cursor()
    c.execute("SELECT * FROM urls")
    x = c.fetchall()
    n = False
    for y in x:
        if y[0] == l:
            n = y[1]
    if not n:
        return abort(404)
    return redirect(n, code=301)

@app.errorhandler(404)
def notfound(x):
    return render_template('err404.html'), 404

@app.errorhandler(500)
def internalerror(x):
    return render_template('err500.html'), 500

if __name__ == '__main__':
    app.run(port=80)

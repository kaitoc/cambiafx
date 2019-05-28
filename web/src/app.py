from flask import Flask, jsonify
from lib.parser import parseBloomberg, parseInvesting, parseCuantodolar

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Flask Dockerized'


@app.route('/bloomberg')
def bloomberg():
    res = parseBloomberg()
    return jsonify(res)


@app.route('/investing')
def investing():
    res = parseInvesting()
    return jsonify(res)


@app.route('/cuantodolar')
def cuantodolar():
    res = parseCuantodolar()
    print(res)
    print(type(res))
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

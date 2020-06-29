from flask import Flask, request
from .blockchain import getHead, getBlockchain
from datetime import datetime

app = Flask(__name__)


@app.route('/timestamp', methods=['GET'])
def timestamp():
    time = getHead()['header']['timestamp']
    return datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')


@app.route('/head', methods=['GET'])
def head():
    return getHead()


@app.route('/transfer', methods=['POST'])
def transfer():
    src = request.form['from']
    dst = request.form['to']
    amount = request.form['amount']
    print(src, dst, amount)
    return 'success!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)

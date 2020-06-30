from flask import Flask, request, g
from .blockchain import getHead, getBlockchain
from datetime import datetime
from .transaction import Transaction, transfer
from .mempool import insertToMempool
from .broadcast import broadcastTx
import asyncio

app = Flask(__name__)

def run(loop):
    with app.app_context():
        g.main_thread_loop = loop
        app.run(host='0.0.0.0', port=1337, debug=False)

@app.route('/timestamp', methods=['GET'])
def timestamp():
    time = getHead()['header']['timestamp']
    return datetime.utcfromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')


@app.route('/head', methods=['GET'])
def head():
    return getHead()


@app.route('/transfer', methods=['POST'])
def makeTransfer():
    src = request.form['from']
    dst = request.form['to']
    amount = request.form['amount']

    tx = transfer(src, dst, amount)
    insertToMempool(tx)

    # with app.app_context():
    #     loop = g.main_thread_loop
    #     asyncio.run_coroutine_threadsafe(broadcastTx(tx), loop=loop)

    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1337)

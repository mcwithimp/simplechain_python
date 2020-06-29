from argparse import ArgumentParser
from flask import Flask
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


@app.route('/head/header', methods=['GET'])
def headHeader():
    return getHead()['header']

# parser = ArgumentParser()
# parser.add_argument(
#     '-p',
#     '--port',
#     default=1337,
#     type=int,
#     help='port to listen on')
# args = parser.parse_args()
# port = args.port

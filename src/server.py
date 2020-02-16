
import hashlib
import json
import sys
import getopt

from textwrap import dedent
from time import time
from uuid import uuid4

from zero_chain import ZeroChain

from flask import Flask, jsonify, request

app = Flask(__name__)

identifier = str(uuid4()).replace('-', '')

# The instance of the ZeroChain, which contains the main chain logic
zeroChain = ZeroChain()


@app.route('/mine', methods=['GET'])
def mine():
    response = {
        'height': zeroChain.block_height,
        'block' : zeroChain.create_block().to_json()
    }
    return jsonify(response), 200


@app.route('/create_transaction', methods=['POST'])
def create_transaction():
    return "We'll add a new transaction"


@app.route('/status', methods=['GET'])
def full_chain():
    response = {
        'block height': zeroChain.block_height,
        'blocks': [h.to_json() for h in zeroChain.block_headers],
    }
    return jsonify(response), 200


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hp:",["port="])
    except getopt.GetoptError:
        print("server.py -p <port_number>")
        sys.exit(2)

    p = 9000  # default port number 9000
    for opt, arg in opts:
        if opt == '-h':
            print("server.py -p <port_number>")
            sys.exit()
        elif opt in ("-p", "--port"):
            p = int(arg)
    # start the application
    app.run(host='0.0.0.0', port=p)


if __name__ == '__main__':
    main(sys.argv[1:])

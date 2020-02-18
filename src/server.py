
import sys
import getopt
from flask import Flask, jsonify, request, redirect, url_for, render_template

from src.zero_chain import ZeroChain


app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


# The instance of the ZeroChain, which contains the main chain logic
zeroChain = ZeroChain()

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))


@app.route("/")
def index():
    return render_template("index.html", request=request)


@app.route("/mine", methods=["GET"])
def mine():
    response = {
        "block_header" : zeroChain.create_block().to_json()
    }
    return jsonify(response), 200


@app.route("/create_transaction", methods=["POST"])
def create_transaction():
    sender = request.form["sender"]
    receiver = request.form["receiver"]
    amount = str(request.form["amount"])
    txn = zeroChain.transfer(sender, receiver, amount)
    return jsonify(txn.to_json()), 200


@app.route("/register_node", methods=["POST"])
def register_node():
    node = request.form["node"]
    txn = zeroChain.nodes.add(node)
    return "Node added: " + node


@app.route("/status", methods=["GET"])
def status():
    response = {
        "block_height": zeroChain.block_height,
        "block_headers": [h.to_json() for h in zeroChain.block_headers],
        "pending_transactions": [t.to_json() for t in zeroChain.new_transactions],
        "nodes": [n for n in zeroChain.nodes],
    }
    return jsonify(response), 200


@app.route("/fullnode", methods=["GET"])
def fullnode():
    response = {
        "block_height": zeroChain.block_height,
        "block_headers": [h.to_json() for h in zeroChain.block_headers],
        "transactions": [[t.to_json() for t in ts] for ts in zeroChain.transactions],
        "nodes": [n for n in zeroChain.nodes],
    }
    return jsonify(response), 200


@app.route("/sync", methods=["GET"])
def sync():
    if zeroChain.sync():
        return "This node has been replaced!"
    else :
        return "This node is already the longest one in the network."


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hp:",["port="])
    except getopt.GetoptError:
        print("server.py -p <port_number>")
        sys.exit(2)

    p = 8900  # default port number 8900
    for opt, arg in opts:
        if opt == "-h":
            print("server.py -p <port_number>")
            sys.exit()
        elif opt in ("-p", "--port"):
            p = int(arg)
    # start the application
    app.run(host="127.0.0.1", port=p)


if __name__ == "__main__":
    main(sys.argv[1:])

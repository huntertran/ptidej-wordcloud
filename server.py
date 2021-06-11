from flask import Flask
from flask import jsonify
from auto_runner import crawl
from twisted.internet import reactor, defer

# $ export FLASK_APP=server
# $ flask run

app = Flask(__name__)

@app.route("/")
def set_input():
    return jsonify("Hello, World!")

@app.route("/run")
def run_crawler():
    crawl("./data/sitelist.json")
    return reactor.run()
    # return jsonify("running")
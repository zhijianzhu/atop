# Ref: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04

import datetime

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

import sqlite3
from flask import g
#import pandas as pd

from flask_basicauth import BasicAuth

#import sys
#sys.path.append('../')

#from elasticsearch import Elasticsearch
#es = Elasticsearch('localhost', port=9200)


app = Flask(__name__)


@app.route("/")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')

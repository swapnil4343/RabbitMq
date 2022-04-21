from flask import Flask, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
import flask
import json

app = Flask(__name__)

mongo = MongoClient('localhost', 27017)
db = mongo.msgqueuedb


@app.route("/")
def home():
    qinfo = db.msgqueue.find()
    return render_template('index.html', qinfo=qinfo)


# @app.route('/')
# def index():
#    return render_template("index.html")

@app.route('/<name>')
def index1(name):
    return "hello " + name


if __name__ == "__main__":
    app.run(debug=True)

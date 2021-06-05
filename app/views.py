from flask import render_template, jsonify, request
from . import app
import app.grandpy_bot as gpy


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def ajax():
    text = request.form["question"]
    return(gpy.answer(text))

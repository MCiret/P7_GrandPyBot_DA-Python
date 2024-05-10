from flask import render_template, request
from . import app
import app.grandpy_bot as gpy

import logging
import os


@app.route("/")
def home():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(os.environ)
    return render_template("index.html")


@app.route("/", methods=["POST"])
def ajax():
    text = request.form["question"]
    return(gpy.answer(text))

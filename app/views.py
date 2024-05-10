from flask import render_template, request
from . import app
import app.grandpy_bot as gpy


@app.route("/")
def home():
    print(">>>>>>>>>> PRINT in home() view <<<<<<<<<<")
    return render_template("index.html")


@app.route("/", methods=["POST"])
def ajax():
    print(">>>>>>>>>> PRINT in ajax() view <<<<<<<<<<")
    text = request.form["question"]
    return(gpy.answer(text))

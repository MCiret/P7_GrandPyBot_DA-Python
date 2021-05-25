from flask import render_template, jsonify, request
from . import app

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def ajax():
    text = request.form["question"]
    print(text)
    text_dict = {"text": text}
    return jsonify(text_dict)

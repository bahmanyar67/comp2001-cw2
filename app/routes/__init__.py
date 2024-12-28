from flask import render_template


def home():
    return render_template("index.html")


def health():
    return {"message": "The server is working!"}, 200

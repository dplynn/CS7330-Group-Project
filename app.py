from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/hello/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/')
def index():
    return render_template('home.html')
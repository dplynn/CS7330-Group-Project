from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add-post')
def add_post():
    return render_template('add_post.html')

if __name__ == '__main__':
    app.run(debug=True)
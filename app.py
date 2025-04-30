from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add-post')
def add_post():
    return render_template('add_post.html')

@app.route('/add-project')
def add_project():
    return render_template('add_project.html')

if __name__ == '__main__':
    app.run(debug=True)
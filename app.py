from flask import Flask, render_template, request, redirect, url_for, flash
import DBInit
import DBInteract
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    # if request.method == 'POST':
    #     user = {
    #         'username': request.form['username'],
    #         'social_media': request.form['social_media'],
    #         'first_name': request.form['first_name'],
    #         'last_name': request.form['last_name'],
    #         'country_birth': request.form['country_birth'],
    #         'country_residence': request.form['country_residence'],
    #         'age': int(request.form['age']),
    #         'gender': request.form['gender'],
    #         'verified': request.form['verified'] == 'True'
    #     }

    #     connection = DBInit.connect_to_database()
    #     try:
    #         DBInteract.insert_user(connection, user)
    #         connection.commit()
    #         flash('User added successfully!', 'success')
    #     except Exception as e:
    #         connection.rollback()
    #         flash(f"Error: {e}", 'danger')
    #     finally:
    #         connection.close()
    #     return redirect(url_for('add_users'))

    return render_template('add_user.html')

@app.route('/add-post')
def add_post():
    return render_template('add_post.html')

@app.route('/add-project')
def add_project():
    return render_template('add_project.html')

@app.route('/add-post-to-project')
def add_ptp():
    return render_template('add_ptp.html')

@app.route('/add-result')
def add_result():
    return render_template('add_result.html')

@app.route('/add-result2')
def add_result2():
    return render_template('add_result2.html')

if __name__ == '__main__':
    try:
        connection = DBInit.connect_to_database()  # Connect to the database using pymysql
        DBInit.drop_tables(connection)  # Drop existing tables in the database
        DBInit.create_tables(connection)  # Create tables in the database
        print("Database setup completed.\n")
    except Exception as e:
        print(f"Error during database setup: {e}\n")

    app.run(debug=True)
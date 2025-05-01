from flask import Flask, render_template, request, redirect, url_for, flash
import DBInit
import DBInteract
import pymysql

app = Flask(__name__)
app.secret_key = 'bonita123'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        print("Form data received:", request.form)

        user = [
            request.form['username'],
            request.form['social_media'],
            request.form['first_name'],
            request.form['last_name'],
            request.form['country_birth'],
            request.form['country_residence'],
            int(request.form['age']),
            request.form['gender'],
            request.form['verified'] == 'yes'  # Convert 'yes'/'no' to boolean
        ]

        connection = DBInit.connect_to_database()
        try:
            DBInteract.insert_user(connection, user)
            connection.commit()
            flash('User added successfully!\n', 'success')
        except Exception as e:
            connection.rollback()
            flash(f"Error: {e}", 'danger')
        finally:
            connection.close()
        return redirect(url_for('add_user'))

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
        connection = DBInit.connect_to_database()
        if connection:
            DBInit.drop_tables(connection)
            DBInit.create_tables(connection)
            print("Database setup completed.\n")
            connection.close()
        else:
            print("Could not establish database connection.\n")
    except Exception as e:
        print(f"Error during database setup: {e}\n")

    app.run(debug=True)
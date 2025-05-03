from flask import Flask, render_template, request, redirect, url_for, flash, session
import DBInit
import DBInteract
from datetime import datetime
import pandas as pd

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

@app.route('/add-post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        print("Form data received:", request.form)

        post = {
            'username': request.form['username'],
            'social_media': request.form['social_media'],
            'time_posted': datetime.strptime(request.form['time_posted'], '%Y-%m-%dT%H:%M'),
            'text': request.form['text'],
            'city': request.form['city'],
            'state': request.form['state'],
            'country': request.form['country'],
            'num_likes': int(request.form['num_likes']),
            'num_dislikes': int(request.form['num_dislikes']),
            'multimedia': request.form['multimedia'] == 'yes',
            'is_repost': request.form['is_repost'] == 'yes'
        }

        if request.form['is_repost'] == 'yes':
            session['repost_data'] = post
            return redirect(url_for('add_post2'))
        print("Post data: " + str(post))
        post_list = list(post.values()) + [None, None, pd.NaT]
        print("Post List: " + str(post_list))  
        print(post_list)

        connection = DBInit.connect_to_database()

        try:
            DBInteract.insert_post(connection, post_list)
            connection.commit()
            flash('Post added successfully!\n', 'success')
        except Exception as e:
            connection.rollback()
            flash(f"Error: {e}", 'danger')
        finally:
            connection.close()
        
        return redirect(url_for('add_post'))

    return render_template('add_post.html')

@app.route('/add-post-original', methods=['GET', 'POST'])
def add_post2():
    post = session.get('repost_data')
    print("Form data received:", request.form)

    if request.method == 'POST':
        post['orig_user'] = request.form['orig_user']
        post['orig_platform'] = request.form['orig_platform']
        post['orig_time'] = datetime.strptime(request.form['orig_time'], '%Y-%m-%dT%H:%M')
        post_list = [
            post['username'],
            post['social_media'],
            post['time_posted'],
            post['text'],
            post['city'],
            post['state'],
            post['country'],
            post['num_likes'],
            post['num_dislikes'],
            post['multimedia'],
            post['is_repost'],
            post['orig_user'], 
            post['orig_platform'], 
            post['orig_time'] 
        ]

        print("Post + Repost Data: " + str(post_list))

        connection = DBInit.connect_to_database()

        try:
            DBInteract.insert_post(connection, post_list)
            connection.commit()
            flash('Post added successfully!\n', 'success')
        except Exception as e:
            connection.rollback()
            flash(f"Error: {e}", 'danger')
        finally:
            connection.close()

        return redirect(url_for('add_post'))
    
    return render_template('add_post2.html')

@app.route('/add-project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        print("Form data received:", request.form)

        project = [
            request.form['project_name'],
            request.form['manager'],
            request.form['institute'],
            ','.join(request.form.getlist('field_name[]')),
            datetime.strptime(request.form['start'], '%Y-%m-%d'),
            datetime.strptime(request.form['end'], '%Y-%m-%d')
        ]

        connection = DBInit.connect_to_database()
        try:
            DBInteract.insert_project(connection, project)
            connection.commit()
            flash('Project added successfully!\n', 'success')
        except Exception as e:
            connection.rollback()
            flash(f"Error: {e}", 'danger')
        finally:
            connection.close()
        return redirect(url_for('add_project'))

    return render_template('add_project.html')

@app.route('/add-post-to-project', methods=['GET', 'POST'])
def add_ptp():
    if request.method == 'POST':
        print("Form data received:", request.form)

        data = [
            request.form['project_name'],
            request.form['username'],
            request.form['social_media'],
            datetime.strptime(request.form['time_posted'], '%Y-%m-%dT%H:%M')
        ]

        connection = DBInit.connect_to_database()
        try:
            DBInteract.insert_post_no_data(connection, data)
            connection.commit()
            flash('Post added to project successfully!\n', 'success')
        except Exception as e:
            connection.rollback()
            flash(f"Error: {e}", 'danger')
        finally:
            connection.close()
        return redirect(url_for('add_ptp'))
    return render_template('add_ptp.html')

@app.route('/add-result', methods=['GET', 'POST'])
def add_result():
    if request.method == 'POST':
        session.pop('repost_data', None)
        session['project_data'] = {'project_name': request.form['project_name']}
        
        return redirect(url_for('add_result2'))

    return render_template('add_result.html')

@app.route('/add-result2', methods=['GET', 'POST'])
def add_result2():
    project_data = session.get('project_data')
    print("Session data in add_result2:", session)
    print("Form data received:", request.form)

    if request.method == 'POST':
        result = [
            project_data['project_name'],
            request.form['username'],
            request.form['media_platform'],
            datetime.strptime(request.form['time_posted'], '%Y-%m-%dT%H:%M'),
            request.form['field'],
            request.form['result']
        ]

        print("Result data: " + str(result))

        connection = DBInit.connect_to_database()

        try:
            DBInteract.insert_field_values(connection, result)
            connection.commit()
            flash('Result added successfully!\n', 'success')
        except Exception as e:
            connection.rollback()
            flash(f"Error: {e}", 'danger')
        finally:
            connection.close()

        return redirect(url_for('add_result'))
    
    return render_template('add_result2.html')

@app.route('/query-posts', methods=['GET', 'POST'])
def query_posts():
    return render_template('query_posts.html')

@app.route('/query-posts-results.html', methods=['GET', 'POST'])
def query_posts_results():
    connection = DBInit.connect_to_database()

    try:
        results = DBInteract.fetch_posts_all4(connection, request.args.get('social_media'),
                                    datetime.strptime(request.args.get('start_time'), '%Y-%m-%dT%H:%M'),
                                    datetime.strptime(request.args.get('end_time'), '%Y-%m-%dT%H:%M'),
                                    request.args.get('username'), request.args.get('first_name'), 
                                    request.args.get('last_name'))
        print(str(results))

    except Exception as e:
        connection.rollback()
        flash(f"Error: {e}", 'danger')
        return redirect(url_for('query_posts'))
    finally:
        connection.close()

    return render_template('query_posts_results.html', results=results)

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
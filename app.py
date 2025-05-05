from flask import Flask, render_template, request, redirect, url_for, flash, session
import DBInit
import DBInteract
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv

app = Flask(__name__)

# set secret key from env variable
load_dotenv()
app.secret_key = os.environ.get('SECRET_KEY')
if not app.secret_key:
    raise ValueError("No secret key set for Flask application!")

# homepage
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        print("Form data received:", request.form) # for debugging

        # format form data into list for insert_user()
        try:
            age = int(request.form['age'])
        except ValueError:
            age = 0

        try:
            gender = request.form['gender']
        except KeyError:
            gender = "NA"

        try:
            verified = request.form['verified'] == 'yes'  # convert 'yes'/'no' to boolean
        except KeyError:
            verified = False

        user = [
            request.form['username'],
            request.form['social_media'],
            request.form['first_name'],
            request.form['last_name'],
            request.form['country_birth'],
            request.form['country_residence'],
            age,
            gender,
            verified
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
        print("Form data received:", request.form) # for debugging

        # format form data into dictionary
        try:
            num_likes = int(request.form['num_likes'])
        except (ValueError, KeyError):
            num_likes = 0

        try:
            num_dislikes = int(request.form['num_dislikes'])
        except (ValueError, KeyError):
            num_dislikes = 0

        try:
            multimedia = request.form['multimedia'] == 'yes'
        except KeyError:
            multimedia = bool(0)
        from datetime import datetime

        try:
            time_posted = datetime.strptime(request.form['time_posted'], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            # Append ":00" if seconds are missing and try again
            time_str = request.form['time_posted']
            if len(time_str) == 16:  # Format is '%Y-%m-%dT%H:%M'
                time_str += ':00'
            time_posted = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')

        post = {
            'username': request.form['username'],
            'social_media': request.form['social_media'],
            'time_posted': time_posted,
            'text': request.form['text'],
            'city': request.form['city'],
            'state': request.form['state'],
            'country': request.form['country'],
            'num_likes': num_likes,
            'num_dislikes': num_dislikes,
            'multimedia': multimedia,
            'is_repost': request.form['is_repost'] == 'yes'
        }

        # if repost, pass form data to add-post-original page
        if request.form['is_repost'] == 'yes':
            session['repost_data'] = post
            return redirect(url_for('add_post2'))
        
        # if not repost, make into list for insert_post() and add null values to repost columns
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
        
        try:
            post['orig_time'] = datetime.strptime(request.form['orig_time'], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            # Append ":00" if seconds are missing and try again
            time_str = request.form['orig_time']
            if len(time_str) == 16:  # Format is '%Y-%m-%dT%H:%M'
                time_str += ':00'
            post['orig_time'] = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        
        # add original post data to dictionary
        post['orig_user'] = request.form['orig_user']
        post['orig_platform'] = request.form['orig_platform']
        #post['orig_time'] = datetime.strptime(request.form['orig_time'], '%Y-%m-%dT%H:%M:%S')

        # format data into list for insert_post()
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

        print("Post + Repost Data: " + str(post_list)) # for debug

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
        print("Form data received:", request.form) # for debug

        # format data into list for insert_project()
        project = [
            request.form['project_name'],
            request.form['manager'],
            request.form['institute'],

            # format fields to csv string
            ','.join(request.form.getlist('field_name[]')),

            # format to datetime
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
        print("Form data received:", request.form) # for debug

        try:
            time_posted = datetime.strptime(request.form['time_posted'], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            # Append ":00" if seconds are missing and try again
            time_str = request.form['time_posted']
            if len(time_str) == 16:  # Format is '%Y-%m-%dT%H:%M'
                time_str += ':00'
            time_posted = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
        
        # format into list for insert_post_no_data()
        data = [
            request.form['project_name'],
            request.form['username'],
            request.form['social_media'],
            time_posted
            #datetime.strptime(request.form['time_posted'], '%Y-%m-%dT%H:%M:%S')
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
        # save form data to session for passing to add-result2
        session.pop('repost_data', None)
        session['project_data'] = {'project_name': request.form['project_name']}
        
        return redirect(url_for('add_result2'))

    return render_template('add_result.html')

@app.route('/add-result2', methods=['GET', 'POST'])
def add_result2():
    project_data = session.get('project_data')

    # for debug
    print("Session data in add_result2:", str(session))
    print("Form data received:", str(request.form))
    
    if request.method == 'POST':

        try:
            time_posted = datetime.strptime(request.form['time_posted'], '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            # Append ":00" if seconds are missing and try again
            time_str = request.form['time_posted']
            if len(time_str) == 16:  # Format is '%Y-%m-%dT%H:%M'
                time_str += ':00'
            time_posted = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')

        # format into list for insert_field_values()
        result = [
            project_data['project_name'],
            request.form['username'],
            request.form['media_platform'],
            time_posted,
            #datetime.strptime(request.form['time_posted'], '%Y-%m-%dT%H:%M:%S'),
            request.form['field'],
            request.form['result']
        ]

        print("Result data: " + str(result)) # for debug

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

    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')

    start_time = None
    end_time = None

    # Parse start_time only if provided
    if start_time_str:
        try:
            start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            if len(start_time_str) == 16:  # e.g., no seconds
                start_time_str += ':00'
                start_time = datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')

    # Parse end_time only if provided
    if end_time_str:
        try:
            end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            if len(end_time_str) == 16:  # e.g., no seconds
                end_time_str += ':00'
                end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S')   

    try:
        results = DBInteract.fetch_posts_all4(connection, request.args.get('social_media'),
                                    start_time,
                                    #datetime.strptime(request.args.get('start_time'), '%Y-%m-%dT%H:%M:%S'),
                                    end_time,
                                    #datetime.strptime(request.args.get('end_time'), '%Y-%m-%dT%H:%M:%S'),
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

@app.route('/query-projects', methods=['GET', 'POST'])
def query_projects():
    return render_template('query_projects.html')

@app.route('/query-projects-results', methods=['GET', 'POST'])
def query_projects_results():
    connection = DBInit.connect_to_database()

    try:
        result1, result2 = DBInteract.fetch_posts_experiment(connection, request.args.get('project_name'))

        # format decimal values into %
        result2 = [(field, f"{float(percent):.0f}%") for field, percent in result2]

        # debug
        print(str(result1))
        print(str(result2))

    except Exception as e:
        connection.rollback()
        flash(f"Error: {e}", 'danger')
        return redirect(url_for('query_posts'))
    finally:
        connection.close()

    return render_template('query_projects_results.html', result1=result1, result2=result2)

# set up database on startup
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
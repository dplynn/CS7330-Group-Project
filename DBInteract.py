import pymysql
import csv
import pandas as pd
import datetime

# SHOULD PROBABLY ADD A TRY CATCH BLOCK FOR EVERY SQL FUNCTION JUST TO BE SAFE

def insert_user(connection, user_data): # Insert user data into the database
    #check if user exists
    if fetch_user(connection, user_data[0], user_data[1]) is not None:
        print("User already exists in the database.")
        return
    #check if user_data is valid
    if len(user_data) != 9:
        print("Invalid user data. Expected 9 fields.")
        return
    if not isinstance(user_data[0], str) or not isinstance(user_data[1], str):
        print("Invalid user data. Username and social media should be strings.")
        return
    if not isinstance(user_data[2], str) or not isinstance(user_data[3], str):
        print("Invalid user data. First name and last name should be strings.")
        return
    if not isinstance(user_data[4], str) or not isinstance(user_data[5], str):
        print("Invalid user data. Country of birth and country of residence should be strings.")
        return
    if not isinstance(user_data[6], int):
        print("Invalid user data. Age should be an integer.")
        return
    if user_data[6] < 0:
        print("Invalid user data. Age should be a positive integer.")
        return
    with connection.cursor() as cursor:
        insert_query = """
        INSERT INTO user (username,social_media,first_name,last_name,country_birth,country_residence,age,gender,verified)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, user_data)
    connection.commit()   
def insert_post(connection, post_data): # Insert post data into the database
    #username,social_media,time_posted,text,city,state,country,num_likes,num_dislikes,multimedia,is_repost,orig_user,orig_social_media,orig_time_posted,orig_text
    post_data = list(post_data) if isinstance(post_data, tuple) else post_data
    if fetch_post(connection, post_data[0], post_data[1], post_data[2]) is not None:
        print("Post already exists in the database.")
        return
    #check if post_data is valid
    if len(post_data) != 15:
        print("Invalid post data. Expected 15 fields.")
        return
    if not isinstance(post_data[0], str) or not isinstance(post_data[1], str):
        print("Invalid post data. Username and social media should be strings.")
        # print types for debugging
        print(f"Username type: {type(post_data[0])}, Social media type: {type(post_data[1])}")
        return
    if not isinstance(post_data[2], datetime.datetime):
        print("Invalid post data. Time posted should be a datetime object.")
        return
    if not isinstance(post_data[3], str):
        print("Invalid post data. Text should be a string.")
        return
    if not isinstance(post_data[4], str) or not isinstance(post_data[5], str) or not isinstance(post_data[6], str):
        print("Invalid post data. City, state, and country should be strings.")
        return
    if not isinstance(post_data[7], int) or not isinstance(post_data[8], int):
        print("Invalid post data. Number of likes and dislikes should be integers.")
        return
    if post_data[7] < 0 or post_data[8] < 0:
        print("Invalid post data. Number of likes and dislikes should be positive integers.")
        return
    if not isinstance(post_data[9], bool) or not isinstance(post_data[10], bool):
        print("Invalid post data. Multimedia and is repost should be boolean values.")
        return
    if post_data[10] and (post_data[11] is None or post_data[12] is None or post_data[14] is None):
        print("Invalid post data. Original user, social media, time posted, and text should not be None if is repost is True.")
        return
    if post_data[10] and (not isinstance(post_data[11], str) or not isinstance(post_data[12], str)):
        print("Invalid post data. Original user, social media, and text should be strings.")
        #types for debugging
        print(f"Original user type: {type(post_data[11])}, Original social media type: {type(post_data[12])}, Original text type: {type(post_data[14])}")
        return
    if not isinstance(post_data[13], datetime.datetime):
        print("Invalid post data. Original time posted should be a datetime object.")
        return
    #convert orig_user, orig_social_media, orig_time_posted, orig_text to null if is_repost is False
    if not post_data[10]:
        post_data[11] = None
        post_data[12] = None
        post_data[13] = None
        post_data[14] = None
    with connection.cursor() as cursor:
        insert_query = """
        INSERT INTO Post (username, social_media, time_posted, text, city, state, country, num_likes, num_dislikes, multimedia, is_repost, orig_user, orig_social_media, orig_time_posted, orig_text)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, post_data)
    connection.commit()
def insert_project(connection, project_data): # Insert projects into the database
    #project_name, project_manager, institute, start_date, end_date
    #check if project exists
    if fetch_project(connection, project_data[0]) is not None:
        print("Project already exists in the database.")
        return
    #check if project_data is valid
    if len(project_data) != 5:
        print("Invalid project data. Expected 5 fields.")
        return
    if not isinstance(project_data[0], str) or not isinstance(project_data[1], str):
        print("Invalid project data. Project name and project manager should be strings.")
        return
    if not isinstance(project_data[2], str):
        print("Invalid project data. Institute should be a string.")
        return
    if not isinstance(project_data[3], datetime.datetime) or not isinstance(project_data[4], datetime.datetime):
        print("Invalid project data. Start date and end date should be datetime objects.")
        return
    if project_data[3] > project_data[4]:
        print("Invalid project data. Start date should be before end date.")
        print(f"Start date: {project_data[3]}, End date: {project_data[4]}")
        return
    
    with connection.cursor() as cursor:
        insert_query = """
        INSERT INTO Project (project_name, project_manager, institute, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, project_data)
    connection.commit()
def insert_projectdata(connection, project_data): # Insert project data into the database
    #Labels: project_name,post_username,post_social_media,post_time_posted,field,result
    #check if projectdata exists
    if fetch_projectdata(connection, project_data[0], project_data[1], project_data[2], project_data[3]) is not None:
        print("ProjectData already exists in the database.")
        return
    #check if project_data is valid
    if len(project_data) != 6:
        print("Invalid project data. Expected 6 fields.")
        return
    if not isinstance(project_data[0], str) or not isinstance(project_data[1], str):
        print("Invalid project data. Project name and post username should be strings.")
        return
    if not isinstance(project_data[2], str):
        print("Invalid project data. Post social media should be a string.")
        return
    if not isinstance(project_data[3], datetime.datetime):
        print("Invalid project data. Post time posted should be a datetime object.")
        return
    if not isinstance(project_data[4], str):
        print("Invalid project data. Field should be a string.")
        return
    with connection.cursor() as cursor:
        insert_query = """
        INSERT INTO ProjectData (project_name, post_username, post_social_media, post_time_posted, field, result)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, project_data)
    connection.commit()

def fetch_user(connection, username, social_media): # Fetch user data from the database
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM user WHERE username = %s AND social_media = %s;
        """
        cursor.execute(select_query, (username, social_media))
        result = cursor.fetchone()
    return result

def fetch_post(connection, username, social_media, time_posted): # Fetch post data from the database
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Post WHERE username = %s AND social_media = %s AND time_posted = %s;
        """
        cursor.execute(select_query, (username, social_media, time_posted))
        result = cursor.fetchone()
    return result

def fetch_project(connection, project_name): # Fetch a project from the database
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Project WHERE project_name = %s;
        """
        cursor.execute(select_query, (project_name,))
        result = cursor.fetchone()
    return result

def fetch_projectdata(connection, project_name, post_username, post_social_media, post_time_posted): # Fetch project data from the database
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM ProjectData WHERE project_name = %s AND post_username = %s AND post_social_media = %s AND post_time_posted = %s;
        """
        cursor.execute(select_query, (project_name, post_username, post_social_media, post_time_posted))
        result = cursor.fetchone()
    return result

def fetch_all_users(connection): # Returns all users in the database
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM user;
        """
        cursor.execute(select_query)
        result = cursor.fetchall()
    return result

def fetch_all_posts(connection): # Returns all posts in the database
    result = []
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Post;
        """
        cursor.execute(select_query)
        result = cursor.fetchall()
    return result

def fetch_all_projects(connection): # Returns all projects in the database
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Project;
        """
        cursor.execute(select_query)
        result = cursor.fetchall()
    return result

def fetch_all_projectdata(connection): # Returns all project data in the database
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM ProjectData;
        """
        cursor.execute(select_query)
        result = cursor.fetchall()
    return result

#functions for the queries described in the project description pdf
#find posts of a social media type
def fetch_posts_socialmedia(connection, social_media):
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Post WHERE social_media = %s;
        """
        cursor.execute(select_query, (social_media,))
        result = cursor.fetchall()
    return result

#Find posts between a certain period of time
def fetch_posts_betweentime(connection, beginning_time, ending_time):
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Post WHERE time_posted > %s AND time_posted < %s;
        """
        cursor.execute(select_query, (beginning_time, ending_time)) # NEED TO ERROR HANDLE THIS FOR NOT CORRECT INPUTS
        result = cursor.fetchall()
    return result

#Find posts that is posted by a certain username of a certain media
def fetch_posts_user(connection, user, social_media):
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Post WHERE username = %s AND social_media = %s;
        """
        cursor.execute(select_query, (user, social_media))
        result = cursor.fetchall()
    return result

#Find posts that is posted by someone with a certain first/last name
def fetch_posts_twonames(connection, first_name, last_name):
    with connection.cursor() as cursor:
        select_query = """
        SELECT *
        FROM Post p, user u
        WHERE (p.username = u.username AND p.social_media = u.social_media)
        AND (u.first_name = %s AND u.last_name = %s);
        """
        cursor.execute(select_query, (first_name, last_name)) # NEED TO ERROR HANDLE THIS FOR NOT CORRECT INPUTS
        result = cursor.fetchall()
    return result

#Querying experiment: You should ask the user for the name of the experiment, and it should
#return the list of posts that is associated with the experiment, and for each post, any results that
#has been entered. Also you need to display for each field, the percentage of posts that contain a
#value of that field.

def fetch_posts_experiment(connection, project_name): #not sure for this one if we just need the primary key of the post, or the actual post text itself
    with connection.cursor() as cursor:
        select_query1 = """
        SELECT *
        FROM ProjectData
        WHERE project_name = %s;
        """
        cursor.execute(select_query1, (project_name,)) # NEED TO ERROR HANDLE THIS FOR NOT CORRECT INPUTS
        result1 = cursor.fetchall()

        select_query2 = """
        SELECT field, ROUND((SUM(CASE WHEN result IS NOT NULL AND result != 'None' THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) AS percentage_filled
        FROM ProjectData
        WHERE project_name = %s
        GROUP BY field;
        """
        cursor.execute(select_query2, (project_name,)) # NEED TO ERROR HANDLE THIS FOR NOT CORRECT INPUTS
        result2 = cursor.fetchall()
    return result1, result2
import pymysql
import csv
import pandas as pd
from datetime import datetime
import csv
from io import StringIO

# SHOULD PROBABLY ADD A TRY CATCH BLOCK FOR EVERY SQL FUNCTION JUST TO BE SAFE

def insert_user(connection, user_data): # Insert user data into the database

    #check if user_data is valid
    if len(user_data) != 9:
        raise ValueError("Invalid user data. Expected 9 fields.")
    if not isinstance(user_data[0], str) or not isinstance(user_data[1], str):
        raise TypeError("Invalid user data. Username and social media should be strings.")
    if not isinstance(user_data[2], str) or not isinstance(user_data[3], str):
        raise TypeError("Invalid user data. First name and last name should be strings.")
    if not isinstance(user_data[4], str) or not isinstance(user_data[5], str):
        raise TypeError("Invalid user data. Country of birth and country of residence should be strings.")
    if not isinstance(user_data[6], int):
        raise TypeError("Invalid user data. Age should be an integer.")
    if user_data[6] < 0:
        raise ValueError("Invalid user data. Age should be a positive integer.")
    
    #check if user exists
    if fetch_user(connection, user_data[0], user_data[1]) is not None:
        raise ValueError("User already exists in the database.")

    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO user (username,social_media,first_name,last_name,country_birth,country_residence,age,gender,verified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, user_data)
        connection.commit()  
    except pymysql.MySQLError as e:
        print(f"Error adding user to database: {e}")


def insert_post(connection, post_data): # Insert post data into the database
    #username,social_media,time_posted,text,city,state,country,num_likes,num_dislikes,multimedia,is_repost,orig_user,orig_social_media,orig_time_posted
    
    post_data = list(post_data) if isinstance(post_data, tuple) else post_data
    
    #check if post_data is valid
    if len(post_data) != 14:
        raise ValueError("Invalid post data. Expected 14 fields, got " + str(len(post_data)) + ".")
    if not isinstance(post_data[0], str) or not isinstance(post_data[1], str):
        # print types for debugging
        print(f"Username type: {type(post_data[0])}, Social media type: {type(post_data[1])}")
        raise TypeError("Invalid post data. Username and social media should be strings.")
    if not isinstance(post_data[2], datetime):
        raise TypeError("Invalid post data. Time posted should be a datetime object.")
    if not isinstance(post_data[3], str):
        raise TypeError("Invalid post data. Text should be a string.")
    if not isinstance(post_data[4], str) or not isinstance(post_data[5], str) or not isinstance(post_data[6], str):
        raise TypeError("Invalid post data. City, state, and country should be strings.")
    if not isinstance(post_data[7], int) or not isinstance(post_data[8], int):
        raise TypeError("Invalid post data. Number of likes and dislikes should be integers.")
    if post_data[7] < 0 or post_data[8] < 0:
        raise ValueError("Invalid post data. Number of likes and dislikes should be positive integers.")
    if not isinstance(post_data[9], bool) or not isinstance(post_data[10], bool):
        raise TypeError("Invalid post data. Multimedia and is repost should be boolean values.")
    if post_data[10] and (post_data[11] is None or post_data[12] is None):
        raise ValueError("Invalid post data. Original user, social media and time posted should not be None if is repost is True.")
    if post_data[10] and (not isinstance(post_data[11], str) or not isinstance(post_data[12], str)):
        #types for debugging
        print(f"Original user type: {type(post_data[11])}, Original social media type: {type(post_data[12])}")
        raise TypeError("Invalid post data. Original user and social media should be strings.")
    if not isinstance(post_data[13], datetime):
        raise TypeError("Invalid post data. Original time posted should be a datetime object.")
    
    # check if posts already exists
    if fetch_post(connection, post_data[0], post_data[1], post_data[2]) is not None:
        raise ValueError("Post already exists in the database.")
    
    # check if user already exist
    if fetch_user(connection, post_data[0], post_data[1]) is None:
        raise ValueError("User doesn't exist in the database.")
    
    # check if the orginal posts exists in case of repost
    if post_data[10]:
        if fetch_post(connection, post_data[11], post_data[12], post_data[13]) is None:
            raise ValueError("Original post does not exist in database.")

    #convert orig_user, orig_social_media, orig_time_posted to null if is_repost is False
    if not post_data[10]:
        post_data[11] = None
        post_data[12] = None
        post_data[13] = None
    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO Post (username, social_media, time_posted, text, city, state, country, num_likes, num_dislikes, multimedia, is_repost, orig_user, orig_social_media, orig_time_posted)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, post_data)
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error adding post to database: {e}")

def insert_project(connection, project_data): # Insert projects into the database
    #project_name, project_manager, institute, field_names, start_date, end_date
    
    #check if project_data is valid
    if len(project_data) != 6:
        raise ValueError("Invalid project data. Expected 6 fields.")
    if not isinstance(project_data[0], str) or not isinstance(project_data[1], str):
        raise TypeError("Invalid project data. Project name and project manager should be strings.")
    if not isinstance(project_data[2], str):
        raise TypeError("Invalid project data. Institute should be a string.")
    if not isinstance(project_data[3], str):
        raise TypeError("Invalid project data. Field names should be a string.")
    if not isinstance(project_data[4], datetime) or not isinstance(project_data[5], datetime):
        raise TypeError("Invalid project data. Start date and end date should be datetime objects.")
    if project_data[4] > project_data[5]:
        print(f"Start date: {project_data[4]}, End date: {project_data[5]}")
        raise ValueError("Invalid project data. Start date should be before end date.")
    
    #check if project exists
    if fetch_project(connection, project_data[0]) is not None:
        raise ValueError("Project already exists in the database.")
    
    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO Project (project_name, project_manager, institute, field_names, start_date, end_date)
            VALUES (%s, %s, %s, %s,%s, %s)
            """
            cursor.execute(insert_query, project_data)
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error adding project to database: {e}")

# USED WITH OLD DATA ENTRY METHOD
def insert_projectdata(connection, project_data): # Insert project data into the database
    #Labels: project_name,post_username,post_social_media,post_time_posted,field,result

    #check if project_data is valid
    if len(project_data) != 6:
        raise ValueError("Invalid project data. Expected 6 fields.")
    if not isinstance(project_data[0], str) or not isinstance(project_data[1], str):
        raise TypeError("Invalid project data. Project name and post username should be strings.")
    if not isinstance(project_data[2], str):
        raise TypeError("Invalid project data. Post social media should be a string.")
    if not isinstance(project_data[3], datetime):
        raise TypeError("Invalid project data. Post time posted should be a datetime object.")
    if not isinstance(project_data[4], str):
        raise TypeError("Invalid project data. Field should be a string.")
    if not isinstance(project_data[5], str): #ADDED THIS
        raise TypeError("Invalid project data. Result should be a string.")
    
    #check if projectdata exists
    if fetch_projectdata(connection, project_data[0], project_data[1], project_data[2], project_data[3]) is not None: # CHANGED TO INCLUDE project_data[4] since field is now part of the primary key
        raise ValueError("ProjectData already exists in the database.")
    
    try:
        with connection.cursor() as cursor:
            insert_query = """
            INSERT INTO ProjectData (project_name, post_username, post_social_media, post_time_posted, field, result)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, project_data)
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error adding project data to database: {e}")

# USED WITH NEW DATA ENTRY METHOD
def insert_post_no_data(connection, post_data): 
    #Labels: 'project_name', 'post_username', 'post_social_media', 'post_time_posted'
    
    #check if project_data is valid
    if len(post_data) != 4:
        raise ValueError("Invalid project data. Expected 4 fields.")
    if not isinstance(post_data[0], str) or not isinstance(post_data[1], str):
        raise TypeError("Invalid project data. Project name and post username should be strings.")
    if not isinstance(post_data[2], str):
        raise TypeError("Invalid project data. Post social media should be a string.")
    if not isinstance(post_data[3], datetime):
        raise TypeError("Invalid project data. Post time posted should be a datetime object.")
    
    #check if project exists
    if fetch_project(connection, post_data[0]) is None:
        raise ValueError("The project \"" + post_data[0] + "\" associated with this post doesn't exist in the database.")
    
    #check if post exists
    if fetch_post(connection, post_data[1], post_data[2], post_data[3]) is None:
        raise ValueError("Post does not yet exist in the database.")
    
    try:
        with connection.cursor() as cursor:
            find_proj_fields_query = """
            SELECT field_names 
            FROM Project
            WHERE project_name = %s
            """
            cursor.execute (find_proj_fields_query,post_data[0])
            field_names = cursor.fetchone()
    except pymysql.MySQLError as e:
        print(f"Error searching project for fields: {e}")

    if len(field_names) == 0:
        raise ValueError("This post is not associated with a project that contains fields. Project \"" + post_data[0] + "\" has no fields.")
    
    f = StringIO(field_names[0])
    reader = csv.reader(f)
    field_list = next(reader)  

    try:
        for field in field_list:
            with connection.cursor() as cursor:
                insert_query = """
                INSERT INTO ProjectData (project_name, post_username, post_social_media, post_time_posted, field)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, tuple(post_data) + (field,))
            connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error adding project/post/field combo to database: {e}")

# USED WITH NEW DATA ENTRY METHOD  
def insert_field_values(connection, project_data):
    #Labels: project_name,post_username,post_social_media,post_time_posted,field,result
    
    #check if project_data is valid
    if len(project_data) != 6:
        raise ValueError("Invalid project data. Expected 6 fields.")
    if not isinstance(project_data[0], str) or not isinstance(project_data[1], str):
        raise TypeError("Invalid project data. Project name and post username should be strings.")
    if not isinstance(project_data[2], str):
        raise TypeError("Invalid project data. Post social media should be a string.")
    if not isinstance(project_data[3], datetime):
        raise TypeError("Invalid project data. Post time posted should be a datetime object.")
    if not isinstance(project_data[4], str):
        raise TypeError("Invalid project data. Field should be a string.")
    if not isinstance(project_data[5], str):
        raise TypeError("Invalid project data. Result should be a string.")
     
    #check if the correct spot for data entry exists
    if fetch_projectdata(connection, project_data[0], project_data[1], project_data[2], project_data[3], project_data[4]) is None:
        raise ValueError("The project/post/field combo you are trying to insert data for is incorrect: " + str(project_data))
    
    try:
        with connection.cursor() as cursor:
            update_query = """
            UPDATE ProjectData
            SET result = %s
            WHERE project_name = %s AND post_username = %s AND post_social_media = %s AND post_time_posted = %s AND field = %s;
            """
            cursor.execute(update_query, (project_data[5], project_data[0], project_data[1], project_data[2], project_data[3], project_data[4]))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error adding field value to database: {e}")

def fetch_user(connection, username, social_media): # Fetch user data from the database
    try:
        with connection.cursor() as cursor:
            select_query = """
            SELECT * FROM user WHERE username = %s AND social_media = %s;
            """
            cursor.execute(select_query, (username, social_media))
            result = cursor.fetchone()
        return result
    except pymysql.MySQLError as e:
        print(f"Error fetching user in database: {e}")

def fetch_post(connection, username, social_media, time_posted): # Fetch post data from the database
    try:  
        with connection.cursor() as cursor:
            select_query = """
            SELECT * FROM Post WHERE username = %s AND social_media = %s AND time_posted = %s;
            """
            cursor.execute(select_query, (username, social_media, time_posted))
            result = cursor.fetchone()
        return result
    except pymysql.MySQLError as e:
        print(f"Error fetching post in database: {e}")

def fetch_project(connection, project_name): # Fetch a project from the database
    try:
        with connection.cursor() as cursor:
            select_query = """
            SELECT * FROM Project WHERE project_name = %s;
            """
            cursor.execute(select_query, (project_name,))
            result = cursor.fetchone()
        return result
    except pymysql.MySQLError as e:
        print(f"Error fetching project in database: {e}")

def fetch_projectdata(connection, project_name, post_username, post_social_media, post_time_posted, field): # Fetch project data from the database
    try:
        with connection.cursor() as cursor:
            select_query = """
            SELECT * FROM ProjectData WHERE project_name = %s AND post_username = %s AND post_social_media = %s AND post_time_posted = %s AND field = %s;
            """
            cursor.execute(select_query, (project_name, post_username, post_social_media, post_time_posted, field))
            result = cursor.fetchone()
        return result
    except pymysql.MySQLError as e:
        print(f"Error fetching project data in database: {e}")

def fetch_all_users(connection): # Returns all users in the database
    try:
        with connection.cursor() as cursor:
            select_query = """
            SELECT * FROM user;
            """
            cursor.execute(select_query)
            result = cursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        print(f"Error fetching all users in database: {e}")

def fetch_all_posts(connection): # Returns all posts in the database
    result = []
    try:
        with connection.cursor() as cursor:
            select_query = """
            SELECT * FROM Post;
            """
            cursor.execute(select_query)
            result = cursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        print(f"Error fetching all posts in database: {e}")

def fetch_all_projects(connection): # Returns all projects in the database
    try:
        with connection.cursor() as cursor:
            select_query = """
            SELECT * FROM Project;
            """
            cursor.execute(select_query)
            result = cursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        print(f"Error fetching all projects in database: {e}")

def fetch_all_projectdata(connection): # Returns all project data in the database
    try:
        with connection.cursor() as cursor:
            select_query = """
            SELECT * FROM ProjectData;
            """
            cursor.execute(select_query)
            result = cursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        print(f"Error fetching all project data in database: {e}")

# individual functions for the queries described in the project description pdf (probably don't use since we have the all-purpose function now)
# NOT implementing error checking here becuase I don't think we will even use these.

#find posts of a social media type
def fetch_posts_socialmedia(connection, social_media):
    try:
        with connection.cursor() as cursor:
            select_query = """
            SELECT DISTINCT p.*, pd.project_name, pd.field, pd.result
            FROM Post p
            LEFT JOIN ProjectData pd ON 
                p.username = pd.post_username 
                AND p.social_media = pd.post_social_media 
                AND p.time_posted = pd.post_time_posted
            WHERE p.social_media = %s
            ORDER BY p.time_posted;
            """
            cursor.execute(select_query, (social_media,))
            result = cursor.fetchall()
        return result
    except pymysql.MySQLError as e:
        raise Exception(f"Error fetching posts by social media in database: {e}")
#Find posts between a certain period of time
def fetch_posts_betweentime(connection, beginning_time, ending_time):
    
    beginning_date_time = datetime.strptime(beginning_time, "%m/%d/%Y %H:%M")
    ending_date_time = datetime.strptime(ending_time, "%m/%d/%Y %H:%M")
    
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Post WHERE time_posted > %s AND time_posted < %s
        ORDER BY time_posted ASC;
        """
        cursor.execute(select_query, (beginning_date_time, ending_date_time)) # NEED TO ERROR HANDLE THIS FOR NOT CORRECT INPUTS
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

#Query for all 4 at once (This is the correct one we should use, so I added error checking)
def fetch_posts_all4(connection, social_media, beginning_time, ending_time, username, first_name, last_name):
    
    # checking data types
    if not isinstance(social_media, str):
        raise TypeError("Invalid query data. Social media should be a string.")
    if not isinstance(beginning_time, datetime) or not isinstance(ending_time, datetime):
        raise TypeError("Invalid query data. Beginning and ending times should be datetime.")
    if not isinstance(username, str):
        raise TypeError("Invalid query data. Username should be a string.")
    if not isinstance(first_name, str) or not isinstance(last_name, str):
        raise TypeError("Invalid query data. First name and last name should be a strings.")
    
    try:
        with connection.cursor() as cursor:
            query = """
            SELECT DISTINCT p.text,p.social_media,p.username,p.time_posted, pd.project_name, pd.field, pd.result
            FROM Post p
            LEFT JOIN user u ON p.username = u.username AND p.social_media = u.social_media
            LEFT JOIN ProjectData pd ON 
                p.username = pd.post_username 
                AND p.social_media = pd.post_social_media 
                AND p.time_posted = pd.post_time_posted
            WHERE 1=1
            """
            params = []

            if social_media:
                query += " AND p.social_media = %s"
                params.append(social_media)

            if beginning_time and ending_time:
                query += " AND p.time_posted BETWEEN %s AND %s"
                params.extend([beginning_time, ending_time])

            if username:
                query += " AND p.username = %s"
                params.append(username)

            if first_name and last_name:
                query += " AND u.first_name = %s AND u.last_name = %s"
                params.extend([first_name, last_name])

            query += " ORDER BY p.time_posted;"

            cursor.execute(query, params)
            result = cursor.fetchall()

        return result
    except pymysql.MySQLError as e:
        print(f"Error executing query in database: {e}")
        return None

#Querying experiment: You should ask the user for the name of the experiment, and it should
#return the list of posts that is associated with the experiment, and for each post, any results that
#has been entered. Also you need to display for each field, the percentage of posts that contain a
#value of that field.

# might need to change our interpretation of this function depending on Lin's email

def fetch_posts_experiment(connection, project_name): #not sure for this one if we just need the primary key of the post, or the actual post text itself
    
    # checking data type
    if not isinstance(project_name, str):
        raise TypeError("Invalid query data. Project name should be a string.")
    
    try:
        with connection.cursor() as cursor:
            select_query1 = """
            SELECT *
            FROM ProjectData
            WHERE project_name = %s;
            """
            cursor.execute(select_query1, (project_name,))
            result1 = cursor.fetchall()

            select_query2 = """
            SELECT field, ROUND((SUM(CASE WHEN result IS NOT NULL AND result != 'None' THEN 1 ELSE 0 END) * 100.0) / COUNT(*), 2) AS percentage_filled
            FROM ProjectData
            WHERE project_name = %s
            GROUP BY field;
            """
            cursor.execute(select_query2, (project_name,))
            result2 = cursor.fetchall()
        return result1, result2
    except pymysql.MySQLError as e:
        print(f"Error executing query in database: {e}")
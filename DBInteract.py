import pymysql
import csv
import pandas as pd
import datetime

def insert_user(connection, user_data):
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
def insert_post(connection, post_data):
    #check if post exists
    if fetch_post(connection, post_data[0], post_data[1], post_data[2]) is not None:
        print("Post already exists in the database.")
        return
    with connection.cursor() as cursor:
        insert_query = """
        INSERT INTO Post (username, social_media, time_posted, text, city, state, country, num_likes, num_dislikes, multimedia, is_repost)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, post_data)
    connection.commit()
def insert_project(connection, project_data):
    #check if project exists
    if fetch_project(connection, project_data[0]) is not None:
        print("Project already exists in the database.")
        return
    with connection.cursor() as cursor:
        insert_query = """
        INSERT INTO Project (project_name, project_manager, institute, start_date, end_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, project_data)
    connection.commit()
def insert_projectdata(connection, project_data):
    #check if projectdata exists
    if fetch_projectdata(connection, project_data[0], project_data[1], project_data[2], project_data[3]) is not None:
        print("ProjectData already exists in the database.")
        return
    with connection.cursor() as cursor:
        insert_query = """
        INSERT INTO ProjectData (project_name, post_username, post_social_media, post_time_posted, field, result)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, project_data)
    connection.commit()

def fetch_user(connection, username, social_media):
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM user WHERE username = %s AND social_media = %s
        """
        cursor.execute(select_query, (username, social_media))
        result = cursor.fetchone()
    return result
def fetch_post(connection, username, social_media, time_posted):
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Post WHERE username = %s AND social_media = %s AND time_posted = %s
        """
        cursor.execute(select_query, (username, social_media, time_posted))
        result = cursor.fetchone()
    return result
def fetch_project(connection, project_name):
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Project WHERE project_name = %s
        """
        cursor.execute(select_query, (project_name,))
        result = cursor.fetchone()
    return result
def fetch_projectdata(connection, project_name, post_username, post_social_media, post_time_posted):
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM ProjectData WHERE project_name = %s AND post_username = %s AND post_social_media = %s AND post_time_posted = %s
        """
        cursor.execute(select_query, (project_name, post_username, post_social_media, post_time_posted))
        result = cursor.fetchone()
    return result

def fetch_all_users(connection):
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM user
        """
        cursor.execute(select_query)
        result = cursor.fetchall()


    return result
def fetch_all_posts(connection):
    result = []
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Post
        """
        cursor.execute(select_query)
        result = cursor.fetchall()

    return result
def fetch_all_projects(connection):
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM Project
        """
        cursor.execute(select_query)
        result = cursor.fetchall()

    return result
def fetch_all_projectdata(connection):
    with connection.cursor() as cursor:
        select_query = """
        SELECT * FROM ProjectData
        """
        cursor.execute(select_query)
        result = cursor.fetchall()
    return result
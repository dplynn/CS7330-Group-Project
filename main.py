import pymysql
import csv
import pandas as pd
import datetime
import DBInit
import DBInteract
import testing

def main():
    connection = DBInit.connect_to_database() # Connect to the database using pymysql
    DBInit.create_tables(connection) # Create tables in the database
    DBInit.clear_tables(connection) # Clear tables in the database

    name = input("Whose test files are we running? Davis, Lucas, or Katherine? ")
    print("\n")

    users_data = DBInit.read_user_data(name+'_data_files/user_data.csv') # Read user data from CSV file
    for user in users_data:
        DBInteract.insert_user(connection, user) # Insert each user into the database
    result = DBInteract.fetch_all_users(connection) # Fetch all users from the database
    #print length of result
    print(f"Number of users in the database: {len(result)}")

    posts_data = DBInit.read_post_data(name+'_data_files/post_data.csv') # Read post data from CSV file
    for post in posts_data:
        DBInteract.insert_post(connection, post) # Insert each post into the database
    result = DBInteract.fetch_all_posts(connection) # Fetch all posts from the database
    print(f"Number of posts in the database: {len(result)}")

    projects_data = DBInit.read_project_data(name+'_data_files/project_data.csv') # Read project data from CSV file
    for project in projects_data:
        DBInteract.insert_project(connection, project) # Insert each project into the database
    result = DBInteract.fetch_all_projects(connection) # Fetch all projects from the database
    print(f"Number of projects in the database: {len(result)}")
    
    projectdata_data = DBInit.read_projectdata_data(name+'_data_files/projectdata_data.csv') # Read project data from CSV file
    for projectdata in projectdata_data:
        DBInteract.insert_projectdata(connection, projectdata) # Insert each project into the database
    result = DBInteract.fetch_all_projectdata(connection) # Fetch all project data from the database
    print(f"Number of project data in the database: {len(result)}")

    # UNCOMMENT TO RUN TESTING
    # testing.testing(connection)

if __name__ == "__main__": 
    main()
import pymysql
import csv
import pandas as pd
import datetime
import DBInit
import DBInteract

def main():
    connection = DBInit.connect_to_database() # Connect to the database using pymysql
    DBInit.create_tables(connection) # Create tables in the database
    DBInit.clear_tables(connection) # Clear tables in the database
    users_data = DBInit.read_user_data('user_data.csv') # Read user data from CSV file
    for user in users_data:
        DBInteract.insert_user(connection, user) # Insert each user into the database
    result = DBInteract.fetch_all_users(connection) # Fetch all users from the database
    posts_data = DBInit.read_post_data('post_data.csv') # Read post data from CSV file
    for post in posts_data:
        DBInteract.insert_post(connection, post) # Insert each post into the database
    result = DBInteract.fetch_all_posts(connection) # Fetch all posts from the database
    print("All posts in the database:")
    for row in result:
        print(row)
    
if __name__ == "__main__": 
    main()
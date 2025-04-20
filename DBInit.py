import pymysql
import csv
import pandas as pd
import datetime
def connect_to_database(): #Connect to the database using pymysql
    csv_file_path = 'DB_Info.csv'

    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        db_info = [row for row in reader]
    
    db_info = db_info[0]
    host = db_info['host']
    user = db_info['user']
    password = db_info['password']
    database = db_info['db_name']
    print(host, user, password, database)

    try:
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Connection to the database was successful.")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to the database: {e}")
        return None

def create_tables(connection): #Creates the tables in the database
    with connection.cursor() as cursor: # Create User Table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user (
            username VARCHAR(40) NOT NULL,
            social_media VARCHAR(40) NOT NULL,
            first_name VARCHAR(40) NOT NULL,
            last_name VARCHAR(40) NOT NULL,
            country_birth VARCHAR(40) NOT NULL,
            country_residence VARCHAR(40) NOT NULL,
            age INT NOT NULL,
            gender VARCHAR(10) NOT NULL,
            verified BOOLEAN NOT NULL,
            PRIMARY KEY (username, social_media)
        )
        """
        cursor.execute(create_table_query)

    with connection.cursor() as cursor: # Create Post Table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Post (
            username VARCHAR(40) NOT NULL,
            social_media VARCHAR(40) NOT NULL,
            time_posted DATETIME NOT NULL,
            text TEXT NOT NULL,
            city VARCHAR(40) NOT NULL,
            state VARCHAR(40) NOT NULL,
            country VARCHAR(40) NOT NULL,
            num_likes INT NOT NULL,
            num_dislikes INT NOT NULL,
            multimedia BOOLEAN NOT NULL,
            is_repost BOOLEAN NOT NULL,
            orig_user VARCHAR(40),
            orig_social_media VARCHAR(40),
            orig_time_posted DATETIME,
            orig_text TEXT,
            PRIMARY KEY (username, social_media, time_posted),
            FOREIGN KEY (orig_user, orig_social_media) REFERENCES user(username, social_media),
            FOREIGN KEY (username, social_media) REFERENCES user(username, social_media)
        )
        """
        cursor.execute(create_table_query)

    with connection.cursor() as cursor: # Create Project Table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Project (
            project_name VARCHAR(40) NOT NULL PRIMARY KEY,
            project_manager VARCHAR(40) NOT NULL,
            institute VARCHAR(40) NOT NULL,
            start_date DATETIME NOT NULL,
            end_date DATETIME NOT NULL
        )
        """
        cursor.execute(create_table_query)

    with connection.cursor() as cursor: # Create ProjectData Table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS ProjectData (
            project_name VARCHAR(40) NOT NULL,
            post_username VARCHAR(40) NOT NULL,
            post_social_media VARCHAR(40) NOT NULL,
            post_time_posted DATETIME NOT NULL,
            field VARCHAR(40) NOT NULL,
            result VARCHAR(40),
            PRIMARY KEY (project_name, post_username, post_social_media, post_time_posted),
            FOREIGN KEY (post_username, post_social_media, post_time_posted) REFERENCES Post(username, social_media, time_posted),
            FOREIGN KEY (project_name) REFERENCES Project(project_name)
        )
        """
        cursor.execute(create_table_query)

def clear_tables(connection): #Clears the tables in the database
    with connection.cursor() as cursor:
        # Clear the ProjectData table
        clear_query = "DELETE FROM ProjectData"
        cursor.execute(clear_query)

        # Clear the Post table
        clear_query = "DELETE FROM Post"
        cursor.execute(clear_query)

        # Clear the Project table
        clear_query = "DELETE FROM Project"
        cursor.execute(clear_query)

        # Clear the User table
        clear_query = "DELETE FROM user"
        cursor.execute(clear_query)

    connection.commit()

def read_user_data(file_path): #Reads the user data from a CSV file and returns it as a list of tuples, for testing ONLY
    # Labels: username,social_media,first_name,last_name,country_birth,country_residence,age
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path, skiprows=1, header=None, names=['username', 'social_media', 'first_name', 'last_name', 'country_birth', 'country_residence', 'age','gender','verified'])
    # Convert the 'age' column to integer
    try:
        df['age'] = df['age'].astype(int)
    except ValueError:
        # remove rows with invalid age values
        df = df[pd.to_numeric(df['age'], errors='coerce').notnull()]
        df['age'] = df['age'].astype(int)
        print("Invalid age values found and removed from the DataFrame.")
    try: 
        df['verified'] = df['verified'].astype(bool)
    except ValueError:
        # remove rows with invalid verified values
        df = df[pd.to_numeric(df['verified'], errors='coerce').notnull()]
        df['verified'] = df['verified'].astype(bool)
        print("Invalid verified values found and removed from the DataFrame.")
    user_data = [tuple(row) for row in df.values]     # Convert the DataFrame to a list of tuples
    return user_data
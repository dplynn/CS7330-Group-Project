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
        print("Connection to the database was successful.\n")
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
            FOREIGN KEY (username, social_media) REFERENCES user(username, social_media),
            FOREIGN KEY (orig_user, orig_social_media) REFERENCES user(username, social_media)
        )
        """
        #  FOREIGN KEY (username, social_media) REFERENCES user(username, social_media), / Foreign Key to user table NYI
        # FOREIGN KEY (orig_user, orig_social_media, orig_time_posted) REFERENCES Post(username, social_media, time_posted) / Foreign Key to user table. NYI
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
            FOREIGN KEY (project_name) REFERENCES Project(project_name),
            FOREIGN KEY (post_username, post_social_media, post_time_posted) REFERENCES Post(username, social_media, time_posted)
        )
        """
        # FOREIGN KEY (post_username, post_social_media, post_time_posted) REFERENCES Post(username, social_media, time_posted), # Foreign Key to Post table. NYI
        # FOREIGN KEY (project_name) REFERENCES Project(project_name) # Foreign Key to Project table. NYI
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

def read_post_data(file_path): #Reads the post data from a CSV file and returns it as a list of tuples, for testing ONLY
    #Labels: username,social_media,time_posted,text,city,state,country,num_likes,num_dislikes,multimedia,is_repost,orig_user,orig_social_media,orig_time_posted,orig_text
    df = pd.read_csv(file_path, skiprows=1, header=None, names=['username', 'social_media', 'time_posted', 'text', 'city', 'state', 'country', 'num_likes', 'num_dislikes', 'multimedia', 'is_repost', 'orig_user', 'orig_social_media', 'orig_time_posted', 'orig_text'])
    # Convert the 'time_posted' column to datetime
    df['time_posted'] = pd.to_datetime(df['time_posted'], errors='coerce')
    # Convert the 'orig_time_posted' column to datetime, if it doesnt exist, set it to None
    df['orig_time_posted'] = pd.to_datetime(df['orig_time_posted'], errors='coerce')
    df['orig_time_posted'] = df['orig_time_posted'].fillna(pd.NaT)
    

    # Remove rows with invalid datetime values
    df = df.dropna(subset=['time_posted'])
    # Convert the 'num_likes' and 'num_dislikes' columns to integer
    try:
        df['num_likes'] = df['num_likes'].astype(int)
        df['num_dislikes'] = df['num_dislikes'].astype(int)
    except ValueError:
        # remove rows with invalid num_likes or num_dislikes values
        df = df[pd.to_numeric(df['num_likes'], errors='coerce').notnull()]
        df = df[pd.to_numeric(df['num_dislikes'], errors='coerce').notnull()]
        df['num_likes'] = df['num_likes'].astype(int)
        df['num_dislikes'] = df['num_dislikes'].astype(int)
        print("Invalid num_likes or num_dislikes values found and removed from the DataFrame.")

    try:
        df['multimedia'] = df['multimedia'].astype(bool)
        df['is_repost'] = df['is_repost'].astype(bool)
    except ValueError:
        # remove rows with invalid multimedia or is_repost values
        df = df[pd.to_numeric(df['multimedia'], errors='coerce').notnull()]
        df = df[pd.to_numeric(df['is_repost'], errors='coerce').notnull()]
        df['multimedia'] = df['multimedia'].astype(bool)
        df['is_repost'] = df['is_repost'].astype(bool)
        print("Invalid multimedia or is_repost values found and removed from the DataFrame.")
    # remove emojis
    df['text'] = df['text'].str.replace(r'[^\x00-\x7F]+', '', regex=True)
    df['orig_text'] = df['orig_text'].str.replace(r'[^\x00-\x7F]+', '', regex=True)
    # convert username, social_media, city, state, country, orig_user, orig_social_media to string
    df['username'] = df['username'].astype(str)
    df['social_media'] = df['social_media'].astype(str)
    df['city'] = df['city'].astype(str)
    df['state'] = df['state'].astype(str)
    df['country'] = df['country'].astype(str)
    # Convert the DataFrame to a list of tuples
    post_data = [tuple(row) for row in df.values]
    return post_data

def read_project_data(file_path): #Reads the project data from a CSV file and returns it as a list of tuples, for testing ONLY
    #Labels: project_name,project_manager,institute,start_date,end_date
    df = pd.read_csv(file_path, skiprows=1, header=None, names=['project_name', 'project_manager', 'institute', 'start_date', 'end_date'])
    # Convert the 'start_date' and 'end_date' columns to datetime
    df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], errors='coerce')
    # Remove rows with invalid datetime values
    df = df.dropna(subset=['start_date', 'end_date']) #DOES THIS CHECK IF THE END DATE IS AFTER THE START DATE?
    # Convert the DataFrame to a list of tuples
    project_data = [tuple(row) for row in df.values]
    return project_data

def read_projectdata_data(file_path): #Reads the project data from a CSV file and returns it as a list of tuples, for testing ONLY
    #Labels: project_name,post_username,post_social_media,post_time_posted,field,result
    df = pd.read_csv(file_path, skiprows=1, header=None, names=['project_name', 'post_username', 'post_social_media', 'post_time_posted', 'field', 'result'])
    # Convert the 'post_time_posted' column to datetime


    #THIS IS VERY SPECIFIC, NOT SURE IF WE SHOULD LEAVE IT LIKE THIS? IF WE DO IT THIS SPECIIFC HERE, SHOULD WE DO THAT FOR OTHER TABLES AS WELL?
    df['post_time_posted'] = pd.to_datetime(df['post_time_posted'], format='%Y-%m-%d %H:%M:%S', errors='coerce')    # Remove rows with invalid datetime values
    
    
    df = df.dropna(subset=['post_time_posted'])
    #If result does not exist, set it to None
    df['result'] = df['result'].fillna('None')
    # Convert the DataFrame to a list of tuples
    projectdata_data = [tuple(row) for row in df.values]
    return projectdata_data
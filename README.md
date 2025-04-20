# Database Group Project - CS5330

### Per Person Tasks
Database Creation (Davis) - **DONE**
Insert Statements for Each Table (Davis)
    * Done, but Foreign Keys are NYI for the sake of testing
UI (Bonita)
Querying Statements / General Implementation (Lucas)
Report / Demo (Katherine)
Instalation / User Manual (Katherine) 
Slides (Katherine)
Data Validation and Test Cases (Lucas)

### Python File Descriptions:
**main.py** - runs all programs through this file, use this file to run tests
**DBInit.py** - Database initialization: Creates Tables, Connects to Database, Reads in Test Files 

**DBInteract.py** - Database interaction: Inserts into tables, connects tables, fetches from tables, and prints full tables
*Functions:*
* insert_####_data(connection, data) - Inserts data, requires a tuple of data to insert and the database connection
* fetch_####(connection, keys) - Fetches one relevant result based on criteria, used in insert functions to check for duplicates before insertion
* fetch_all_####(connection) - returns all values in a table, returns them as a 2d vector. 
*Better querying with more granularity is absolutely needed, if you are looking for something to do, this would be it. However, please don't mess with my fetch, create a new function.

### CSV File Descriptions:
**DB_info.csv** - Database connection info, **change before running**
**user_data.csv** - fake user data, can be read in through DBInit.read_user_data
**post_data.csv** - fake post data, can be read in through DBInit.read_post_data
**project_data.csv** - fake project data, can be read in through DBInit.read_project_data
**projectdata_data.csv** - fake project data(table) data, can be read in through DBInit.read_projectdata_data

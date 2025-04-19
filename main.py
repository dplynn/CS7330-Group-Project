import pymysql
import csv
import pandas as pd
import datetime
import DBInteract


def main():
    connection = DBInteract.connect_to_database() # Connect to the database using pymysql
    DBInteract.create_tables(connection) # Create tables in the database


if __name__ == "__main__": 
    main()
import pymysql
import csv
import pandas as pd
import datetime
import DBConnect


def main():
    connection = DBConnect.connect_to_database()
    DBConnect.create_tables(connection)

if __name__ == "__main__": 
    main()
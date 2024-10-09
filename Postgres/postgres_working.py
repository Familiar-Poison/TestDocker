# Go to D:\RandomPrograms\PostgreSQL\16\bin
# .\pg_ctl start -D D:\RandomPrograms\PostgreSQL\16\data
# .\pg_ctl.exe restart -D D:\RandomPrograms\PostgreSQL\16\data

# Open SQL Shell (psql) - D:\RandomPrograms\PostgreSQL\16\scripts\runpsql.exe
# Use default values: (windows)
# Server - localhost
# Database - postgres
# Post - 5432
# Username - postgres
# Password - password
# Use default values: (Mac)
# Server - localhost
# Database - postgres
# Post - 5432
# Username - franz
# Password - password
import csv
import psycopg2
from psycopg2 import OperationalError
from psycopg2 import sql
from file_cv_working import *
# Test change
def write_postgres_table(host, database, user, password, port, csv_file):
    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )

    except OperationalError as e:
        print("Unable to connect to the PostgreSQL server: ", e)
    
    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Set automatic commit to be true, so that each action is committed without having to call conn.committ() after each command
    connection.set_session(autocommit=True)

    # Create postgres table if it does not exist with 4 columns - user_name, time_stamp, working_hours, project_name
    table_name = 'timesheet'
    create_table_query = f'CREATE TABLE IF NOT EXISTS {table_name} (user_name varchar NOT NULL, time_stamp timestamp, working_hours float, project_name varchar);'

    # Old/alternative
    # create_table_query = '''CREATE TABLE IF NOT EXISTS timesheet (user_name varchar NOT NULL, 
    #                             time_stamp timestamp, 
    #                             working_hours float, 
    #                             project_name varchar);'''

    cursor.execute(create_table_query)

    # Reads the parsed and formatted csv file
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        #next(reader)

        # Pushes it to postgres table
        for row in reader:
            insert_query = sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s)").format(sql.Identifier("timesheet"))
            # insert_query = sql.SQL(f"INSERT INTO {table_name} VALUES ( {row[0]} , {row[1]} , {row[2]} , {row[3]} )")
            cursor.execute(insert_query, row)

    # Close the cursor and connection
    cursor.close()
    connection.close()




to_parse_column = 1 # Index of column to read and parse

postgres_table = parse_date_time_column(csv_read_path, to_parse_column)

write_datetime_column(csv_write_path, postgres_table)



# Provide PostgreSQL connections details
# If you are using Docker-for-mac or Docker-for-Windows 18.03+, connect to your mysql service using the 
# host host.docker.internal (instead of the 127.0.0.1 in your connection string).

host = "host.docker.internal"
database = "postgres"
user = "franz"
password = "password"
port = "5432"  # Default PostgreSQL port is 5432

csv_read_path = 'testing.csv' # Provide path to the CSV file containing the ...
csv_write_path = 'parsed.csv'

write_postgres_table(host, database, user, password, port, csv_write_path)
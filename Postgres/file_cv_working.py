import csv
import datetime
from dateutil import parser

def parse_date_time_column(csv_file, column_index):
    column_values = []
    final_table = []
    parsed_column = []
    counter = 0

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader) # Needed to skip the header row
        table_holder = list(reader) # Contains the whole table from the csv file 

    # Retrieves only the date/time column and stores it to column_values[]
    for i in table_holder:
        column_values.append(i[column_index])
    
    # Reference for parsing the russian months to english
    month_mapping = {
        'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
        'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
        'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12
    }

    for value in column_values:
        try:
            parsed_datetime = parser.parse(value, fuzzy=True) 
            # Parses value as a datetime object
            # fuzzy=True indicates that the parses should attempt to intelligently guess the format of the datetime string
            
            formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S") 
            # Format all the date/time values into a single unified format = YYYY-MM-DD HH:MM:SS

            parsed_column.append(formatted_datetime)
        except parser._parser.ParserError:
            # Workaround (works like an if condition) for months in Russian language. 

            day, month_str, year, time = value.split()

            # Parses the month string to get its numerical representation - from month_mapping
            month = month_mapping[month_str]

            # Formats into the single unified format = YYYY-MM-DD HH:MM:SS
            formatted_datetime = datetime.datetime(int(year), month, int(day), hour=int(time.split(':')[0]), minute=int(time.split(':')[1]))
            parsed_column.append(formatted_datetime)
    
    for i in table_holder:
        temp = list(i) # Iterates table_holder values per row
        temp[column_index] = parsed_column[counter] # Retrieves only the parsed&formatted time/date column
        final_table.append(temp) # and stores it to final_table
        counter += 1 # Counter represents the current row
    
    return final_table

def write_datetime_column(csv_file, final_table):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(final_table)

csv_file_path = 'testing.csv' # Provide path to the CSV file containing the ...

to_parse_column = 1 # Index of column to read and parse

postgres_table = parse_date_time_column(csv_file_path, to_parse_column)

write_datetime_column(csv_file_path, postgres_table)


import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

DB_USER = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'DCC_Assignment_4'

def create_database():
    connection = mysql.connector.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    connection.close()
create_database()

def load_csv_to_mysql(csv_file,table_name):
    connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # username, password, hostname, port, and database name
    engine = create_engine(connection_string, echo=True)
    df = pd.read_csv(f"{csv_file}")
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

load_csv_to_mysql('EB_Redemption_Details.csv', 'redemption_details')
load_csv_to_mysql('EB_Purchase_Details.csv', 'purchase_details')
print("CSV files loaded into MySQL tables successfully.")
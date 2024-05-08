import configparser
import os
import sys
import psycopg2
from pathlib import Path
import re
import pandas as pd


class dataRetriever:
    def __init__(self, path_to_ini):
        self.path_to_ini = path_to_ini

    def database_create_connection(self):
        try:

            config = configparser.ConfigParser()

            config.read(self.path_to_ini)

            # Extract connection parameters
            user = config.get('postgresql', 'user')
            password = config.get('postgresql', 'password')
            host = config.get('postgresql', 'host')
            port = config.get('postgresql', 'port')
            database = config.get('postgresql', 'database')

            # Create the connection using psycopg2
            connection = psycopg2.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                database=database
            )
            return connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL:", error)
            return None

    def database_read_data(self, schema, table_name):
        try:
            cursor = self.database_create_connection().cursor()
            schema_table = schema + '.' + table_name
            # SQL query to select rows between two timestamps
            query = f"SELECT * FROM {schema_table}"

            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            data = pd.DataFrame(rows, columns=column_names)

            return data
        except (Exception, psycopg2.Error) as error:
            print("Error while selecting rows:", error)
            return None

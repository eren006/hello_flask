# database.py
import sqlitecloud
import pandas as pd
import numpy as np

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = self.get_db_connection()

    def get_db_connection(self):
        """
        Establishes a connection to the SQLite Cloud database using an API key and database name.

        Returns:
            sqlitecloud.Connection: An active connection to the SQLite Cloud database.
        """
        # Open the connection to SQLite Cloud
        conn = sqlitecloud.connect("sqlitecloud://cbgnacvcik.sqlite.cloud:8860?apikey=Mx2cK8ScRiNgZl31SFhJCezNWBXAtRBbtsdvvBVA5xw")
        conn.execute(f"USE DATABASE {self.db_name}")
        print("DB connection has been established ")
        return conn

    def execute_query(self, query, params=None):
        """
        Executes a given SQL query with optional parameters.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to substitute in the query.

        Returns:
            sqlitecloud.Cursor: The result of the query.
        """
        conn = self.connection
        if params:
            conn.execute(query, params)
            conn.commit()
        else:
            conn.execute(query)
            conn.commit()
        return conn

    def fetch_all(self, query, params=None):
        """
        Fetches all results from a given SQL query.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to substitute in the query.

        Returns:
            list: List of tuples containing the query results.
        """
        conn = self.connection
        if params:
            results = conn.execute(query, params).fetchall()
        else:
            results = conn.execute(query).fetchall()
        return results
    
    def fetch_one(self,query, params=None):
        """
        Fetches single result from a given sql query

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to substitute in the query.

        Returns:
            list: Tuple containing the query results.
        """
        conn = self.connection
        if params:
            result = conn.execute(query, params).fetchone()
        else:
            result = conn.execute(query).fetchone()
        return result
      
      

    def close_connection(self):
        """
        Closes the connection to the database.
        """
        self.connection.close()

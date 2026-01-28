"""
Database Configuration and Connection Handler
Provides database connection for all modules
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Create and return a MySQL database connection
    Returns: MySQL connection object
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'digital_event_organizer')
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def execute_query(query, params=None, fetch=False):
    """
    Execute a SQL query with optional parameters
    
    Args:
        query: SQL query string
        params: Tuple of parameters for the query
        fetch: Boolean, True to fetch results, False for insert/update/delete
    
    Returns:
        For SELECT: List of results
        For INSERT/UPDATE/DELETE: Number of affected rows
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        else:
            connection.commit()
            affected_rows = cursor.rowcount
            last_id = cursor.lastrowid
            cursor.close()
            connection.close()
            return last_id if last_id else affected_rows
            
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        connection.rollback()
        connection.close()
        return None

def execute_one(query, params=None):
    """
    Execute a query and fetch one result
    
    Args:
        query: SQL query string
        params: Tuple of parameters
    
    Returns:
        Single row as dictionary
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        return result
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        connection.close()
        return None

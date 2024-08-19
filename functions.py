import streamlit as st
from psycopg2 import pool

# Function to create a connection pool for PostgreSQL database
def create_connection_pool(host, dbname, user, password):
    """
    Creates and returns a connection pool to the specified PostgreSQL database.
    
    Parameters:
        host (str): The host address of the database server.
        dbname (str): The name of the database.
        user (str): The username used to authenticate.
        password (str): The password used to authenticate.
    
    Returns:
        pool.SimpleConnectionPool: A new connection pool with minimum 1 and maximum 10 connections.
    """
    return pool.SimpleConnectionPool(1, 10, host=host, dbname=dbname, user=user, password=password)


# Function to get a database connection from the connection pool
def get_db_connection(connection_pool):
    """
    Retrieves a database connection from the connection pool. If no open connection exists
    in the session state, or if the existing connection is closed, a new connection is fetched 
    and stored in the session state.
    
    Parameters:
        connection_pool (pool.SimpleConnectionPool): The pool from which to get the connection.
    
    Returns:
        psycopg2.extensions.connection: An open database connection.
    """
    if 'conn' not in st.session_state or st.session_state.conn.closed:
        st.session_state.conn = connection_pool.getconn()
        st.session_state.conn.autocommit = True
    return st.session_state.conn


# Function to release a database connection back to the pool
def release_db_connection(connection_pool, conn):
    """
    Releases a connection back to the connection pool and removes it from session state.
    
    Parameters:
        connection_pool (pool.SimpleConnectionPool): The pool to which the connection belongs.
        conn (psycopg2.extensions.connection): The connection to release.
    """
    if 'conn' in st.session_state:
        connection_pool.putconn(conn)
        del st.session_state['conn']


# Function to execute a query and fetch the results
def query_db(conn, query, params):
    """
    Executes a SQL query using a given connection and returns fetched results.
    
    Parameters:
        conn (psycopg2.extensions.connection): The connection to use to execute the query.
        query (str): The SQL query to execute.
        params (tuple/list): Parameters to substitute into the query.
    
    Returns:
        list: A list of tuples representing the rows fetched from the database.
    """
    with conn.cursor() as cur:
        cur.execute(query, params)
        records = cur.fetchall()
        return records
    
    
# Function to check if a string represents a number
def is_number(input_str):
    """
    Checks if the input string can be converted to an integer.
    
    Parameters:
        input_str (str): The string to check.
    
    Returns:
        bool: True if the string can be converted to an integer, False otherwise.
    """
    try:
        int(input_str)
        return True
    except ValueError:
        return False
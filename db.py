import psycopg2
import streamlit as st
from psycopg2 import pool

db_pool = None  # to hold global connection

# cache_resource : suitable for database pools, loaded ML moodels, global resources
@st.cache_resource # to cache the data connection pool once its deploy
def get_connection():
    global db_pool
    if db_pool is None:
        try:
            db_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=5,
                maxconn=60,
                host=st.secrets["db"]["host"],
                dbname=st.secrets["db"]["dbname"],
                user=st.secrets["db"]["user"],
                password=st.secrets["db"]["password"],
                port=st.secrets["db"]["port"]
            )
            print("Connection pool is created successfully")

        except (Exception, psycopg2.DatabaseError) as e:
            print("Failed to create connectioon pool: ", e)
            db_pool = None
    
    return db_pool

get_connection()

# Function to retrive staff data
def get_by_query(query: str, params=None, single_row=False):

    conn = None
    cur = None
    data, columns = None, []

    try:
        db_pool = get_connection()
        if db_pool is None:
            raise Exception("Database connection pool: Not Available")
        else:
            print("Database connection pool: Connected")

        conn = db_pool.getconn() # Borrow connection (no need to fetch directly to database)
        cur = conn.cursor()
        cur.execute(query, params or ())

        if single_row:
            data = cur.fetchone()
        else:
            data = cur.fetchall()

        columns = [desc[0] for desc in cur.description]

    except Exception as e:
        print(f"Error executing query: {e}")
        if conn:
            conn.rollback()
        data , columns = None, []

    finally:
        if cur:
            cur.close()
        if conn:
            db_pool.putconn(conn) # return to connection pool
            print("Database connection pool: Disconnected")

    return data, columns
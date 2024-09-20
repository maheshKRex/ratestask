import os
import psycopg2

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DATABASE_HOST'),
            database=os.getenv('DATABASE_NAME'),
            user=os.getenv('DATABASE_USER'),
            password=os.getenv('DATABASE_PASSWORD')
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        raise e
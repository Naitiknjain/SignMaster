import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="127.0.0.1",
        port=5432,
        database="signmaster",
        user="postgres",
        password="system"
    )
    return conn

import psycopg2
# pyrefly: ignore [missing-import]
from pgvector.psycopg2 import register_vector
import configuration as config

def get_connection():
    conn = psycopg2.connect(
        host=config.DB_HOST,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASS,
        port=config.DB_PORT
    )
    register_vector(conn)
    return conn
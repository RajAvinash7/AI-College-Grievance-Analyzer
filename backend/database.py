import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "database": "college_grievance",
    "user": "postgres",
    "password": "YOUR_POSTGRES_PASSWORD",
    "port": 5432
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)
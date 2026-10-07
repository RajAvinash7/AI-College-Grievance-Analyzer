from database import get_connection

try:
    conn = get_connection()
    print("✅ PostgreSQL connection successful!")

    cursor = conn.cursor()
    cursor.execute("SELECT current_database();")

    database = cursor.fetchone()
    print("Connected database:", database[0])

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Database connection failed:")
    print(e)
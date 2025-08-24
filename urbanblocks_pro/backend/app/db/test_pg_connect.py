import psycopg2
from urbanblocks_pro.backend.app.db.session import engine

try:
    conn = psycopg2.connect(
        dbname="mydb",
        user="admin",
        password="admin123",
        host="127.0.0.1",
        port="5432"
    )
    print("✅ Connection successful!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)

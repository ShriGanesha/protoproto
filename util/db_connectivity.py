import psycopg2

conn_str = "postgresql://lovemeplease@localhost:5432/embedding"

try:
    conn = psycopg2.connect(conn_str)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print("Connection failed:", e)
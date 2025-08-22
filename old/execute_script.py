import psycopg2


def delete():
    DB_NAME = "embedding"
    DB_USER = "lovemeplease"
    DB_HOST = "localhost"
    DB_PORT = 5432
    SQL_FILE = "../script/delete_embed.sql"

    with open(SQL_FILE, "r") as f:
        sql_script = f.read()

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    try:
        cur.execute(sql_script)

        if sql_script.strip().lower().startswith("select"):
            rows = cur.fetchall()
            print("Query result:")
            for row in rows:
                print(row)
        else:
            conn.commit()
            print("Script executed successfully.")

    except Exception as e:
        print("Error executing SQL:", e)

    finally:
        cur.close()
        conn.close()

def viewEmbed():
    DB_NAME = "embedding"
    DB_USER = "lovemeplease"
    DB_HOST = "localhost"
    DB_PORT = 5432
    SQL_FILE = "../script/view_embed.sql"

    with open(SQL_FILE, "r") as f:
        sql_script = f.read()

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    try:
        cur.execute(sql_script)

        res = []

        if sql_script.strip().lower().startswith("select"):
            rows = cur.fetchall()
            print("Query result:")
            for row in rows:
                print(row[3])
                res.append(row)
        else:
            conn.commit()
            print("Script executed successfully.")

        return res

    except Exception as e:
        print("Error executing SQL:", e)

    finally:
        cur.close()
        conn.close()


def viewEmbedForFile(fileName):
    DB_NAME = "embedding"
    DB_USER = "lovemeplease"
    DB_HOST = "localhost"
    DB_PORT = 5432
    SQL_FILE = "../script/view_embed.sql"

    with open(SQL_FILE, "r") as f:
        sql_script = f.read()

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    try:
        cur.execute(sql_script)

        res = []

        if sql_script.strip().lower().startswith("select"):
            rows = cur.fetchall()
            print("Query result:")
            for row in rows:
                print(row[3])
                if(row[3]["source"] == fileName):
                    res.append(row)
        else:
            conn.commit()
            print("Script executed successfully.")

        return res

    except Exception as e:
        print("Error executing SQL:", e)

    finally:
        cur.close()
        conn.close()

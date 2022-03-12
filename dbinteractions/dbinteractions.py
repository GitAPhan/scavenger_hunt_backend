import mariadb as db
import dbinteractions.dbcreds as c

# connect to database function
def connect_db():
    conn = None
    cursor = None
    try:
        conn = db.connect(user=c.user,
                          password=c.password,
                          host=c.host,
                          port=c.port,
                          database=c.database)
        cursor = conn.cursor()
    except db.OperationalError:
        print("Db Connection Error: something went wrong with the DB, please try again in 5 minutes")
    except:
        print("Db Connection Error: General database connection error")
    return conn, cursor  

# disconnect from database function
def disconnect_db(conn, cursor):
    try:
        cursor.close()
    except Exception as e:
        print(e)
        print("Db Connection Error: cursor close error")

    try:
        conn.close()
    except Exception as e:
        print(e)
        print("Db Connection Error: conn close error")


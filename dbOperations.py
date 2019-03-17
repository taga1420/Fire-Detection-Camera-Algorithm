import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = ("""
        CREATE TABLE location_id (
            analysis_id SERIAL PRIMARY KEY,
            date INTEGER[] NOT NULL,
            status VARCHAR NOT NULL,
            paste_name VARCHAR NOT NULL 
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insertData(go, resposta, now):

    sql = """INSERT INTO location_id (date, status, paste_name)
                 VALUES(%s,%s,%s) ; """

    data = (go, resposta, now)
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, data)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
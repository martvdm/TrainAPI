import mysql

def index(cursor):
    cursor.execute("DROP TABLE IF EXISTS NOTIFICATIONS")

    sql = '''CREATE TABLE NOTIFICATIONS(
    ID int AUTO_INCREMENT,
    CLIENT_ID INTEGER NOT NULL,
    STATION VARCHAR(5) NOT NULL,
    PRIMARY KEY (ID)
    )'''

    cursor.execute(sql)

def create(config, client_id, stationcode):
    conn = mysql.connector.connect(user=config['database']['username'], password=config['database']['password'], host=config['database']['host'], port=config['database']['port'], database=config['database']['database'])
    import database.tables.trips as trips
    cursor = conn.cursor()
    trips.index(cursor)
    sql = "INSERT INTO NOTIFICATIONS (CLIENT_ID, STATION) VALUES (%s, %s)"
    cursor.execute(sql, (client_id, stationcode))
    conn.commit()
    print(cursor.rowcount, "record inserted.")
    conn.close()
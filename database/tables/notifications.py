import mysql


def index(cursor):
    sql = '''CREATE TABLE IF NOT EXISTS NOTIFICATIONS(
    ID int AUTO_INCREMENT,
    CLIENT_ID VARCHAR(255) NOT NULL,
    STATION VARCHAR(5) NOT NULL,
    PRIMARY KEY (ID)
    )'''
    cursor.execute(sql)


def create(config, action, client_id, station):
    stationcode = station['stationCode']
    import pandas as pd
    conn = mysql.connector.connect(user=config['database']['username'], password=config['database']['password'],
                                   host=config['database']['host'], port=config['database']['port'],
                                   database=config['database']['database'])
    cursor = conn.cursor()
    searchnotification = pd.read_sql(f"SELECT * FROM NOTIFICATIONS WHERE STATION = '{stationcode}' AND CLIENT_ID = '{client_id}'", conn)
    if action == 'subscribe':
        sql = "INSERT INTO NOTIFICATIONS (CLIENT_ID, STATION) VALUES (%s, %s)"
        if searchnotification.values.any():
            message = f"Client already has a notification set on station {station['name']}"
        else:
            cursor.execute(sql, (client_id, stationcode))
            conn.commit()
            message = f"Subscribed to notifications for station {station['name']}"
    elif action == 'unsubscribe':
        if searchnotification.values.any():
            sql = f"DELETE FROM NOTIFICATIONS WHERE CLIENT_ID = '{client_id}' AND STATION = '{stationcode}'"
            cursor.execute(sql)
            conn.commit()
            message = f"Unsubscribed from notifications for station {station['name']}"
        else:
            message = f"No notification found for station {station['name']}"
    conn.close()
    return message


def find_users(config, stationcode):
    import pandas as pd
    conn = mysql.connector.connect(user=config['database']['username'], password=config['database']['password'],
                                   host=config['database']['host'], port=config['database']['port'],
                                   database=config['database']['database'])
    sql = f"SELECT CLIENT_ID FROM NOTIFICATIONS WHERE STATION = '{stationcode}'"
    users = pd.read_sql(sql, conn)
    conn.close()
    return users.values.tolist()

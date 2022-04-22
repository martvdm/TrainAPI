import mysql

def index(cursor):
    cursor.execute("DROP TABLE IF EXISTS NOTIFICATIONS")

    sql = '''CREATE TABLE NOTIFICATIONS(
    ID int AUTO_INCREMENT,
    CLIENT_ID VARCHAR(255) NOT NULL,
    STATION VARCHAR(5) NOT NULL,
    PRIMARY KEY (ID)
    )'''

    cursor.execute(sql)


async def create(config, ctx, client_id, stationcode):
    import pandas as pd
    conn = mysql.connector.connect(user=config['database']['username'], password=config['database']['password'], host=config['database']['host'], port=config['database']['port'], database=config['database']['database'])
    cursor = conn.cursor()
    sql = "INSERT INTO NOTIFICATIONS (CLIENT_ID, STATION) VALUES (%s, %s)"
    statement = pd.read_sql(f"SELECT * FROM NOTIFICATIONS WHERE STATION = '{stationcode}' AND CLIENT_ID = '{client_id}'", conn)
    if statement.values.any():
        await ctx.send(f"Client already has a notification set")
    else:
        cursor.execute(sql, (client_id, stationcode))
        conn.commit()
        message = f"Notification created for client {client_id} at station {stationcode}"
    conn.close()
    return message

def find_users(config,  stationcode):
    import warnings
    import pandas as pd
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
    conn = mysql.connector.connect(user=config['database']['username'], password=config['database']['password'], host=config['database']['host'], port=config['database']['port'], database=config['database']['database'])
    cursor = conn.cursor()
    sql = f"SELECT CLIENT_ID FROM NOTIFICATIONS WHERE STATION = '{stationcode}'"
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        users = pd.read_sql(sql, conn)
    conn.close()
    return users.values
def index(cursor):

    sql = '''CREATE TABLE IF NOT EXISTS TRIPS(
    ID FLOAT NOT NULL,
    CLIENT_ID FLOAT NOT NULL,
    CHANNEL_ID FLOAT NOT NULL,
    OWNER_ID FLOAT NOT NULL,
    ACTIVE BOOLEAN NOT NULL,
    CREATED_AT DATE NOT NULL
    )'''

    cursor.execute(sql)

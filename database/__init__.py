import mysql.connector
import os

def create_tables(config):
    conn = mysql.connector.connect(user=config['database']['username'], password=config['database']['password'], host=config['database']['host'], port=config['database']['port'], database=config['database']['database'])
    import database.tables.trips as trips
    import database.tables.notifications as notifications
    cursor = conn.cursor()
    trips.index(cursor)
    notifications.index(cursor)
    conn.close()
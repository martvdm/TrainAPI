import mysql.connector
import os

def connect(config):
    dbconfig = config['database']
    conn = mysql.connector.connect(user=dbconfig['user'], password=dbconfig['password'], host=dbconfig['host'], port=dbconfig['port'], database=dbconfig['database'])
    return conn

def create_tables(config):
    conn = connect(config)
    import database.tables.trips as trips
    import database.tables.notifications as notifications
    import database.tables.disruptions as disruptions
    cursor = conn.cursor()
    disruptions.index(cursor)
    trips.index(cursor)
    notifications.index(cursor)
    conn.close()

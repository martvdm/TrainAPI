import pandas as pd
import mysql


def index(cursor):
    sql = '''CREATE TABLE IF NOT EXISTS DISRUPTIONS(
    ID VARCHAR(255),
    SITUATION LONGTEXT
    )'''
    cursor.execute(sql)  # Create the table if it doesn't exist


def check_action(disruption, config):
    action = 'none'
    situation = disruption['timespans'][0]['situation']['label']
    conn = mysql.connector.connect(user=config['database']['username'], password=config['database']['password'],
                                   host=config['database']['host'], port=config['database']['port'],
                                   database=config['database']['database'])
    cursor = conn.cursor()
    search1 = f"SELECT * FROM DISRUPTIONS WHERE ID = '{disruption['id']}'"  # Check if the disruption is already in the database
    search2 = f"SELECT * FROM DISRUPTIONS WHERE ID = '{disruption['id']}' AND SITUATION = '{situation}'" # Check if the situation has changed
    if not pd.read_sql(search1, conn).index.values.any():  # If the disruption doesn't exist in the database
        sql = f"INSERT INTO DISRUPTIONS (ID, SITUATION) VALUES (%s, %s)"
        cursor.execute(sql, (disruption['id'], situation))  # Add the disruption to the database
        conn.commit()
        print(f"Added disruption {disruption['id']} to the database")
        action = 'new'
    elif not pd.read_sql(search2, conn).index.values.any():  # If the disruption exists but the situation is different
        sql = f"UPDATE DISRUPTIONS SET SITUATION = '{situation}' WHERE ID = '{disruption['id']}'"
        cursor.execute(sql)  # Update the situation
        conn.commit()
        print(f"Updated situation for disruption {disruption['id']}")
        action = 'update'
    else:
        pass  # If the disruption exists and the situation is the same, do nothing
        action = 'none'
    conn.close()
    return action

import mysql.connector

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port='3306',
            user='root',
            password='k2s54j7l',
            database='startup'
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

if __name__ == "__main__":
    db_connection = connect_to_db()
    if db_connection:
        db_connection.close()

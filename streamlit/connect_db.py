import mysql.connector
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            port='3306',
            user='root',
            password='141201',  # Root password set during secure installation
            database='startup',
            connect_timeout=5


        )
        if connection.is_connected():
            logger.info("Successfully connected to the database")
            return connection
    except mysql.connector.Error as err:
        logger.error(f"Database connection error: {err}")
        logger.info("Please ensure MariaDB is running and credentials are correct")
        return None


if __name__ == "__main__":
    db_connection = connect_to_db()
    if db_connection:
        try:
            cursor = db_connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            logger.info(f"Database version: {version[0]}")
            cursor.close()
        except Exception as e:
            logger.error(f"Error testing connection: {e}")
        finally:
            db_connection.close()
            logger.info("Database connection closed")

import psycopg2
from psycopg2 import sql
from policy_core.SupportUtils.secret_utils.config import Settings
from policy_core.SupportUtils.audit_utils.logging import logger

def get_db_config():
    """
    Retrieves database configuration from settings.
    """
    return {
        'user': Settings().POSTGRES_ADMIN_USER,
        'password': Settings().POSTGRES_ADMIN_PASSWORD,  # Replace with your actual password
        'host': Settings().POSTGRES_HOST,
        'port': Settings().POSTGRES_PORT,
        'dbname': Settings().POSTGRES_INSDB,
    }

def connect_to_db():
    """
    Establishes a connection to the PostgreSQL database and returns the connection and cursor.
    """
    try:
        db_config = get_db_config()
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        logger.info("Connectd to DB")
        return connection, cursor
    except Exception as error:
        logger.error(f"Error while connecting to PostgreSQL: {error}")
        return None, None

def close_db_connection(connection, cursor):
    """
    Closes the database connection and cursor.
    """
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    logger.info("PostgreSQL connection is closed")


if __name__ == "__main__":
    connection, cursor = connect_to_db()
    
    if cursor:
        #  database operations  using cursor
        # Example: cursor.execute("SELECT version();")
        
        # Close the connection when done
        close_db_connection(connection, cursor)

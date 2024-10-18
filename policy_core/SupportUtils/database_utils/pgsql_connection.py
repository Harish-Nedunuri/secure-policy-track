import asyncpg
from policy_core.SupportUtils.secret_utils.config import Settings
from policy_core.SupportUtils.audit_utils.logging import logger

async def get_db_config():
    """
    Retrieves database configuration from settings.
    """
    return {
        'user': Settings().POSTGRES_ADMIN_USER,
        'password': Settings().POSTGRES_ADMIN_PASSWORD,  
        'host': Settings().POSTGRES_HOST,
        'port': Settings().POSTGRES_PORT,
        'database': Settings().POSTGRES_INSDB,
    }

async def connect_to_db():
    """
    Asynchronously establishes a connection to the PostgreSQL database and returns the connection object.
    """
    try:
        db_config = await get_db_config()
        connection = await asyncpg.connect(**db_config)
        logger.info("Connected to DB")
        return connection
    except Exception as error:
        logger.error(f"Error while connecting to PostgreSQL: {error}")
        return None
    
async def close_db_connection(connection):
    """
    Asynchronously closes the database connection.
    """
    if connection:
        await connection.close()
        logger.info("PostgreSQL connection is closed")



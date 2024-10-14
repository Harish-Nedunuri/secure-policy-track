import pytest
import asyncio
from policy_core.SupportUtils.database_utils.pgsql_connection import connect_to_db, close_db_connection,get_db_config

@pytest.mark.asyncio
async def test_db_connection():
    connection = await connect_to_db()
    assert connection is not None, "Database connection failed"
    await close_db_connection(connection)



@pytest.mark.asyncio
async def test_db_config():
    db_config = await get_db_config()
    assert "user" in db_config, "Missing 'user' in DB config"
    assert "password" in db_config, "Missing 'password' in DB config"
    assert "host" in db_config, "Missing 'host' in DB config"
    assert "port" in db_config, "Missing 'port' in DB config"
    assert "database" in db_config, "Missing 'database' in DB config"



@pytest.mark.asyncio
async def test_db_query():
    connection = await connect_to_db()
    
    assert connection is not None, "Failed to connect to the database"
    
    try:
        result = await connection.fetch('SELECT 1')
        assert result[0]['?column?'] == 1, "Query did not return expected result"
    finally:
        await close_db_connection(connection)


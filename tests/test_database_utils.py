import pytest
from unittest import mock
import asyncpg
import asyncio
from policy_core.SupportUtils.database_utils.pgsql_connection import connect_to_db, close_db_connection

# Mock for asyncpg connection
@pytest.fixture
def mock_asyncpg_connect():
    # Correct the path to patch asyncpg.connect where it's used in your code
    with mock.patch("policy_core.SupportUtils.database_utils.pgsql_connection.asyncpg.connect") as mock_connect:
        yield mock_connect

# Given-When-Then: Test for successful connection (async version)
@pytest.mark.asyncio
async def test_connect_to_db_success(mock_asyncpg_connect):
    """
    GIVEN valid database configuration
    WHEN connect_to_db is called
    THEN it should return a connection
    """
    # Given
    mock_connection = mock.AsyncMock()
    mock_asyncpg_connect.return_value = mock_connection

    # When
    connection = await connect_to_db()

    # Then
    assert connection == mock_connection
    mock_asyncpg_connect.assert_called_once()  # Ensure connect was called once

# Given-When-Then: Test for failed connection (async version)
@pytest.mark.asyncio
async def test_connect_to_db_failure(mock_asyncpg_connect):
    """
    GIVEN invalid database configuration or error in connection
    WHEN connect_to_db is called
    THEN it should return None for connection
    """
    # Given
    mock_asyncpg_connect.side_effect = Exception("Connection failed")

    # When
    connection = await connect_to_db()

    # Then
    assert connection is None
    mock_asyncpg_connect.assert_called_once()  # Ensure connect was called once

# Given-When-Then: Test for closing the connection successfully (async version)
@pytest.mark.asyncio
async def test_close_db_connection_success():
    """
    GIVEN an open connection
    WHEN close_db_connection is called
    THEN it should close the connection
    """
    # Given
    mock_connection = mock.AsyncMock()

    # When
    await close_db_connection(mock_connection)

    # Then
    mock_connection.close.assert_called_once()

# Given-When-Then: Test for closing without a connection (async version)
@pytest.mark.asyncio
async def test_close_db_connection_no_connection():
    """
    GIVEN no connection
    WHEN close_db_connection is called
    THEN it should handle the absence of the connection without raising an error
    """
    # Given
    mock_connection = None

    # When
    await close_db_connection(mock_connection)

    # Then
    # Ensure connection.close() is not called because the connection is None

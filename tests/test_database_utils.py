import pytest
from unittest import mock
from policy_core.SupportUtils.database_utils.pgsql_crud import connect_to_db, close_db_connection

# Mock for psycopg2 connection
@pytest.fixture
def mock_psycopg2_connect():
    # Mocking psycopg2.connect in the context of where it's used
    with mock.patch("policy_core.SupportUtils.database_utils.pgsql_crud.psycopg2.connect") as mock_connect:
        yield mock_connect

# Given-When-Then: Test for successful connection
def test_connect_to_db_success(mock_psycopg2_connect):
    """
    GIVEN valid database configuration
    WHEN connect_to_db is called
    THEN it should return a connection and cursor
    """
    # Given
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()
    mock_psycopg2_connect.return_value = mock_connection
    mock_connection.cursor.return_value = mock_cursor

    # When
    connection, cursor = connect_to_db()

    # Then
    assert connection == mock_connection
    assert cursor == mock_cursor
    mock_psycopg2_connect.assert_called_once()  # Ensure connect was called once
    mock_connection.cursor.assert_called_once()  # Ensure cursor was called once

# Given-When-Then: Test for failed connection
def test_connect_to_db_failure(mock_psycopg2_connect):
    """
    GIVEN invalid database configuration or error in connection
    WHEN connect_to_db is called
    THEN it should return None for both connection and cursor
    """
    # Given
    mock_psycopg2_connect.side_effect = Exception("Connection failed")

    # When
    connection, cursor = connect_to_db()

    # Then
    assert connection is None
    assert cursor is None
    mock_psycopg2_connect.assert_called_once()  # Ensure connect was called once

# Given-When-Then: Test for closing the connection successfully
def test_close_db_connection_success():
    """
    GIVEN an open connection and cursor
    WHEN close_db_connection is called
    THEN it should close both the connection and cursor
    """
    # Given
    mock_connection = mock.Mock()
    mock_cursor = mock.Mock()

    # When
    close_db_connection(mock_connection, mock_cursor)

    # Then
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()

# Given-When-Then: Test for closing without a cursor
def test_close_db_connection_no_cursor():
    """
    GIVEN an open connection but no cursor
    WHEN close_db_connection is called
    THEN it should only close the connection and not raise an error for the cursor
    """
    # Given
    mock_connection = mock.Mock()
    mock_cursor = None

    # When
    close_db_connection(mock_connection, mock_cursor)

    # Then
    mock_connection.close.assert_called_once()
    # Ensure cursor.close() is not called

# Given-When-Then: Test for closing without a connection
def test_close_db_connection_no_connection():
    """
    GIVEN an open cursor but no connection
    WHEN close_db_connection is called
    THEN it should only close the cursor and not raise an error for the connection
    """
    # Given
    mock_connection = None
    mock_cursor = mock.Mock()

    # When
    close_db_connection(mock_connection, mock_cursor)

    # Then
    mock_cursor.close.assert_called_once()
    # Ensure connection.close() is not called

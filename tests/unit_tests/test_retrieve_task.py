
import pytest
from policy_core.RetrieveTask.src.retrieve_data_from_db import get_query_for_search  
import pytest
import asyncio
from decimal import Decimal
from datetime import date
from policy_core.RetrieveTask.src.retrieve_data_from_db import get_query_for_search
from policy_core.RetrieveTask.args import RetrieverTaskArgs
from policy_core.RetrieveTask.entry import RetrieverDataTask
from policy_core.SupportUtils.database_utils.pgsql_connection import connect_to_db, close_db_connection
from policy_core.SupportUtils.audit_utils.logging import logger

def normalize_query(query):
    """
    Helper function to remove excessive whitespaces, newlines, and indentation
    for easy comparison.
    """
    return " ".join(query.split())

def test_get_query_for_search_valid_criteria():
    # Given: valid search criteria and a row limit
    search_criteria = "policy_number"
    row_limit = 10
    
    # When: the function is called
    query = get_query_for_search(search_criteria, row_limit)
    
    # Normalize the query to remove unnecessary whitespace and make it easier to test
    normalized_query = normalize_query(query)
    
    # Then: it should return the correct SQL query containing the valid search criteria and row limit
    assert "WHERE TRIM(policy_number) ILIKE '%' || TRIM($1) || '%'" in normalized_query
    assert f"LIMIT {row_limit}" in normalized_query
    assert "FROM insurance.policies" in normalized_query
    assert "SELECT" in normalized_query

def test_get_query_for_search_invalid_criteria():
    # Given: invalid search criteria
    search_criteria = "invalid_column"
    row_limit = 10
    
    # When/Then: the function should raise a ValueError when called with an invalid search criteria
    with pytest.raises(ValueError) as exc_info:
        get_query_for_search(search_criteria, row_limit)
    
    # Then: the error message should mention "Invalid search criteria"
    assert "Invalid search criteria" in str(exc_info.value)

def test_get_query_for_search_check_row_limit():
    # Given: a valid search criteria and a specific row limit
    search_criteria = "full_name"
    row_limit = 5
    
    # When: the function is called with the given row limit
    query = get_query_for_search(search_criteria, row_limit)
    
    # Normalize the query to remove unnecessary whitespace and make it easier to test
    normalized_query = normalize_query(query)
    
    # Then: the query should contain the exact row limit in the LIMIT clause
    assert f"LIMIT {row_limit}" in normalized_query


@pytest.mark.asyncio
async def test_retrieve_data_by_criteria(mocker):
    # Given: Setup the arguments and mock the necessary external functions
    args = RetrieverTaskArgs(
        search_criteria="email",
        search_value="@gmail.com",
        row_limit=2
    )

    # Mock the database connection
    mock_connection = mocker.Mock()
    mocker.patch('policy_core.SupportUtils.database_utils.pgsql_connection.connect_to_db', return_value=mock_connection)
    mocker.patch('policy_core.SupportUtils.database_utils.pgsql_connection.close_db_connection')

    # Mock the fetch results from the connection using the provided mock data
    mock_record_1 = {
        'policy_number': 'POL-25761-2573', 'premium_amount': 4638.73, 'coverage_amount': 55111.14, 'status': 'cancelled',
        'start_date': '2022-04-20', 'end_date': '2025-07-28', 'full_name': 'William Richardson',
        'address': '741 Taylor Shoal Suite 151, Port Amymouth, PA 00974', 'email': 'elizabeth67@gmail.com',
        'phone_number': '(880)340-1251', 'type_name': 'Health', 'description': 'Covers medical expenses for illnesses, injuries, and preventive care.'
    }

    mock_record_2 = {
        'policy_number': 'POL-37208-6868', 'premium_amount': 3705.25, 'coverage_amount': 69442.15, 'status': 'expired',
        'start_date': '2020-02-24', 'end_date': '2025-04-26', 'full_name': 'Scott Fleming',
        'address': '97659 Peters Light, New Nicole, CO 44392', 'email': 'janice56@gmail.com', 'phone_number': '5332989928',
        'type_name': 'Business', 'description': 'Protects businesses from financial losses due to unforeseen events.'
    }
    
    mock_connection.fetch.return_value = [mock_record_1, mock_record_2]

    # Mock the get_query_for_search function
    mocker.patch('policy_core.RetrieveTask.src.retrieve_data_from_db.get_query_for_search', return_value="SELECT * FROM policies WHERE email LIKE $1 LIMIT $2")

    # When: Instantiate the RetrieverDataTask and call the function
    retriever_task = RetrieverDataTask(args)
    result = await retriever_task.retrieve_data_by_criteria()

    # Then: Validate the result
    expected_result = [
        {
            'policy_number': 'POL-25761-2573', 'premium_amount': 4638.73, 'coverage_amount': 55111.14, 'status': 'cancelled',
            'start_date': '2022-04-20', 'end_date': '2025-07-28', 'full_name': 'William Richardson',
            'address': '741 Taylor Shoal Suite 151, Port Amymouth, PA 00974', 'email': 'elizabeth67@gmail.com',
            'phone_number': '(880)340-1251', 'type_name': 'Health', 'description': 'Covers medical expenses for illnesses, injuries, and preventive care.'
        },
        {
            'policy_number': 'POL-37208-6868', 'premium_amount': 3705.25, 'coverage_amount': 69442.15, 'status': 'expired',
            'start_date': '2020-02-24', 'end_date': '2025-04-26', 'full_name': 'Scott Fleming',
            'address': '97659 Peters Light, New Nicole, CO 44392', 'email': 'janice56@gmail.com', 'phone_number': '5332989928',
            'type_name': 'Business', 'description': 'Protects businesses from financial losses due to unforeseen events.'
        }
    ]

    assert result == expected_result

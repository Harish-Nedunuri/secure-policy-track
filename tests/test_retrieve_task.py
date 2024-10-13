
import pytest
from policy_core.RetrieveTask.src.retrieve_data_from_db import get_query_for_search  

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

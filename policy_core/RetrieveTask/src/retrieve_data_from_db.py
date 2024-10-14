from policy_core.RetrieveTask.src.models import SearchCriteriaEnum
def get_query_for_search(search_criteria: str, row_limit: int):
    """
    Generates an SQL query that searches policies based on dynamic search criteria and limits the number of rows returned.
    
    Parameters:
    - search_criteria (str): The column to search by.
    - row_limit (int): The maximum number of rows to return.
    
    Returns:
    - query (str): The SQL query string with the search criteria, value, and row limit.
    """
    # Check if the search_criteria is part of the SearchCriteriaEnum
    if search_criteria not in SearchCriteriaEnum.__members__:
        valid_columns = ', '.join([e.value for e in SearchCriteriaEnum])
        raise ValueError(f"Invalid search criteria. Must be one of: {valid_columns}")
    
    
    # Construct the SQL query
    query = f"""
        SELECT
            p.policy_number,
            p.premium_amount,
            p.coverage_amount,
            p.status,
            p.start_date,
            p.end_date,
            ph.full_name,
            ph.address,
            ph.email,
            ph.phone_number,
            pt.type_name,
            pt.description
        FROM
            insurance.policies p
        INNER JOIN
            insurance.policyholders ph ON p.policyholder_id = ph.id
        INNER JOIN
            insurance.policy_types pt ON p.policy_type_id = pt.id
        WHERE TRIM({search_criteria}) ILIKE '%' || TRIM($1) || '%'
        LIMIT {row_limit}
    """
    return query

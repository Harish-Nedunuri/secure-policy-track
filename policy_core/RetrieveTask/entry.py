import asyncio
from policy_core.SupportUtils.audit_utils.logging import logger
from policy_core.SupportUtils.secret_utils.config import Settings
from policy_core.SupportUtils.database_utils.pgsql_connection import (connect_to_db,close_db_connection)
from policy_core.RetrieveTask.args import parse_arguments
from policy_core.RetrieveTask.src.retrieve_data_from_db import get_query_for_search

class RetrieverDataTask:
    def __init__(self, args):
        self.args = args
        self.settings = Settings()

    async def retrieve_data_by_criteria(self):
        """
        Retrieves data from policies, policyholders, and policy_types tables based on user-provided search criteria.
        
        :param search_criteria: The column name to filter the data on.
        :param search_value: The value to search for in the column.
        :return: Combined data from all three tables in JSON format.
        """
        connection = await connect_to_db()
        if not connection:
            return {}

        try:            
            # get query to execute
            query = get_query_for_search(self.args.search_criteria,self.args.row_limit)

            # Execute the query and fetch all results
            rows = await connection.fetch(query, self.args.search_value)

            # Define the column names to match the select statement
            columns = [
                "policy_number", "premium_amount", "coverage_amount", "status", 
                "start_date", "end_date", "full_name", "address", "email", 
                "phone_number", "type_name", "description"
            ]

            # Convert the rows into a list of dictionaries
            result = [dict(zip(columns, row)) for row in rows]

            # Return the result as JSON
            return result if result else {}
        
        except Exception as error:
            logger.error(f"Error while retrieving data: {error}")
            return {}
        finally:
            await close_db_connection(connection)

async def main():
    args = parse_arguments()   
    ret_instace =  RetrieverDataTask(args)  
    _ = await ret_instace.retrieve_data_by_criteria()
    logger.info(f"Retrieve Data Task Completed")
    

if __name__ == "__main__":    
    asyncio.run(main())
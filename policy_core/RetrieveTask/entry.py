import asyncio
from decimal import Decimal
from datetime import date
from policy_core.SupportUtils.audit_utils.logging import logger
from policy_core.SupportUtils.secret_utils.config import Settings
from policy_core.SupportUtils.database_utils.pgsql_connection import (connect_to_db,close_db_connection)
from policy_core.RetrieveTask.args import parse_arguments,RetrieverTaskArgs
from policy_core.RetrieveTask.src.retrieve_data_from_db import get_query_for_search

class RetrieverDataTask:
    def __init__(self, args):
        self.args = args
        self.settings = Settings()

    async def retrieve_data_by_criteria(self):
        connection = await connect_to_db()
        if not connection:
            return {}

        try:
            # Get query to execute
            query = get_query_for_search(self.args.search_criteria, self.args.row_limit)

            # Execute the query and fetch all results
            records = await connection.fetch(query, self.args.search_value)

            # Assuming 'records' is the list of <asyncpg.Record> objects
            records_list = []

            for record in records:
                record_dict = {}
                for key, value in record.items():
                    # Handle special cases like Decimal and date
                    if isinstance(value, Decimal):
                        record_dict[key] = float(value)  # Convert Decimal to float
                    elif isinstance(value, date):
                        record_dict[key] = value.isoformat()  # Convert date to ISO string
                    else:
                        record_dict[key] = value  # Use the value as it is for other types

                records_list.append(record_dict)

            # Return the result as JSON (move this outside the loop)
            return records_list if records_list else {}
            
        except Exception as error:
            logger.error(f"Error while retrieving data: {error}")
            return {}
        finally:
            if connection:
                await close_db_connection(connection)



async def main():
    # args = parse_arguments()   
    args = {
        "search_criteria": "email",
        "search_value": "@gmail.com",
        "row_limit": 2
    }
    args = RetrieverTaskArgs(**args)
    logger.info(f"Retrieve Data Task Started")
    ret_instace =  RetrieverDataTask(args)  
    result = await ret_instace.retrieve_data_by_criteria()
    print(result)
    logger.info(f"Retrieve Data Task Completed")
    

if __name__ == "__main__":    
    asyncio.run(main())
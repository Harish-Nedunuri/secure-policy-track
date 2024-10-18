from fastapi import Depends, HTTPException, status, Query
from fastapi.routing import APIRouter
from policy_core.RetrieveTask.args import RetrieverTaskArgs
from policy_core.RetrieveTask.entry import RetrieverDataTask
from policy_core.SupportUtils.security_utils.auth_routers import oauth2Scheme
from policy_core.RetrieveTask.src.models import  SearchCriteriaEnum

retrieve_router = APIRouter(
    prefix="/retrieve-data",
    tags=["Retrieve Data by Search Criteria"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2Scheme)]  
)

@retrieve_router.get('', status_code=status.HTTP_200_OK, description="Retrieve data based on search criteria")  
async def retrieve_data(
    search_criteria: SearchCriteriaEnum = Query(..., description="Select the search criteria"),
    search_value: str = Query(..., description="Provide the search value, e.g., 'POL-53709-2950' for policy_number or '@yahoo.com' for email"),
    row_limit: int = Query(10, description="Limit the number of rows returned to avoid poor latency")
):
    try:
        # Create the arguments object
        args = RetrieverTaskArgs(
            search_criteria=search_criteria,
            search_value=search_value,
            row_limit=row_limit
        )
        
        # Initialize and run the task
        ret_instance = RetrieverDataTask(args)
        response = await ret_instance.retrieve_data_by_criteria()
        
        # Assuming the response is a list of dictionaries, return it as-is
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Internal server error for unexpected issues

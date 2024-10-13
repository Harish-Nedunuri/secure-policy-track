from fastapi import Depends, HTTPException, status, Query
from fastapi.routing import APIRouter
from typing import List
from policy_core.RetreiveTask.args import RetreiverTaskArgs
from policy_core.RetreiveTask.entry import RetreiverDataTask
from policy_core.SupportUtils.security_utils.auth_routers import oauth2Scheme
from policy_core.RetreiveTask.src.models import RetriverResponse,SearchCriteriaEnum

retrive_router = APIRouter(
    prefix="/retreive-data",
    tags=["Retreive Data by Search Criteria"],
    responses={404: {"description": "Not found"}},
    dependencies={Depends(oauth2Scheme)}
)

@retrive_router.get('', status_code=status.HTTP_201_CREATED, description="Retrieve data based on search criteria")
async def retreive_data(
    search_criteria: SearchCriteriaEnum = Query(..., description="Select the search criteria from the dropdown"),
    search_value: str = Query(..., description="Provide the search value, e.g., 'POL-53709-2950' for policy_number or '@yahoo.com' for email"),
    row_limit: int = Query(10, description="Limit the number of rows returned to avoid poor latency")
):
    try:
        # Create the arguments object
        args = RetreiverTaskArgs(
            search_criteria=search_criteria,
            search_value=search_value,
            row_limit=row_limit
        )
        
        # Initialize and run the task
        ret_instance = RetreiverDataTask(args)
        response = await ret_instance.retrieve_data_by_criteria()
        print(type(response))
        # Assuming the response is a list of dictionaries, return it as-is
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

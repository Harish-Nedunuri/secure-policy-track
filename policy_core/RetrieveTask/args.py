from pydantic import BaseModel, Field
from policy_core.SupportUtils.package_utils.arguments_utils import ArgumentsUnpacker

class RetrieverTaskArgs(BaseModel):
    search_criteria: str = Field(description = "Select the attribute/column to search the policies by. Example policy_number,email")
    search_value: str = Field(description= "search value associated to the search criteria")
    row_limit: int = Field(default=10,description="Limit the rows to fetch")    
    
def parse_arguments() -> RetrieverTaskArgs:
    # This is for using the policy_core as pip package/ parse argument 
    parser = ArgumentsUnpacker(RetrieverTaskArgs)
    return parser.run()
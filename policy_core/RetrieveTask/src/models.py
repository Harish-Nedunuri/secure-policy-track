from pydantic import BaseModel
from typing import Optional
from enum import Enum

class SearchCriteriaEnum(str, Enum):
    policy_number = "policy_number"    
    status = "status"    
    full_name = "full_name"
    address = "address"
    email = "email"   
    type_name = "type_name"

    # TODO: use below columns for advanced search.     
        # premium_amount = "premium_amount"
        # coverage_amount = "coverage_amount" 
        # start_date = "start_date"
        # end_date = "end_date"  
        # phone_number = "phone_number"

class RetreiverResponse(BaseModel):
    policy_number: str
    premium_amount: float
    coverage_amount: float
    status: str
    start_date: str
    end_date: Optional[str] = None
    full_name: str
    address: str
    email: str
    phone_number: str
    type_name: str
    description: str

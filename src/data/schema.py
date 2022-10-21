from datetime import datetime
from typing import Dict, List, Optional, Union
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field


class UserData(BaseModel):
    id: Optional[UUID4] = Field(default_factory=uuid4)
    name: str
    mobile: int
    is_active: Optional[bool]
    created_at: Optional[datetime]
    last_updated_by: Optional[UUID4]
    last_updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class GroupData(BaseModel):
    id: Optional[UUID4] = Field(default_factory=uuid4)
    name: Optional[str]
    description: Optional[str]
    users: Optional[List[Union[UUID4, UserData]]]
    created_at: Optional[datetime]
    created_by: Optional[UUID4]
    last_updated_by: Optional[UUID4]
    last_updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class ExpenseCreate(BaseModel):
    id: Optional[UUID4] = Field(default_factory=uuid4)
    title: str
    description: Optional[str] 
    total_amount: int
    paid_by: UUID4
    group_id: Optional[UUID4]
    shares: Optional[Dict[UUID4, int]]
    created_at: Optional[datetime]
    created_by: Optional[UUID4]
    last_updated_by: Optional[UUID4]
    last_updated_at: Optional[datetime]

class ExpenseHistory(BaseModel):
    id: Optional[UUID4] = Field(default_factory=uuid4)
    title: str
    description: Optional[str] 
    total_amount: int
    paid_by: UUID4
    group_id: Optional[UUID4]
    shares: Optional[Dict[UUID4, int]]
    created_at: Optional[datetime]
    created_by: Optional[UUID4]
    last_updated_by: Optional[UUID4]
    last_updated_at: Optional[datetime]

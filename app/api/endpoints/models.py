from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class WalletInfoRequest(BaseModel):
    address: str = Field(..., example="TNPZ5QY86Jd8QBrR6jRj6UjJq7y1Z1fX1J")


class WalletInfoResponse(BaseModel):
    address: str
    trx_balance: float = Field(..., example=123.456)
    bandwidth: float = Field(..., example=1500.25)
    energy: float = Field(..., example=350.75)
    updated_at: datetime = Field(...)

class QueryRecord(WalletInfoResponse):
    id: int
    created_at: datetime


class QueryHistoryResponse(BaseModel):
    items: List[QueryRecord]
    total: int
    page: int
    pages: int


class PaginationQuery(BaseModel):
    offset: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)
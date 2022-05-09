from typing import Optional

from pydantic import BaseModel
import datetime


class AuthDetails(BaseModel):
    email: str
    password: str


class StockRequest(BaseModel):
    category: str
    broker: str
    ticker: str
    date: datetime.date
    operation: str
    qtd: int
    price: float
    wallet: str


class StocksResponse(BaseModel):
    id: int
    category: str
    broker: str
    ticker: str
    date: datetime.date
    operation: str
    qtd: int
    price: float
    wallet: Optional[str]

    class Config:
        orm_mode = True


class Patrimony(BaseModel):
    ticker: str
    qtd: int
    pm: float
    price: float

    # class Config:
    #     orm_mode = True


class Rentability(BaseModel):
    Date: datetime.datetime
    rentability: float

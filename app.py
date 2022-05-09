from typing import List, Tuple

import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from http import HTTPStatus
import logging

from python_stocks.auth import AuthHandler
from python_stocks.schemas import AuthDetails, StocksResponse, StockRequest, Patrimony, Rentability
from python_stocks.models import Users, Stocks
from python_stocks.finance import get_last_price, rentability

app = FastAPI()

auth = AuthHandler()


@app.post('/register/user', status_code=201)
async def register_user(auth_details: AuthDetails):
    if await Users.get_by_email(auth_details.email):
        raise HTTPException(status_code=400, detail="email is already in use")
    hashed_password = auth.get_password_hash(auth_details.password)
    obj = {"email": auth_details.email, "password": hashed_password}
    await Users.create(**obj)
    return


@app.post('/register/stock', status_code=201)
async def register_stock(stock_details: StockRequest, user_id=Depends(auth.auth_wrapper)):
    user = await Users.get(user_id)
    await Stocks.create(user=user, **stock_details.dict())
    return


@app.post('/login')
async def login(auth_details: AuthDetails):
    user = await Users.get_by_email(auth_details.email)
    if (user is None) or (not auth.verify_password(auth_details.password, user[0].password)):
        raise HTTPException(status_code=401, detail="invalid username or password")

    token = auth.encode_token(user[0].id)
    return {'token': token}


@app.get('/operations', response_model=List[StocksResponse])
async def operations(user_id=Depends(auth.auth_wrapper)):
    stocks = await Stocks.get_all(user_id)
    return stocks


@app.get('/patrimony', response_model=List[Patrimony])
async def patrimony(user_id=Depends(auth.auth_wrapper)):
    # Database Values
    stocks = await Stocks.get_patrimony(user_id)
    # Yfinance values
    ticker = [i.ticker + '.SA' for i in stocks]
    price = get_last_price(ticker)
    stocks = pd.DataFrame(stocks)
    price = pd.DataFrame(price)
    stocks['ticker'] = stocks['ticker'] + '.SA'

    return pd.merge(stocks, price, left_on='ticker', right_on='ticker').to_dict('records')


@app.get('/rentabilidade', response_model=List[Rentability])
async def rentabilidade(user_id=Depends(auth.auth_wrapper)):
    # database Values
    stocks = await Stocks.get_all(user_id)
    rent = rentability(stocks)
    return rent


@app.get('/health')
def health():
    return HTTPStatus.OK


@app.get('/error')
def error():
    logging.critical("forced error")
    return {"error": "logged"}


if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8001, workers=1, reload=True)

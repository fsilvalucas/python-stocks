import datetime

from pytest import fixture
from python_stocks.models import Users, Stocks, create_database, drop_database
from python_stocks.schemas import StockRequest
from fastapi.testclient import TestClient
from app import app
from faker import Faker

fake = Faker()


@fixture
async def create_and_drop():
    await create_database()
    yield  # Todos os testes vão acontecer aqui!
    await drop_database()


@fixture
def client() -> TestClient:
    client = TestClient(app)
    return client


@fixture
def client_and_token(client):
    body = {'email': 'lucas', 'password': 'lucas'}

    # _ = client.post('/register/user', json=body)
    r2 = client.post('/login', json=body)

    token = r2.json()['token']

    yield client, token


@fixture
def stock():
    return {
        'category': fake.pystr(),
        'broker': fake.pystr(),
        'ticker': fake.pystr(),
        'date': datetime.date.today(),
        'operation': 'C',
        'qtd': fake.pyint(),
        'price': abs(round(fake.pyfloat(), 2)),
        'wallet': fake.pystr()
    }


@fixture
def stocks():
    aux = []
    for i in range(15):
        aux.append({
            'category': fake.pystr(),
            'broker': fake.pystr(),
            'ticker': fake.pystr(),
            'date': datetime.date.today(),
            'operation': 'C',
            'qtd': fake.pyint(),
            'price': abs(round(fake.pyfloat(), 2)),
            'wallet': fake.pystr()
        })
    return aux


@fixture
def client_token_stocks(client_and_token, stocks):
    client, token = client_and_token

    auth = {'Authorization': f'Bearer {token}'}

    for i in stocks:
        _ = client.post('/register/stock', data=StockRequest(**i).json(), headers=auth)

    return client, token

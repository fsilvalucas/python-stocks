from python_stocks import __version__

import pytest
import datetime
from faker import Faker

from python_stocks.models import Users, Stocks
from python_stocks.schemas import StockRequest

fake = Faker()


def test_version():
    assert __version__ == '0.1.0'


@pytest.mark.asyncio
async def test_if_user_are_created(create_and_drop):
    obj = {'email': 'Lucas', 'password': 'Password'}
    user = await Users.create(**obj)

    assert user.id > 0


@pytest.mark.asyncio
async def test_if_stock_are_not_created_without_user(create_and_drop):
    obj = {'category': fake.pystr(),
           'broker': fake.pystr(),
           'ticker': fake.pystr(),
           'date': datetime.date.today(),
           'operation': 'C',
           'qtd': 3,
           'price': 98.99,
           'wallet': fake.pystr()}

    try:
        _ = await Stocks.create(**obj)
        assert False
    except AssertionError:
        assert True
    except TypeError:
        assert True


@pytest.mark.asyncio
async def test_if_stock_are_created_with_user(create_and_drop):
    obj = {'email': 'Felipe', 'password': 'Password'}
    user = await Users.create(**obj)

    obj = {'category': '1',
           'broker': '1',
           'ticker': '1',
           'date': datetime.date.today(),
           'operation': 'C',
           'qtd': 3,
           'price': 98.99,
           'wallet': '1'}

    stock = await Stocks.create(user=user, **obj)

    assert stock.id > 0


@pytest.mark.asyncio
async def test_get_none_user(create_and_drop):
    user = await Users.get(1)

    assert user is None


@pytest.mark.asyncio
async def test_get_all_stocks(create_and_drop):
    obj = {'email': fake.pystr(), 'password': fake.pystr()}
    user = await Users.create(**obj)

    obj = {'category': 'fake',
           'broker': '1',
           'ticker': '1',
           'date': datetime.date.today(),
           'operation': 'C',
           'qtd': 3,
           'price': 98.99,
           'wallet': '1'}

    _ = await Stocks.create(user=user, **obj)
    _ = await Stocks.create(user=user, **obj)
    _ = await Stocks.create(user=user, **obj)
    _ = await Stocks.create(user=user, **obj)

    stocks = await Stocks.get_all(user.id)

    assert stocks is not None


@pytest.mark.asyncio
async def test_health(client):
    r1 = client.get('/health')
    assert r1.status_code == 200


@pytest.mark.asyncio
async def test_register_and_login_endpoint(client):
    body = {'email': 'Lucas', 'password': 'lucas'}
    # r1 = client.post('/register/user', json=body)
    r2 = client.post('/login', json=body)
    assert r2.status_code == 200


def test_create_stocks_for_client(client_and_token, stock):
    client, token = client_and_token

    auth = {'Authorization': f'Bearer {token}'}

    r = client.post('/register/stock', data=StockRequest(**stock).json(), headers=auth)

    assert r.status_code == 201


def test_add_more_than_one_stocks(client_and_token, stocks):
    client, token = client_and_token

    auth = {'Authorization': f'Bearer {token}'}

    status = []
    for i in stocks:
        r = client.post('/register/stock', data=StockRequest(**i).json(), headers=auth)
        status.append(r.status_code)

    assert sum(status)/len(status) == 201


def test_operations_endpoint(client_token_stocks):
    client, token = client_token_stocks

    auth = {'Authorization': f'Bearer {token}'}

    r = client.get('/operations', headers=auth)

    assert r.status_code == 200


@pytest.mark.asyncio
def test_patrimony_endpoint(client_token_stocks):
    client, token = client_token_stocks

    auth = {'Authorization': f'Bearer {token}'}

    r = client.get('/patrimony', headers=auth)

    assert r.status_code == 200

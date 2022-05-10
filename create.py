from dotenv import load_dotenv

load_dotenv()

from python_stocks.models import create_database
import asyncio

asyncio.run(create_database())

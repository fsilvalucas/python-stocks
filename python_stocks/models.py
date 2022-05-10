from __future__ import annotations

import asyncio
import os
from sqlalchemy import Column, String, Integer, VARCHAR, Date, Numeric, ForeignKey, Float
from sqlalchemy import update, delete, func, case, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref


# URL_do_banco = 'sqlite+aiosqlite:///db.db'
URL_do_banco = 'mysql+aiomysql://{0}:{1}@{2}/{3}'.format(
    os.environ.get('userdb'),
    os.environ.get('passwordb'),
    os.environ.get('hostdb'),
    os.environ.get('database'),
)

engine = create_async_engine(URL_do_banco)

session = sessionmaker(
    engine,
    expire_on_commit=False,
    future=True,
    class_=AsyncSession
)

Base = declarative_base()


class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    password = Column(String(300), nullable=False)

    # stocks = relationship("Stocks", backref="Users", cascade="all, delete",
    #                       passive_deletes=True)

    def __repr__(self):
        return f"(id: {self.id} - user: {self.email})"

    @classmethod
    async def create(cls, **kwargs) -> Users:  # Change return for an interface
        async with session() as s:
            obj_instantiate = cls(**kwargs)
            s.add(obj_instantiate)
            try:
                await s.commit()
            except Exception:
                await s.rollback()
                raise
            return obj_instantiate

    @classmethod
    async def update(cls, obj_id, **kwargs) -> Users:
        async with session() as s:
            try:
                await s.execute(
                    update(cls)
                        .where(cls.id == obj_id)
                        .values(**kwargs)
                        .execution_options(synchronize_session="fetch")
                )
                await s.commit()
                return await Users.get(obj_id)
            except Exception:
                await s.rollback()
                raise

    @classmethod
    async def get(cls, obj_id) -> Users:
        async with session() as s:
            query = select(cls).where(cls.id == obj_id)
            users = await s.execute(query)
            user = users.scalar()
            return user

    @classmethod
    async def get_by_email(cls, email) -> Users:
        async with session() as s:
            query = select(cls).where(cls.email == email)
            users = await s.execute(query)
            user = users.first()
            s.close_all()
            return user

    @classmethod
    async def delete(cls, obj_id):
        async with session() as s:
            query = delete(cls).where(cls.id == obj_id)
            await s.execute(query)
            try:
                await s.commit()
            except Exception:
                await s.rollback()
                raise
            return True


class Stocks(Base):
    __tablename__ = 'Stocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(VARCHAR(length=15), nullable=False)
    broker = Column(VARCHAR(length=15), nullable=False)
    ticker = Column(VARCHAR(length=6), nullable=False)
    date = Column(Date, nullable=False)
    operation = Column(VARCHAR(length=1, ), nullable=False)
    qtd = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    wallet = Column(VARCHAR(length=10))

    user_id = Column(Integer, ForeignKey('Users.id', ondelete="CASCADE"))
    user = relationship('Users', backref="Stocks")

    def __repr__(self):
        return f'Stock(id:{self.id} - user_id: {self.user_id} - wallet: {self.wallet} - ticker: {self.ticker}' \
               f' - date: {self.date})'

    @property
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    async def create(cls, user: Users, **kwargs) -> Stocks:  # Change return for an interface
        async with session() as s:
            obj_instantiate = cls(user=user, **kwargs)
            s.add(obj_instantiate)
            try:
                await s.commit()
            except Exception:
                await s.rollback()
                raise
            return obj_instantiate

    @classmethod
    async def update(cls, obj_id, **kwargs) -> Stocks:
        async with session() as s:
            try:
                await s.execute(
                    update(cls)
                        .where(cls.id == obj_id)
                        .values(**kwargs)
                        .execution_options(synchronize_session="fetch")
                )
                await s.commit()
                return await cls.get(obj_id)
            except Exception:
                await s.rollback()
                raise

    @classmethod
    async def get(cls, obj_id):
        async with session() as s:
            query = select(cls).where(cls.id == obj_id)
            users = await s.execute(query)
            stocks = users.first()
            return stocks

    @classmethod
    async def get_all(cls, user_id):
        async with session() as s:
            query = select(cls).where(cls.user_id == user_id)
            stocks = await s.execute(query)
            return stocks.scalars().all()

    @classmethod
    async def get_patrimony(cls, user_id):
        async with session() as s:
            query = f"""
            SELECT 
    ticker,
    SUM(CASE 
        WHEN operation = 'C' THEN qtd
        WHEN operation = 'V' THEN -qtd
        END) AS qtd,
        
    SUM(CASE 
        WHEN operation = 'C' THEN qtd*price
        WHEN operation = 'V' THEN -(qtd*price)
        END)/
    SUM(CASE 
        WHEN operation = 'C' THEN qtd
        WHEN operation = 'V' THEN -qtd
        END) AS pm
        
FROM 
    Stocks
WHERE 
    user_id = {user_id}
GROUP BY
    ticker, wallet
HAVING
    qtd > 0;
            """
            rst = await s.execute(query)

            return rst.all()

    @classmethod
    async def delete(cls, obj_id):
        async with session() as s:
            query = delete(cls).where(cls.id == obj_id)
            await s.execute(query)
            try:
                await s.commit()
            except Exception:
                await s.rollback()
                raise
            return True


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# asyncio.run(drop_database())
# asyncio.run(create_database())

# asyncio.run(Stocks.get_patrimonio(1))

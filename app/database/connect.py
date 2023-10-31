#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   app/database/connect.py
@Time    :   2023/10/31 12:46:16
@Author  :   WhaleFall
@License :   (C)Copyright 2020-2023, WhaleFall
@Desc    :  SQLAlchemy 数据库连接
"""


from typing import AsyncIterator, AsyncGenerator  # 异步迭代器 异步生成器
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)

from app.utils import logger
from app.config import settings

# reference: https://fastapi.tiangolo.com/tutorial/sql-databases/#note
# is needed only for SQLite. It's not needed for other databases.
# connect_args={"check_same_thread": False}

# SQL ERROR: QueuePool limit of size <x> overflow <y> reached, connection timed out, timeout <z>
# https://docs.sqlalchemy.org/en/20/errors.html#connections-and-transactions

async_engine = create_async_engine(
    url=settings.DATABASE_URI,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True,  # 表示在每个连接被使用之前，会自动发送一个"ping"来检查连接的有效性。这样可以避免使用无效的连接。
    pool_recycle=600,  # 连接在被放回连接池之前，会被回收并重新创建，以避免连接长时间处于打开状态导致的问题。
    pool_size=30,  # 指定了连接池中的最大连接数，即最多可以同时处理的数据库连接数
    max_overflow=100,  # 指定了在达到 pool_size 上限后，可以额外创建的连接数。这样可以应对短时间内的连接请求高峰。
    future=True,  # 异步支持
)

# 在引擎初始化时指定 echo=True 将使我们能够在控制台中看到生成的 SQL 查询。
# expire_on_commit=False 禁用会话的“提交时过期”行为。这是因为在异步设置中，我们不希望 SQLAlchemy 在访问已提交的对象时向数据库发出新的 SQL 查询。
AsyncSessionMaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    async_engine, expire_on_commit=False
)


# FastAPI Dependent
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        yield session

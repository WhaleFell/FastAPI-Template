#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   app/database/crud.py
@Time    :   2023/10/31 12:47:02
@Author  :   WhaleFall
@License :   (C)Copyright 2020-2023, WhaleFall
@Desc    :   数据库 CRUD
"""

from .connect import AsyncSessionMaker
from .model import User
from typing import Optional, List, Sequence, Union

# sqlalchemy type
from sqlalchemy import (
    ForeignKey,
    func,
    select,
    update,
    String,
    DateTime,
)

from sqlalchemy.ext.asyncio import AsyncSession


async def getUserByID(session: AsyncSession, user_id: int) -> Optional[User]:
    result = await session.get(User, ident=user_id)
    return result


async def registerUser(session: AsyncSession, user: User) -> Optional[User]:
    """注册用户,并返回注册后的用户"""
    session.add(user)
    await session.commit()
    # 刷新（以便它包含数据库中的任何新数据，例如生成的 ID）。
    # reference: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-data
    await session.refresh(user)
    return user


async def dumpUsers(session: AsyncSession) -> Union[Sequence[User], List]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def authenticateUser(
    session: AsyncSession, username: str, password: str
) -> Union[bool, User]:
    """验证一个用户
    authenticate /ɔːˈθen.tɪ.keɪt/ v. 验证
    """
    result = await session.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()
    if user:
        if user.password == password:
            return user

    return False

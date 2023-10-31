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


class UserCrud:
    """储存 users 表的 CRUD"""

    @staticmethod
    async def getUserByID(
        session: AsyncSession, user_id: int
    ) -> Optional[User]:
        result = await session.get(User, ident=user_id)
        return result

    @staticmethod
    async def getUserByName(
        session: AsyncSession, username: str
    ) -> Optional[User]:
        result = await session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def registerUser(
        session: AsyncSession, username: str, password: str
    ) -> Optional[User]:
        """提供账号密码注册用户 返回用户对象 如果用户名存在就 raise"""

        existUser = await UserCrud.getUserByName(session, username=username)
        if existUser:
            raise Exception(
                f"The username{username} is exist 已经存在的用户名:{username}"
            )

        user = User(username=username, password=password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def dumpUsers(session: AsyncSession) -> Union[Sequence[User], List]:
        result = await session.execute(select(User))
        return result.scalars().all()

    @staticmethod
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

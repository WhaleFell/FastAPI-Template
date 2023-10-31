#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   app/routers/user.py
@Time    :   2023/10/31 13:21:26
@Author  :   WhaleFall
@License :   (C)Copyright 2020-2023, WhaleFall
@Desc    :   

处理用户登陆, security、jwt 相关的路由
JWT means "JSON Web Tokens".
"""


"""
Reference:

Annotated 参数:
- https://fastapi.tiangolo.com/tutorial/body-multiple-params/#singular-values-in-body

OAuth2 validate security:
- https://fastapi.tiangolo.com/tutorial/security/
"""

from fastapi import APIRouter, HTTPException, status
from fastapi import Query, Body, Depends, Form
from typing_extensions import Annotated
from typing import List, Optional, Union, Dict
from datetime import timedelta, datetime

from app.schemas import User, TokenData, BaseResp
from app.config import settings
from app.utils import logger

# database
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.crud import UserCrud
from app.database.connect import get_session

# security n.安全
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt


router = APIRouter()

# oauth2_schema depend instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


# oauth2_schema sub-dependency -- get_current_user
# 根据 Token 获取当前的用户
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> User:
    # authorization error
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.OAUTH2_SECRET, algorithms=[settings.ALGORITHM]
        )
        username: Optional[str] = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = await UserCrud.getUserByName(
        session=db, username=token_data.username
    )
    if user is None:
        raise credentials_exception
    return User.model_validate(user)


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None
) -> str:
    """创建一个 token 传入 data 和 expire 获取 token"""
    to_encode = data.copy()  # deep copy
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)  # 15 分钟后过期
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.OAUTH2_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


@router.post("/token/")
async def login_for_access_token(
    username: Annotated[str, Body()],
    password: Annotated[str, Body()],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> BaseResp[Dict]:
    """登录并获取 token"""
    user = await UserCrud.authenticateUser(
        session=db, username=username, password=password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = create_access_token(
        data=TokenData(username=username).model_dump(),
        expires_delta=access_token_expires,
    )
    return BaseResp(
        code=1,
        msg="Token获取成功!",
        data={"access_token": access_token, "token_type": "bearer"},
    )


@router.post("/register/", tags=["user"])
async def register(
    username: Annotated[str, Body(title="用户名", description="注册的用户名")],
    password: Annotated[
        str, Body(title="明文密码", description="明文密码 show password")
    ],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> BaseResp[User]:
    """注册用户并返回注册后的用户对象"""
    user = await UserCrud.registerUser(
        session=db, username=username, password=password
    )

    return BaseResp(
        code=1, msg=f"{username} 注册成功", data=User.model_validate(user)
    )


@router.get("/me/", description="获取已经登陆的用户")
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)]
) -> BaseResp[User]:
    """获取已经登陆的用户"""
    return BaseResp(
        code=1, msg=f"当前已登录{current_user.username}!", data=current_user
    )

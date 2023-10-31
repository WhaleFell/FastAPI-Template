#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   app/register/router.py
@Time    :   2023/10/31 12:52:50
@Author  :   WhaleFall
@License :   (C)Copyright 2020-2023, WhaleFall
@Desc    :   注册路由
"""

from fastapi import FastAPI
from app.routers import index, user


def register_router(app: FastAPI):
    """注册路由"""

    # app.include_router(
    #     public.router, prefix=settings.API_PREFIX, tags=["Public"]
    # )

    app.include_router(index.router, tags=["index"])
    app.include_router(user.router, tags=["user"], prefix="/user")

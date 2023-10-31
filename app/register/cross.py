#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   app/register/cors.py
@Time    :   2023/10/31 12:51:16
@Author  :   WhaleFall
@License :   (C)Copyright 2020-2023, WhaleFall
@Desc    :   处理跨域 Cross 请求
"""


from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.config import settings


def register_cors(app: FastAPI):
    """跨域请求 -- https://fastapi.tiangolo.com/zh/tutorial/cors/"""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

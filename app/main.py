#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   main.py
@Time    :   2023/10/31 13:00:39
@Author  :   WhaleFall
@License :   (C)Copyright 2020-2023, WhaleFall
@Desc    :   FastAPI Main run.
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager


from app.database import init_table
from app.config import settings
from app.register import (
    register_cors,
    register_router,
    register_exception,
    register_middleware,
)
from app.utils import logger


# I.ni.tia.lize /[ɪˈnɪʃ(ə)lˌaɪz/ database 初始化数据库
# fastapi lifespan 生命周期 https://fastapi.tiangolo.com/advanced/events/
@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app start 应用开始前执行
    logger.success("Before app start")
    yield
    # after app stop 应用结束后执行
    logger.success("After app stop")


app = FastAPI(
    description=settings.PROJECT_DESC,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
)

# register
register_cors(app)  # 注册跨域请求
register_router(app)  # 注册路由
register_exception(app)  # 注册异常捕获
register_middleware(app)  # 注册请求响应拦截


logger.info("The FastAPI Start Success!")


if __name__ == "__main__":
    # Optimize Python Aysncio
    # to fix: ValueError: too many file descriptors in select()
    # reference: https://blog.csdn.net/qq_36759224/article/details/123084133
    import sys

    if sys.platform == "win32":
        from asyncio import (
            ProactorEventLoop,
            set_event_loop,
            get_event_loop,
        )
        from uvicorn import Config, Server

        set_event_loop(ProactorEventLoop())
        server = Server(
            config=Config(app=app, host="127.0.0.1", port=8000, workers=16)
        )
        get_event_loop().run_until_complete(server.serve())

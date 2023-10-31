#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   app/schema/__init__.py
@Time    :   2023/10/31 12:45:47
@Author  :   WhaleFall
@License :   (C)Copyright 2020-2023, WhaleFall
@Desc    :   schemas 响应数据模型
"""


from .connect import async_engine
from .model import Base, User
from app.utils.custom_log import logger


async def init_table(is_drop: bool = True):
    """创建 database 下的所有表"""
    if is_drop:
        await drop_table()
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.success("Create Database Table Sccuess!")
    except Exception as e:
        logger.error(f"Create Database Table ERROR{e}")


async def drop_table():
    """删除 database 下的所有表"""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        logger.success("Drop Database All Table Success!")
    except Exception as e:
        logger.error(f"Drop Database Table ERROR{e}")

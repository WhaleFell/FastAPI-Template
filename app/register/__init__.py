#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   app/register/__init__.py
@Time    :   2023/10/31 12:50:11
@Author  :   WhaleFall
@License :   (C)Copyright 2020-2023, WhaleFall
@Desc    :   FastAPI register 全局注册
"""


from .cross import register_cors
from .router import register_router
from .exception import register_exception
from .middleware import register_middleware

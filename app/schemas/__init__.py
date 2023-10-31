#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
@File    :   app/schema/__init__.py
@Time    :   2023/10/31 12:58:12
@Author  :   WhaleFall
@License :   (C)Copyright 2020-2023, WhaleFall
@Desc    :   

储存 Pydantic 的模型
注意要和 SQLAlchemy 数据库ORM模型分开
"""


from .base import BaseResp
from .user import Token, User, TokenData

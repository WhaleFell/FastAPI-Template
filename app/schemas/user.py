#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# schemas/user.py
# User 模型

from .base import BaseResp
from pydantic import Field, BaseModel, ConfigDict
from datetime import datetime


class User(BaseModel):
    id: int = Field(description="数据库生成的 ID")
    username: str = Field(description="用户名")
    password: str = Field(description="密码")
    create_at: datetime = Field(description="注册时间")

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

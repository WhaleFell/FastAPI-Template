#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# schemas/user.py
# User 模型

from typing import Any, Dict, Optional, Union
from typing_extensions import Annotated, Doc
from pydantic import Field, BaseModel, ConfigDict
from datetime import datetime
from fastapi import HTTPException, status


class AuthenticateError(HTTPException):
    """用户登陆/验证/注册 错误"""

    def __init__(
        self,
        detail: Any = None,
    ) -> None:
        super().__init__(
            status.HTTP_401_UNAUTHORIZED, detail, {"WWW-Authenticate": "Bearer"}
        )


class User(BaseModel):
    id: int = Field(description="数据库生成的 ID")
    username: str = Field(description="用户名")
    password: str = Field(description="密码")
    create_at: datetime = Field(description="注册时间")

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str

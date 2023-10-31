#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# schemas/base.py
# API 基模型

from pydantic import BaseModel, Field
from typing import Optional, Any
from pydantic import ConfigDict

# Pydantic Generic Type 泛型
# reference:
# 1. https://blog.csdn.net/qq_45668004/article/details/113730684
# 2. https://docs.pydantic.dev/2.4/concepts/models/#generic-models
from typing import Generic, TypeVar

T = TypeVar("T")


class BaseResp(BaseModel, Generic[T]):
    code: int = Field(default=1, description="响应状态码 1 true 正常 | 0 false 错误")
    msg: Optional[str] = Field(default=None, description="响应信息")

    data: Optional[T] = None

    # Pydantic V2 changes
    # https://docs.pydantic.dev/latest/migration/#changes-to-config
    # class Config:
    # no only trying to get the id value from a dict
    # also try to get it from an attribute,
    # id = data["id"] 或者 id = data.id
    model_config = ConfigDict(from_attributes=True)

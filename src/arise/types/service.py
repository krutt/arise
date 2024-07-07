#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/types/service.py
# VERSION:     0.1.0
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List, Literal

### Third-party packages ###
from pydantic import BaseModel, StrictStr


class Service(BaseModel):
  command: List[StrictStr] = []
  env_vars: List[StrictStr] = []
  image: StrictStr
  ports: List[StrictStr]


ServiceName = Literal["arise-bitcoind"]

__all__ = ("Service", "ServiceName")

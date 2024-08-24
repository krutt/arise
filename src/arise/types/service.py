#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/types/service.py
# VERSION:     0.1.3
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, List, Literal
from typing_extensions import Annotated

### Third-party packages ###
from pydantic import BaseModel, Field, StrictStr

PortMapping = Annotated[StrictStr, Field(pattern=r"^\d{1,5}:\d{1,5}$")]


class Service(BaseModel):
  command: Dict[int, StrictStr] = {}
  env_vars: List[StrictStr] = []
  image: StrictStr
  ports: List[PortMapping]


ServiceName = Literal[
  "arise-bitcoind", "arise-mainnet", "arise-signet", "arise-testnet", "arise-testnet4"
]

__all__ = ("PortMapping", "Service", "ServiceName")

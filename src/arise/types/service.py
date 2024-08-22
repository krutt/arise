#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/types/service.py
# VERSION:     0.1.1
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, List, Literal

### Third-party packages ###
from pydantic import BaseModel, StrictStr


class Service(BaseModel):
  command: Dict[int, StrictStr] = {}
  env_vars: List[StrictStr] = []
  image: StrictStr
  ports: List[StrictStr]


ServiceName = Literal[
  "arise-bitcoind", "arise-mainnet", "arise-signet", "arise-testnet", "arise-testnet4"
]

__all__ = ("Service", "ServiceName")

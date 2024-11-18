#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/types/build_enum.py
# VERSION:     0.2.2
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, Literal

from pydantic import BaseModel, StrictStr


class Build(BaseModel):
  instructions: Dict[int, StrictStr]
  platform: StrictStr = "linux/amd64"


BuildEnum = Literal[
  "arise-bitcoind",
  "arise-electrs",
  "arise-mainnet",
  "arise-mariadb",
  "arise-mempool",
  "arise-mutiny-web",
  "arise-signet",
  "arise-testnet",
]


__all__ = ("Build", "BuildEnum")

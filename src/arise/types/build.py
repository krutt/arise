#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/types/build_enum.py
# VERSION:     0.1.0
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import List, Literal

from pydantic import BaseModel, StrictStr


class Build(BaseModel):
  instructions: List[StrictStr]
  platform: StrictStr = "linux/amd64"


BuildEnum = Literal["arise-bitcoind"]


__all__ = ("Build", "BuildEnum")

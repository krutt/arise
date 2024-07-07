#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/configs.py
# VERSION:     0.1.0
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from pathlib import Path
from typing import Any, Dict, Optional

### Standard packages ###
from pydantic import TypeAdapter
from yaml import Loader, load

### Local modules ###
from arise.types import Build, BuildEnum, Service, ServiceName

BUILDS: Dict[BuildEnum, Build]
CLUSTERS: Dict[ServiceName, Service]
NETWORK: str

file_path: Path = Path(__file__).resolve()
with open(str(file_path).replace("configs.py", "schemas.yml"), "rb") as stream:
  schema: Optional[Dict[str, Any]] = load(stream, Loader=Loader)
  if schema:
    BUILDS = TypeAdapter(Dict[BuildEnum, Build]).validate_python(schema["builds"])
    CLUSTERS = TypeAdapter(Dict[ServiceName, Service]).validate_python(schema["clusters"])
    NETWORK = schema.get("network", "arise")

__all__ = ("BUILDS", "CLUSTERS", "NETWORK")

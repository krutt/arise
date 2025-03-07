#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/clean.py
# VERSION:     0.2.3
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import match
from typing import List

### Third-party packages ###
from click import option
from docker import DockerClient, from_env
from docker.errors import DockerException, NotFound
from docker.models.containers import Container
from docker.models.networks import Network
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from arise.configs import NETWORK


@option("--inactive", help="Query inactive containers for removal.", is_flag=True, type=bool)
def clean(inactive: bool) -> None:
  """
  Remove containers with baring "arise-" prefix, drop network.

  Options:
    * --inactive (bool) if present, targets both active and inactive or stopped containers.
  """
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  outputs: List[str] = []
  containers: List[Container] = client.containers.list(all=inactive)
  for container in track(containers, f"Clean {('active','all')[inactive]} containers:".ljust(42)):
    if match(r"^arise-*", container.name) is not None:
      container.stop()
      container.remove(v=True)  # if `v` is true, remove associated volume
      outputs.append(f"<Container '{ container.name }'> removed.")
  try:
    network: Network = client.networks.get(NETWORK)
    network.remove()
    outputs.append(f"<Network '{ NETWORK }'> removed.")
  except NotFound:
    pass
  list(map(rich_print, outputs))


__all__ = ("clean",)

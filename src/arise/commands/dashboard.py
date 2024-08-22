#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/mine.py
# VERSION:     0.1.1
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
from click import command
from docker import DockerClient, from_env
from docker.errors import DockerException, NotFound
from docker.models.containers import Container
from rich import print as rich_print

### Local modules ###
from arise.shadows import Bellion


@command
def dashboard() -> None:
  """Dashboard for checking current state of images deployed."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to daemon.")
    return

  ### Retrieve bitcoind container ###
  bitcoind: Container
  try:
    bitcoind = client.containers.get("arise-bitcoind")
  except NotFound:
    rich_print('[red bold]Unable to find "arise-bitcoind" container.')
    return

  ### Retrieve other containers ###
  arise_containers: List[Container] = list(
    filter(lambda container: match(r"arise-*", container.name), reversed(client.containers.list()))
  )
  container_names: List[str] = list(map(lambda container: container.name, arise_containers))
  bellion: Bellion = Bellion(
    bitcoind=bitcoind,
    containers=arise_containers,
    container_index=0,
    container_names=container_names,
  )
  bellion.display()


__all__ = ("dashboard",)

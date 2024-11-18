#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/mine.py
# VERSION:     0.2.2
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
from docker.errors import DockerException
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

  daemon: Container
  try:
    daemon = next(
      filter(
        lambda container: match(r"arise-(mainnet|signet|testnet)", container.name),
        reversed(client.containers.list()),
      )
    )
  except StopIteration:
    rich_print("[red bold] Cannot find active daemon.")
    return

  ### Retrieve other containers ###
  arise_containers: List[Container] = list(
    filter(lambda container: match(r"arise-*", container.name), reversed(client.containers.list()))
  )
  container_names: List[None | str] = list(map(lambda container: container.name, arise_containers))
  bellion: Bellion = Bellion(
    containers=arise_containers,
    container_index=0,
    container_names=[name for name in container_names if name is not None],
    daemon=daemon,
  )
  bellion.display()


__all__ = ("dashboard",)

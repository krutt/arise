#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/pull.py
# VERSION:     0.2.2
# CREATED:     2024-01-01 01:48
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Dict, List, Set

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import DockerException
from rich import print as rich_print

### Local modules ###
from arise.configs import BUILDS


@command
@option("--electrs", is_flag=True, help="Build arise-electrs image", type=bool)
@option("--mainnet", is_flag=True, help="Build arise-mainnet image", type=bool)
@option("--mariadb", is_flag=True, help="Build arise-mariadb image", type=bool)
@option("--mempool", is_flag=True, help="Build arise-mempool image", type=bool)
@option("--mutiny-web", is_flag=True, help="Build arise-mutiny-web image", type=bool)
@option("--signet", is_flag=True, help="Build arise-signet image", type=bool)
@option("--testnet", is_flag=True, help="Build arise-testnet image", type=bool)
def pull(
  electrs: bool,
  mainnet: bool,
  mariadb: bool,
  mempool: bool,
  mutiny_web: bool,
  signet: bool,
  testnet: bool,
) -> None:
  """Pull core and peripheral images from GitHub container registry."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  image_names: List[str] = list(
    map(
      lambda image: image.tags[0].split(":")[0],
      filter(lambda image: len(image.tags) != 0, client.images.list()),
    )
  )
  pull_select: Dict[str, bool] = {
    "arise-bitcoind": False,  # exclude base-image
    "arise-electrs": electrs,
    "arise-mainnet": mainnet,
    "arise-mariadb": mariadb,
    "arise-mempool": mempool,
    "arise-mutiny-web": mutiny_web,
    "arise-signet": signet,
    "arise-testnet": testnet,
  }

  ### Checks if specified images had been built previously ###
  outputs: List[str] = []
  built: Set[str] = {tag for tag in BUILDS.keys() if pull_select[tag] and tag in image_names}
  outputs += map(lambda tag: f"<Image: '{tag}'> already exists in local docker images.", built)
  list(map(rich_print, outputs))


__all__ = ("pull",)

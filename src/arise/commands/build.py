#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/build.py
# VERSION:     0.2.2
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from io import BytesIO
from typing import Dict, List, Set

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import BuildError, DockerException
from rich import print as rich_print

### Local modules ###
from arise.configs import BUILDS
from arise.shadows import Igris
from arise.types import Build


@command
@option("--electrs", is_flag=True, help="Build arise-electrs image", type=bool)
@option("--mainnet", is_flag=True, help="Build arise-mainnet image", type=bool)
@option("--mariadb", is_flag=True, help="Build arise-mariadb image", type=bool)
@option("--mempool", is_flag=True, help="Build arise-mempool image", type=bool)
@option("--mutiny-web", is_flag=True, help="Build arise-mutiny-web image", type=bool)
@option("--signet", is_flag=True, help="Build arise-signet image", type=bool)
@option("--testnet", is_flag=True, help="Build arise-testnet image", type=bool)
def build(
  electrs: bool,
  mainnet: bool,
  mariadb: bool,
  mempool: bool,
  mutiny_web: bool,
  signet: bool,
  testnet: bool,
) -> None:
  """Build peripheral images for the desired cluster."""
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
  build_select: Dict[str, bool] = {
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
  built: Set[str] = {tag for tag in BUILDS.keys() if build_select[tag] and tag in image_names}
  outputs += map(lambda tag: f"<Image: '{tag}'> already exists in local docker images.", built)
  list(map(rich_print, outputs))

  builds: Dict[str, Build] = {
    tag: build for tag, build in BUILDS.items() if build_select[tag] and tag not in image_names
  }
  build_count: int = len(builds.keys())
  if build_count != 0:
    builds_items = builds.items()
    with Igris(row_count=10) as igris:
      task_id: int = igris.add_task("", progress_type="primary", total=build_count)
      for tag, build in builds_items:
        build_task_id: int = igris.add_task(tag, progress_type="build", total=100)
        with BytesIO("\n".join(build.instructions.values()).encode("utf-8")) as fileobj:
          try:
            igris.progress_build(  # type: ignore[misc]
              client.api.build(
                decode=True, fileobj=fileobj, gzip=True, platform=build.platform, rm=True, tag=tag
              ),
              build_task_id,
            )
          except BuildError:
            igris.update(build_task_id, completed=0)
          igris.update(build_task_id, completed=100)
          igris.update(task_id, advance=1)
      igris.update(task_id, completed=build_count, description="[blue]Complete[reset]")


__all__ = ("build",)

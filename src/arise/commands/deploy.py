#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/deploy.py
# VERSION:     0.1.1
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
# from io import BytesIO
from typing import Dict, List

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import APIError, DockerException
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from arise.configs import NETWORK, SERVICES
from arise.types import Service, ServiceName


@command
@option("--mainnet", is_flag=True, type=bool)
@option("--signet", is_flag=True, type=bool)
@option("--testnet", is_flag=True, type=bool)
@option("--testnet4", is_flag=True, type=bool)
def deploy(mainnet: bool, signet: bool, testnet: bool, testnet4: bool) -> None:
  """Deploy cluster."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  selector: Dict[ServiceName, bool] = {
    "arise-bitcoind": False,  # exclude base-image
    "arise-mainnet": mainnet,
    "arise-signet": signet,
    "arise-testnet": testnet,
    "arise-testnet4": testnet4,
  }
  service_name: ServiceName = "arise-mainnet"
  try:
    service_name = next(filter(lambda value: value[1], selector.items()))[0]
  except StopIteration:
    pass
  service: Service = SERVICES[service_name]
  ports: Dict[str, str] = dict(
    map(lambda item: (item[0], item[1]), [port.split(":") for port in service.ports])
  )
  command: List[str] = list(service.command.values())

  ### Attempts to create network if not exist ###
  try:
    client.networks.create(NETWORK, check_duplicate=True)
  except APIError:
    pass

  ### Deploy specified cluster ###
  client.containers.run(
    service.image,
    command=command,
    detach=True,
    environment=service.env_vars,
    name=service_name,
    network=NETWORK,
    ports=ports,
  )

  ### Build missing image if any ###
  # builds: Dict[str, Build] = {
  #   tag: build for tag, build in BUILDS.items() if selector[tag] and tag not in image_names
  # }
  # build_count: int = len(builds.keys())
  # if build_count != 0:
  #   builds_items = builds.items()
  #   with Igris(row_count=10) as igris:
  #     task_id: int = igris.add_task("", progress_type="primary", total=build_count)
  #     for tag, build in builds_items:
  #       build_task_id: int = igris.add_task(tag, progress_type="build", total=100)
  #       with BytesIO("\n".join(build.instructions).encode("utf-8")) as fileobj:
  #         try:
  #           igris.progress_build(  # type: ignore[misc]
  #             client.api.build(
  #               decode=True, fileobj=fileobj, platform=build.platform, rm=True, tag=tag
  #             ),
  #             build_task_id,
  #           )
  #         except BuildError:
  #           igris.update(
  #             build_task_id,
  #             completed=0,
  #             description=f"[red bold]Build unsuccessful for <Image '{tag}'>.",
  #           )
  #         igris.update(
  #           build_task_id,
  #           completed=100,
  #           description=f"[blue]Built <[bright_magenta]Image [green]'{tag}'[reset]> successfully.",
  #         )
  #         igris.update(task_id, advance=1)
  #     igris.update(task_id, completed=build_count, description="[blue]Complete")


__all__ = ("deploy",)

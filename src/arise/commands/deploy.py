#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/deploy.py
# VERSION:     0.1.3
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
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

  ### Attempts to create network if not exist ###
  try:
    client.networks.create(NETWORK, check_duplicate=True)
  except APIError:
    pass

  ### Deploy specified service ###
  for _ in track(range(1), f"Deploy { service_name }".ljust(42)):
    flags: List[str] = list(service.command.values())
    ports: Dict[str, int] = {port.split(":")[0]: int(port.split(":")[1]) for port in service.ports}
    client.containers.run(
      service.image,
      command=flags,
      detach=True,
      environment=service.env_vars,
      name=service_name,
      network=NETWORK,
      ports=ports,  # type: ignore
    )



__all__ = ("deploy",)

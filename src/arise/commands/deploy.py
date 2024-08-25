#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/deploy.py
# VERSION:     0.1.4
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
from arise.types import Chain, Service, ServiceName


@command
@option("--mainnet", cls=Chain, is_flag=True, type=bool, variants=("signet", "testnet", "testnet4"))
@option("--signet", cls=Chain, is_flag=True, type=bool, variants=("mainnet", "testnet", "testnet4"))
@option("--testnet", cls=Chain, is_flag=True, type=bool, variants=("mainnet", "signet", "testnet4"))
@option("--testnet4", cls=Chain, is_flag=True, type=bool, variants=("mainnet", "signet", "testnet"))
@option("--with-electrs", is_flag=True, type=bool)
def deploy(mainnet: bool, signet: bool, testnet: bool, testnet4: bool, with_electrs: bool) -> None:
  """Deploy cluster."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return

  network_select: Dict[ServiceName, bool] = {
    "arise-bitcoind": False,  # exclude base-image
    "arise-electrs": False, # exclude peripheral arise-electrs
    "arise-mainnet": mainnet,
    "arise-signet": signet,
    "arise-testnet": testnet,
    "arise-testnet4": testnet4,
  }
  daemon_name: ServiceName = "arise-mainnet"
  try:
    daemon_name = next(filter(lambda value: value[1], network_select.items()))[0]
  except StopIteration:
    pass
  daemon: Service = SERVICES[daemon_name]

  ### Attempts to create network if not exist ###
  try:
    client.networks.create(NETWORK, check_duplicate=True)
  except APIError:
    pass

  for _ in track(range(1), f"Deploy { daemon_name }".ljust(42)):
    flags: List[str] = list(daemon.command.values())
    ports: Dict[str, int] = {port.split(":")[0]: int(port.split(":")[1]) for port in daemon.ports}
    client.containers.run(
      daemon.image,
      command=flags,
      detach=True,
      environment=service.env_vars,
      name=service_name,
      network=NETWORK,
      ports=ports,  # type: ignore
    )


__all__ = ("deploy",)

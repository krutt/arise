#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/deploy.py
# VERSION:     0.2.2
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from time import sleep
from typing import Dict, List, Tuple

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
@option("--mainnet", cls=Chain, is_flag=True, type=bool, variants=("signet", "testnet"))
@option("--signet", cls=Chain, is_flag=True, type=bool, variants=("mainnet", "testnet"))
@option("--testnet", cls=Chain, is_flag=True, type=bool, variants=("mainnet", "signet"))
@option("--with-electrs", is_flag=True, type=bool)
@option("--with-mempool", is_flag=True, type=bool)
@option("--with-mutiny-web", is_flag=True, type=bool)
def deploy(
  mainnet: bool,
  signet: bool,
  testnet: bool,
  with_electrs: bool,
  with_mempool: bool,
  with_mutiny_web: bool,
) -> None:
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
    "arise-mainnet": mainnet,
    "arise-signet": signet,
    "arise-testnet": testnet,
  }
  daemon_name: ServiceName = "arise-mainnet"
  try:
    daemon_name = next(filter(lambda value: value[1], network_select.items()))[0]
  except StopIteration:
    pass
  daemon: Service = SERVICES[daemon_name]

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
      environment=daemon.env_vars,
      name=daemon_name,
      network=NETWORK,
      ports=ports,  # type: ignore
    )

  middleware_select: Dict[ServiceName, bool] = {"arise-mariadb": with_mempool}
  middlewares: List[Tuple[ServiceName, Service]] = [
    (key, value)
    for key, value in SERVICES.items()
    if value.service_type == "middleware" and middleware_select[key]
  ]
  for name, middleware in track(middlewares, f"Deploy middleware services".ljust(42)):
    flags: List[str] = list(middleware.command.values())
    ports: Dict[str, int] = {p.split(":")[0]: int(p.split(":")[1]) for p in middleware.ports}
    client.containers.run(
      middleware.image,
      command=flags,
      detach=True,
      environment=middleware.env_vars,
      name=name,
      network=NETWORK,
      ports=ports,  # type: ignore
    )

  peripheral_select: Dict[ServiceName, bool] = {
    "arise-electrs": with_electrs,
    "arise-mempool": with_mempool,
    "arise-mutiny-web": with_mutiny_web,
  }
  peripherals: List[Tuple[ServiceName, Service]] = [
    (key, value)
    for key, value in SERVICES.items()
    if value.service_type == "peripheral" and peripheral_select[key]
  ]
  for name, peripheral in track(peripherals, f"Deploy peripheral services".ljust(42)):
    flags: List[str] = list(peripheral.command.values())
    environment: List[str] = peripheral.env_vars
    if name == "arise-electrs":
      if daemon_name == "arise-mainnet":
        flags.append("--cookie-file=/home/bitcoin/.bitcoin/.cookie")
        flags.append("--daemon-p2p-addr=arise-mainnet:8333")
        flags.append("--daemon-rpc-addr=arise-mainnet:8332")
      elif daemon_name == "arise-signet":
        flags.append("--cookie-file=/home/bitcoin/.bitcoin/.cookie")
        flags.append("--daemon-p2p-addr=arise-signet:38333")
        flags.append("--daemon-rpc-addr=arise-signet:38332")
        flags.append("--network=signet")
      elif daemon_name == "arise-testnet":
        flags.append("--cookie-file=/home/bitcoin/.bitcoin/.cookie")
        flags.append("--daemon-p2p-addr=arise-testnet:18333")
        flags.append("--daemon-rpc-addr=arise-testnet:18332")
        flags.append("--network=testnet")
      sleep(1)  # wait for authentication cookie to be generated
    elif name == "arise-mempool":
      if daemon_name == "arise-mainnet":
        environment += ["CORE_RPC_HOST=arise-mainnet", "CORE_RPC_PORT=8332"]
      elif daemon_name == "arise-signet":
        environment += ["CORE_RPC_HOST=arise-signet", "CORE_RPC_PORT=38332"]
      elif daemon_name == "arise-testnet":
        environment += ["CORE_RPC_HOST=arise-testnet", "CORE_RPC_PORT=18332"]
      sleep(15)  # wait for arise-mariadb
    ports: Dict[str, int] = {p.split(":")[0]: int(p.split(":")[1]) for p in peripheral.ports}
    client.containers.run(
      peripheral.image,
      command=flags,
      detach=True,
      environment=environment,
      name=name,
      network=NETWORK,
      ports=ports,  # type: ignore
      volumes_from=[daemon_name],
    )


__all__ = ("deploy",)

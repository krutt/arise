#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/deploy.py
# VERSION:     0.1.0
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from io import BytesIO
from typing import Dict, List

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import APIError, BuildError, DockerException, ImageNotFound
from rich import print as rich_print
from rich.progress import track

### Local modules ###
from arise.configs import BUILDS, CLUSTERS, NETWORK
from arise.types import Build, MutexOption, NewAddress, Service, ServiceName
from arise.views import Yggdrasil


@command
@option("--cat", alternatives=["duo", "ohm", "uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--duo", alternatives=["cat", "ohm", "uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--ohm", alternatives=["cat", "duo", "uno"], cls=MutexOption, is_flag=True, type=bool)
@option("--uno", alternatives=["cat", "duo", "ohm"], cls=MutexOption, is_flag=True, type=bool)
@option("--with-cashu-mint", is_flag=True, help="Deploy cashu-mint peripheral service", type=bool)
@option("--with-lnd-krub", is_flag=True, help="Deploy lnd-krub peripheral service", type=bool)
@option("--with-ord-server", is_flag=True, help="Deploy ord-server peripheral service", type=bool)
@option("--with-postgres", is_flag=True, help="Deploy postgres peripheral service", type=bool)
@option("--with-redis", is_flag=True, help="Deploy redis peripheral service", type=bool)
def deploy(
  cat: bool,
  duo: bool,
  ohm: bool,
  uno: bool,
  with_cashu_mint: bool,
  with_lnd_krub: bool,
  with_ord_server: bool,
  with_postgres: bool,
  with_redis: bool,
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

  ### Defaults to duo network; Derive cluster information from parameters ###
  selector: Dict[ServiceName, bool] = {"cat": cat, "duo": duo, "ohm": ohm, "uno": uno}
  cluster_name: ServiceName = "duo"
  try:
    cluster_name = next(filter(lambda value: value[1], selector.items()))[0]
  except StopIteration:
    pass
  cluster: Dict[ServiceName, Service] = CLUSTERS[cluster_name]

  ### Attempts to create network if not exist ###
  try:
    client.networks.create(NETWORK, check_duplicate=True)
  except APIError:
    pass

  ### Deploy specified cluster ###
  for name, service in track(cluster.items(), f"Deploy { cluster_name } cluster:".ljust(42)):
    client.containers.run(
      service.image,
      command=service.command,
      detach=True,
      environment=service.env_vars,
      name=name,
      network=NETWORK,
      ports=ports,
    )

  ### Define selection for shared-volume peripherals ###
  selector = {
    "bitcoind-cat": False,
    "cashu-mint": with_cashu_mint,
    "lnd-krub": with_lnd_krub and with_postgres and with_redis,
    "ord-server": with_ord_server,
    "postgres": False,
    "redis": False,
  }

  ### Build missing images if any for shared-volume peripherals ###
  image_names: List[str] = list(
    map(
      lambda image: image.tags[0].split(":")[0],
      filter(lambda image: len(image.tags) != 0, client.images.list()),
    )
  )
  builds: Dict[str, Build] = {
    tag: build for tag, build in BUILDS.items() if selector[tag] and tag not in image_names
  }
  build_count: int = len(builds.keys())
  if build_count != 0:
    builds_items = builds.items()
    with Yggdrasil(row_count=10) as yggdrasil:
      task_id: int = yggdrasil.add_task("", progress_type="primary", total=build_count)
      for tag, build in builds_items:
        build_task_id: int = yggdrasil.add_task(tag, progress_type="build", total=100)
        with BytesIO("\n".join(build.instructions).encode("utf-8")) as fileobj:
          try:
            yggdrasil.progress_build(  # type: ignore[misc]
              client.api.build(
                decode=True, fileobj=fileobj, platform=build.platform, rm=True, tag=tag
              ),
              build_task_id,
            )
          except BuildError:
            yggdrasil.update(
              build_task_id,
              completed=0,
              description=f"[red bold]Build unsuccessful for <Image '{tag}'>.",
            )
          yggdrasil.update(
            build_task_id,
            completed=100,
            description=f"[blue]Built <[bright_magenta]Image [green]'{tag}'[reset]> successfully.",
          )
          yggdrasil.update(task_id, advance=1)
      yggdrasil.update(task_id, completed=build_count, description="[blue]Complete")

  ### Deploy shared volume peripherals ###
  run_errors: List[str] = []
  peripherals = {f"arise-{k}": v[f"arise-{k}"] for k, v in PERIPHERALS.items() if selector[k]}  # type: ignore[index, misc]
  volume_target: str = "arise-ping" if duo else "arise-lnd"
  for name, service in track(peripherals.items(), "Deploy shared-volume peripherals:".ljust(42)):
    ports = dict(map(lambda item: (item[0], item[1]), [port.split(":") for port in service.ports]))
    volume_target = "arise-bitcoind" if name == "arise-ord" else volume_target
    try:
      client.containers.run(
        service,
        command=service.command,
        detach=True,
        environment=service.env_vars,
        name=name,
        network=NETWORK,
        ports=ports,
        volumes_from=[volume_target],
      )
    except ImageNotFound:
      run_errors.append(
        f"<[bright_magenta]Image [green]'{ service }'[reset]> [red]is not found.[reset]"
      )
  list(map(rich_print, run_errors))

  ### Show warnings ###
  warnings: List[str] = []
  list(map(rich_print, warnings))


__all__ = ("deploy",)

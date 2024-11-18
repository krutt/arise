#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/auth.py
# VERSION:     0.2.2
# CREATED:     2024-01-01 01:48
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from os import getenv, path
from re import findall
from typing import Dict, List, Optional, Tuple

### Third-party packages ###
from click import argument, command, option
from docker import DockerClient, from_env
from docker.errors import DockerException
from rich import print as rich_print


@command
@argument("rpcuser", required=False)
@argument("dbuser", required=False)
@argument("dbpass", required=False)
@option("--bash", is_flag=True, help="Persist authentications in .bashrc", type=bool)
@option("--zsh", is_flag=True, help="Persist authentications in .zshrc", type=bool)
def auth(
  bash: bool, dbpass: Optional[str], dbuser: Optional[str], rpcuser: Optional[str], zsh: bool
) -> None:
  """Persist authentications in desired run-control file."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return
  shell_select: Dict[str, bool] = {"/bin/bash": bash, "/bin/zsh": zsh}
  shell: str = getenv("SHELL", "/bin/bash")
  try:
    shell = next(filter(lambda value: value[1], shell_select.items()))[0]
  except StopIteration:
    pass
  outputs: List[str] = []
  rc_path: str = {"/bin/bash": "~/.bashrc", "/bin/zsh": "~/.zshrc"}[shell]
  keys: Tuple[str, ...] = ("ARISE_AUTH_DBPASS", "ARISE_AUTH_DBUSER", "ARISE_AUTH_RPCUSER")
  write_count: int = 0
  for key, value in zip(keys, (dbpass, dbuser, rpcuser)):
    authenticated: bool = False
    if getenv(key, None) is not None:
      authenticated = True
    else:
      with open(path.expanduser(rc_path), "r") as rc_readonly:
        found: List[str] = findall(f"export { key }=", rc_readonly.read())
        authenticated = len(found) != 0
    if authenticated:
      outputs.append(f"[yellow]{ key } is already authenticated![reset]")
      continue
    if value is not None:
      with open(path.expanduser(rc_path), "a") as rc_output:
        rc_output.write(f"export { key }={ value }\n")
        write_count += 1
  if write_count > 0:
    outputs.append("[green]Success!")
    outputs.append(f"In order to activate authentication, run the following command:")
    outputs.append(f"    [blue]source { path.expanduser(rc_path) }[reset]")
  list(map(rich_print, outputs))


__all__ = ("auth",)

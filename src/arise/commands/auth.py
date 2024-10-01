#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/auth.py
# VERSION:     0.2.1
# CREATED:     2024-01-01 01:48
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from os import getenv, path
from re import findall
from typing import Dict, List

### Third-party packages ###
from click import argument, command, option
from docker import DockerClient, from_env
from docker.errors import DockerException
from rich import print as rich_print


@command
@argument("rpcuser", nargs=1)
@option("--bash", is_flag=True, help="Persist authentications in .bashrc", type=bool)
@option("--fish", is_flag=True, help="Persist authentications in .fishrc", type=bool)
@option("--zsh", is_flag=True, help="Persist authentications in .zshrc", type=bool)
def auth(bash: bool, fish: bool, rpcuser: str, zsh: bool) -> None:
  """Persist authentications in desired run-control file."""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return
  shell_select: Dict[str, bool] = {"/bin/bash": bash, "/bin/fish": fish, "/bin/zsh": zsh}
  shell: str = getenv("SHELL", "/bin/bash")
  try:
    shell = next(filter(lambda value: value[1], shell_select.items()))[0]
  except StopIteration:
    pass
  # TODO: validate rpcuser
  rc_path: str = {"/bin/bash": "~/.bashrc", "/bin/fish": "~/.fishrc", "/bin/zsh": "~/.zshrc"}[shell]
  authenticated: bool = False
  if getenv("ARISE_AUTH_RPCUSER", None) is not None:
    authenticated = True
  else:
    with open(path.expanduser(rc_path), "r") as rc_readonly:
      found: List[str] = findall(r"export ARISE_AUTH_RPCUSER=", rc_readonly.read())
      authenticated = len(found) != 0
  if authenticated:
    rich_print("[yellow]Already authenticated![reset]")
    return
  if rpcuser is not None:
    with open(path.expanduser(rc_path), "a") as rc_output:
      rc_output.write(f"export ARISE_AUTH_RPCUSER={ rpcuser }\n")
  rich_print("[green]Success!")
  rich_print(f"In order to activate authentication, run the following command:")
  rich_print(f"    [blue]source { path.expanduser(rc_path) }[reset]")


__all__ = ("auth",)

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

### Third-party packages ###
from click import command, option
from docker import DockerClient, from_env
from docker.errors import DockerException
from rich import print as rich_print


@command
@option("--bash", is_flag=True, help="Persist authentications in .bashrc", type=bool)
@option("--fish", is_flag=True, help="Persist authentications in .fishrc", type=bool)
@option("--zsh", is_flag=True, help="Persist authentications in .zshrc", type=bool)
def auth(bash: bool, fish: bool, zsh: bool) -> None:
  """Persist authentications in desired run-control file or currently active shell's run-control"""
  client: DockerClient
  try:
    client = from_env()
    if not client.ping():
      raise DockerException
  except DockerException:
    rich_print("[red bold]Unable to connect to docker daemon.")
    return



__all__ = ("auth",)

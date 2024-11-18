#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/core.py
# VERSION:     0.2.2
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from click import group

### Local modules ###
from arise.commands import auth, build, clean, dashboard, deploy, pull


@group
def cli() -> None:
  """arise"""


cli.add_command(auth, "auth")
cli.add_command(build, "build")
cli.add_command(clean, "clean")
cli.add_command(dashboard, "dashboard")
cli.add_command(deploy, "deploy")
cli.add_command(pull, "pull")


if __name__ == "__main__":
  cli()

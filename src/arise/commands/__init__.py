#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/commands/__init__.py
# VERSION:     0.2.2
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Local modules ###
from arise.commands.auth import auth
from arise.commands.build import build
from arise.commands.clean import clean
from arise.commands.dashboard import dashboard
from arise.commands.deploy import deploy
from arise.commands.pull import pull

__all__ = ("auth", "build", "clean", "dashboard", "deploy", "pull")

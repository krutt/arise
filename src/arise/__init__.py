#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/__init__.py
# VERSION:     0.2.3
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION: https://www.w3docs.com/snippets/python/what-is-init-py-for.html
#
# HISTORY:
# *************************************************************

### Local modules ###
from arise.commands import auth, build, clean, deploy, dashboard, pull

__all__ = ("auth", "build", "clean", "dashboard", "deploy", "pull")

__version__ = "0.2.3"

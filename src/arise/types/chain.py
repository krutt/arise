#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/types/chain.py
# VERSION:     0.2.3
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from typing import Any, List, Mapping, Tuple

### Third-party packages ###
from click import Context, Option, UsageError


class Chain(Option):
  def __init__(self, *args: Any, **kwargs: Any) -> None:
    self.variants: list = kwargs.pop("variants")
    assert self.variants, "'variants' parameter required."
    kwargs["help"] = (
      kwargs.get("help", "") + f"Option is mutually exclusive with {', '.join(self.variants)}."
    ).strip()
    super(Chain, self).__init__(*args, **kwargs)

  def handle_parse_result(
    self, ctx: Context, opts: Mapping[str, Any], args: List[str]
  ) -> Tuple[Any, List[str]]:
    current_opt: bool = self.name in opts
    for mutex_option in self.variants:
      if mutex_option in opts:
        if current_opt:
          raise UsageError(
            f"Illegal usage: '{self.name}' is mutually exclusive with '{mutex_option}'."
          )
        else:
          self.prompt = None
    return super(Chain, self).handle_parse_result(ctx, opts, args)


__all__ = ("Chain",)

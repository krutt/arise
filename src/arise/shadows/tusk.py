#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/florent/views/flame.py
# VERSION:     0.2.2
# CREATED:     2024-08-30 20:16
# AUTHOR:      Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from math import floor
from random import choice, random
from typing import ClassVar, List, Literal, get_args

### Third-party packages ###
from apscheduler.schedulers.background import BackgroundScheduler
from pydantic import BaseModel, ConfigDict, StrictInt
from rich.console import RenderableType
from rich.text import Text

HellFire = Literal[
  " ",
  ",",
  ";",
  "+",
  "l",
  "t",
  "g",
  "t",
  "i",
  "!",
  "l",
  "I",
  "?",
  "/",
  "\\",
  "|",
  ")",
  "(",
  "1",
  "}",
  "{",
  "]",
  "[",
  "r",
  "c",
  "v",
  "z",
  "j",
  "f",
  "t",
  "J",
  "U",
  "O",
  "Q",
  "o",
  "c",
  "x",
  "f",
  "X",
  "h",
  "q",
  "w",
  "W",
  "B",
  "8",
  "&",
  "%",
  "$",
  "#",
  "@",
]


class Tusk(BaseModel):
  model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)  # type: ignore[misc]
  pixels: List[HellFire] = []
  ### Dimensions ###
  height: StrictInt
  width: StrictInt
  ### Split layouts ###
  scheduler: ClassVar[BackgroundScheduler] = BackgroundScheduler()

  def model_post_init(self, _) -> None:
    self.scheduler.add_job(self.update, "interval", seconds=0.25)
    self.scheduler.start()
    for _ in range(self.height * self.width):
      self.pixels.append(" ")

  @property
  def renderable(self) -> RenderableType:
    chars: str = "".join(self.pixels)
    fire: str = "\n".join(
      [
        chars[i + 2 : i + self.width - 2]
        for i in range(self.width, self.width * (self.height - 1), self.width)
      ]
    )
    return Text.assemble(fire)

  def update(self) -> None:
    fire_chars = get_args(HellFire)
    for _ in range(self.width - 2):
      index: int = 2 + int(random() * (self.width - 2)) + (self.width * (self.height - 2))
      self.pixels[index] = choice(fire_chars)
    offset: int = 1 + (self.width * (self.height - 3))
    for i in range(self.width - 2):
      snuff: bool = int(random() * 10) <= 5
      self.pixels[i + offset] = " " if snuff else self.pixels[i + offset]
    for i in range(self.width * (self.height - 2)):
      average_value = (
        int(
          fire_chars.index(self.pixels[i])
          + fire_chars.index(self.pixels[i + 1])
          + fire_chars.index(self.pixels[i + self.width])
          + fire_chars.index(self.pixels[i + self.width + 1])
        )
        / 4
      )
      self.pixels[i] = fire_chars[floor(average_value)]


__all__ = ("Tusk",)

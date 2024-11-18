#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/types/difficulty_adjustment.py
# VERSION:     0.2.2
# CREATED:     2024-09-04 00:56
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Third-party packages ###
from pydantic import BaseModel, Field, StrictFloat, StrictInt


class DifficultyAdjustment(BaseModel):
  adjusted_time_average: StrictInt = Field(alias="adjustedTimeAvg")
  difficulty_change: StrictFloat = Field(alias="difficultyChange")
  estimated_retarget_date: StrictInt = Field(alias="estimatedRetargetDate")
  next_retarget_height: StrictInt = Field(alias="nextRetargetHeight")
  previous_retarget: StrictFloat = Field(alias="previousRetarget")
  remaining_blocks: StrictFloat = Field(alias="remainingBlocks")
  remaining_time: StrictFloat = Field(alias="remainingTime")
  time_average: StrictInt = Field(alias="timeAvg")
  time_offset: StrictInt = Field(alias="timeOffset")


__all__ = ("DifficultyAdjustment",)

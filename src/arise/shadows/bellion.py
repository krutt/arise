#!/usr/bin/env python3.8
# coding:utf-8
# Copyright (C) 2024 All rights reserved.
# FILENAME:    ~~/src/arise/shadows/bellion.py
# VERSION:     0.2.2
# CREATED:     2024-07-07 16:11
# AUTHOR:      Sitt Guruvanich <aekasitt.g+github@siamintech.co.th>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from re import Match, match, search
from typing import ClassVar, List, Optional
from webbrowser import open_new

### Third-party packages ###
from blessed import Terminal
from blessed.keyboard import Keystroke
from docker.models.containers import Container
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr, TypeAdapter
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

### Local modules ###
from arise.shadows.tusk import Tusk
from arise.types import BlockchainInfo, DifficultyAdjustment, MempoolInfo


class Bellion(BaseModel):
  model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True)  # type: ignore[misc]
  container_index: StrictInt = 0
  container_names: List[StrictStr] = []
  containers: List[Container] = []
  daemon: Container

  ### Split layouts ###
  body: ClassVar[Layout] = Layout(name="body", minimum_size=4, ratio=8, size=17)
  domains: ClassVar[Layout] = Layout(name="domains", size=20)
  footer: ClassVar[Layout] = Layout(name="footer", size=3)
  main: ClassVar[Layout] = Layout(size=72)
  pane: ClassVar[Layout] = Layout()
  sidebar: ClassVar[Layout] = Layout(size=24)
  tusk: ClassVar[Tusk] = Tusk(height=16, width=72)

  ### Terminal ###
  terminal: ClassVar[Terminal] = Terminal()

  def model_post_init(self, _) -> None:  # type: ignore[no-untyped-def]
    self.pane.split_row(self.sidebar, self.main)
    self.main.split_column(self.body, self.footer)
    self.sidebar.split_column(self.domains)

  def display(self) -> None:
    with self.terminal.cbreak(), self.terminal.hidden_cursor(), Live(
      self.pane, refresh_per_second=4, transient=True
    ):
      try:
        while True:
          ### Process input key ###
          keystroke: Keystroke = self.terminal.inkey(timeout=0.25)
          if keystroke.code == self.terminal.KEY_UP and self.container_index > 0:
            self.container_index -= 1
          elif (
            keystroke.code == self.terminal.KEY_DOWN
            and self.container_index < len(self.container_names) - 1
          ):
            self.container_index += 1
          elif keystroke in {"Q", "q"}:
            raise StopIteration

          container_rows: str = ""
          if self.container_index > 0:
            container_rows = "\n".join(self.container_names[: self.container_index])
            container_rows += f"\n[reverse]{self.container_names[self.container_index]}[reset]\n"
          else:
            container_rows = f"[reverse]{self.container_names[self.container_index]}[reset]\n"
          if self.container_index < len(self.container_names) - 1:
            container_rows += "\n".join(self.container_names[self.container_index + 1 :])
          self.pane["domains"].update(Panel(container_rows, title="domains"))
          container_name: str = self.container_names[self.container_index]

          ### Open new tab ####
          if keystroke in {"O", "o"} and match(r"arise-mutiny-web", container_name):
            open_new("http://localhost:8000")

          body_table: Table = Table(expand=True, show_lines=True)
          body_table.add_column(container_name, "dark_sea_green bold")
          network: Optional[Match] = search(r"(?<=arise)-(mainnet|signet|testnet)", container_name)
          if network:
            chain: str = network.group().replace("-mainnet", "")
            blockchain_info: BlockchainInfo = TypeAdapter(BlockchainInfo).validate_json(
              self.daemon.exec_run(
                f"""
                bitcoin-cli {chain} -rpcuser=arise -rpccookiefile=/home/bitcoin/.bitcoin/.cookie getblockchaininfo
                """
              ).output
            )
            mempool_info: MempoolInfo = TypeAdapter(MempoolInfo).validate_json(
              self.daemon.exec_run(
                f"""
                bitcoin-cli {chain} -rpcuser=arise -rpccookiefile=/home/bitcoin/.bitcoin/.cookie getmempoolinfo
                """
              ).output
            )
            body_table.add_row(
              Text.assemble(
                f"\n{ 'Blockchain information:'.ljust(20) }\n",
                ("Chain: ", "bright_magenta bold"),
                blockchain_info.chain.ljust(9),
                ("Blocks: ", "green bold"),
                f"{blockchain_info.blocks}".ljust(8),
                ("Size: ", "blue bold"),
                f"{blockchain_info.size_on_disk}".ljust(10),
                ("Time: ", "cyan bold"),
                f"{blockchain_info.time}".rjust(10),
                "\n",
              )
            )
            body_table.add_row(
              Text.assemble(
                "\n",
                ("Mempool information".ljust(19), "bold"),
                "\n".ljust(19),
                ("Fees:".ljust(15), "green bold"),
                f"{mempool_info.total_fee}".rjust(15),
                "\n".ljust(19),
                ("Transactions:".ljust(15), "cyan bold"),
                f"{mempool_info.txn_count}".rjust(15),
                "\n".ljust(19),
                ("Size:".ljust(15), "blue bold"),
                f"{mempool_info.txn_bytes}".rjust(15),
                "\n".ljust(19),
                ("Loaded?:".ljust(15), "bright_magenta bold"),
                ("true".rjust(15), "green") if mempool_info.loaded else ("false".rjust(15), "red"),
                "\n".ljust(19),
                ("Usage:".ljust(15), "light_coral bold"),
                f"{mempool_info.usage}".rjust(15),
                "\n",
              )
            )
          elif container_name == "arise-mempool":
            difficulty_adjustment: DifficultyAdjustment = TypeAdapter(
              DifficultyAdjustment
            ).validate_json(
              self.containers[self.container_index]
              .exec_run(
                """
                curl -sSL localhost:8999/api/v1/difficulty-adjustment
                """
              )
              .output
            )
            body_table.add_row(
              Text.assemble(
                "\n",
                ("Difficulty Adjustment", "bold"),
                "\n".ljust(15),
                ("Adjusted Time Average:".ljust(24), "green bold"),
                f"{difficulty_adjustment.adjusted_time_average}".rjust(16),
                "\n".ljust(15),
                ("Remaining Blocks:".ljust(24), "cyan bold"),
                f"{difficulty_adjustment.remaining_blocks}".rjust(16),
                "\n".ljust(15),
                ("Remaining Time:".ljust(24), "blue bold"),
                f"{difficulty_adjustment.remaining_time}".rjust(16),
                "\n".ljust(15),
                ("Next Retarget Height:".ljust(24), "bright_magenta bold"),
                f"{difficulty_adjustment.next_retarget_height}".rjust(16),
                "\n".ljust(15),
                ("Estimated Retarget Date:".ljust(24), "light_coral bold"),
                f"{difficulty_adjustment.estimated_retarget_date}".rjust(16),
                "\n",
              )
            )
            self.pane["footer"].update(
              Panel(
                Text.assemble(
                  "Select:".rjust(16),
                  (" ↑↓ ", "bright_magenta bold"),
                  " " * 20,
                  "Exit:".rjust(16),
                  ("  Q ", "red bold"),
                )
              )
            )
          elif container_name == "arise-mutiny-web":
            body_table.add_row(self.tusk.renderable)
            self.pane["footer"].update(
              Panel(
                Text.assemble(
                  "Select:".rjust(10),
                  (" ↑↓ ", "bright_magenta bold"),
                  " " * 8,
                  "Open:".rjust(10),
                  ("  O ", "cyan"),
                  " " * 8,
                  "Exit:".rjust(10),
                  ("  Q ", "red bold"),
                )
              )
            )
          else:
            body_table.add_row(self.tusk.renderable)
            self.pane["footer"].update(
              Panel(
                Text.assemble(
                  "Select:".rjust(16),
                  (" ↑↓ ", "bright_magenta bold"),
                  " " * 20,
                  "Exit:".rjust(16),
                  ("  Q ", "red bold"),
                )
              )
            )
          self.pane["body"].update(body_table)

      except StopIteration:
        print("Glory to Ashborn!")


__all__ = ("Bellion",)

from __future__ import annotations
from math import ceil
from typing import List

import pygame

import model
from model import GVec, GAgent, GLine

class GBarrierLine(GAgent):
    def __init__(self, server: model.GServer, line: GLine) -> None:
        super().__init__(server)
        self.line = line

    def interact(self, agents: List[GBarrierLine]) -> None:
        pass

    def update(self) -> None:
        pass

    def draw_graphic(self) -> None:
        draw_scale = self.server.display.draw_scale
        pygame.draw.line(self.server.display.canvas, self.server.display.BLACK,
                         (self.line.pt1 * draw_scale).xy,
                         (self.line.pt2 * draw_scale).xy,
                         ceil(0.1 * draw_scale))

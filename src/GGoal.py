from __future__ import annotations
from math import ceil, pi
from typing import List

import pygame

import model
from model import GAgent, GLine

class GGoal(GAgent):
    def __init__(self, server: model.GServer, 
                 line: GLine,
                 lam: float = 1, d_th: float = 0.8,
                 draw_circle: bool = False
                 ) -> None:
        super().__init__(server)
        server.goals.append(self)
        self.line = line
        self.lam, self.d_th = lam, d_th
        self.lw2 = lam**2 * line.len2
        self.people_cnt = self.den = 0
        self.draw_circle = draw_circle

    def interact(self, agents: List[GGoal]) -> None:
        self.people_cnt = 0
        for agent in agents:
            if isinstance(agent, model.GPerson):
                if self.line.closest_pt(agent.pos).dif(agent.pos).len <= 0.1:
                    agent.delete()
                else:
                    d2 = (self.line.mid - agent.pos).len2
                    self.people_cnt += d2 <= self.lw2
        self.den = max(self.d_th, self.people_cnt * 2 / (pi * self.lw2))

    def update(self) -> None:
        pass

    def draw_graphic(self) -> None:
        draw_scale = self.server.display.draw_scale
        pygame.draw.line(self.server.display.canvas, self.server.display.GOAL,
                         (self.line.pt1 * draw_scale).xy,
                         (self.line.pt2 * draw_scale).xy,
                         ceil(0.2 * draw_scale))
        if self.draw_circle:
            pygame.draw.circle(self.server.display.canvas, self.server.display.GOAL,
                               (self.line.mid * draw_scale).xy,
                               self.line.len * self.lam * draw_scale, 1)
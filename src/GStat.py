from __future__ import annotations
from math import ceil
from typing import List

import pygame
import pygame.freetype

import model
from model import GAgent, GVec

class GStat(GAgent):
    def __init__(self, server: model.GServer, output_filename=None) -> None:
        super().__init__(server)
        self.stats = []
        self.output_filename = output_filename
        self.font = None

    def interact(self, agents: List[GStat]) -> None:
        cnt = v_avg = 0
        for agent in agents:
            if isinstance(agent, model.GPerson):
                cnt += 1
                v_avg += agent.v.len
        if cnt: v_avg /= cnt
        self.stats.append((self.server.time_step * self.server.update_rate, cnt, v_avg))

    def update(self) -> None:
        if self.output_filename and self.stats and self.stats[-1][1] == 0:
            self.save_csv(self.output_filename)
            self.output_filename = None
        if self.stats and self.stats[-1][1] == 0: self.server.stop()

    def draw_graphic(self) -> None:
        if self.font is None:
            pygame.freetype.init()
            self.font = pygame.freetype.SysFont(None, 18)
        self.font.render_to(
            self.server.display.canvas, (10, 10), 
            f'Time: {self.server.time_step * self.server.update_rate:.2f}s; '
            f'Remaining: {self.stats[-1][1] if self.stats else "n/a"}',
            self.server.display.BLACK)

    def save_csv(self, fname):
        with open(fname, 'w') as f:
            f.write('Time Step,People #, Average V\n')
            for a in self.stats:
                f.write(','.join(map(str, a)) + '\n')
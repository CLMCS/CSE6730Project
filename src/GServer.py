from typing import List

import pygame
from pygame.color import Color

import model

class GDisplay:
    BLACK = Color(0, 0, 0)
    WHITE = Color(255, 255, 255)
    YELLOW = Color(255, 233, 0)
    RED = Color(200, 20, 20, 235)
    PERSON = RED
    PERSON_INJ = Color(115, 10, 20, 255)
    GOAL = Color(80, 150, 255)

    def __init__(self, server: 'GServer') -> None:
        self.server = server
        pygame.init()
        self.framerate = 1 / server.update_rate
        self.clock = pygame.time.Clock()
        self.screen_size = (960, 720)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.draw_scale = 50
        self.zoom_scale = 1.0
        self.canvas_size = self.screen_size
        self.canvas = pygame.Surface(self.canvas_size, pygame.SRCALPHA)
        self.canvas_size_vec = pygame.math.Vector2(self.canvas_size)

    def draw(self) -> None:
        self.screen.fill('white')
        self.canvas.fill('white')
        for agent in self.server.agents:
            agent.draw_graphic()
        scaled_surf = pygame.transform.scale(self.canvas, self.canvas_size_vec * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2))

        self.screen.blit(scaled_surf, scaled_rect)
        pygame.display.update()

        self.clock.tick(self.framerate)

class GServer:
    def __init__(self, update_rate: float = 1/60, display: bool = False) -> None:
        self.update_rate: float = update_rate  # in seconds
        self.running: bool = True
        self.terminating: bool = False
        self.agents: List[model.GAgent] = []
        self.goals: List[model.GGoal] = []
        self.view: bool = display
        self.display: GDisplay = None
        self.time_step = 0

    def add_agent(self, agent: 'model.GAgent') -> None:
        self.agents.append(agent)

    def remove_agent(self, agent: 'model.GAgent') -> None:
        self.agents.remove(agent)
    
    def step(self):
        for i in range(len(self.agents)):
            if i >= len(self.agents): break
            self.agents[i].interact(self.agents)
        for i in range(len(self.agents)):
            if i >= len(self.agents): break
            self.agents[i].update()
        self.time_step += 1

    def stop(self):
        self.running, self.terminating = False, True

    def run(self) -> None:
        if self.view:
            self.display = GDisplay(self)
        while not self.terminating:
            if self.running: self.step()
            if self.view:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.stop()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.running = not self.running
                self.display.draw()
        if self.view: pygame.quit()

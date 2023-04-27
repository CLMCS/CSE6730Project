from __future__ import annotations
import math
from typing import List

import pygame

import model
from model import GVec, GAgent

class GPerson(GAgent):
    # constant
    k = 12000  # (kg*s^-2)
    kappa = 24000  # (kg*m^-1*s^-1)

    def __init__(self, server: model.GServer,
                 pos: GVec, radius: float = 0.25,
                 mass: float = 80, desired_v: float = 1.5,
                 max_v: float = 5,
                 goal_select: callable = None
                 ) -> None:
        super().__init__(server)

        # constants
        self.A = 180  # (N)
        self.B = 0.08  # (m)
        self.tau = 0.5  # (s)
        self.injured_threshold = 1600  # N*m^-1
        self.kr, self.kd, self.kw, self.ka, self.kb, self.kg = [1] * 6

        self.pos = pos
        self.radius = radius
        self.mass = mass
        self.v, self.acc = GVec(0, 0), GVec(0, 0)
        self.desired_v = desired_v
        self.max_v = max_v
        self.goal_select = goal_select or GPerson.goal_select_3

        self.radial_force = 0
        self.circum = math.pi * 2 * self.radius
        self.injured = False

    def psychological_force(self, overlap: float):
        return self.A * math.exp(overlap / self.B)

    @classmethod
    def young_force(cls, overlap: float):  # overlap > 0
        return cls.k * overlap

    @classmethod
    def tangential_force(cls, overlap: float, v_diff: GVec, tang: GVec):  # overlap > 0
        return cls.kappa * overlap * v_diff.dot(tang)

    def goal_select_1(person: GPerson, goals: List[model.GGoal]):
        if len(goals) <= 1: return goals[0]
        ds = [person.pos.dist2(g.line.closest_pt(person.pos)) for g in goals]
        return min(zip(ds, goals), key=lambda x: x[0])[1]
    
    def goal_select_3(person: GPerson, goals: List[model.GGoal]):
        if len(goals) <= 1: return goals[0]
        rs, ds, ws = [], [], []
        for goal in goals:
            rs.append((goal.line.mid - person.pos).len)
            ds.append(goal.den)
            ws.append(goal.line.len)
        fs = lambda a, k: sum(x**k for x in a)
        sr, sd, sw = fs(rs, -person.kr), fs(ds, -person.kd), fs(ws, person.kw)
        Pr = [x**(-person.kr) / sr for x in rs]
        Pd = [x**(-person.kd) / sd for x in ds]
        Pw = [x**person.kw / sw for x in ws]
        def f2(a, k):
            n, s = len(a), sum(a)
            return sum(abs(1 - n * x / s)**k for x in a) / n
        al, be, ga = f2(rs, person.ka), f2(ds, person.kb), f2(ws, person.kg)
        P = [(al*pr+be*pd+ga*pw)/(al+be+ga) for pr, pd, pw in zip(Pr, Pd, Pw)]
        return max(zip(P, goals), key=lambda x: x[0])[1]
    
    def push(self, f: GVec, is_pressure: bool = True) -> GPerson:
        self.acc.add(f / self.mass)
        if is_pressure: self.radial_force += f.len
        return self

    def pull(self, f: GVec) -> GPerson:
        return self.push(-f)

    def interact_person(self, other: GPerson) -> None:
        overlap = self.radius + other.radius - self.pos.dist(other.pos)
        normal_vec = (self.pos - other.pos).unit()
        self.push(self.interaction_force(overlap, other.v - self.v, normal_vec))

    def interact_barrier_line(self, barrier: model.GBarrierLine):
        bpt = barrier.line.closest_pt(self.pos)
        overlap = self.radius - self.pos.dist(bpt)
        self.push(self.interaction_force(overlap, -self.v, (self.pos - bpt).unit()))
        return

    def interaction_force(self, overlap: float, v_diff: GVec, normal_vec: GVec) -> GVec:
        f_psy = self.psychological_force(overlap)
        f_young = self.young_force(overlap) if overlap > 0 else 0
        tang_vec = GVec(-normal_vec.y, normal_vec.x)
        f_tangent = self.tangential_force(overlap, v_diff, tang_vec) if overlap > 0 else 0
        return ((f_psy + f_young) * normal_vec) + (f_tangent * tang_vec)

    def self_driven_force(self, goal: model.GGoal):
        di = goal.line.extend(-self.radius*3.0).closest_pt(self.pos) - self.pos
        di.set_len(self.desired_v).sub(self.v)
        return di.mul(self.mass / self.tau)

    def interact(self, agents: List[GPerson]) -> None:
        self.push(self.self_driven_force(self.goal_select(self, self.server.goals)), False)
        for agent in agents:
            if agent != self and isinstance(agent, model.GPerson):
                self.interact_person(agent)
            elif isinstance(agent, model.GBarrierLine):
                self.interact_barrier_line(agent)

    def update(self) -> None:
        self.v.add(self.acc * self.server.update_rate)
        self.acc.zero()
        if self.radial_force / self.circum > 1600: self.injured = True
        self.radial_force = 0
        if self.v.len > self.max_v: self.v.len = self.max_v
        self.pos.add(self.v * self.server.update_rate)

    def draw_graphic(self) -> None:
        draw_scale = self.server.display.draw_scale
        spos = self.pos * draw_scale
        spos2 = (self.pos + self.v).mul(draw_scale)
        clr = self.server.display.PERSON_INJ if self.injured else self.server.display.PERSON
        pygame.draw.circle(self.server.display.canvas, clr,
                           spos.xy, self.radius * draw_scale)
        pygame.draw.line(self.server.display.canvas, self.server.display.PERSON,
                         spos.xy, spos2.xy, 2)

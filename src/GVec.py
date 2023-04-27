from __future__ import annotations
from ast import List
from typing import Tuple

class GVec:
    def __init__(self, x: float = 0, y: float = 0) -> None:
        self.x, self.y = x, y

    def __str__(self):
        return f'Vec({self.x}, {self.y})'

    def __sub__(self, other: GVec):
        return GVec(self.x - other.x, self.y - other.y)

    def __add__(self, other: GVec):
        return GVec(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float):
        return GVec(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float):
        return GVec(self.x * scalar, self.y * scalar)

    def __neg__(self):
        return GVec(-self.x, -self.y)

    def __truediv__(self, scalar):
        return GVec(self.x / scalar, self.y / scalar)

    @property
    def xy(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @property
    def len(self) -> float:
        return (self.x**2 + self.y**2) **.5

    @len.setter
    def len(self, ln: float):
        self.set_len(ln)

    def set_len(self, ln: float) -> GVec:
        ln /= self.len
        return self.mul(ln)

    @property
    def len2(self) -> float:
        return self.x**2 + self.y**2

    def dup(self) -> GVec:
        return GVec(self.x, self.y)

    cp = dup

    def zero(self) -> GVec:
        self.x, self.y = 0, 0
        return self

    def add(self, other: GVec) -> GVec:
        self.x += other.x
        self.y += other.y
        return self

    def sub(self, other: GVec) -> GVec:
        self.x -= other.x
        self.y -= other.y
        return self

    def mul(self, v: float) -> GVec:
        self.x *= v
        self.y *= v
        return self

    def neg(self) -> GVec:
        self.x = -self.x
        self.y = -self.y
        return self

    def flip(self) -> GVec:
        return self.neg()

    def unit(self) -> GVec:
        return self.set_len(1)

    def dif(self, other: GVec) -> GVec:
        return self - other

    diff = dif

    def dist(self, other: GVec) -> float:
        return ((self.x-other.x)**2 + (self.y-other.y)**2)**.5

    def dist2(self, other: GVec) -> float:
        return (self.x-other.x)**2 + (self.y-other.y)**2

    def cross2d(self, other: GVec) -> float:
        return self.x*other.y - self.y*other.x

    def dot(self, other: GVec) -> float:
        return self.x*other.x + self.y*other.y
    
    def inside(self, pts: List['GVec']) -> bool:
        '''https://wrfranklin.org/Research/Short_Notes/pnpoly.html'''
        res = False
        for i in range(len(pts)):
            if (((pts[i].y>self.y) != (pts[i-1].y>self.y)) and
                (self.x < (pts[i-1].x-pts[i].x) * (self.y-pts[i].y) / (pts[i-1].y-pts[i].y) + pts[i].x)):
                res = not res
        return res
    
    @classmethod
    def bounds(cls, pts: List['GVec']) -> List[float]:
        '''return [x0, y0, x1, y1]'''
        return [min(pt.x for pt in pts), min(pt.y for pt in pts),
                max(pt.x for pt in pts), max(pt.y for pt in pts)]

if __name__ == '__main__':
    # v1 = GVec(1, 1)
    # v1 += GVec(2, 3)
    # v1.add(GVec(2, 3)).mul(2)
    # v1.mul(2).add(GVec(-1, -1)).mul(-1)
    # print(v1)
    pts = [GVec(10, 10), GVec(20, 5), GVec(25, 15), GVec(15, 12), GVec(10, 15)]
    print(GVec(5, 5).inside(pts))
    print(GVec(11, 11).inside(pts))
    print(GVec(15, 11).inside(pts))
    print(GVec(15, 15).inside(pts))
    print(GVec(21, 6.9).inside(pts))
    print(GVec(21, 7).inside(pts))
    print(GVec(21, 7.1).inside(pts))
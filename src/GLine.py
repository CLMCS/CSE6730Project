from __future__ import annotations
from typing import List

from sympy import Point, Line
from sympy.geometry import intersection

from model import GVec

class GLine:
    def __init__(self, *args) -> None:
        if len(args) == 2:
            self.pt1: GVec = args[0]
            self.pt2: GVec = args[1]
        else:
            self.pt1: GVec = GVec(args[0], args[1])
            self.pt2: GVec = GVec(args[2], args[3])
        self.len_ = self.pt1.dist(self.pt2)
        self.len2_ = self.pt1.dist2(self.pt2)

    def __str__(self):
        return f'Line({self.pt1}, {self.pt2})'

    @property
    def len(self):
        return self.len_

    @property
    def len2(self):
        return self.len2_

    @property
    def mid(self):
        return (self.pt1 + self.pt2) / 2

    def add(self, other: GVec) -> GVec:
        self.pt1.add(other)
        self.pt2.add(other)
        return self

    def extend(self, d: float) -> GLine:
        ln = self.len
        if -d * 2 > ln: d = -ln / 2
        di = (self.pt2 - self.pt1).set_len(d)
        return GLine(self.pt1 - di, self.pt2 + di)

    def closest_pt(self, pt: GVec) -> GVec:
        if self.len == 0: return self.pt1.cp()
        di = (self.pt2 - self.pt1).unit()
        px = (pt - self.pt1).dot(di)

        return (self.pt1.cp() if px <= 0 else
                self.pt2.cp() if px >= self.len else
                self.pt1 + di.set_len(px))

    def intersect(self, other: GLine) -> bool:
        l0 = Line(Point(*self.pt1.xy), Point(*self.pt2.xy))
        l1 = Line(Point(*other.pt1.xy), Point(*other.pt2.xy))
        s = intersection(l0, l1)
        return GVec(s[0].x, s[0].y) if s and isinstance(s[0], Point) else None
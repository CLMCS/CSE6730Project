from sympy import *
from sympy.geometry import *

class MyVec2D(Point2D):
    def add(self, other):
        self.translate(*other.coordinates)
        return self

Point.add = MyVec2D.add

p1 = Point(0, 0)
p2 = Point(2, 2)
p2.x += 1
p2.add(Point(1, 1)).add(Point(2, 2))
print(p2, p2.x, p2.y)
p2.add(Point(2, 2))
print(p2)
l1 = Line(p1, p2)
print(l1)
l2 = Line(Point(1, 1), Point(3, 3))
l3 = Line(Point(1, 0), Point(0, 1))
l4 = Line(Point(1, 1), Point(0, 1))
l5 = Line(Point(1, 0), Point(2, 1))

i1 = intersection(l1, l2)[0]
i2 = l1.intersect(l3)
i3 = l1.intersection(l4)[0]
i4 = intersection(l1, l5)

print(i1)
print(i2)
print(i3)
print(i4)

print(isinstance(i1, Line))
print(isinstance(i1, Line2D))
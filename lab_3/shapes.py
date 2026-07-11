"""Lab 3: Inheritance, Shape3D
Kim Huynh, 2026-04-15, CS 211
"""

import math

# 2.1 Print Info
class Shape3D:
    def __init__(self):
        raise NotImplementedError("Abstract class cannot be instantiated")  

    def volume(self) -> float:
        raise NotImplementedError("Not implemented for abstract class")

    def area(self) -> float:
        raise NotImplementedError("Not implemented for abstract class")

    def print_info(self):
        return f"Area: {self.area()}, Volume: {self.volume()}"

# 2.2 Cylinders
class Cylinder(Shape3D):
    def __init__(self, radius, height):
        self.radius = float(radius)     # radius
        self.height = float(height)     # height

    def volume(self):
        return math.pi * (self.radius ** 2) * self.height   # volume = pir^2*h

    def area(self):
        return 2 * math.pi * (self.radius ** 2) + 2 * math.pi * self.radius * self.height   # area = 2pir^2 + 2pirh

# 2.3 Cuboids
class Cuboid(Shape3D):
    def __init__(self, width, length, height):
        self.width = float(width)       # width
        self.length = float(length)     # length
        self.height = float(height)     # height

    def volume(self):
        return self.width * self.length * self.height    # volume = lwh

    def area(self):
        return 2 * (self.width * self.length + self.width * self.height + self.length * self.height)    # area = 2(lw + lh + wh)

# 2.4 Cubes
class Cube (Cuboid):
    def __init__(self, width):
        super().__init__(width, width, width)

# 2.5 Test It
if __name__ == "__main__":
    cyl = Cylinder(3, 5)
    cuboid = Cuboid(6, 4, 9)
    cube = Cube(3)

    shapes = [cube, cyl, cuboid]

    for shape in shapes:
        print(shape.print_info())
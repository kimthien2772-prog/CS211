"""Homework 1: Point3D
Kim Huynh, 2026-04-06, CS 211
"""

import math

class Point3D:
    """Represents a point in 3D space as a class, e.g., Point3D(x, y, z)."""

    def __init__(self, x_value: float, y_value: float, z_value: float):
        """
        Initializes a Point3D object with x, y, z coordinates.

        Args:
            x_value (float or int): x-coordinate of the point
            y_value (float or int): y-coordinate of the point
            z_value (float or int): z-coordinate of the point
        """
        assert isinstance(x_value, (int, float)), 'x value must be float or integer'
        assert isinstance(y_value, (int, float)), 'y value must be float or integer'
        assert isinstance(z_value, (int, float)), 'z value must be float or integer'
        self.x = x_value
        self.y = y_value
        self.z = z_value

    def __str__(self) -> str:
        """Return a string representation of the Point3D object."""
        return f'Point3D({self.x}, {self.y}, {self.z})'

    def euclidean_distance(self, other: 'Point3D') -> float:
        """
        Calculates the Euclidean distance between this point and another Point3D.

        Args:
            other (Point3D): Another point in 3D space to measure distance to

        Returns:
            float: Euclidean distance between the two points
        """
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx**2 + dy**2 + dz**2)


if __name__ == '__main__':
    # Three test points
    point1 = Point3D(3.5, -2.0, 7.1)   # 12.88
    point2 = Point3D(-4.2, 5.5, 0.0)   # 8.24
    point3 = Point3D(10.0, -3.3, 2.2)  # 16.85

    # Compute and print distances between each pair
    print(f"Distance between {point1} and {point2}: {point1.euclidean_distance(point2):.2f}")
    print(f"Distance between {point1} and {point3}: {point1.euclidean_distance(point3):.2f}")
    print(f"Distance between {point2} and {point3}: {point2.euclidean_distance(point3):.2f}")
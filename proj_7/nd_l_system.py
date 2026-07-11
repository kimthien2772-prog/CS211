"""Project 7 Extra-Credit : Non-deterministic Structures
Kim Huynh, 2026-05-14, CS 211
"""

import turtle
import random
from state import Stack, State

class LSystem:
    """
    This class represents an L-system with its axiom, rules, and drawing functions.
    """

    def __init__(
        self,
        axiom,
        rules,
        n=3,
        angle=0,
        step=5,
        starting_pos=(-200, 0),
        starting_angle=0,
        color="blue",
    ):
        """
        Initializes an L-system with the given parameters.

        Parameters:
            axiom (str): The initial string from which the L-system starts.
            rules (dict): A dictionary defining the replacement rules for the L-system.
            n (int, optional): The number of iterations to apply the rules. Default is 3.
            angle (float, optional): The angle (in degrees) used for turning in the L-system. Default is 0.
            step (float, optional): The step size for moving forward in the L-system. Default is 5.
            starting_pos (tuple, optional): The starting position (x, y) for the L-system. Default is (-200, 0).
            starting_angle (float, optional): The initial angle (in degrees) for the L-system. Default is 0.
            color (str, optional): The color used for drawing the L-system. Default is "blue".
        Attributes:
            commands (str): Stores the generated commands for the L-system. Initially empty.
        """
        self.axiom = axiom
        self.rules = rules
        self.n = n
        self.angle = angle
        self.step = step
        self.starting_pos = starting_pos
        self.starting_angle = starting_angle
        self.color = color
        self.commands = ""

    def choose_rule(self, options):
        """
        Randomly chooses one substitution based on probability.
        Options is a list of tuples: (probability, substitution).
        """
        # generate random value between 0 and 1
        r = random.random()
        total = 0

        for probability, substitution in options:
            total += probability
            if r <= total:
                return substitution

        return options[-1][1]

    def iterate(self):
        """
        This function iterates the L-system n times, applying the rules.
        Args:
            none
        Actions:
            The attribute commands is set to the resulting string after n iterations.
        Returns:
            None
        """
        current_string = self.axiom

        for _ in range(self.n):
            new_string = ""

            for char in current_string:
                if char in self.rules:
                    rule = self.rules[char]

                    # stochastic rule with multiple possible substitutions
                    if isinstance(rule, list):
                        # randomly select one substitution rule
                        new_string += self.choose_rule(rule)
                    else:
                        new_string += rule
                else:
                    new_string += char

            current_string = new_string

        self.commands = current_string

    def draw(self):
        """
        This function draws the L-system string using the turtle.
        Args:
            string: The L-system string to be drawn.
            turtle: The turtle object used for drawing.
        """
        t = self.init_turtle()
        # stores turtle states for branching structures
        stack = Stack()

        for command in self.commands:
            if command == "F":
                t.forward(self.step)

            elif command == "f":
                t.penup()
                t.forward(self.step)
                t.pendown()

            elif command == "+":
                t.left(self.angle)

            elif command == "-":
                t.right(self.angle)

            # save current turtle state
            elif command == "[":
                current_state = State(t.xcor(), t.ycor(), t.heading())
                stack.push(current_state)

            # restore previous turtle state
            elif command == "]":
                if not stack.is_empty():
                    saved_state = stack.pop()
                    saved_state.set_state(t)

    def init_turtle(self):
        """
        Initializes and configures a turtle object for drawing.
        This method creates a new turtle instance, sets its speed, color, 
        starting position, and orientation based on the object's attributes.
        Returns:
            turtle.Turtle: A configured turtle object ready for drawing.
        """
        t = turtle.Turtle()
        t.speed(0)
        t.color(self.color)
        t.penup()
        t.goto(self.starting_pos)
        t.setheading(self.starting_angle)
        t.pendown()
        return t

    def plot(self, n=None):
        """
        Plot the L-system by iterating and drawing it.
        This method performs the following steps:
        1. Iterates the L-system to generate the final string representation.
        2. Draws the L-system using the turtle graphics module.
        3. Keeps the turtle graphics window open until it is closed manually.
        Parameters:
            n (int): The number of iterations to perform on the L-system.
        Returns:
            None
        """
        if n is not None:
            self.n = n

        self.iterate()
        self.draw()
        turtle.exitonclick()


def main():
    # seed random generator for reproducible output
    random.seed(42)

    # draw multiple stochastic trees to replicate Fig.7 in
    # project document
    positions = [
        (-300, -250),
        (-150, -250),
        (0, -250),
        (150, -250),
        (300, -250),
    ]

    # generate a tree at each starting position
    for pos in positions:
        nd_ls_1 = LSystem(
            axiom="F",
            rules={
                "F": [
                    (.33, "F[+F]F[-F]F"),
                    (.33, "F[+F]F"),
                    (.33, "F[-F]F"),
                ]
            },
            angle=25.7,
            step=6,
            n=5,
            starting_pos=pos,
            starting_angle=90,
            color="blue",
        )

        nd_ls_1.iterate()
        nd_ls_1.draw()

    turtle.exitonclick()


if __name__ == "__main__":
    main()
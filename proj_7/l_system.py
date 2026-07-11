"""Project 7: L-Systems
Kim Huynh, 2026-05-13, CS 211
"""

# credit: slides from class

import turtle
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
                    new_string += self.rules[char]
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

            elif command == "[":
                current_state = State(t.xcor(), t.ycor(), t.heading())
                stack.push(current_state)

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

    def plot(self, n):
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
    # create the L-system object
    ls1 = LSystem(
        axiom="-L",
        rules={"L": "LF+RFR+FL-F-LFLFL-FRFR+", "R": "-LFLF+RFRFR+F+RF-LFL-FR"},
        angle=90,
        step=10,
    )

    ls2 = LSystem(axiom="F-F-F-F", rules={"F": "F-F+F+FF-F-F+F"}, angle=90, step=2)

    ls3 = LSystem(
        axiom="F+F+F+F",
        rules={"F": "F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF", "f": "ffffff"},
        angle=90,
        step=3,
        n=2,
    )

    # iterate the L-system and plot the result
    ls3.iterate()
    ls3.plot(n=2)
    print(ls3.commands)


if __name__ == "__main__":
    main()
"""Project 4: Reverse Polish Expression Evaluator, rpncalc.py
Kim Huynh, 2026-04-22, CS 211
"""

# credits: project 4 template, slides from class

from expr import *
from typing import List

# auxiliary function
def is_binop(op: str) -> bool:
    """Return True if op is a binary operator."""
    return op in ["+", "-", "*", "/"]

# auxiliary function
def is_unop(op: str) -> bool:
    """Return True if op is a unary operator."""
    return op in ["~", "@"]

# auxiliary function
def is_var(op: str) -> bool:
    """Return True if op is a valid variable name."""
    return op.isidentifier() and not is_binop(op) and not is_unop(op) and op != "="

# auxiliary function
def binop_class(op: str) -> "BinOp":
    """Return the BinOp class that matches the operator symbol."""
    if op == "+":
        return Plus
    if op == "-":
        return Minus
    if op == "*":
        return Times
    if op == "/":
        return Div
    raise ValueError(f"Unknown binary operator: {op}")

# auxiliary function
def unop_class(op: str) -> "UnOp":
    """Return the UnOp class that matches the operator symbol."""
    if op == "~":
        return Neg
    if op == "@":
        return Abs
    raise ValueError(f"Unknown unary operator: {op}")

def rpn_parse(text: str) -> List[Expr]:
    """Parse text in reverse Polish notation
    into a list of expressions.

    Example:
        rpn_parse("5 3 + 4 *")
        => [Times(Plus(Const(5), Const(3)), Const(4))]
    """

    stack = []

    for token in text.split():

        # concrete class Const
        # Const is defined in expr.py and used here to store number tokens
        if token.lstrip("-").isdigit():
            stack.append(Const(int(token)))

        # abstract class BinOp
        # cncrete class Plus (refactored)
        # concrete class Times (refactored)
        # BinOp, Plus, Times, Minus, and Div are defined in expr.py
        elif is_binop(token):
            right = stack.pop()
            left = stack.pop()
            op_class = binop_class(token)
            stack.append(op_class(left, right))

        # abstract class UnOp
        # concrete class Neg
        # concrete class Abs
        # UnOp, Neg, and Abs are defined in expr.py
        elif is_unop(token):
            left = stack.pop()
            op_class = unop_class(token)
            stack.append(op_class(left))

        # concrete class Assign
        # Assign is defined in expr.py
        # in RPN, assignment is written like: 3 x =
        elif token == "=":
            left = stack.pop()
            right = stack.pop()

            if not isinstance(left, Var):
                raise SyntaxError("Left side of assignment must be a variable")

            stack.append(Assign(left, right))

        # Var is defined in expr.py
        # method assign of class Var is used later by Assign.eval()
        elif is_var(token):
            stack.append(Var(token))

        else:
            raise SyntaxError(f"Unknown token: {token}")

    return stack

def calc(text: str):
    """Read and evaluate a single line formula."""

    parsed = rpn_parse(text)

    if len(parsed) != 1:
        raise SyntaxError("Expression is not balanced")

    expr = parsed[0]
    result = expr.eval()

    print(f"{expr} => {result}")

# function rpn_calc
def rpn_calc():
    """Interactive RPN calculator loop."""

    while True:
        text = input("Expression (return to quit):")

        if text == "":
            print("Bye! Thanks for the math!")
            break

        try:
            calc(text)
        except Exception as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    """RPN Calculator as main program"""
    rpn_calc()

# basic arithmetic test
expr1 = rpn_parse("3 5 *")[0]
print(expr1, "=>", expr1.eval())   # expected: (3 * 5) => 15

# chained operation test
expr2 = rpn_parse("3 5 * 2 *")[0]
print(expr2, "=>", expr2.eval())   # expected: ((3 * 5) * 2) => 30

# variable assignment test
expr3 = rpn_parse("3 5 * x =")[0]
print(expr3, "=>", expr3.eval())   # expected: (x = (3 * 5)) => 15

# variable usage test
expr4 = rpn_parse("x 2 *")[0]
print(expr4, "=>", expr4.eval())   # expected: (x * 2) => 30
"""Project 4: Reverse Polish Expression Evaluator, expr.py
Kim Huynh, 2026-04-22, CS 211
"""

# credits: project 4 template, slides from class

from typing import Dict

# variable storage in Var and Assign
ENV: Dict[str, "Const"] = {}

class UndefinedVariable(Exception):
    """Raised when a variable is used before it has been assigned."""
    pass

class Expr():
    """Abstract base class of all expressions."""

    def eval(self) -> "Const":
        """Implementations of eval should return an integer constant."""
        raise NotImplementedError(
            f"'eval' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define 'eval'"
        )
    def __str__(self) -> str:
        """Implementations of __str__ should return the expression in algebraic notation."""
        raise NotImplementedError(
            f"'__str__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__str__'"
        )

    def __repr__(self) -> str:
        """Implementations of __repr__ should return a string that looks like the constructor."""
        raise NotImplementedError(
            f"'__repr__' not implemented in {self.__class__.__name__}\n"
            "Each concrete Expr class must define '__repr__'"
        )

# concrete class Const
class Const(Expr):
    """Represents one integer constant, such as 5."""

    def __init__(self, value: int):
        self.value = value

    def eval(self) -> "Const":
        # a constant evaluates to itself
        return self

    def __str__(self) -> str:
        # algebraic notation for a constant is just its number
        return str(self.value)

    def __repr__(self) -> str:
        # constructor-style representation
        return f"Const({self.value})"

    def __eq__(self, other: Expr):
        # two Const objects are equal only if both are Consts with the same value
        return isinstance(other, Const) and self.value == other.value

# abstract class BinOp
class BinOp(Expr):
    """Abstract base class for binary operations with left and right operands."""

    def __init__(self, left: Expr, right: Expr, symbol: str = "?"):
        self.left = left
        self.right = right
        self.symbol = symbol

    def __str__(self) -> str:
        # shared string method for all binary operations
        return f"({self.left} {self.symbol} {self.right})"

    def __repr__(self) -> str:
        # uses dynamic dispatch to get the actual subclass name
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"

    def _apply(self, left_val: int, right_val: int) -> int:
        # each specific binary operation defines its own math
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete BinOp class must define '_apply'"
        )

    def eval(self) -> "Const":
        # recursively evaluates left and right operands
        left_val = self.left.eval()
        right_val = self.right.eval()
        return Const(self._apply(left_val.value, right_val.value))

# concrete class Plus (refactored)
class Plus(BinOp):
    """Represents left + right."""

    def __init__(self, left: Expr, right: Expr):
        # reuses BinOp constructor instead of repeating left/right/symbol setup
        super().__init__(left, right, "+")

    def _apply(self, left_val: int, right_val: int) -> int:
        return left_val + right_val

class Minus(BinOp):
    """Represents left - right."""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "-")

    def _apply(self, left_val: int, right_val: int) -> int:
        return left_val - right_val

# roncrete class Times (refactored)
class Times(BinOp):
    """Represents left * right."""

    def __init__(self, left: Expr, right: Expr):
        # reuses BinOp constructor instead of repeating left/right/symbol setup
        super().__init__(left, right, "*")

    def _apply(self, left_val: int, right_val: int) -> int:
        return left_val * right_val

class Div(BinOp):
    """Represents left / right using integer division."""

    def __init__(self, left: Expr, right: Expr):
        super().__init__(left, right, "/")

    def _apply(self, left_val: int, right_val: int) -> int:
        return left_val // right_val

# abstract class UnOp
class UnOp(Expr):
    """Abstract base class for unary operations with one operand."""

    def __init__(self, left: Expr, symbol: str = "?"):
        self.left = left
        self.symbol = symbol

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.left)})"

    def _apply(self, val: int) -> int:
        raise NotImplementedError(
            f"'_apply' not implemented in {self.__class__.__name__}\n"
            "Each concrete UnOp class must define '_apply'"
        )

    def eval(self) -> "Const":
        # recursively evaluates the one operand
        left_val = self.left.eval()
        return Const(self._apply(left_val.value))

# concrete class Neg
class Neg(UnOp):
    """Represents negation, written with ~ in RPN."""

    def __init__(self, left: Expr):
        super().__init__(left, "~")

    def __str__(self) -> str:
        return f"~{self.left}"

    def _apply(self, val: int) -> int:
        return -val

# concrete class Abs
class Abs(UnOp):
    """Represents absolute value, written with @ in RPN."""

    def __init__(self, left: Expr):
        super().__init__(left, "@")

    def __str__(self) -> str:
        return f"|{self.left}|"

    def _apply(self, val: int) -> int:
        return abs(val)

class Var(Expr):
    """Represents a variable, such as x."""

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var('{self.name}')"

    def eval(self):
        global ENV
        if self.name in ENV:
            return ENV[self.name]
        else:
            raise UndefinedVariable(f"{self.name} has not been assigned a value")

    # method assign of class Var
    def assign(self, value: Const):
        # stores the variable name and its evaluated Const value in ENV
        global ENV
        ENV[self.name] = value

# concrete class Assign
class Assign(Expr):
    """Represents assignment, such as x = 3."""

    def __init__(self, left: Var, right: Expr):
        # only variables can appear on the left side of assignment
        assert isinstance(left, Var)
        self.left = left
        self.right = right

    def eval(self) -> Const:
        # evaluate the right side, assign it to the variable, and return the value
        r_val = self.right.eval()
        self.left.assign(r_val)
        return r_val

    def __str__(self):
        return f"({self.left} = {self.right})"

    def __repr__(self):
        return f"Assign({repr(self.left)}, {repr(self.right)})"

class Plus(Expr):
    '''left and right'''

    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        '''Algebraic notation, fully parenthesized: (left + right)'''
        return f"({self.left} + {self.right})"
    
    def eval(self) -> "Const":
        '''Implementations of eval should return an integer constant'''
        left_val = self.left.eval()
        right_val = self.right.eval()
        return Const(left_val.value + right_val.value)
    
    def __repr__(self) -> str:
        "'Implementations of __repr__ should return a string that looks like"
        "the constructor, e.g., Plus(Const(5), Const(4))"
        return f"Times({repr(self.left)}, {repr(self.right)})"
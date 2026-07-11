"""
The game state and logic (model component) of 512, 
a game based on 2048 with a few changes. 
This is the 'model' part of the model-view-controller
construction plan.  It must NOT depend on any
particular view component, but it produces event 
notifications to trigger view updates. 
"""

from game_element import GameElement, GameEvent, EventKind
from typing import List, Tuple, Optional
import random

# Configuration constants
GRID_SIZE = 4


class Vec():
    """A Vec is an (x,y) or (row, column) pair that
    represents distance along two orthogonal axes.
    Interpreted as a position, a Vec represents
    distance from (0,0).  Interpreted as movement,
    it represents distance from another position.
    Thus we can add two Vecs to get a Vec.
    """
    # FIXME:  We need a constructor, and __add__, and __eq__ methods.
    pass


class Tile(GameElement):
    """A slidy numbered thing.
    # FIXME:  complete the constructor method.
"""

    def __init__(self):
        super().__init__()


class Board(GameElement):
    """The game grid.  Inherits 'add_listener' and 'notify_all'
    methods from game_element.GameElement so that the game
    can be displayed graphically.
    """

    def __init__(self):
        super().__init__()
        self.tiles = [None]
        # FIXME: a grid holds a matrix of tiles

    def has_empty(self) -> bool:
        """Is there at least one grid element without a tile?"""
        return False
        # FIXME: Should return True if there is some element with value None

    def place_tile(self):
        """Place a tile on a randomly chosen empty square."""
        return
        # FIXME

    def score(self) -> int:
        """Calculate a score from the board.
        The Score is the sum of the values of all squares.
        """
        return 0
        # FIXME

    def _empty_positions(self) -> List[Vec]:
        """Return a list of positions of None values,
        i.e., unoccupied spaces.
        """
        pass
        return []
        # FIXME

    # FIXME: include the to_list method to convert the grid to a list

    # FIXME: implement the from_list method to convert a list to grid

    # FIXME: implement the slide method to slide the tiles in a given direction

    # FIXME: implement the _move_tile method to move a tile in a given direction

    # FIXME: implement the right, left, up, and down methods

    # FIXME: implement the score method to calculate the score of the game

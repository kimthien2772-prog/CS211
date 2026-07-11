"""Project 2: FiveTwelve
Kim Huynh, 2026-04-12, CS 211
"""

"""
The game state and logic (model component) of 512, 
a game based on 2048 with a few changes. 
This is the 'model' part of the model-view-controller
construction plan.  It must NOT depend on any
particular view component, but it produces event 
notifications to trigger view updates. 
"""
# credits: Lab 2, slides from class, model.py from https://github.com/UO-CIS211/FiveTwelve
# python3 game_manager.py

from game_element import GameElement, GameEvent, EventKind
from typing import List, Tuple, Optional
import random

# Configuration constants
GRID_SIZE = 4

# 2.1 Vector Class
class Vec():
    """A Vec is an (x,y) or (row, column) pair that
    represents distance along two orthogonal axes.
    Interpreted as a position, a Vec represents
    distance from (0,0).  Interpreted as movement,
    it represents distance from another position.
    Thus we can add two Vecs to get a Vec.
    """

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
    
    def __add__(self, other: "Vec") -> "Vec":
        return Vec(self.row + other.row, self.col + other.col)
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vec):
            return False
        return self.row == other.row and self.col == other.col
    

class Tile(GameElement):
    """A slidy numbered thing."""

    def __init__(self, row: int, col: int, value: int = 2):
        super().__init__()
        self.row = row
        self.col = col
        self.value = value


class Board(GameElement):
    """The game grid.  Inherits 'add_listener' and 'notify_all'
    methods from game_element.GameElement so that the game
    can be displayed graphically.
    """

    # 2.2 Board Constructor
    def __init__(self):
        super().__init__()
        self.tiles = []
        for _ in range(GRID_SIZE):
            self.tiles.append([None] * GRID_SIZE)
        
    # 2.1 Full Board
    def has_empty(self) -> bool:
        """Is there at least one grid element without a tile?"""
        for row in self.tiles:
            for tile in row:
                if tile is None:
                    return True
        return False

    # 2.5 Random Tile
    def place_tile(self):
        """Place a tile on a randomly chosen empty square."""
        empty = self._empty_positions()
        if not empty:
            return
        
        pos = random.choice(empty)
        tile = Tile(pos.row, pos.col, 2)
        self.tiles[pos.row][pos.col] = tile
        self.notify_all(GameEvent(EventKind.tile_created, tile))
        
    # 2.6 Game Score
    def score(self) -> int:
        """Calculate a score from the board.
        The Score is the sum of the values of all squares.
        """
        total = 0
        for row in self.tiles:
            for tile in row:
                if tile is not None:
                    total += tile.value         
        return total
        

    def _empty_positions(self) -> List[Vec]:
        """Return a list of positions of None values,
        i.e., unoccupied spaces.
        """
        empty = []
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.tiles[row][col] is None:
                    empty.append(Vec(row, col))
        return empty
    
    # 2.1 Valid Position
    def in_bounds(self, pos: Vec) -> bool:
        '''Return True if pos is on the board'''
        return 0 <= pos.row < GRID_SIZE and 0 <= pos.col < GRID_SIZE
    
    # 2.1 Scaffolding Methods
    def to_list(self) -> List[List[int]]:
        '''Convert board contents to a list of integers'''
        values = []
        for row in self.tiles:
            value_row = []
            for tile in row:
                if tile is None:
                    value_row.append(0)
                else:
                    value_row.append(tile.value)
            values.append(value_row)
        return values
    
    # 2.3 Move Tile
    def _move_tile(self, old_pos: Vec, new_pos: Vec):
        '''Move tile from old_pos to new_pos
        if new_pos is empty, slide there. If same value, merge'''
        old_tile = self.tiles[old_pos.row][old_pos.col]
        new_tile = self.tiles[new_pos.row][new_pos.col]
        

        if old_tile is None:
            return
        
        if new_tile is None:
            self.tiles[new_pos.row][new_pos.col] = old_tile
            self.tiles[old_pos.row][old_pos.col] = None

            old_tile.row = new_pos.row
            old_tile.col = new_pos.col
            self.notify_all(GameEvent(EventKind.tile_created, old_tile))

        elif new_tile.value == old_tile.value:
            new_tile.value += old_tile.value
            self.tiles[old_pos.row][old_pos.col] = None

            self.notify_all(GameEvent(EventKind.tile_created,new_tile))
            self.notify_all(GameEvent(EventKind.tile_removed, old_tile))
    
    # 2.2 Slide 
    def slide(self, direction: Vec):
        '''Slide all tiles in the given direction'''
        moved = False

        row_range = range(GRID_SIZE)
        col_range = range(GRID_SIZE)

        if direction.row > 0:
            row_range = range(GRID_SIZE -1, -1, -1)
        if direction.col > 0:
            col_range = range(GRID_SIZE -1, -1, -1)

        for row in row_range:
            for col in col_range:
                current = Vec(row, col)
                tile = self.tiles[row][col]

                if tile is None:
                    continue
                
                while True:
                    next_pos = current + direction

                    if not self.in_bounds(next_pos):
                        break

                    next_tile = self.tiles[next_pos.row][next_pos.col]

                    if next_tile is None:
                        self._move_tile(current, next_pos)
                        current = next_pos
                        moved = True
                    elif next_tile.value == self.tiles[current.row][current.col].value:
                        self._move_tile(current, next_pos)
                        moved = True
                        break
                    else:
                        break
                
            if moved or self.has_empty():
                self.place_tile()

    # 2.4 Directional Movements
    def left(self):
        '''slide left'''
        self.slide(Vec(0, -1))

    def right(self):
        '''slide right'''
        self.slide(Vec(0, 1))

    def up(self):
        '''slide up'''
        self.slide(Vec(-1, 0))
        
    def down(self):
        '''slide down'''
        self.slide(Vec(1, 0))
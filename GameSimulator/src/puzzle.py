# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Puzzle API

Works in conjunction with solver.py to enable a generic algorithm
to solve one-player puzzles.
"""


class Puzzle:
    """Abstract class for a generic one-player puzzle.

    Note that this class really represents a puzzle *state*
    and not just a generic type of puzzle. In other words,
    an instance of this class could represent one particular
    Sudoku puzzle, with a partially filled-in board.

    The rules of the game are encoded in the 'is_solved'
    and 'extensions' methods.

    Subclasses are responsible for tracking the internal state
    of the puzzle, and implementing six methods:
        - __str__
        - is_solved
        - extensions
        - move
        - find_user_input
        - same_game_state
    """
    def __str__(self):
        """Return a human-readable representation of this puzzle.

        @type self: Puzzle
        @rtype: str
        """
        raise NotImplementedError()

    def is_solved(self):
        """Return whether this puzzle is in a solved state.

        @type self: Puzzle
        @rtype: bool
        """
        raise NotImplementedError()

    def extensions(self):
        """Return a list of possible new states reachable by one move.

        First compute a list of possible moves based on the current
        puzzle state. Then, return a list of the new puzzle states
        that the puzzle could be in after each move.

        @type self: Puzzle
        @rtype: list[Puzzle]
        """
        raise NotImplementedError()

    def move(self, move):
        """Return a new puzzle state specified by making the given move.

        Raise a ValueError if <move> represents an invalid move.
        Do *NOT* change the state of <self>. This is not a mutating method!

        NOTE: You can ignore this completely until Part 2.

        @type self: Puzzle
        @type move: str
        @rtype: Puzzle
        """
        raise NotImplementedError()

    def find_user_input(self, other):
        """ Return the user input in correct the format that the user would have
            to input to get from game state at state self to game state state at other.

        Precondition: 1.self and other are puzzles which are one move apart.
                      2.self and other are the same type of puzzles
        @type self: Puzzle
        @type other: Puzzle
        @rtype: str
        """
        raise NotImplementedError

    def same_game_state(self, other):
        """ Return True iff self and <other> are at the same game state.

        @type self: Puzzle
        @type other: Puzzle
        @rtype: bool
        """
        raise NotImplementedError

# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Sudoku puzzle module.

Here are the rules of Sudoku:

- The puzzle consists of an n-by-n grid, where n = 4, 9, 16, or 25.
  Each square contains a uppercase letter between A and the n-th letter
  of the alphabet, or is empty.
  For example, on a 4-by-4 Sudoku board, the available letters are
  A, B, C, or D. On a 25-by-25 board, every letter A-Y is available.
- The goal is to fill in all empty squares with available letters so that
  the board has the following property:
    - no two squares in the same row have the same letter
    - no two squares in the same column have the same letter
    - no two squares in the same *subsquare* has the same letter
  A *subsquare* is found by dividing the board evenly into sqrt(n)-by-sqrt(n)
  pieces. For example, a 4-by-4 board would have 4 subsquares: top left,
  top right, bottom left, bottom right.

Note that most, but not all, of the code is given to you already.
"""
from puzzle import Puzzle
from math import sqrt

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class SudokuPuzzle(Puzzle):
    """Implementation of a Sudoku puzzle."""
    # === Private Attributes ===
    # @type _n: int
    #     The size of the board. Must be 4, 9, 16, or 25.
    # @type _grid: list[list[str]]
    #     A representation of the Sudoku grid. Consists of a list of lists,
    #     where each inner list represents a row of the grid.
    #
    #     Each item of the inner list is either an uppercase letter,
    #     or is the empty string '', representing an empty square.
    #     Each letter must be between 'A' and the n-th letter of the alphabet.
    def __init__(self, grid):
        """Create a new Sudoku puzzle with an initial grid 'grid'.

        Precondition: <grid> is a valid Sudoku grid.

        @type self: SudokuPuzzle
        @type grid: list[list[str]]
        @rtype: None
        """
        self._n = len(grid)
        self._grid = grid

    def __str__(self):
        """Return a human-readable string representation of <self>.

        Note that the numbers at the top and left cycle 0-9,
        to help the user when they want to enter a move.

        @type self: SudokuPuzzle
        @rtype: str

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> print(s)
          01|23
         ------
        0|AB|CD
        1|DC|BA
         ------
        2| D|
        3|  |
        <BLANKLINE>
        """
        m = int(sqrt(self._n))
        s = ''
        # Column label
        s += '  '
        for col in range(self._n):
            s += str(col % 10)
            # Vertical divider
            if (col + 1) % m == 0 and col + 1 != self._n:
                s += '|'
        # Horizontal divider
        s += '\n ' + ('-' * (self._n + m)) + '\n'
        for i in range(self._n):
            # Row label
            s += str(i % 10) + '|'
            for j in range(self._n):
                cell = self._grid[i][j]
                if cell == '':
                    s += ' '
                else:
                    s += str(cell)
                # Vertical divider
                if (j + 1) % m == 0 and j + 1 != self._n:
                    s += '|'
            s = s.rstrip()
            s += '\n'

            # Horizontal divider
            if (i + 1) % m == 0 and i + 1 != self._n:
                s += ' ' + ('-' * (self._n + m)) + '\n'

        return s

    def is_solved(self):
        """Return whether <self> is solved.

        A Sudoku puzzle is solved if its state matches the criteria
        listed at the end of the puzzle description.

        @type self: SudokuPuzzle
        @rtype: bool

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', 'D', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        True
        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'D', 'A', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        False
        """
        # Check for empty cells
        for row in self._grid:
            if '' in row:
                return False

        # Check rows
        for row in self._grid:
            if sorted(row) != list(CHARS[:self._n]):
                return False

        # Check cols
        for i in range(self._n):
            # Note the use of a list comprehension here.
            if sorted([row[i] for row in self._grid]) != list(CHARS[:self._n]):
                return False

        # Check all subsquares
        m = int(sqrt(self._n))
        for x in range(0, self._n, m):
            for y in range(0, self._n, m):
                items = [self._grid[x + i][y + j]
                         for i in range(m)
                         for j in range(m)]

                if sorted(items) != list(CHARS[:self._n]):
                    return False

        # All checks passed
        return True

    def extensions(self):
        """Return list of extensions of <self>.

        This method picks the first empty cell (looking top-down,
        left-to-right) and returns a list of the new puzzle states
        obtained by filling in the empty cell with one of the
        available letters that does not violate any of the constraints
        listed in the problem description. (E.g., if there is
        already an 'A' in the row with the empty cell, this method should
        not try to fill in the cell with an 'A'.)

        If there are no empty cells, returns an empty list.

        @type self: SudokuPuzzle
        @rtype: list[SudokuPuzzle]

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> lst = list(s.extensions())
        >>> len(lst)
        1
        >>> print(lst[0])
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA|D
        3|DC|
        <BLANKLINE>
        """
        # Search for the first empty cell
        row_index, col_index = None, None
        for i in range(self._n):
            row = self._grid[i]
            if '' in row:
                row_index, col_index = i, row.index('')
                break

        if row_index is None:
            return []
        else:
            # Calculate possible letter to fill the empty cell
            letters = self._possible_letters(row_index, col_index)
            return [self._extend(letter, row_index, col_index)
                    for letter in letters]

    # ------------------------------------------------------------------------
    # Helpers for method 'extensions'
    # ------------------------------------------------------------------------
    def _possible_letters(self, row_index, col_index):
        """Return a list of the possible letters for a cell.

        The returned letters must be a subset of the available letters.
        The returned list should be sorted in alphabetical order.

        @type self: SudokuPuzzle
        @type row_index: int
        @type col_index: int
        @rtype: list[str]

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> s._possible_letters(2, 0)
        ['B', 'C']
        >>> s._possible_letters(2, 2)
        ['A']
        """
        # Start with a list of possible letters, A to the Nth Alphabet, where
        # n is the length of the grid.
        possible_letter = list(CHARS[:self._n])
        # check the letters already in the row.
        for letter in self._grid[row_index]:
            if letter in possible_letter:
                possible_letter.remove(letter)
        # check the letters in the column
        for row in self._grid:
            if row[col_index] in possible_letter:
                possible_letter.remove(row[col_index])
        # Check the letters in the subsquare
        # use helper function to find the subsqure the cell is located with in
        location = self._subsquare_finder(row_index, col_index)
        # generate the subsquare using our helper
        sub_square = self._subsquare_generator(location)
        for row in sub_square:
            for letter in row:
                if letter in possible_letter:
                    possible_letter.remove(letter)
        return possible_letter

    def _subsquare_finder(self, row_index, col_index):
        """ Return a list of coordinates of a subsquare given
        a the row location row_index and column location col_index

        The function first identify which subsquare the cell
        is located in, and return the coordinates for the subsquare.

        @type row_index: int
        @type col_index: int
        @rtype: list
        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> print(s)
          01|23
        ------
        0|AB|CD
        1|DC|BA
         ------
        2| D|
        3|  |

        >>> s.subsquare_finder(3, 3)
        [2, 2]
        # 1 in the list is equal to square root of the length
        of the board.
        # So 2, 2 here represent the corner subsquare of the board
        >>> s._subsquare_finder(2, 0)
        [2, 1]
        # The third subsquare in the board, counting from left to right.

        """
        # this takes care of the case for cell locations which contain 0s.
        location = [1, 1]
        # m is the size of the subsquare
        m = int(sqrt(self._n))
        if row_index != 0:
            #  If the column number divide by the size of the subsquare is not a
            # whole number ,we should round it up, since it belongs in the
            # next subsquare. This is like the ceiling function
            if row_index / m > row_index // m:
                location[0] = row_index // m + 1
            else:
                location[0] += int(row_index / m)
        if col_index != 0:
            # if the row number divide by the size of the subsquare is not a
            # whole number, we should round it up. This is like the ceiling
            # function
            if col_index / m > col_index // m:
                location[1] = col_index // m + 1
            else:
                location[1] += int(col_index / m)

        return location

    def _subsquare_generator(self, location):
        """ Return a list of lists representing a sub square given location of
            the subsquare location.

        @type location: list
        @rtype: list of lists

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> s._subsquare_generator([2, 2])
        [['', ''], ['', '']]
        >>> s._subsquare_generator([1,1])
        [['A', 'B'], ['D', 'C']]
        """
        # m is the size of the sub suqare which should be m x m
        m = int(sqrt(self._n))
        # the starting row of the subsquare
        row_start = (location[0] - 1) * m
        # ending row of the subsquare
        row_finish = location[0] * m
        # slice the grid by the row numbers
        new_list = self._grid[row_start:row_finish]
        col_start = (location[1] - 1) * m
        col_finish = location[1] * m
        lst = []
        # slice the grid by column number
        for item in new_list:
            lst.append(item[col_start:col_finish])
        return lst

    def _extend(self, letter, row_index, col_index):
        """Return a new Sudoku puzzle obtained after one move.

        The new puzzle is identical to <self>, except that it has
        the value at position (row_index, col_index) equal to 'letter'
        instead of empty.

        'letter' must be an available letter.
        'row_index' and 'col_index' are between 0-3.

        @type self: SudokuPuzzle
        @type letter: str
        @type row_index: int
        @type col_index: int
        @rtype: SudokuPuzzle

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> print(s._extend('B', 2, 3))
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA| B
        3|DC|
        <BLANKLINE>
        """
        new_grid = [row.copy() for row in self._grid]
        new_grid[row_index][col_index] = letter
        return SudokuPuzzle(new_grid)

    def move(self, move):
        """Return a new puzzle state specified by making the given move.

        Raise a ValueError if <move> represents an invalid move.
        Do *NOT* change the state of <self>. This is not a mutating method!

        @type self: SudokuPuzzle
        @type move: str
        @rtype: Puzzle

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> g = s.move('(2, 1 -> C')
        >>> print(g)
          01|23
         ------
        0|AB|CD
        1|DC|BA
         ------
        2|CD|
        3|  |
        <BLANKLINE>
        """
        # use the helper function to check the format of the string.
        # if it's valid, a list of size 3 is returned.
        lst = self._check_format(move)
        row_index = lst[0]
        col_index = lst[1]
        # Check the possible moves at that location using the helper function.
        valid_moves = self._possible_letters(lst[0], lst[1])
        # make a new grid.
        new_grid = [row.copy() for row in self._grid]
        if lst[2] in valid_moves:
            new_grid[row_index][col_index] = lst[2]
            return SudokuPuzzle(new_grid)
        else:
            raise ValueError

    # ------------------------------------------------------------------------
    # Helper for method 'move'
    # ------------------------------------------------------------------------
    def _check_format(self, move):
        """ Return a list of int and characters given user's input.

        This function first check whether user's input is a valid move.
        If it is a valid move, this function takes in the user's input
        and return a list of size 3. The first item in the list to be returned
        is the row index. The second item in the list to be returned is the
        column index. The third item is the letter to be inserted to the puzzle.

        Raise ValueError, if the move was in the wrong format. Note: This
        function only checks the format of the user input, does not check
        whether the move is a valid move with in the puzzle.

        @type move: str
        @rtype: list

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> s._check_format('(2, 2) -> A')
        [2, 2, A]
        >>> s._check_format('22c')
        ValueError
        >>> s._check_format('(2, 2) -> c')
        ValueError

        """
        # correct length for user input is 11
        if len(move) != 11:
            raise ValueError
        lst = []
        # item at index 1 should be the row number
        row_index = move[1]
        if row_index.isnumeric():
            lst.append(int(row_index))
        else:
            raise ValueError
        # item at index 4 should be column number
        col_index = move[4]
        if col_index.isnumeric():
            lst.append(int(col_index))
        else:
            raise ValueError
        # last valud should be a capital letter
        alpha = move[-1]
        if alpha.isalpha() and alpha.isupper():
            lst.append(alpha)
        else:
            raise ValueError
        return lst

    def find_user_input(self, other):
        """ Return the user input in correct format that user have to put in
            to get from game state at state self to game state state at other

        Precondition: 1.self and other are puzzles which are one move apart.
                      2.self and other are the same type of puzzles
        @type self: SudokuPuzzle
        @type other: SudokuPuzzle
        @rtype: str

        >>>s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> g = s.move('(2, 0) -> C')
        >>> s.find_user_input(g)
        '(2, 0) -> C'
        """
        curr_puzzle = self._grid
        want_puzzle = other._grid
        num_col = len(self._grid[0])
        num_row = self._n
        # Since the puzzles are assumed to be one move apart
        # Find the column which is different and convert that into valid format
        for i in range(num_row):
            for j in range(num_col):
                if curr_puzzle[i][j] != want_puzzle[i][j]:
                    user_input = (i, j)
                    letter = want_puzzle[i][j]
                    return str(user_input) + ' ' + '->' + ' ' + letter
        raise NoinputError

    def same_game_state(self, other):
        """ Return True iff self and other are at the same game state.

        @type self: SudokuPuzzle
        @type other: SudokuPuzzle
        @rtype: bool
        """
        return self._grid == other._grid


class NoinputError(Exception):
    pass

if __name__ == '__main__':
    # Note: the doctest of 'extensions' currently fails. See Part 1.
    import doctest
    doctest.testmod()

    # Here is a bigger Sudoku puzzle
    big = SudokuPuzzle(
        [['E', 'C', '', '', 'G', '', '', '', ''],
         ['F', '', '', 'A', 'I', 'E', '', '', ''],
         ['', 'I', 'H', '', '', '', '', 'F', ''],
         ['H', '', '', '', 'F', '', '', '', 'C'],
         ['D', '', '', 'H', '', 'C', '', '', 'A'],
         ['G', '', '', '', 'B', '', '', '', 'F'],
         ['', 'F', '', '', '', '', 'B', 'H', ''],
         ['', '', '', 'D', 'A', 'I', '', '', 'E'],
         ['', '', '', '', 'H', '', '', 'G', 'I']]
    )
    print(big)

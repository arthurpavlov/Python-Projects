# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""This module contains functions responsible for solving a puzzle.

This module can be used to take a puzzle and generate one or all
possible solutions. It can also generate hints for a puzzle (see Part 4).
"""
from puzzle import Puzzle


def solve(puzzle, verbose=False):
    """Return a solution of the puzzle.

    Even if there is only one possible solution, just return one of them.
    If there are no possible solutions, return None.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds a solution.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: Puzzle | None
    """
    if puzzle.is_solved():
        if verbose:
            print(puzzle)
        return puzzle
    else:
        for item in puzzle.extensions():
            if verbose and not item.is_solved():
                print(item)
            final = solve(item, verbose)
            # if a solved puzzle state is found
            if final is not None:
                return final


def solve_complete(puzzle, verbose=False):
    """Return all solutions of the puzzle.

    Return an empty list if there are no possible solutions.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds all solutions.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: list[Puzzle]
    """
    if puzzle.is_solved():
        if verbose:
            print(puzzle)
        return [puzzle]
    elif len(puzzle.extensions()) == 0:
        return []
    else:
        acc = []
        for item in puzzle.extensions():
            if verbose and not item.is_solved():
                print(item)
            acc += solve_complete(item, verbose)
        return acc


def hint_by_depth(puzzle, n):
    """Return a valid str representation of what the user would need to input to
    get a step closer to the solution.

    If <puzzle> is already solved, return the string 'Already at a solution!'.
    If <puzzle> cannot lead to a solution or other valid state within <n> moves,
    return the string 'No possible extensions!'.

    Precondition: n >= 1

    @type puzzle: Puzzle
    @type n: int
        The number of steps.
    @rtype: str
    """
    if puzzle.is_solved():
        return 'Already at a solution!'
    soln = _get_sol_and_num_moves(puzzle)
    # if number of steps took to get solution is greater than n move, there is
    # no solution in n move, so set it to None.
    if soln is not None:
        if soln[1] > n:
            soln = None
    puzzles_with_one_move = puzzle.extensions()
    # if soln is None, we did not find a solution with in n moves.
    if soln is None:
        if len(_items_at_move(puzzle, n)) != 0:
            # if there exists a valid state after n moves, pick the first one.
            valid_state = _items_at_move(puzzle, n)[0]
            if n > 1:
                # find which one of the first moves, the valid state belongs to
                puzzle_want = find_hint_puzzle(valid_state, puzzles_with_one_move, n)
                return puzzle.find_user_input(puzzle_want)
            else:
                # valid state is one move away, find the user input to that.
                return puzzle.find_user_input(valid_state)
        else:
            return 'No possible extensions!'
    else:
        solved_puzzle = soln[0]
        steps_took = soln[1]
        if n == 1:
            return puzzle.find_user_input(soln[0])
        else:
            puzzle_want = find_hint_puzzle(solved_puzzle, puzzles_with_one_move,
                                           steps_took)
            return puzzle.find_user_input(puzzle_want)


def find_hint_puzzle(solved_puzzle, puzzles_with_one_move, steps_took):
    """ Return the one puzzle which would lead user to the solution or a
    valid state.

    @type solved_puzzle: Puzzle
    @type puzzles_with_one_move: list[Puzzle]
    @type steps_took: int
    @rtype: Puzzle
    """
    for puzzle in puzzles_with_one_move:
        for item in _items_at_move(puzzle, steps_took - 1):
            if solved_puzzle.same_game_state(item):
                return puzzle


def _items_at_move(puzzle, d):
        """Return a list of possible puzzles after d number of possible moves made to the puzzle.
         created by extensions game sate.

        Precondition: d >= 0.

        @type puzzle: Puzzle
        @type d: int
        @rtype: list
        """
        if d == 0:
            return [puzzle]
        else:
            items = []
            for new_state in puzzle.extensions():
                items.extend(_items_at_move(new_state, d - 1))
            return items


def _get_sol_and_num_moves(puzzle, n=0):
        """ Return a tuple of solved item and the number of moves it took to get
        to the solution

        If it did not find a solution in n stpes, return None

        @type puzzle: Puzzle
        @type n: int
        @rtype: tuple(Puzzle, int) | None
        """
        # if there is no extension for the puzzle
        if len(puzzle.extensions()) == 0:
            return None
        else:
            # if item is solved
            for new_state in puzzle.extensions():
                if new_state.is_solved():
                    return new_state, n + 1
            # recursive to solve the puzzle
            for new_state in puzzle.extensions():
                if new_state is not None:
                    return _get_sol_and_num_moves(new_state, n + 1)

if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle
    s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])

    # s = SudokuPuzzle([['B', 'A', 'D', 'C'],
    #                  ['D', 'C', 'A', ''],
    #                  ['C', 'D', 'A', 'B'],
    #                  ['A', 'B', 'C', 'D']])

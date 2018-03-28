# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Module containing the Controller class."""
from view import TextView, WebView
from puzzle import Puzzle
from solver import *


class _PuzzleTree:
    """A recursive tree data structure.

    Note: This is a private class, which is meant to be used in this module
    by the Controller class, but not by client code.

    === Attributes ===
    @type current_move: Puzzle
        This is the root of the tree, which is type Puzzle.
    @type next_moves: list[Puzzle]
        A list of next puzzles created by user after they entered one move.
    @type prev_moves: list[Puzzle]
        A list of puzzles one move prior to the current puzzle.
    @type user_input: str
        The input user gamer entered inorder to get to the current puzzle
    """

    # === Representation Invariants ===
    # - If self.current_move is None then Puzzle is empty.
    #   This setting of attributes represents an empty Tree.
    # - self.next_moves does not contain any empty puzzles.
    # - self.next_moves does not contain duplicate puzlles

    def __init__(self, puzzle, user_input=''):
        """Initialize a new Tree with the given root value.

        If <current_move> is None, the tree is empty.
        A new tree always has no subtrees.

        @type self: _PuzzleTree
        @type puzzle : Puzzle
        @type user_input : str
        @rtype: None
        """
        self.current_move = puzzle
        self.next_moves = []
        self.prev_moves = []
        self.user_input = user_input

    def check_duplicate(self, new_puzzle_tree):
        """ If a PuzzleTree obj with the same state as <new_puzzle_tree>,
        return a tuple with the duplicate obj and True. If no duplicate
        is found, return a tuple of <new_puzzle_tree> and False.

        Precondition: self.next_moves is not empty

        @type self: _PuzzleTree
        @type new_puzzle_tree: _PuzzleTree
        @rtype: tuple(_PuzzleTree, bool)

        """
        duplicate = False
        for puzzle_tree in self.next_moves:
            new_move = new_puzzle_tree.current_move
            if new_move.same_game_state(puzzle_tree.current_move):
                duplicate = True
                return puzzle_tree, duplicate
        return new_puzzle_tree, duplicate

    def empty_next_move(self):
        """ Return true iff next move attribute of self is empty

        @type: _PuzzleTree
        @rtype: bool
        """
        return self.next_moves == []

    def empty_prev_move(self):
        """ Return truue iff prev move attribute of self if empty

        @type self: _PuzzleTree
        @rtype: bool
        """
        return self.prev_moves == []

    def add_next_move(self, new_puzzle):
        """ Add to the next move list a new puzzle Tree

        @type self: _PuzzleTree
        @type new_puzzle: _PuzzleTree
        @rtype: None
        """
        self.next_moves.append(new_puzzle)

    def add_prev_move(self, prev_puzzle):
        """ Add to the previous move list the old puzzletree connecting
        to the new puzzle tree

        @type self: _PuzzleTree
        @type prev_puzzle: _PuzzleTree
        @rtype: None
        """
        self.prev_moves.append(prev_puzzle)


class Controller:
    """Class responsible for connection between puzzles and views.

    You may add new *private* attributes to this class to help you
    in your implementation.
    """
    # === Private Attributes ===
    # @type _puzzle: _PuzzleTree
    #     The puzzle tree associated with this game controller
    # @type _view: View
    #     The view associated with this game controller

    def __init__(self, puzzle, mode='text'):
        """Create a new controller.

        <mode> is either 'text' or 'web', representing the type of view
        to use.

        By default, <mode> has a value of 'text'.

        @type puzzle: Puzzle
        @type mode: str
        @rtype: None
        """
        self._puzzle = _PuzzleTree(puzzle)
        if mode == 'text':
            self._view = TextView(self)
        elif mode == 'web':
            self._view = WebView(self)
        else:
            raise ValueError()

        # Start the game.
        self._view.run()

    def state(self):
        """Return a string representation of the current puzzle state.

        @type self: Controller
        @rtype: str
        """
        return str(self._puzzle.current_move)

    def act(self, action):
        """Run an action represented by string <action>.

        Return a string representing either the new state or an error message,
        and whether the program should end.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """
        try:
            if action == ':SOLVE':
                return self.action_solve()
            elif action == ':SOLVE-ALL':
                return self.action_solve_all()
            elif action == 'exit':
                return '', True
            elif action == ':UNDO':
                return self.action_undo()
            elif action == ':ATTEMPTS':
                return self.action_attempts()
            elif action[:5] == ':HINT':
                return self.action_hint(action)
            else:
                return self.action_move(action)
        except ValueError:
            print('InvalidMove. Please try again!')
            return '', False
        except CannotUndo:
            print('Sorry, there was no previous state')
            return '', False
        except AttemptError:
            print('Sorry, no attempt was made from current game')
            return '', False
        except NoSolutionError:
            return 'Sorry, no solution was found!', True

    # ------------------------------------------------------------------------
    # Helpers for method 'act'
    # ------------------------------------------------------------------------

    def action_solve(self):
        """ Return a solution of the puzzle.

        If there is no solution, print a message saying that.

        @type: Controller
        @rtype: (str, bool)
        """
        if solve(self._puzzle.current_move) is None:
            raise NoSolutionError()
        else:
            return str(solve(self._puzzle.current_move)), True

    def action_solve_all(self):
        """ return all possible solution of the puzzle.

        If there is no solution, print a message saying that

        @type: Controller
        @rtype:(str, bol)
        """
        sol_lst = solve_complete(self._puzzle.current_move)
        if len(sol_lst) == 0:
            raise NoSolutionError()
        acc = ''
        for item in sol_lst:
            acc += str(item) + '\n'
        return acc, True

    def action_undo(self):
        """ Rever the puzzle state to the previous one.

        If there is no previous move, raise an error and let act handle that
        error

        @type: Controller
        @rtype:(str, bool)
        """
        if self._puzzle.empty_prev_move():
            raise CannotUndo()
        else:
            self._puzzle = self._puzzle.prev_moves[-1]
            return str(self._puzzle.current_move), False

    def action_attempts(self):
        """Print out all of the puzzle states resulting from moves the user made
        at the current state, along with the string the user typed in to make
        the corresponding move.

        The states and moves should be printed out in the order the user made
        them. If the user hasn't made any moves from the current state
        (i.e., they just reached the state for the first time),
        print a message saying that.

        @type: Controller
        @rtype: (str, bool)
        """
        if self._puzzle.empty_next_move():
            raise AttemptError
        else:
            s = ''
            i = 1
            for puzzle_tree in self._puzzle.next_moves:
                s += 'attempt' + str(i) + '\n'
                s += str(puzzle_tree.current_move) + '\n'
                s += 'Your command:' + puzzle_tree.user_input + '\n'
                s += '\n'
                i += 1
            s += 'Current game' + '\n'
            s += str(self._puzzle.current_move) + '\n'
            return s, False

    def action_hint(self, action):
        """ Return a "hint" for a puzzle state is the string representation of a
        valid move from the current state that brings the user one step closer
        to solving the puzzle.

        if no solution is found in move, but a valid state is found in n moves,
        return the string representation of a move that would lead
        to that state.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """
        self._check_format(action)
        n = int(action[6:])
        hint = hint_by_depth(self._puzzle.current_move, n)
        if hint == 'No possible extensions!':
            return 'No hint was found! Please try again!', False
        elif input == 'Already at a solution!':
            return 'Already at a solution!', False
        else:
            return hint, False

    # This is a helper function for action_hint

    def _check_format(self, action):
        """ Check the format of user input specifically for Hint.

        Raise Value error, if there exists letter after the 6th index,
        or the number of moves indicated is less than 1.

        @type self: Controller
        @type action: str
        @rtype: None
        """
        for letter in action[6:]:
            if not letter.isnumeric():
                raise ValueError()
        n = int(action[6:])
        if n < 1:
            raise ValueError()

    def action_move(self, action):
        """ Change the game state according to command given by action

        @type self: Controller
        @type action: str
        @rtype: None
        """
        # create a new puzzle tree with the given action
        new_puzzle_game = self._puzzle.current_move.move(action)
        new_tree = _PuzzleTree(new_puzzle_game, action)
        # before adding the new tree to the tree, check for duplicates
        if not self._puzzle.empty_next_move():
            puzzle_tree = self._puzzle.check_duplicate(new_tree)[0]
            duplicate = self._puzzle.check_duplicate(new_tree)[1]
            if duplicate:
                self._puzzle = puzzle_tree
                curr_puzzle = self._puzzle.current_move
                return self.check_puzzle_solved(curr_puzzle)
            else:
                self.update_game(new_tree)
                curr_puzzle = self._puzzle.current_move
                return self.check_puzzle_solved(curr_puzzle)

        # no duplicate possible, since there is no next move
        else:
            self.update_game(new_tree)
            curr_puzzle = self._puzzle.current_move
            return self.check_puzzle_solved(curr_puzzle)

    def update_game(self, new_tree):
        """ Update the game according to gamer's command.

        @type self: Controller
        @type new_tree: _PuzzleTree
        @rtype: None
        """
        self._puzzle.add_next_move(new_tree)
        new_tree.add_prev_move(self._puzzle)
        self._puzzle = new_tree

    def check_puzzle_solved(self, curr_puzzle):
        """ Return a tuple of a string representation of current
        puzzle and a boolean express to determine whether the
        game should continue.

        @type curr_puzzle: Puzzle
        @rtype: (str, bool)
        """
        if curr_puzzle.is_solved():
            return str(curr_puzzle), True
        else:
            return str(curr_puzzle), False


class InvalidMove(Exception):
    pass


class CannotUndo(Exception):
    pass


class AttemptError(Exception):
    pass


class NoSolutionError(Exception):
    pass

if __name__ == '__main__':
    from sudoku_puzzle import *
    s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'],
        ['', 'D', '', ''], ['', '', '', '']])
    c = Controller(s)

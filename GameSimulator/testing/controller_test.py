# Assignment 2 - Test Runner for the Controller
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
#
# ***IMPORTANT NOTE***
# Because you have some flexibility in how the controller behaves
# (e.g., the exact messages which are displayed to the user),
# we will not be grading the output of the controller automatically.
#
# Instead, what we provide here is a structured way to feed
# the controller certain instructions, and save the output to a file.
# Your TAs will be reading these outputs and assessing their
# correctness.
# We have given one example in the 'main' block below.
# We encourage you to make your own tests, and
# you may share the outputs of these tests with your classmates.
# ---------------------------------------------
from controller import Controller
import sys
from io import StringIO


def run_controller(puzzle, commands, filename=''):
    """Simulate running the game on a given puzzle and set of commands.

    If a file name is specified, write output to that file.
    Otherwise, print to the screen.

    Precondition: <commands> must be a sequence of commands which causes
    the controller to terminate (e.g., by entering 'exit' or ':SOLVE').

    @type puzzle: Puzzle
    @type commands: list[str]
    @rtype: None
    """
    out = StringIO('')
    sys.stdout = out
    sys.stdin = StringIO('\n'.join(commands))
    Controller(puzzle)
    r = out.getvalue()
    out.close()
    sys.stdin = sys.__stdin__
    sys.stdout = sys.__stdout__

    outputs = r.split('Enter a command:\n> ')
    messages = []
    for i in range(len(outputs)):
        messages.append(outputs[i])
        if i < len(commands):
            messages.append('Enter a command:\n> ')
            messages.append(commands[i] + '\n')

    if filename == '':
        print(''.join(messages))
    else:
        with open(filename, 'w') as result_file:
            result_file.writelines(messages)

if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle
    s = SudokuPuzzle([['A', 'B', 'C', 'D'],
                      ['C', 'D', 'A', 'B'],
                      ['B', 'A', '', ''],
                      ['D', 'C', '', '']])

    run_controller(s, ['(2, 2) -> D',
                       '(2, 3) -> D',  # Note: invalid move
                       ':UNDO',
                       '(2, 3) -> C',
                       ':UNDO',
                       ':ATTEMPTS',
                       ':SOLVE'],
                   # If you omit the following filename,
                   # the output will be printed to the console.
                   # Otherwise, after you run the program, open
                   # the new file to see the output.
                   'solved.txt')

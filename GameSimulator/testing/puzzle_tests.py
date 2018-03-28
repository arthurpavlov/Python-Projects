# Assignment 2 - Unit Tests for Puzzle and Solver
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
import unittest
from sudoku_puzzle import SudokuPuzzle
from word_ladder_puzzle import WordLadderPuzzle
from solver import solve, solve_complete


class SudokuPossibleLettersTest(unittest.TestCase):
    # Note that we are explicitly testing the _possible_letters
    # private method. This is a little unorthodox (usually we would
    # only test public methods), but because we aren't asking you to
    # do much for the SudokuPuzzle class, we wanted to isolate
    # exactly what we're looking for.

    def test_sample1(self):
        s = SudokuPuzzle([['A', 'B', 'C', 'D'],
                          ['C', 'D', 'A', 'B'],
                          ['B', 'A', '', ''],
                          ['D', 'C', '', '']])
        self.assertEqual(s._possible_letters(2, 2), ['D'])

    def test_sample2(self):
        s = SudokuPuzzle([['A', 'B', '', 'D'],
                          ['C', 'D', '', 'B'],
                          ['B', '', '', ''],
                          ['D', '', '', '']])
        self.assertEqual(s._possible_letters(2, 2), ['A', 'C', 'D'])

    def test_sample3(self):
        s = SudokuPuzzle([['A', 'B', '', 'D'],
                          ['C', 'D', '', 'B'],
                          ['B', '', '', ''],
                          ['D', '', 'A', '']])
        self.assertEqual(s._possible_letters(2, 3), ['C'])


class SudokuMoveTest(unittest.TestCase):
    def test_sample(self):
        s = SudokuPuzzle([['A', 'B', 'C', 'D'],
                          ['C', 'D', 'A', 'B'],
                          ['B', 'A', '', ''],
                          ['D', 'C', '', '']])
        new_s = s.move('(2, 2) -> D')
        s1 = SudokuPuzzle([['A', 'B', 'C', 'D'],
                           ['C', 'D', 'A', 'B'],
                           ['B', 'A', 'D', ''],
                           ['D', 'C', '', '']])
        self.assertEqual(str(new_s), str(s1))

    def test_invalid_move(self):
        s = SudokuPuzzle([['A', 'B', 'C', 'D'],
                          ['C', 'D', 'A', 'B'],
                          ['B', 'A', '', ''],
                          ['D', 'C', '', '']])
        with self.assertRaises(ValueError):
            s.move('(2, 2) -> C')

    def test_bad_format(self):
        s = SudokuPuzzle([['A', 'B', 'C', 'D'],
                          ['C', 'D', 'A', 'B'],
                          ['B', 'A', '', ''],
                          ['D', 'C', '', '']])
        with self.assertRaises(ValueError):
            s.move('2 2 C')

    def test_nine_extensions(self):
        big = SudokuPuzzle([
            ['E', 'C', '', '', 'G', '', '', '', ''],
            ['F', '', '', 'A', 'I', 'E', '', '', ''],
            ['', 'I', 'H', '', '', '', '', 'F', ''],
            ['H', '', '', '', 'F', '', '', '', 'C'],
            ['D', '', '', 'H', '', 'C', '', '', 'A'],
            ['G', '', '', '', 'B', '', '', '', 'F'],
            ['', 'F', '', '', '', '', 'B', 'H', ''],
            ['', '', '', 'D', 'A', 'I', '', '', 'E'],
            ['', '', '', '', 'H', '', '', 'G', 'I']])

        self.assertEqual(big._possible_letters(4, 4),
                         ['E'])
        self.assertEqual(big._possible_letters(3, 3),
                         ['E', 'G', 'I'])


class WordLadderPart1Test(unittest.TestCase):
    # Note: replace the given wordsEn.txt with
    # the much smaller provided file wordsEnTest.txt.
    #
    # Keep in mind that we aren't specifying an output
    # format, so we arn't testing the internal state
    # of your WordLadder class explicitly.
    # Instead, we'll be running some implicit tests based
    # on the structure required by the 'extensions' method.
    def test_is_not_solved_start(self):
        word_ladder = WordLadderPuzzle('mist', 'mare')
        self.assertFalse(word_ladder.is_solved())

    def test_is_solved_start(self):
        word_ladder = WordLadderPuzzle('mist', 'mist')
        self.assertTrue(word_ladder.is_solved())

    def test_no_extensions(self):
        word_ladder = WordLadderPuzzle('mist', 'mare')
        self.assertEqual(word_ladder.extensions(), [])

    def test_one_extensions(self):
        word_ladder = WordLadderPuzzle('mire', 'mare')
        self.assertEqual(len(word_ladder.extensions()), 1)

    # Also checking is_solved here.
    def test_solved_extension(self):
        word_ladder = WordLadderPuzzle('mire', 'mare')
        self.assertTrue(word_ladder.extensions()[0].is_solved())

    def test_alphabetical(self):
        word_ladder = WordLadderPuzzle('mare', 'mire')
        # Should have 4 extensions: 'care', 'male', 'mars', 'mire',
        # in that order.
        exts = word_ladder.extensions()
        self.assertEqual(len(exts), 4)
        self.assertTrue(exts[-1].is_solved())

    def test_no_duplicates(self):
        word_ladder = WordLadderPuzzle('mare', 'mire')
        exts = word_ladder.extensions()
        should_be_care = exts[0]
        # Only one extension: 'cars'. 'mare' should not be revisited.
        self.assertEqual(len(should_be_care.extensions()), 1)
        should_be_cars = should_be_care.extensions()[0]
        # 'cars' should extend to 'mars'.
        self.assertEqual(len(should_be_cars.extensions()), 1)
        should_be_mars = should_be_cars.extensions()[0]
        # 'mars' has no more extensions.
        self.assertEqual(len(should_be_mars.extensions()), 0)


class WordLadderPart2Test(unittest.TestCase):
    def test_move_simple(self):
        word_ladder = WordLadderPuzzle('mare', 'mire')
        new_ladder = word_ladder.move('mire')
        self.assertTrue(new_ladder.is_solved())

    def test_invalid_word1(self):
        word_ladder = WordLadderPuzzle('mare', 'mire')
        with self.assertRaises(ValueError):
            # Not in dictionary
            word_ladder.move('maze')

    def test_invalid_word2(self):
        word_ladder = WordLadderPuzzle('mare', 'mire')
        with self.assertRaises(ValueError):
            # In dictionary, but not one letter away.
            word_ladder.move('cars')


class SolveTest(unittest.TestCase):
    def test_solve_one(self):
        s = SudokuPuzzle([['A', 'B', 'C', 'D'],
                          ['C', 'D', 'A', 'B'],
                          ['B', 'A', '', ''],
                          ['D', 'C', '', '']])
        solved = solve(s)
        # Note: when we run our tests, we will replace
        # this with our own "is_solved" method
        # to make sure the puzzle is correctly solved.
        # This means you should *not* change the internal state
        # of the Sudoku Puzzle class!
        self.assertTrue(solved.is_solved())

    def test_solve_complete(self):
        s = SudokuPuzzle([['A', 'B', '', ''],
                          ['C', 'D', '', ''],
                          ['B', '', '', ''],
                          ['D', '', 'A', '']])

        solutions = solve_complete(s)
        self.assertEqual(len(solutions), 2)
        for solution in solutions:
            self.assertTrue(solution.is_solved())

    def test_hint_already_solved(self):
        s = SudokuPuzzle([['A', 'B', 'C', 'D'],
                          ['C', 'D', 'A', 'B'],
                          ['B', 'A', 'D', 'C'],
                          ['D', 'C', 'B', 'A']])
        self.assertEqual(hint_by_depth(s, 10), 'Already at a solution!')

    def test_hint_no_possible_extensions(self):
        s = SudokuPuzzle([['A', 'B', 'C', 'D'],
                          ['C', 'D', '', 'B'],
                          ['B', 'A', 'D', 'C'],
                          ['C', '', 'A', 'A']])
        self.assertEqual(hint_by_depth(s, 10), 'No possible extensions!')

    def test_hint_can_reach_solution(self):
        s = SudokuPuzzle([['A', 'B', 'C', 'D'],
                          ['C', 'D', '', 'B'],
                          ['B', 'A', 'D', 'C'],
                          ['D', 'C', 'B', 'A']])
        for p in s.extensions():
            print(p)
        self.assertEqual(hint_by_depth(s, 10), '(1, 2) -> A')

    def test_hint_valid_state(self):
        s = SudokuPuzzle([['', 'B', 'C', 'D'],
                          ['C', 'D', '', 'B'],
                          ['B', '', 'D', 'C'],
                          ['D', 'C', 'B', '']])
        self.assertTrue(hint_by_depth(s, 3) in ['(0, 0) -> A',
                                                '(1, 2) -> A',
                                                '(2, 1) -> A',
                                                '(3, 3) -> A'])

if __name__ == '__main__':
    unittest.main(exit=False)

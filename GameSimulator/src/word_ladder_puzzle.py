# Assignment 2 - Puzzle Game
#
# CSC148 Fall 2015, University of Toronto
# Instructor: David Liu
# ---------------------------------------------
"""Word ladder module.

Your task is to complete the implementation of this class so that
you can use it to play Word Ladder in your game program.

Rules of Word Ladder
--------------------
1. You are given a start word and a target word (all words in this puzzle
   are lowercase).
2. Your goal is to reach the target word by making a series of *legal moves*,
   beginning from the start word.
3. A legal move at the current word is to change ONE letter to get
   a current new word, where the new word must be a valid English word.

The sequence of words from the start to the target is called
a "word ladder," hence the name of the puzzle.

Example:
    Start word: 'make'
    Target word: 'cure'
    Solution:
        make
        bake
        bare
        care
        cure

    Note that there are many possible solutions, and in fact a shorter one
    exists for the above puzzle. Do you see it?

Implementation details:
- We have provided some starter code in the constructor which reads in a list
  of valid English words from wordsEn.txt. You should use this list to
  determine what moves are valid.
- **WARNING**: unlike Sudoku, Word Ladder has the possibility of getting
  into infinite recursion if you aren't careful. The puzzle state
  should keep track not just of the current word, but all words
  in the ladder. This way, in the 'extensions' method you can just
  return the possible new words which haven't already been used.
"""
from puzzle import Puzzle


CHARS = 'abcdefghijklmnopqrstuvwyz'


class WordLadderPuzzle(Puzzle):
    """A word ladder puzzle."""
    # === Private attributes ===
    # @type _words: list[str]
    #     List of allowed English words
    # @type _start: str
    #    the starting word of the game
    # @type _target: str
    #    the target word of the game
    # @type _moves: list of str
    #    the list of moves player has made

    def __init__(self, start, target):
        """Create a new word ladder puzzle with given start and target words.

        Note: you may add OPTIONAL arguments to this constructor,
        but you may not change the purpose of <start> and <target>.

        @type self: WordLadderPuzzle
        @type start: str
        @type target: str
        @rtype: None
        """
        # Code to initialize _words - you don't need to change this.
        self._words = []
        with open('C:\\Users\\ASUS\\Desktop\\CSC148 NOTES\\csc148copy\\assignments\\a2\\wordsEnTest.txt') as wordfile:
            for line in wordfile:
                self._words.append(line.strip())
        if len(start) != len(target):
            raise InvalidGameError()
        self._start = start
        self._target = target
        self._moves = [self._start]

    def __str__(self):
        """Return a human-readable string representation of <self>

        @type self: WordLadderPuzzle
        @rtype: str

        >>> s = WordLadderPuzzle('mare', 'mire')
        >>> g = s.move('make')
        >>> print(g)
        Start word: mare
        Target word: mire
        Your moves:
        mare
        make
        >>> f = g.move('cake')
        >>> print(f)
        Start word: mare
        Target word: mire
        Your moves:
        mare
        make
        cake
        """
        # add the starting word
        s = 'Start word: ' + self._start
        # add the target move
        s += "\n" + 'Target word: ' + self._target
        s += '\n' + 'Your moves:'
        # add all the moves player made
        for move in self._moves:
            s += "\n" + move
        return s

    def is_solved(self):
        """ Return whether the puzzle is in solved state
        @type self; WordLadderPuzzle
        @rtype: bool
        """
        # if last move = target, puzzle is solved.
        if self._moves[-1] == self._target:
            return True
        return False

    def extensions(self):
        """Return a list of possible new states after a valid move.

        The valid move must change exactly one character of the
        current word, and must result in an English word stored in
        self._words.

        You should *not* perform any moves which produce a word
        that is already in the ladder.

        The returned moves should be sorted in alphabetical order
        of the produced word.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> s = WordLadderPuzzle('cake', 'bake')
        >>> g = s.extensions()
        >>> len(g)
        28
        >>> print(g[0])
        Start word: mare
        Target word: mire
        Your moves:
        mare
        bare
        >>> print(g[1])
        Start word: mare
        Target word: mire
        Your moves:
        mare
        care
        """
        puzzles = []
        list_words = self._possible_words()
        # extension always explores the last word in the game
        # so words already explored is equal to self._moves
        words_explored = self._moves
        for word in words_explored:
            if word in list_words:
                list_words.remove(word)
        list_words.sort()
        for word in list_words:
            new_game = WordLadderPuzzle(self._start, self._target)
            new_game._moves += self._moves[1:]
            new_game._moves.append(word)
            puzzles.append(new_game)
        return puzzles

    def _possible_words(self):
        """ Takes the current word and return a list of possible
            words that are valid.

        @type self: WordLadderPuzzle
        @rtype: list of str

        >>> s = WordLadderPuzzle('mare', 'mire')
        >>> s._possible_words()
        ['bare', 'care', 'dare', 'fare', 'hare', 'mace', 'made', 'mage', 'make',
         'male', 'mane', 'marc', 'mark', 'marl', 'mars', 'mart', 'marx', 'mary',
          'mate', 'maze', 'mere', 'mire', 'more', 'pare', 'rare', 'tare', 'ware'
          , 'yare']
        >>> s = WordLadderPuzzle('ahh', 'cat')
        ['aah', 'aha', 'ahs', 'ash']
        """
        possible_words = []
        letters = []
        curr_word = self._moves[-1]
        for letter in curr_word:
            letters.append(letter)
        # find whether a word is a letter different from current word
        for word in self._words:
            repeat = 0
            if len(word) == len(curr_word):
                index = 0
                for letter in word:
                    if letter == letters[index]:
                        index += 1
                        repeat += 1
                    else:
                        index += 1
                if len(curr_word) >= 2:
                    if repeat == len(curr_word) - 1:
                        possible_words.append(word)
                else:
                    possible_words.append(word)
        # if starting word is in the list, delete it.
        if self._start in possible_words:
            possible_words.remove(self._start)
        return possible_words

    def move(self, move):
        """ Return a new puzzle state specified by making the given move.

        @type move: str
        @rtype: WordLadderPuzzle

        >>> s = WordLadderPuzzle('mare', 'mire')
        >>> g = s.move('make')
        >>> print(g)
        Start word: mare
        Target word: mire
        Your moves:
        mare
        make
        >>> f = g.move('cake')
        >>> print(f)
        Start word: mare
        Target word: mire
        Your moves:
        mare
        make
        cake
        """
        valid_words = self._possible_words()
        if move in valid_words:
            new_game = WordLadderPuzzle(self._start, self._target)
            new_game._moves += self._moves[1:]
            new_game._moves.append(move)
            return new_game
        else:
            raise ValueError

    def same_game_state(self, other):
        """ Return True iff self and other are at the same game state.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle
        @rtype: bool
        """
        return self._moves[-1] == other._moves[-1]

    def find_user_input(self, other):
        """ Return the user input in correct format that user must input to
            get from the current game state to the game state at <other>.

        Precondition: 1. self and <other> are puzzles which are one move apart
                      2. self and <other> are the same type of puzzles

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle
        @rtype: str
        """
        if len(self._moves) == len(other._moves) - 1:
            return other._moves[-1]
        else:
            raise NoinputError()


class NoinputError(Exception):
    pass


class InvalidGameError(Exception):
    pass

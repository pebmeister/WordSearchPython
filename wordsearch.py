# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 13:20:11 2024

@author: Paul Baxter
"""
import random
import argparse
import numpy
import numpy as np


class WordSearch:
    rows: int
    cols: int
    words: numpy.array(str)
    board: numpy.array(str)
    dir_list: list
    row_list: list
    col_list: list
    error: bool
    failed_word: str
    row_col_offsets: list

    # initialize
    def __init__(self, rows: int, cols: int, words: list) -> None:
        self.rows = rows
        self.cols = cols
        self.words = np.array(words)
        self.board = np.eye(rows, cols, dtype=np.str_)
        self.dir_list = list(range(8))
        self.row_list = list(range(rows))
        self.col_list = list(range(cols))
        self.error = False
        self.failed_word = ''

        # row col offsets for directions
        self.row_col_offsets = [
            [-1, 0],
            [1, 0],
            [0, -1],
            [0, 1],
            [-1, -1],
            [-1, 1],
            [1, -1],
            [1, 1]]

        self.clear_board()
        self.add_words(self.words)

    # -------------------------------------------------------------

    def clear_board(self) -> None:
        # * represents a blank spot in the board
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col] = '*'

    # -------------------------------------------------------------

    def fill_blanks(self) -> None:
        list_upper = list(map(chr, range(ord('A'), ord('Z'))))
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == '*':
                    index = random.randrange(len(list_upper))
                    self.board[row][col] = list_upper[index]

    # -------------------------------------------------------------

    # check if a word fits in the given position and direction
    def word_fits(self, word: str, row: int, col: int, direction: int) -> bool:
        # assign current row and column
        rr = row
        cc = col

        # get the row and column increment
        row_inc = self.row_col_offsets[direction][0]
        col_inc = self.row_col_offsets[direction][1]

        # loop through each letter
        for ch in word:
            # make sure we are still on the board
            if rr < 0 or rr >= self.rows:
                return False
            if cc < 0 or cc >= self.cols:
                return False

            # check if letter is the same or blank
            c = self.board[rr][cc]
            if ch != c and c != '*':
                return False

            # increment row and column
            rr += row_inc
            cc += col_inc

        return True

    # -------------------------------------------------------------

    # place a word in puzzle
    # must first call word_fits
    def place_word(self, word: str, row: int, col: int, direction: int) -> None:
        row_inc = self.row_col_offsets[direction][0]
        col_inc = self.row_col_offsets[direction][1]
        for ch in word:
            self.board[row][col] = ch
            row += row_inc
            col += col_inc

    # -------------------------------------------------------------

    # add one word to the board in a random location and direction
    def add_word(self, word: str) -> bool:
        random.shuffle(self.row_list)
        random.shuffle(self.col_list)
        random.shuffle(self.dir_list)

        for row in self.row_list:
            for col in self.col_list:
                for d in self.dir_list:
                    if self.word_fits(word, row, col, d):
                        self.place_word(word, row, col, d)
                        return True

        self.error = True
        self.failed_word = word
        return False

    # -------------------------------------------------------------

    # add the words to the board
    # return True if success
    def add_words(self, words: numpy.ndarray) -> bool:

        # words tend to fit easier if long words are added first
        word: str
        for word in np.array(sorted(words, key=len, reverse=True)):
            word_added: bool = self.add_word(word)

            if not word_added:
                return False
        return True

    # -------------------------------------------------------------

    # print the board
    def print_board(self, margin: int) -> None:
        for row in range(self.rows):
            for i in range(margin):
                print('', end=' ')
            for col in range(self.cols):
                print(self.board[row][col], end=' ')
            print()

    # -------------------------------------------------------------

    def print_words(self, word_width: int, num_columns: int) -> None:

        col = 0
        for word in self.words:
            l: int = word_width - len(word)
            print(word, end='')
            for i in range(l):
                print(' ', end='')
            if col == num_columns - 1:
                print()
                col = 0
                continue
            col += 1

    # -------------------------------------------------------------


def main():
    # create parser
    desc_str = "This program creates a wordsearch."
    parser = argparse.ArgumentParser(prog='wordsearch', description=desc_str)
    # add expected arguments
    parser.add_argument('-cols', dest='cols', type=int, required=True, help='number of columns')
    parser.add_argument('-rows', dest='rows', type=int, required=True, help='number of rows')
    parser.add_argument('-tries', dest='tries', type=int, default=1, required=False,
                        help='max number of attempts to make puzzle')
    parser.add_argument('-margin', dest='margin', type=int, default=12, required=False, help='left margin for puzzle')
    parser.add_argument('-ww', dest='word_width', type=int, default=20, required=False,
                        help='width for column of word list')
    parser.add_argument('-wc', dest='word_cols', type=int, default=4, required=False,
                        help='number of columns for word list')
    parser.add_argument(dest="words", nargs='+', type=str, help='words to add')

    # parse args
    try:
        args = parser.parse_args()

    except argparse.ArgumentError:
        print('Argument error. Unable to parse arguments.')
        parser.print_help()
        return

    except argparse.ArgumentTypeError:
        print('Argument type error. Unable to parse arguments.')
        parser.print_help()
        return

    word = ''
    # try to make the word search
    for tries in range(args.tries):

        # create the wordsearch
        ws = WordSearch(args.rows, args.cols, args.words)

        # check for an error
        if not ws.error:
            ws.fill_blanks()
            print()
            ws.print_board(args.margin)
            print()
            print()
            ws.print_words(args.word_width, args.word_cols)
            print()
            return

        # get the word that failed
        word = ws.failed_word

    print("Unable to add word", word)

    # -------------------------------------------------------------


# call main
if __name__ == '__main__':
    main()

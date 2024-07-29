# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 13:20:11 2024

@author: Paul Baxter
"""
import random, argparse
import numpy as np

class wordsearch:

    # initialize
    def __init__(self, rows, cols, words):
        self.rows = rows
        self.cols = cols
        self.words = np.array(words)
        self.board = np.eye(rows, cols, dtype=np.str_)
        self.dir_array = list(range(8))
        self.row_array = list(range(rows))
        self.col_array = list(range(cols))
        self.error = False
        self.failed_word = ''

        # row col offsets for directions
        self.row_col_offsets = [
            [-1, 0],
            [ 1, 0],
            [ 0,-1],
            [ 0, 1],
            [-1,-1],
            [-1, 1],
            [ 1,-1],
            [ 1, 1]]

        self.clear_board()
        self.add_words(self.words)

    # -------------------------------------------------------------

    def clear_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col] = '*'

    # -------------------------------------------------------------

    def fill_blanks(self):
        list_upper = list(map(chr, range(65, 91)))
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == '*':
                    chindex = random.randrange(26)
                    self.board[row][col] = list_upper[chindex]

    # -------------------------------------------------------------

    # check if a word fits in the given position and direction
    def word_fits(self, word, row, col, direction):
        rr = row
        cc = col

        rinc = self.row_col_offsets[direction][0]
        cinc = self.row_col_offsets[direction][1]

        for ch in word:
            if rr < 0 or rr >= self.rows:
                return False
            if cc < 0 or cc >= self.cols:
                return False
            c = self.board[rr][cc];
            if ch != c and c != '*':
                return False

            rr += rinc
            cc += cinc

        return True

    # -------------------------------------------------------------

    # place a word in puzzle
    # must first call wordfits
    def place_word(self, word, row, col, direction):
        rinc = self.row_col_offsets[direction][0]
        cinc = self.row_col_offsets[direction][1]
        for ch in word:
            self.board[row][col] = ch
            row += rinc
            col += cinc

    # -------------------------------------------------------------

    # add one word to the board in a random location and direction
    def add_word(self, word):

        random.shuffle(self.row_array)
        random.shuffle(self.col_array)
        random.shuffle(self.dir_array)

        for row in self.row_array:
            for col in self.col_array:
                for d in self.dir_array:
                    if self.word_fits(word, row, col, d) == True:
                        self.place_word(word, row, col, d)
                        return True

        self.error = True
        self.failed_word = word
        return False

    # -------------------------------------------------------------

    # add the words to the board
    # return True if success
    def add_words(self, words):

        # words tend to fit easier if long words are added first
        srt_words = np.array(sorted(words, key=len, reverse=True))

        for word in srt_words:
            word_added = self.add_word(word)

            if word_added == False:
                return False
        return True

    # -------------------------------------------------------------

    # print the board
    def print_board(self, margin):
        for row in range(self.rows):
            for i in range(margin):
                print('', end=' ');
            for col in range(self.cols):
                print(self.board[row][col], end= ' ')
            print()

    # -------------------------------------------------------------

    def print_words(self):
        # get the length of the longest word to make sure all words fit
        srt_words = np.array(sorted(self.words, key=len, reverse=True))
        sz = len(srt_words[0]);

        col = 0
        for word in self.words:
            l = sz + 3 - len(word)
            print(word, end="")
            for i in range(l):
                print(' ', end='')
            if col == 3:
                print()
                col = 0
                continue
            col += 1

    # -------------------------------------------------------------
def main():

    # create parser
    descStr = "This program creates a wordsearch."
    parser = argparse.ArgumentParser(prog='wordsearch', description=descStr)
    # add expected arguments
    parser.add_argument('-cols', dest='cols', type=int, required=True)
    parser.add_argument('-rows', dest='rows', type=int, required=True)
    parser.add_argument('-tries', dest='tries', type=int, default=1, required=False)
    parser.add_argument('-margin', dest='margin', type=int, default=12, required=False)
    parser.add_argument('-words', dest="words", nargs='+', type=str, required=True)

    # parse args
    args = parser.parse_args()

    # try up to 20 times to make the word search
    for tries in range(args.tries):

        # create the wordsearch
        ws = wordsearch(args.rows, args.cols, args.words)

        # check for an error
        if not ws.error:
            ws.fill_blanks()
            print()
            ws.print_board(args.margin)
            print()
            print()
            ws.print_words()
            return

        # get the word that failed
        word = ws.failed_word

    print("Unable to add word", word)

    # -------------------------------------------------------------

# call main
if __name__ == '__main__':
  main()

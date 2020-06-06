NUM_SIDES = 3

import pandas
import random
import numpy as np
from tabulate import tabulate

class Tile():
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return "{}, {}".format(self.row, self.col)

    def __eq__(self, other):
        try:
            return self.row == other.row and self.col == other.col
        except AttributeError: # compare Tile to a Nan object
            return False


class Board():
    def __init__(self, num_sides):

        df = pandas.DataFrame(index=range(num_sides),columns=range(num_sides))
        list_of_tiles_to_shuffle = []

        for row in range(num_sides):
            for col in range(num_sides):
                current_tile = Tile(row, col)
                df.iloc[row, col] = current_tile
                list_of_tiles_to_shuffle.append(current_tile)

        df.iloc[2, 2] = np.nan

        self.correct_board = df
        print("Here's what it should look like: ")
        print(self.correct_board)

        # self.current_board = df

        df_current = pandas.DataFrame(index=range(num_sides),columns=range(num_sides))

        list_of_tiles_to_shuffle = list_of_tiles_to_shuffle[:-1]
        random.shuffle(list_of_tiles_to_shuffle)

        for row_index in range(num_sides):
            row = pandas.Series(list_of_tiles_to_shuffle[0:num_sides])
            list_of_tiles_to_shuffle = list_of_tiles_to_shuffle[num_sides:]
            df_current[row_index] = row

        self.current_board = df_current

        self.tiles_to_move = [] # list of dictionaries where key = tile, value = location

    def check_if_done(self):
        for row in range(NUM_SIDES):
            for col in range(NUM_SIDES):
                t1 = self.correct_board.iloc[row, col]
                t2 = self.current_board.iloc[row, col]

                if pandas.isnull(t1) and pandas.isnull(t2):
                    continue
                elif t1 != t2:
                    return False
        return True

    def get_nan_location(self):
        result = {}
        for row in range(NUM_SIDES):
            for col in range(NUM_SIDES):
                if pandas.isnull(self.current_board.iloc[row, col]):
                    result['row'] = row
                    result['col'] = col
                    return result

    def get_neighbors_to_nan_tile(self):
        nan_dict = self.get_nan_location()
        row = nan_dict['row']
        col = nan_dict['col']

        possible_tiles = [
            [row, col - 1],
            [row, col + 1],
            [row - 1, col],
            [row +1, col]
        ]

        count = 0
        for t in possible_tiles:
            try:
                current_row = t[0]
                current_col = t[1]
                if current_row < 0 or current_col < 0:
                    continue
                possible_tile = self.current_board.iloc[current_row, current_col]
                self.tiles_to_move.append([current_row, current_col])

                print("Tile Num {}: {}".format(count, possible_tile))
                count +=1

            except IndexError:
                pass # if nan is on the edge, there will be fewer than 4 tiles

    def move_piece(self, piece_to_move):
        source_location = self.tiles_to_move[int(piece_to_move)]
        source_row = source_location[0]
        source_col = source_location[1]

        nan_dict = self.get_nan_location()
        nan_row = nan_dict['row']
        nan_col = nan_dict['col']

        self.current_board.iloc[nan_row, nan_col] = self.current_board.iloc[source_row, source_col]
        self.current_board.iloc[source_row, source_col] = np.nan
        self.tiles_to_move = []

    def __repr__(self):
        return tabulate(self.current_board, headers=self.current_board.columns, tablefmt="grid")

def play_game():
    df = Board(NUM_SIDES)

    while not df.check_if_done():
        print("--------------------")
        print(df)

        df.get_neighbors_to_nan_tile()
        i = input("Choose tile to move: ")
        df.move_piece(i)

    print("finished! :)")

play_game()

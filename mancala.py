# python -W ignore mancala.py to ignore warnings

import pandas as pd
from itertools import cycle, islice
from texttable import Texttable

def display(board):
    temp = board.copy()
    temp = temp.replace(to_replace=[0, -1], value=["", ""])

    t = Texttable()
    t.add_rows([["P0", '1', '2', '3', '4', '5', '6', "P1"], temp.loc[0, :], temp.loc[1, :]])
    print(t.draw())

def get_move_indices():
    indices = []

    row = 0
    for col in range(6, -1, -1):
        current = [row, col]
        indices.append(current)

    row = 1
    for col in range(1, 8):
        current = [row, col]
        indices.append(current)

    return indices

INDICES = get_move_indices()

def make_starting_board():

    board = pd.DataFrame(data=4, index=range(2),columns=range(8), dtype=int)
    # board[row][col]
    board[0][0] = 0
    board[7][1] = 0
    board[0][1] = -1
    board[7][0] = -1
    return board

board = make_starting_board()
display(board)

def check_if_done(board):
    temp = board.copy()
    temp = temp.replace(to_replace=[0, -1], value=[None, None])

    # board[row][col]
    if any(temp.iloc[0, 1:6]):
        return False
    if any(temp.iloc[1, 1:6]):
        return False
    return True

def get_winner(board):
    results = {0: board[0][0], 1: board[7][1]}

    winning_score = max(results.values())
    for key, value in results.items():
        if value == winning_score:
            winner = key

    print("Player {} won with a score of {}!".format(winner, winning_score))

def get_move(board, player):

    current_cols = board.iloc[player]
    possible_cols = [ind for ind, col_val in enumerate(current_cols) if int(col_val) > 0 and int(ind) > 0 and int(ind) < 7]

    if len(possible_cols) == 0:
        return None

    inp = 0
    while inp not in possible_cols:
        try:
            inp = int(input("Player {}, select a col out of {}: ".format(player, possible_cols)))

            if inp not in possible_cols:
                print("Invalid column value entered, try again")
        except ValueError:
            print("Invalid integer entered, try again.")

    return inp

def make_move(board, player, col_to_move):
    num_pieces = board.iloc[player, col_to_move]

    # adjust indices based on player: skip home base of other player + store home_base for use later
    if player == 0:
        elt_to_remove = [1, 7]
        home_base = [0, 0]
    elif player == 1:
        elt_to_remove = [0, 0]
        home_base = [1, 7]

    this_players_indices = INDICES.copy()
    this_players_indices.remove(elt_to_remove)

    # find starting_location
    starting_location = this_players_indices.index([player, col_to_move])

    # get board indices that will be impacted
    positions = this_players_indices[starting_location+1:starting_location+num_pieces+1]
    if len(positions) != num_pieces:
        remaining = num_pieces - len(positions)
        positions = positions + this_players_indices[:remaining]

    last_piece_location = positions[-1]

    # clear the position selected
    board.iloc[player, col_to_move] = 0

    # distribute the pieces
    for p in positions:
        board.iloc[p[0],p[1]] += 1

        if p == last_piece_location:
            if p == home_base:
                print("it's the player's home base, you should get to go again! (doesn't work yet)")
                    # TODO
            else:
                existing_number_of_pieces = board.iloc[p[0],p[1]]
                # detect if it becoming 1 instead of if it's zero since board +=1 loop happens before this
                if existing_number_of_pieces == 1:
                    pieces_acquired = board.iloc[int(not bool(last_piece_location[0])), last_piece_location[1]] + 1
                    board.iloc[last_piece_location[0], last_piece_location[1]] = 0
                    board.iloc[int(not bool(last_piece_location[0])), last_piece_location[1]] = 0
                    board.iloc[home_base[0], home_base[1]] += pieces_acquired

    return board

turns = [0, 1]
while not check_if_done(board):
    for player in turns:
        # TODO prevent extra turn at the end like farkle
        col_to_move = get_move(board, player)
        if not col_to_move:
            break
        board = make_move(board, player, col_to_move)
        display(board)

get_winner(board)

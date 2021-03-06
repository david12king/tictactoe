import math
import random

board = ['', 1, 2, 3, 4, 5, 6, 7, 8, 9]
WIN_COMBINATIONS = [
    # Horizontal
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 9),
    # Vertical
    (1, 4, 7),
    (2, 5, 8),
    (3, 6, 9),
    # Diagonals
    (1, 5, 9),
    (3, 5, 7),
]


def get_score(letter, player, depth):
    if player == 'X':
        scores = {'X': 10 - depth, 'O': -10 + depth, 'Tie': 0}
    else:
        scores = {'X': -10 + depth, 'O': 10 - depth, 'Tie': 0}
    return scores[letter]


def instructions():
    print('this is the tic-tac-toe board')
    print(board[1], board[2], board[3])
    print(board[4], board[5], board[6])
    print(board[7], board[8], board[9])
    print('each position has a number')
    clear_board()
    # testing positions
    # board[1] = 'O'
    # board[2] = 'O'
    # board[3] = 'X'
    # board[4] = 'X'
    # board[6] = 'O'
    # board[9] = 'X'


def print_board():
    print(board[1], board[2], board[3])
    print(board[4], board[5], board[6])
    print(board[7], board[8], board[9])
    print('/////////////////')


def get_next_move():
    empty_spaces = get_empty_spaces()
    while True:
        try:
            next_move = int(input('what is your move? (a number from 1 to 9)\n'))
            if 0 < next_move <= 9:
                if next_move in empty_spaces:
                    return next_move
                else:
                    continue
            else:
                continue
        except:
            print('That is not a valid number')
            continue


def clear_board():
    for i in range(1, 10):
        board[i] = '_'

def get_empty_spaces():
    empty_spaces = []
    for i in range(1, len(board)):
        if board[i] == '_':
            empty_spaces.append(i)
    return empty_spaces


def minimax(board, depth, is_maximazing, what_letter, alpha, beta):
    result = is_game_over()
    if result is not None:
        score = get_score(result, what_letter, depth)
        return score

    if is_maximazing:
        score = -math.inf
        empty_spaces = get_empty_spaces()
        for i in empty_spaces:
            board[i] = what_letter
            best_score = max(best_score, minimax(board, depth + 1, False, what_letter, alpha, beta))
            board[i] = '_'
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score
    else:
        score = math.inf
        if what_letter == 'X':
            opposite_letter = 'O'
        else:
            opposite_letter = 'X'
        empty_spaces = get_empty_spaces()
        for i in empty_spaces:
            board[i] = opposite_letter
            best_score = min(best_score, minimax(board, depth + 1, True, what_letter, alpha, beta))
            board[i] = '_'
            beta = min(beta, best_score)
        return best_score


def get_comp_move(what_turn, what_letter):
    alpha = -math.inf
    beta = math.inf
    best_score = -math.inf
    move = 0
    alpha = 0
    beta = 0
    empty_spaces = get_empty_spaces()
    for i in empty_spaces:
        board[i] = what_letter
        score = minimax(board, 0, False, what_letter, alpha, beta)
        board[i] = '_'
        if alpha >= beta:
            move = i
    return move


def is_game_over():
    winner = None
    for a, b, c in WIN_COMBINATIONS:
        if board[a] == board[b] == board[c] == 'X' or board[a] == board[b] == board[c] == 'O':
            winner = board[a]
    if winner is None and (len(get_empty_spaces()) == 0):
        return 'Tie'
    else:
        return winner


def add_move_to_board(i, letter):
    board[i] = letter


def get_player_letters(first_p):
    human_letter = input('Do you want to be X or O \n').upper()
    if human_letter == 'X':
        comp_letter = 'O'
    else:
        comp_letter = 'X'
    print(f'you are {human_letter} and the computer is {comp_letter}')

    if first_p == 'human':
        return human_letter, comp_letter
    else:
        return comp_letter, human_letter


def get_player_turns():
    turn = random.randint(1, 2)
    if turn == 1:
        print(f'you will be {turn}st')
    else:
        print(f'you will be {turn}nd')
    if turn == 1:
        return 'human', 'comp'
    else:
        return 'comp', 'human'


def main():
    game_over = False
    instructions()
    move_count = 1
    first_p, second_p = get_player_turns()
    first_p_letter, second_p_letter = get_player_letters(first_p)
    while not game_over:
        winner = is_game_over()
        if winner == 'Tie':
            print(f'The game is a {winner}')
            game_over = True
        elif winner:
            print(f'The winner is {winner}')
            game_over = True
        else:
            if first_p == 'human' and move_count % 2 != 0:
                add_move_to_board(get_next_move(), first_p_letter)
                print_board()
                move_count += 1
            elif first_p == 'human' and move_count % 2 == 0:
                add_move_to_board(get_comp_move(second_p, second_p_letter), second_p_letter)
                print_board()
                move_count += 1
            elif first_p == 'comp' and move_count % 2 != 0:
                add_move_to_board(get_comp_move(first_p, first_p_letter), first_p_letter)
                print_board()
                move_count += 1
            else:
                add_move_to_board(get_next_move(), second_p_letter)
                print_board()
                move_count += 1


if __name__ == '__main__':
    main()

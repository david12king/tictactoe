import math
import random
import pygame

pygame.init()
pygame.font.init()
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

global FIRST_P_LETTER
global SECOND_P_LETTER
global FIRST_P
global SECOND_P
global PLAYING
global INTRO
global board

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
clock.tick(60)

all_sprites = pygame.sprite.Group()

board = ['', '_', '_', '_', '_', '_', '_', '_', '_', '_']
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


def get_next_move(sprites):
    empty_spaces = get_empty_spaces()
    while True:
        try:
            pos = pygame.mouse.get_pos()
            for i in sprites:
                if i.rect.collidepoint(pos):
                    next_move = i.value
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
        best_score = -math.inf
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
        if what_letter == 'X':
            opposite_letter = 'O'
        else:
            opposite_letter = 'X'
        best_score = math.inf
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
    empty_spaces = get_empty_spaces()
    for i in empty_spaces:
        board[i] = what_letter
        score = minimax(board, 0, False, what_letter, alpha, beta)
        board[i] = '_'
        if score > best_score:
            best_score = score
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


def intro():
    global FIRST_P
    global SECOND_P
    global FIRST_P_LETTER
    global SECOND_P_LETTER

    button_font = pygame.font.SysFont('comicsans', 30)
    button_text = button_font.render('Play', True, (0, 0, 0))

    font = pygame.font.SysFont('comicsans', 50)
    text = font.render('Do you want to be X or O?', True, (0, 0, 0))

    letter_font = pygame.font.SysFont('comicsansms', 100)
    letter_x = letter_font.render('X', True, (0, 0, 0))
    letter_o = letter_font.render('O', True, (0, 0, 0))

    button = Button(500, 450, 100, 50, (103, 174, 171), (137, 235, 232), highlight_border_color=(15, 213, 255))

    FIRST_P, SECOND_P = get_player_turns()

    intro_running = True

    while intro_running:
        global FIRST_P_LETTER
        global SECOND_P_LETTER
        global PLAYING

        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                intro_running = False

            if 500 < pos[0] < 600 and 450 < pos[1] < 500:
                button.highlighted = True
            else:
                button.highlighted = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # X is selected
                if 300 < pos[0] < 300 + letter_x.get_width() and 250 < pos[1] < 250 + letter_x.get_height():
                    letter_x = letter_font.render('X', True, (255, 255, 255))
                    letter_o = letter_font.render('O', True, (77, 129, 174))
                    if FIRST_P == 'comp':
                        FIRST_P_LETTER = 'O'
                        SECOND_P_LETTER = 'X'
                    else:
                        FIRST_P_LETTER = 'X'
                        SECOND_P_LETTER = 'O'
                # O is selected
                if 670 < pos[0] < 670 + letter_o.get_width() and 250 < pos[1] < 670 + letter_o.get_height():
                    letter_o = letter_font.render('O', True, (255, 255, 255))
                    letter_x = letter_font.render('X', True, (77, 129, 174))
                    if FIRST_P == 'comp':
                        FIRST_P_LETTER = 'X'
                        SECOND_P_LETTER = 'O'
                    else:
                        FIRST_P_LETTER = 'O'
                        SECOND_P_LETTER = 'X'
                try:
                    if button.highlighted and FIRST_P_LETTER is not None:
                        intro_running = False
                        PLAYING = True
                except:
                    pass

        screen.fill((31, 112, 174))

        # Question text
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100))

        # Letter X and O
        screen.blit(letter_x, (300, 250))
        screen.blit(letter_o, (670, 250))

        button.update()
        button.draw()
        screen.blit(button_text, (int(550 - button_text.get_width() / 2), int(475 - button_text.get_height() / 2)))

        pygame.display.update()


class Button:
    def __init__(self, x, y, width, height, bg_color, highlight_color, border_color=(0, 0, 0),
                 highlight_border_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.highlight_color = highlight_color
        self.border_color = border_color
        self.highlight_border_color = highlight_border_color
        self.highlighted = False

    def update(self):
        pass

    def draw(self):
        if self.highlighted:
            pygame.draw.rect(screen, self.highlight_color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, self.highlight_border_color, (self.x, self.y, self.width, self.height), 2)
        else:
            pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, self.border_color, (self.x, self.y, self.width, self.height), 2)


class Cell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((150, 150))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.value = 0


class CreateText:
    def __init__(self, x, y, text, color, size, font_name):
        self.text = text
        self.color = color
        self.size = size
        self.x = x
        self.y = y
        self.font_name = font_name
        self.button_font = pygame.font.SysFont(font_name, 30)
        self.button_text = self.button_font.render(self.text, True, self.color)

    def update(self):
        pass

    def draw(self):
        screen.blit(self.button_text, (self.x, self.y))


class ScreenBoard:
    def __init__(self):
        self.cell = None
        self.text = None

    def create_screen_board(self):
        val = 0
        for row in range(3):
            for column in range(3):
                self.cell = Cell()
                val += 1
                self.cell.value = val

                x = 25 + 175 * row
                y = 25 + 175 * column
                self.cell.rect.topleft = (y, x)
                all_sprites.add(self.cell)
        for i in all_sprites:
            print(i.value)
            print(i.rect.center)
            print(i.rect.x)
            print(i.rect.y)

    def draw_board(self):
        sprite_list = all_sprites.sprites()
        for i in range(1, 10):
            if board[i] == 'X':
                self.text = CreateText(sprite_list[i-1].rect.x, sprite_list[i-1].rect.y, board[i], BLACK, 50,
                                       'comicsansms')
                self.text.draw()
            elif board[i] == 'O':
                self.text = CreateText(sprite_list[i-1].rect.x, sprite_list[i-1].rect.y, board[i], BLACK, 50, 'comicsansms')
                self.text.draw()


def game():
    global PLAYING
    global board
    move_count = 1
    s_board = ScreenBoard()
    s_board.create_screen_board()
    s_board.draw_board()
    sprite_list = all_sprites.sprites()
    while PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PLAYING = False
        winner = is_game_over()
        if winner == 'Tie':
            print(f'The game is a {winner}')
            PLAYING = False
        elif winner:
            print(f'The winner is {winner}')
            PLAYING = False
        else:
            if FIRST_P == 'human' and move_count % 2 != 0:
                add_move_to_board(get_next_move(sprite_list), FIRST_P_LETTER)
                s_board.draw_board()
                move_count += 1
            elif FIRST_P == 'human' and move_count % 2 == 0:
                add_move_to_board(get_comp_move(SECOND_P, FIRST_P_LETTER), FIRST_P_LETTER)
                s_board.draw_board()
                move_count += 1
            elif FIRST_P == 'comp' and move_count % 2 != 0:
                add_move_to_board(get_comp_move(FIRST_P, FIRST_P_LETTER), FIRST_P_LETTER)
                s_board.draw_board()
                move_count += 1
            else:
                add_move_to_board(get_next_move(sprite_list), FIRST_P_LETTER)
                s_board.draw_board()
                move_count += 1
        # Update
        all_sprites.update()

        # Draw

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.update()


def main():
    intro()
    if PLAYING:
        game()
    
    
if __name__ == '__main__':
    main()

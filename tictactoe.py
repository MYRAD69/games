import pygame as pg
import numpy as np
pg.init()

WIDTH, HEIGHT = 600, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Tic Tac Toe")
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
board = np.zeros((3, 3))
winner = ""
class Tic:
    def __init__(self, x1, y1):
        self.x1 = x1
        self.y1 = y1
    def draw(self):
        x2 = self.x1 + 160
        y2 = self.y1 + 160
        pg.draw.line(WIN, red, (self.x1, self.y1), (x2, y2), 10)
        pg.draw.line(WIN, red, (self.x1, y2), (x2, self.y1), 10)
class Tac:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        pg.draw.circle(WIN, blue, (self.x, self.y), 85, 10)
def construct_board():
    WIN.fill(white)
    pg.draw.line(WIN, black, (0, 200), (600, 200), 10)
    pg.draw.line(WIN, black, (0, 400), (600, 400), 10)
    pg.draw.line(WIN, black, (200, 0), (200, 600), 10)
    pg.draw.line(WIN, black, (400, 0), (400, 600), 10)
def make_move(part, turn):
    if turn == 1:
        x = part[0] * 200 + 20
        y = part[1] * 200 + 20
        res = Tic(x, y)
    else:
        x = part[0] * 200 + 100
        y = part[1] * 200 + 100
        res = Tac(x, y)
    board[part[1]][part[0]] = turn
    res.draw()
def check_win(player):
    winCombinations = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [1, 5, 9],
    [3, 5, 7],
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9]
    ]
    k = np.array(winCombinations)
    x = (k - 1) % 3
    y = (k - 1) // 3
    for i in range(len(k)):
        if board[x[i][0]][y[i][0]] == board[x[i][1]][y[i][1]] == board[x[i][2]][y[i][2]] == player:
            return True
    return False
def check_draw():
    empty = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                empty = False
    return empty
def check_space(x, y):
    if board[x][y] == 0:
        return True
    else:
        return False
def convert_to_ind(n):
    x = (n - 1) % 3
    y = (n - 1) // 3
    return (x, y)
def main_menu():
    pg.draw.rect(WIN, blue, pg.Rect(0, 0, 300, 600))
    pg.draw.rect(WIN, red, pg.Rect(300, 0, 300, 600))
    font = pg.font.Font('freesansbold.ttf', 32)
    text1 = font.render('1 Player', True, white, blue)
    text2 = font.render('2 Players', True, white, red)
    textRect1 = text1.get_rect()
    textRect2 = text2.get_rect()
    textRect1.center = (150, 300)
    textRect2.center = (450, 300)
    WIN.blit(text1, textRect1)
    WIN.blit(text2, textRect2)
    
def comp_play(cboard):
    bestScore = -800
    bestMove = 0
    for i in range(len(cboard)):
        if cboard[i] == 0:
            ind = convert_to_ind(i)
            board[ind[0]][ind[1]] = -1
            cboard[i] = -1
            score = minimax(cboard, 0, False)
            board[ind[0]][ind[1]] = 0
            cboard[i] = 0
            if (score > bestScore):
                bestScore = score
                bestMove = i
    make_move(convert_to_ind(bestMove), -1)

def minimax(cboard, depth, isMaximizing):
    
    if check_win(1):
        return -1
    elif check_win(-1):
        return 1
    elif check_draw():
        return 0
    if isMaximizing:
        bestScore = -800
        for i in range(len(cboard)):
            if cboard[i] == 0:
                ind = convert_to_ind(i)
                board[ind[0]][ind[1]] = -1
                cboard[i] = -1
                score = minimax(cboard, depth - 1, False)
                board[ind[0]][ind[1]] = 0
                cboard[i] = 0
                if score > bestScore:
                    bestScore = score
        return bestScore
    else:
        bestScore = 800
        for i in range(len(cboard)):
            if cboard[i] == 0:
                ind = convert_to_ind(i)
                board[ind[0]][ind[1]] = 1
                cboard[i] = 1
                score = minimax(cboard, depth - 1, True)
                cboard[i] = 0
                board[ind[0]][ind[1]] = 0
                if score < bestScore:
                    bestScore = score
        return bestScore
def main():
    run = True
    menu_run = True
    game_mode = 0
    clock = pg.time.Clock()
    while run and menu_run:
        main_menu()
        clock.tick(60)
        for eve in pg.event.get():
            if eve.type == pg.QUIT:
                run = False
                menu_run = False
            if eve.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if pos[0] > 300:
                    game_mode = 2
                    menu_run = False
                else:
                    game_mode = 1
                    menu_run = False
        pg.display.update()
    construct_board()
    turn = 1
    while run:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                position = pg.mouse.get_pos()
                index = (position[0] // 200, position[1] // 200)
                if board[index[1]][index[0]] != 0:
                    continue
                make_move(index, turn)
                if check_win(turn):
                    if turn == 1:
                        winner = "Cross"
                    else:
                        winner = "Nought"
                    print(f"{winner} wins!")
                    run = False
                if check_draw():
                    print("Draw!")
                    run = False
                if game_mode == 2:
                    turn = -turn
                else:
                    comp_board = np.reshape(board, 9)
                    print(comp_board)
                    comp_play(comp_board)
                    turn = -turn
                    if check_win(turn):
                        if turn == 1:
                            winner = "Cross"
                        else:
                            winner = "Nought"
                        print(f"{winner} wins!")
                        run = False
                    if check_draw():
                        print("Draw!")
                        run = False
                    turn = -turn
        pg.display.update()
    pg.quit()
main()
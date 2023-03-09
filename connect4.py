import pygame
import numpy as np
pygame.init()
WIDTH, HEIGHT = 860, 740
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")
board = np.zeros((6, 7), dtype=tuple)
play_board = np.zeros((6, 7))
BLUE = (0, 128, 234)
RED = (251, 1, 0)
YELLOW = (232, 225, 1)
class Disk:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), 50)

def constructBoard():
    for i in range(0, 6):
        for j in range(0, 7):
            x = 70 + 120 * i
            y = 70 + 120 * j
            board[i][j] = (y, x)
    for i in range(len(board)):
        for j in range(len(board[i])):
            d = Disk(board[i][j][0], board[i][j][1], (255, 255, 255))
            d.draw()

# well somebody brootforced it lmao
def checkOWin(game, turn):

    boardHeight = len(game[0])
    boardWidth = len(game)
    tile = turn
    for y in range(boardHeight):
        for x in range(boardWidth - 3):
            if game[x][y] == tile and game[x+1][y] == tile and game[x+2][y] == tile and game[x+3][y] == tile:
                return True

    for x in range(boardWidth):
        for y in range(boardHeight - 3):
            if game[x][y] == tile and game[x][y+1] == tile and game[x][y+2] == tile and game[x][y+3] == tile:
                return True

    for x in range(boardWidth - 3):
        for y in range(3, boardHeight):
            if game[x][y] == tile and game[x+1][y-1] == tile and game[x+2][y-2] == tile and game[x+3][y-3] == tile:
                return True

    for x in range(boardWidth - 3):
        for y in range(boardHeight - 3):
            if game[x][y] == tile and game[x+1][y+1] == tile and game[x+2][y+2] == tile and game[x+3][y+3] == tile:
                return True

    return False

def make_move(circle, turn):
    color = RED
    if turn == -1:
        color = YELLOW
    for i in range(5, -1, -1):
        if play_board[i][circle] == 0:
            play_board[i][circle] = turn
            pygame.draw.circle(WIN, color, board[i][circle], 50)
            break

def main():
    clock = pygame.time.Clock()
    run = True
    turn = 1
    WIN.fill(BLUE)
    constructBoard()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()[0]
                index = round((position - 70) / 120)
                if (play_board[0][index] != 0):
                    continue
                make_move(index, turn)
                turn = -turn
                if checkOWin(play_board, -turn):
                    winner = "no one"
                    if turn == -1:
                        winner = "Red"
                    else:
                        winner = "Yellow"
                    print(f"{winner} wins!")
                    run = False
                
        pygame.display.update()
    pygame.quit()
main()
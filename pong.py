from random import random
import pygame as pg
WIDTH, HEIGHT = 800, 800
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pong Game")
WHITE = (255, 255, 255)
BLUE = (2,255,255)
BLACK = (0, 0, 0)
X_PLAYER = 794
X_BOT = 3
class Line:
    def __init__(self, x):
        self.x = x
    def draw(self, win, y1):
        x1 = self.x
        x2 = x1
        y2 = y1 + 100
        pg.draw.line(win, WHITE, (x1, y1), (x2, y2), 6)
class Ball:
    def __init__(self, radius):
        self.radius = radius
    def draw(self, win, x, y):
        pg.draw.circle(win, BLUE, (x, y), self.radius)
def setupBoard(l1, y1, l2, y2, b, x3, y3):
    l1.draw(WIN, y1)
    l2.draw(WIN, y2)
    pg.draw.line(WIN, WHITE, (399, 0), (399, 800), 5)
    b.draw(WIN, x3, y3)
def updatePlayerPos(y):
    pos = pg.mouse.get_pos()[1]
    y = pos - 40
    return y
def updateBallVelY(y, vy):
    if y - 12 <= 0 or y + 12 >= 800:
        vy *= -1
    return vy
def updateBotPos(y, by):
    dis = by - y
    down = True
    if dis < 0:
        dis *= -1
        down = False
    velocity = res = 0
    if dis <= 5:
        velocity = 1
    elif dis <= 10:
        velocity = 3
    elif dis <= 20:
        velocity = 6
    elif dis <= 50:
        velocity = 10
    elif dis <= 100:
        velocity = 20
    else:
        velocity = 30
    if down:
        res = y + velocity
    else:
        res = y - velocity
    return res
def main():
    clock = pg.time.Clock()
    run = True
    begin = False
    player = Line(X_PLAYER)
    bot = Line(X_BOT)
    ball = Ball(12)
    vel_x = 3
    vel_y = 0
    player_y = bot_y = 350
    ball_x = ball_y = 400
    setupBoard(player, player_y, bot, bot_y, ball, ball_x, ball_y)
    while run:
        clock.tick(60)
        WIN.fill(BLACK)
        winner = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and not begin:
                begin= True
                dir = random()
                dir = round(dir)
                vel_y = 1 + random() * 5
                if dir == 1:
                    vel_y *= -1
        if begin:
            player_y = updatePlayerPos(player_y)
            vel_y = updateBallVelY(ball_y, vel_y)
            bot_y = updateBotPos(bot_y, ball_y - 50)
            if ball_x + 12 <= 0:
                if ball_y >= bot_y and ball_y <= bot_y + 100:
                    vel_x *= -1.1
                    if not (ball_y >= bot_y + 40 and ball_y <= bot_y + 60):
                        vel_y *= 1.1
                else:
                    winner = 1
                    run = False
            elif ball_x + 12 >= 800:
                if ball_y >= player_y and ball_y <= player_y + 100:
                    vel_x *= -1.1
                    if not (ball_y >= player_y + 40 and ball_y <= player_y + 60):
                        vel_y *= 1.1
                else:
                    winner = -1
                    run = False
            ball_x += vel_x
            ball_y += vel_y
        setupBoard(player, player_y, bot, bot_y, ball, ball_x, ball_y)
        if winner == 1:
            print("Player has won!")
        elif winner == -1:
            print("Bot has won!")
        pg.display.update()
    pg.quit()
main()
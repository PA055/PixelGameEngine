import pygame, sys, random, math
from pygame.locals import *
from PixelGameEngine import PixelEngine 

xpos = 0

Game = PixelEngine('Test', 480, 780, 12, 12, scaleing_factor=0.5, FPS=60)
Game.setBackground((0, 255, 255))


def Start(game):
    game.drawFunction(lambda x: math.sqrt(100 - (x - 20)*(x - 20)) + 20, (0, 0, 0), minX = 10, maxX=30)
    '''
    game.fillRectXY(0, 0, 65, 5, (0, 0, 0))
    game.fillRectXY(0, 5, 65, 5, (255, 255, 255))

    for i in range(0, 256, 20):
        game.fillRectXY(1 + 5 * (i // 20), 1, 3, 3, (255, 255, 255, i))
        game.fillRectXY(1 + 5 * (i // 20), 6, 3, 3, (0, 0, 0, i))

    game.fillRectXY(00, 15, 22, 25, (255, 0, 0))
    game.fillRectXY(22, 15, 22, 25, (0, 255, 0))
    game.fillRectXY(44, 15, 22, 25, (0, 0, 255))

    game.drawLineXY(0, 15, 65, 15, (0, 0, 0))
    '''
    #game.drawBezierCurve((0, 0, 0), (2, 3), (1, 31), (61, -30), (32, 37), (60, 36), (5, 5))
    #game.fillPolygon((255, 0, 0), (22, 10), (40, 15), (52, 11), (36, 20), (34, 20), (34, 22), (30, 38), border_color=(0, 0, 0), border_width=1)
    pass

def Update(game):
    keysDown = game.getKeyPressed()
    if keysDown[K_p]:
        x, y = pygame.mouse.get_pos()
        print((x // game.PIXEL_WIDTH, y // game.PIXEL_HEIGHT))
        print(game.FPS)
    return True

print(Game.WPW, Game.WPH)
Game.Start(Start, Update)


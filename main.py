import pygame, sys, random, math
from pygame.locals import *
from PixelGameEngine import PixelEngine 

xpos = 0

Game = PixelEngine('Test', 480, 780, 12, 12, scaleing_factor=1, FPS=60)
Game.setBackground((0, 255, 255))


def Start(game):
    game.drawBezierCurve((0, 0, 0), (5, 8), (3, 19), (20, 12))
    #game.fillPolygon((255, 0, 0), (22, 10), (40, 15), (52, 11), (36, 20), (34, 20), (34, 22), (30, 38), border_color=(0, 0, 0), border_width=1)

def Update(game):
    keysDown = game.getKeyPressed()
    if keysDown[K_p]:
        x, y = pygame.mouse.get_pos()
        print((x // game.PIXEL_WIDTH, y // game.PIXEL_HEIGHT))
        print(game.FPS)
    

print(Game.WPW, Game.WPH)
Game.Start(Start, Update)


import pygame, sys, random, threading, math
from collections import Counter
from typing import Callable, Iterable
from pygame.locals import *


class PixelEngine:
    def __init__(self, title, screen_height:int, screen_width:int, pixel_height:int, pixel_width:int, scaleing_factor:float=1, FPS=None):
        pygame.init()
        self.WINDOW_WIDTH = round(screen_width * scaleing_factor)
        self.WINDOW_HEIGHT = round(screen_height * scaleing_factor)
        
        self.PIXEL_HEIGHT = round(pixel_height * scaleing_factor)
        self.PIXEL_WIDTH = round(pixel_width * scaleing_factor)
        
        self.WINDOW_PIXEL_HEIGHT = math.ceil(self.WINDOW_HEIGHT / self.PIXEL_HEIGHT)
        self.WPH = self.WINDOW_PIXEL_HEIGHT
        self.WINDOW_PIXEL_WIDTH = math.ceil(self.WINDOW_WIDTH / self.PIXEL_WIDTH)
        self.WPW = self.WINDOW_PIXEL_WIDTH
        
        self.WINDOW = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption(title)

        
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.pixels = [[(0, 0, 0) for i in range(self.WINDOW_PIXEL_HEIGHT)] for j in range(self.WINDOW_PIXEL_WIDTH)]

        self.__keydown = False
        
        if FPS is not None:
            self.FPS = FPS
            self.clock = pygame.time.Clock()
        else:
            self.FPS = None

    def drawScreen(self, screen):
        for x in range(self.WINDOW_WIDTH):
            for y in range(self.WINDOW_HEIGHT):
                px = math.floor(x / self.PIXEL_WIDTH)
                py = math.floor(y / self.PIXEL_HEIGHT)
                self.WINDOW.set_at((x, y), screen[px][py])

    def Start(self, start: Callable=lambda x:1, update:Callable=lambda x:1, end:Callable=lambda x:1):
        start(self)
        self.loop(update, end)
        '''
        gl = threading.Thread(target=self.loop, args=(update, end))
        gl.start()
        '''
    
    def loop(self, update, end):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    end(self)
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP:
                    self.__keydown = False
                elif event.type == KEYDOWN:
                    self.__keydown = True

                    
            update(self)

            self.drawScreen(self.pixels)
            pygame.display.update()
            if self.FPS is not None:
                self.clock.tick(self.FPS)

    def isInRange(self, point: Iterable[int]):
        return (point[0] < self.WPW and point[0] >= 0) and (point[1] < self.WPH and point[1] >= 0) 

    def isInRangeXY(self, x: int, y: int):
        return (x < self.WPW and x >= 0) and (y < self.WPH and y >= 0) 
  
    def isKeyDown(self):
        return self.__keydown
    
    def getKeyPressed(self):
        return pygame.key.get_pressed()

    def clearScreen(self):
        for x in range(self.WPW):
            for y in range(self.WPH):
                self.setPixelXY(x, y, self.BACKGROUND_COLOR)

    def setBackground(self, color: Iterable[int]):
        self.BACKGROUND_COLOR = color
        self.clearScreen()

    def setPixel(self, point: Iterable[int], color: Iterable[int]):
        if self.isInRangeXY(point[0], point[1]):
            self.pixels[point[0]][point[1]] = color

    def setPixelXY(self, x: int, y: int, color: Iterable[int]):
        self.setPixel((x, y), color)
    
    def setThickPixelXY(self, xc: int, yc: int, color: Iterable[int], thickness: int=1):
        if thickness == 1:
            self.setPixelXY(xc, yc, color)
            return
        for x in range(xc - (thickness // 2), xc + math.ceil(thickness / 2)):
            for y in range(yc - (thickness // 2), yc + math.ceil(thickness / 2)):
                self.setPixelXY(x, y, color)
                
    def setThickPixel(self, point: Iterable[int], color: Iterable[int], thickness: int=1):
        self.setThickPixelXY(point[0], point[1], color, thickness)
    
    def drawLine(self, start: Iterable[int], end: Iterable[int], color: Iterable[int], thickness: int=1):

        x0 = round(start[0])
        x1 = round(end[0])
        y0 = round(start[1])
        y1 = round(end[1])
        
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)


        if dx == 0:
            m = math.inf
        else:
            m = dy / dx
        
        if ((x1 - x0) < 0 or (y1 -y0) < 0):
            if m < 1 and x0 > x1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                dx = abs(x1 - x0)
                dy = abs(y1 - y0)
            if m > 1 and y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
                dx = abs(x1 - x0)
                dy = abs(y1 - y0)

        if dx == 0:
            for y in range(y0, y1 + 1):
                self.setThickPixelXY(x0, y, color, thickness)
            return

        if dy == 0:
            for x in range(x0, x1 + 1):
                self.setThickPixelXY(x, y0, color, thickness)
            return
            
                
        
        flag = True
        
        self.setThickPixelXY(x0, y0, color, thickness)
        
        step = 1
        if x0 > x1 or y0 > y1:
            step = -1
    
        mm = False   
        if m < 1:
            x0, x1, y0, y1 = y0, y1, x0, x1
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)
            mm = True
            
        p0 = 2 * dx - dy
        x = x0
        y = y0
        
        for i in range(abs(y1 - y0)):
            if flag:
                x_previous = x0
                p_previous = p0
                p = p0
                flag = False
            else:
                x_previous = x
                p_previous = p
                
            if p >= 0:
                x = x + step
    
            p = p_previous + 2 * dx - 2 * dy * (abs(x - x_previous))
            y = y + 1
            
            if mm:
                self.setThickPixelXY(y, x, color, thickness)
            else:
                self.setThickPixelXY(x, y, color, thickness)
            
    def drawLineXY(self, x1: int, y1: int, x2: int, y2: int, color: Iterable[int], thickness: int=1):
        self.drawLine((x1, y1), (x2, y2), color, thickness)

    def drawRect(self, point: Iterable[int], size: Iterable[int], border_color: Iterable[int], border_width: int=1):
        tl = (point[0], point[1])
        tr = (point[0], point[1] + size[1])
        bl = (point[0] + size[0], point[1])
        br = (point[0] + size[0], point[1] + size[1])
        self.drawLine(tl, tr, border_color, border_width)
        self.drawLine(tr, br, border_color, border_width)
        self.drawLine(bl, br, border_color, border_width)
        self.drawLine(tl, bl, border_color, border_width)

    def drawRectXY(self, x: int, y: int, width: int, height: int, border_color: Iterable[int], border_width: int=1):
        self.drawRect((x, y), (width, height), border_color, border_width)

    def fillRect(self, point: Iterable[int], size: Iterable[int], color: Iterable[int], border_color: Iterable[int]=(0, 0, 0), border_width: int=0):
        for x in range(point[0], point[0] + size[0]):
            for y in range(point[1], point[1] + size[1]):
                if self.isInRangeXY(x, y):
                        self.setPixel((x, y), color)
        self.drawRect(point, size, border_color, border_width)

    def fillRectXY(self, x: int, y: int, width: int, height: int, color: Iterable[int], border_color: Iterable[int]=(0, 0, 0), border_width: int=0):
        for x1 in range(x, x + width):
            for y1 in range(y, y + height):
                if self.isInRangeXY(x1, y1):
                        self.setPixel((x1, y1), color)
        self.drawRect((x, y), (width, height), border_color, border_width)
        
    def drawCircle(self, center: Iterable[int], radius: int, color: Iterable[int], thickness: int=1):
        x = radius
        y = 0

        self.setThickPixelXY(center[0] + x, center[1] + y, color, thickness)

        if radius > 0:
            self.setThickPixelXY(center[0] - x, center[1] + y, color, thickness)
            self.setThickPixelXY(center[0] + y, center[1] + x, color, thickness)
            self.setThickPixelXY(center[0] + y, center[1] - x, color, thickness)


        P = 1 - radius
        
        while x > y:
            y += 1
            
            if P <= 0:
                P = P + 2 * y + 1
            else:        
                x -= 1
                P = P + 2 * y - 2 * x + 1

            if x < y:
                break
            
            self.setThickPixelXY(x + center[0], y + center[1], color, thickness)
            self.setThickPixelXY(-x + center[0], y + center[1], color, thickness)
            self.setThickPixelXY(x + center[0], -y + center[1], color, thickness)
            self.setThickPixelXY(-x + center[0], -y + center[1], color, thickness)

            if x != y:
                self.setThickPixelXY(y + center[0], x + center[1], color, thickness)
                self.setThickPixelXY(-y + center[0], x + center[1], color, thickness)
                self.setThickPixelXY(y + center[0], -x + center[1], color, thickness)
                self.setThickPixelXY(-y + center[0], -x + center[1], color, thickness)

    def drawCircleXY(self, x: int, y: int, radius: int, color: Iterable[int], thickness: int=1):
        self.drawCircle((x, y), radius, color, thickness)
    
    def fillCircle(self, center: Iterable[int], radius: int, color: Iterable[int], border_color: Iterable[int], border_width: int = 0):
        for x in range(center[0] - radius, center[0] + radius + 1):
            for y in range(center[1] - radius, center[1] + radius + 1):
                if ((x - center[0]) ** 2 + (y - center[1]) ** 2) < (radius ** 2):
                    if self.isInRangeXY(x, y):
                        self.setPixelXY(x, y, color)
        self.drawCircle(center, radius, border_color, border_width)

    def fillCircleXY(self, x: int, y: int, radius: int, color: Iterable[int], border_color: Iterable[int], border_width: int = 0):
        self.fillCircle((x, y), radius, color, border_color, border_width)
    
    def drawPolygon(self, color: Iterable[int], *corners: Iterable[int], thickness: int=1):
        if len(corners) < 1:
            return
        for i in range(len(corners)):
            self.drawLine(corners[i - 1], corners[i], color, thickness)

    def fillPolygon(self, color, *corners: Iterable[int], border_color: Iterable[int]=(0, 0, 0), border_width: int=0):
        def getLineEdges(start, end):
            x0 = round(start[0])
            x1 = round(end[0])
            y0 = round(start[1])
            y1 = round(end[1])
            
            dx = abs(x1 - x0)
            dy = abs(y1 - y0)

            points = []


            if dx == 0:
                m = math.inf
            else:
                m = dy / dx
            
            if ((x1 - x0) < 0 or (y1 -y0) < 0):
                if m < 1 and x0 > x1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                    dx = abs(x1 - x0)
                    dy = abs(y1 - y0)
                if m > 1 and y0 > y1:
                    x0, y0, x1, y1 = x1, y1, x0, y0
                    dx = abs(x1 - x0)
                    dy = abs(y1 - y0)

            if dx == 0:
                for y in range(y0, y1 + 1):
                    points.append((x0, y))
                points.append((x1, y1))
                return points

            if dy == 0:
                return [(x0, y0), (x1, y1)]
                
            
            flag = True
            
            step = 1
            if x0 > x1 or y0 > y1:
                step = -1
        
            mm = False   
            if m < 1:
                x0, x1, y0, y1 = y0, y1, x0, x1
                dx = abs(x1 - x0)
                dy = abs(y1 - y0)
                mm = True

            
                
            p0 = 2 * dx - dy
            x = x0
            y = y0
            
            for i in range(abs(y1 - y0)):
                if flag:
                    x_previous = x0
                    p_previous = p0
                    p = p0
                    flag = False
                else:
                    x_previous = x
                    p_previous = p
                    
                if p >= 0:
                    x = x + step
        
                p = p_previous + 2 * dx - 2 * dy * (abs(x - x_previous))
                y = y + 1
                
                if mm:
                    if x != x_previous:
                        points.append((y, x))
                else:
                    points.append((x, y))

            return points
        def getPolygonEdges(*points):
            if len(points) < 1:
                return []
            edges = []
            for i in range(len(points)):
                edges.extend(getLineEdges(points[i - 1], points[i]))
            for point in corners:
                edges.append(point)
            return edges

        edges = getPolygonEdges(*corners)
        print(dict(Counter([item for item in list(map(lambda point: point if point[1] == 15 else None, edges)) if item is not None])))
        minx = min(map(lambda x: x[0], corners))
        maxx = max(map(lambda x: x[0], corners))
        miny = min(map(lambda x: x[1], corners))
        maxy = max(map(lambda x: x[1], corners))
        for y in range(miny + 1, maxy):
            inside = False
            for x in range(minx, maxx):
                if (x, y) in edges:
                    if edges.count((x, y)) & 1 == 1:
                        inside = not inside
                
                if inside:
                    self.setPixel((x, y), color)
        
        if border_width > 0:
            self.drawPolygon(border_color, *corners, thickness=border_width)
        else:
            self.drawPolygon(color, *corners, thickness=border_width)
        #for point in edges:
        #    self.setPixel(point, (0, 255, 0))
        #for point in corners:
        #    self.setPixel(point, (0, 0, 255))

    # TODO text, curves, sprite, color class

    
import pygame as pg
import random

class Figure:
    def __init__(self, size):
        self.x, self.y = pg.mouse.get_pos()
        self.size = size
        self.flag = 6

    def draw(self, win, position):
        pass

    def move(self):
        self.x, self.y = pg.mouse.get_pos()

    def change_size(self):
        self.size += self.flag
        
    def check_size(self):
        if self.size > 200 or self.size < 50:
            self.flag *= -1

class Circle(Figure):

    def draw(self, win):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pg.draw.circle(win, color, (self.x, self.y), self.size // 2)

class Rectangle(Figure):

    def draw(self, win):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        pg.draw.rect(win, color, (self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)) 

Circle_1 = Circle(60)
W, H = 500, 500
pg.init()
win = pg.display.set_mode((W, H))
win.fill((255, 255, 255))

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    

    pg.display.update()
    pg.time.delay(60)
import pygame
import pygame.locals as locals
import random
import sys
import time
from threading import Thread


WINDOWLENGTH = 800
WINDOWHEIGHT = 800
BLACK = (0, 0, 0)
WHITE  = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWLENGTH,WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Snake !')
FPS = 60
fpsClock = pygame.time.Clock()

EAST = 0
WEST = 1
NORTH = 2
SOUTH = 3
toggle = 1
start = [300,300]
stop  = [200 , 300]
Points = [[300,300] , [200 , 300]]
Length = 2
MaxScore = 10
counter = 0
GAMEOVER = False
MARGINTOP = 100
MARGINBOTTOM = 50
MARGINLEFT = 75
TIMEGAP = 9
WIDTH = 4
VELOCITY = 1
DIRECTION = EAST
lengthup = False
triggered = False


def getLength(s):
    rs = 0
    for i in range(len(s) - 1):
        if s[i][0] == s[i+1][0]:
            rs += abs(s[i][1] - s[i+1][1])
        else:
            rs += abs(s[i][0] - s[i+1][0])

    return rs

class Mythread(Thread):
    global toggle

    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = 0
        self.h = 1
        self.center = []

    def getPosition(self):
        self.x = 100
        self.y =  200
        self.type = random.random()%2
        self.h = 5
        if self.type == 1 :
            self.h = 10
        self.center = [self.x , self.y]

    def func(self):
        global toggle
        while 2 > 1:
            time.sleep(5)
            toggle = 1- toggle
            time.sleep(5)


    def drawfood(self):
        pygame.draw.rect(DISPLAYSURF, RED , (self.center[0] - self.h/2, self.center[1] - self.h/2, self.h, self.h))

    def run(self):
        Thread(target = self.func ).start()





class food:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = 0
        self.h = 1
        self.center = []



    def randomize(self):
        self.x = random.randint(100,WINDOWLENGTH - 100)
        self.y = random.randint(100, WINDOWHEIGHT- 100)
        self.h = random.randint(1,3)*5

    def getinitcoord(self):
        return [self.x , self.y]

    def getwidth(self):
        return self.h



def drawSnake():
    global Points, start, stop, lengthup

    for i in range(len(Points)- 1):
        pygame.draw.line(DISPLAYSURF, GREEN, (Points[i][0], Points[i][1]), (Points[i+1][0], Points[i+1][1]) , WIDTH)

    time.sleep((float)(0.02))

    if DIRECTION == EAST:
        start[0] += VELOCITY
        Points[0][0] = start[0]
    elif DIRECTION == WEST:
        start[0] -= VELOCITY
        Points[0][0] = start[0]
    elif DIRECTION == NORTH:
        start[1] -= VELOCITY
        Points[0][1] = start[1]
    else:
        start[1] += VELOCITY
        Points[0][1] = start[1]

    if len(Points) > 1 and not lengthup :
        stop = Points[-1]

        if abs(Points[-2][0] - stop[0]) == VELOCITY or abs(Points[-2][1] - stop[1]) == VELOCITY:

            x = Points[-2][0]
            y = Points[-2][1]
            stop = [x , y]
            Points.pop(-1)
        else:
            if stop[0]  == Points[-2][0] :
                if stop[1] > Points[-2][1]:
                    Points[-1][1] -= VELOCITY
                else:
                    Points[-1][1] += VELOCITY
            else:
                if stop[0] > Points[-2][0] :
                    Points[-1][0] -= VELOCITY
                else:
                    Points[-1][0] += VELOCITY


    if lengthup:
        #print getLength(Points)
        #print Points
        lengthup = False





def main():
    global Points, start, stop, DIRECTION, toggle, lengthup, triggered
    t1 = Mythread()
    t1.run()
    Food = food()
    Food.randomize()

    while True:
        DISPLAYSURF.fill(WHITE)
        drawSnake()
        pygame.draw.rect(DISPLAYSURF, RED, (Food.getinitcoord()[0], Food.getinitcoord()[1], Food.getwidth(), Food.getwidth()))
        if triggered:
            Food.randomize()
            triggered = False
            #pygame.draw.rect(DISPLAYSURF, RED, (Food.getinitcoord()[0], Food.getinitcoord()[1], Food.getwidth(), Food.getwidth()))

        if abs(Points[0][0] - Food.getinitcoord()[0]) <= Food.getwidth() and abs(Points[0][1] - Food.getinitcoord()[1]) <= Food.getwidth() :
            lengthup = True
            print getLength(Points)
            print Points
            triggered = True

        for event in pygame.event.get():

            if event.type == locals.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == locals.KEYUP:
                if event.key == locals.K_LEFT and DIRECTION != WEST and DIRECTION != EAST:
                    DIRECTION = WEST
                    s = [[start[0] - VELOCITY , start[1] ]]
                    s.extend(Points)
                    Points =  s


                if event.key == locals.K_RIGHT and DIRECTION != EAST and DIRECTION != WEST :
                    DIRECTION = EAST
                    s = [[start[0] + VELOCITY, start[1] ]]
                    s.extend(Points)
                    Points =  s

                if event.key == locals.K_UP and DIRECTION != NORTH and DIRECTION != SOUTH :
                    DIRECTION = NORTH
                    s = [[start[0] , start[1] - VELOCITY]]
                    s.extend(Points)
                    Points =  s

                if event.key == locals.K_DOWN and DIRECTION != SOUTH and DIRECTION != NORTH:
                    DIRECTION = SOUTH
                    s = [[start[0] , start[1] + VELOCITY]]
                    s.extend(Points)
                    Points =  s

                if event.key == locals.K_BACKSPACE:
                    print Points


        pygame.display.update()



main()








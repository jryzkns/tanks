import pygame as pg
import math


# adapted from: https://www.pygame.org/wiki/RotateCenter
def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def to_degree(rad):
    return rad * 180/math.pi

def to_radian(degree):
    return degree *math.pi/180

class Tank():

    def __init__(self, x, y, win_w, win_h):
        self.x, self.y = x, y
        self.win_w, self.win_h = win_w, win_h
        self.img = pg.image.load("empty-arrow.png")
        self.heading = 0
        self.speed = 5

    def move(self, isForward):
        self.x += isForward*self.speed*math.cos(to_radian(90 + self.heading))
        self.y -= isForward*self.speed*math.sin(to_radian(90 + self.heading))

    def draw(self, surface):
        surface.blit(rot_center(self.img,self.heading), (self.x, self.y))

class PlayerTank(Tank):

    def __init__(self,x,y,win_w,win_h):
        Tank.__init__(self,x,y,win_w,win_h)
        self.img = pg.image.load("green-arrow.png")
        self.speed = 0.25

    def key_press_handle(self,key):
        if key == pg.K_q:
            self.heading += 10
        elif key == pg.K_e:
            self.heading -= 10

    def key_down_handle(self,keymap):
        if keymap[pg.K_w]:
            self.move(1)
        elif keymap[pg.K_s]:
            self.move(-1)


    def update(self,dt):
        self.heading %= 360

class EnemyTank(Tank):

    def __init__(self,x,y,win_w,win_h):
        Tank.__init__(self,x,y,win_w,win_h)
        self.img = pg.image.load("orange-arrow.png")

    def update(self, player_x, player_y, dt):

        # automatically faces the player, adapt new feature to turn slower
        self.heading = 90 - to_degree(
            math.atan2(self.y - player_y,self.x - player_x)
            )

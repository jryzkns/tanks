import pygame as pg
import random
import math

res = (1280,720)
score = 0
wave_wait = 200

gravelbackground = pg.image.load('assets\\floor_tile.jpg')
background = pg.Surface(res)
for i in range(res[0]//gravelbackground.get_rect().size[0] + 1):
    for j in range(res[1]//gravelbackground.get_rect().size[1] + 1):
            background.blit(    gravelbackground,
                                (   gravelbackground.get_rect().size[0]*i, 
                                    gravelbackground.get_rect().size[1]*j
                                ))

def sq_dist(b,e):
    return (b.x - e.centerx)**2 + (b.y - e.centery)**2

screen_pad_x = 100
screen_pad_y = 100
def rand_loc():
    return (random.randint(screen_pad_x,res[0]-screen_pad_x),
            random.randint(screen_pad_y,res[1]-screen_pad_y))

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
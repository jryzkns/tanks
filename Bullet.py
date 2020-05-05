import pygame
import math

from gameutils import to_radian

class Bullet:

    def __init__(self, x, y, facing, speed):
        
        self.x, self.y = x, y
        self.facing, self.speed = facing, speed
        
        self.lifetime = 3000
        self.w, self.h = 10, 10

    def update(self, dt):
        self.lifetime -= 1
        self.x += -1*self.speed*math.cos(to_radian(90 + self.facing))
        self.y -= -1*self.speed*math.sin(to_radian(90 + self.facing))

    def draw(self, surf):
        pygame.draw.rect(   surf, (255, 255, 0),
                            (self.x - self.w/2, 
                             self.y - self.h/2, 
                             self.w, self.h))
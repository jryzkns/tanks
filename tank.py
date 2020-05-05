import pygame as pg
import random
from Bullet import  *

from gameutils import rot_center, to_degree, to_radian

class Tank():

    def __init__(self, x, y, win_w, win_h):
        
        self.x, self.y = x, y
        self.win_w, self.win_h = win_w, win_h
        self.body_heading, self.head_heading = random.randint(0, 359), random.randint(0, 359)
        self.body = pg.image.load('assets\\TankPlayerBody.png')
        self.h, self.w = self.body.get_rect().size
        self.centerx, self.centery = self.x + self.w/2 ,self.y + self.h/2

        self.speed = 5

    def move(self, dist):
        self.x += dist*self.speed*math.cos(to_radian(90 + self.body_heading))
        self.y -= dist*self.speed*math.sin(to_radian(90 + self.body_heading))

    def draw(self, surface):
        surface.blit(rot_center(self.body,self.body_heading), (self.x, self.y))
        surface.blit(rot_center(self.head,self.head_heading), (self.x, self.y))

    def shoot(self,bullets):
        bullets.append(Bullet(self.x + self.w/2, self.y + self.h/2, self.head_heading, 5))

class player_tank(Tank):

    def __init__(self,x,y,win_w,win_h):

        Tank.__init__(self,x,y,win_w,win_h)
        self.head = pg.image.load("assets\\TankPlayerHead.png")
        self.hp, self.speed = 15, 0.25
        self.shoot_event_handled = False

    def key_down_handle(self,keymap):

        if keymap[pg.K_a]:
            self.body_heading += 1.5
        elif keymap[pg.K_d]:
            self.body_heading -= 1.5
        if keymap[pg.K_w]:
            self.move(-3)
        elif keymap[pg.K_s]:
            self.move(3)

    def update(self,dt, bullets):

        self.centerx, self.centery = self.x + self.w/2 ,self.y + self.h/2
        mouse_pos = pg.mouse.get_pos()
        self.body_heading %= 360
        self.head_heading %= 360

        self.head_heading = -90 - to_degree(math.atan2( self.centery - mouse_pos[1],
                                                        self.centerx - mouse_pos[0]))

        if pg.mouse.get_pressed()[0] and not self.shoot_event_handled:
            self.shoot(bullets)
            self.shoot_event_handled = True

        self.shoot_event_handled = pg.mouse.get_pressed()[0]

class enemy_tank(Tank):

    def __init__(self,x,y,win_w,win_h):
        Tank.__init__(self,x,y,win_w,win_h)
        self.head = pg.image.load("assets\\TankEnemie"+str(random.randint(1, 3))+".png")

        self.currentstate = 1 # states: 1 = wander, 2 = pursuit, 3 = shoot 0 = done
        self.statetimer = 90
        self.rottimer = 30
        self.transtimer = 200
        self.dir = 1
        self.hp = 4
    
    def enemymove(self, dist):

        self.centerx, self.centery = self.x + self.w/2, self.y + self.h/2

        if ((self.centerx > self.win_w) or (self.centerx < 0)
            or (self.centery > self.win_h) or (self.centery < 0)):
            self.body_heading -= 180

        self.move(dist)

    def update(self, dt, player_x, player_y):
        
        self.centerx, self.centery = self.x + self.w/2 ,self.y + self.h/2
        
        if self.currentstate == 1:
            self.enemymove(0.07)
            self.body_heading += self.dir*0.5

            self.rottimer -= 1
            if self.rottimer <= 0:
                self.rottimer = random.randint(20,30)
                self.dir *= (1-2*random.randint(0, 1))
            
            self.statetimer -= 1
            if self.statetimer <= 0:
                self.currentstate = 0

        if self.currentstate == 2:
            self.head_heading = -90 - to_degree((math.atan2(self.y - player_y,self.x - player_x)))
            self.body_heading =  90 - to_degree((math.atan2(self.y - player_y,self.x - player_x)))
            self.enemymove(0.09)
            self.statetimer -= 8

        self.transtimer -= 1
        if  (self.transtimer <= 0) or (self.currentstate == 0):
            self.transtimer = 200
            self.currentstate = random.randint(1, 2)
            self.statetimer = random.randint(70, 170)

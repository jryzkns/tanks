# PYGAME BOILERPLATE CODE
# JRYZKNS 2019

res = (1200,600)

import pygame as pg
from tank import *
import random

pg.init()
clock = pg.time.Clock()
game_win = pg.display.set_mode(res)
running, paused, t, dt = True, False, pg.time.get_ticks(), 0

player = PlayerTank(500,200,res[0],res[1])

enemies = [
    EnemyTank(random.randint(0,res[0]),random.randint(0,res[1]),res[0],res[1]),
    EnemyTank(random.randint(0,res[0]),random.randint(0,res[1]),res[0],res[1]),
    EnemyTank(random.randint(0,res[0]),random.randint(0,res[1]),res[0],res[1])
]

while running:

        # CALLBACKS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                player.key_press_handle(event.key)
                if event.key == 32:     # kbd constant for spacebar
                        paused = not paused

        dt = pg.time.get_ticks() - t

        if not paused:

            keys = pg.key.get_pressed()
            player.key_down_handle(keys)
            player.update(dt)
            for enemy in enemies:
                enemy.update(player.x, player.y, dt)

        game_win.fill((255,255,255))

        player.draw(game_win)
        for enemy in enemies:
            enemy.draw(game_win)

        pg.display.flip()

        t = pg.time.get_ticks()
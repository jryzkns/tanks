from gameutils import *
from tank import *
from Bullet import *
from score_keeper import *
import sys

pg.init()

clock = pg.time.Clock()
game_win = pg.display.set_mode(res)

running, paused = True, False
t, dt = pg.time.get_ticks(), 0

score_notif = score_keeper(*res)
player = player_tank(500, 200, *res)
enemy_queue, bullet_queue = [], []

while running:

        # CALLBACKS
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit(); sys.exit()

            elif event.type == pg.KEYDOWN:
                if event.key == 32:
                    paused = not paused

        dt = (pg.time.get_ticks() - t)/1000.

        if not paused:

            running = player.hp >= 1

            for bullet in bullet_queue:
                bullet.update(dt)
                if bullet.lifetime < 1:
                    bullet_queue.remove(bullet)

                for enemy in enemy_queue:                      
                    if sq_dist(bullet,enemy) <= 1300:
                        bullet_queue.remove(bullet)
                        enemy.hp -= 1
                        if enemy.hp < 1:
                            enemy_queue.remove(enemy)
                        break

            keys = pg.key.get_pressed()
            player.key_down_handle(keys)

            player.update(dt, bullet_queue)

            for enemy in enemy_queue:
                enemy.update(dt, player.x, player.y)
            
            if len(enemy_queue) == 0:
                score_notif.update(score+1)
                score_notif.show = True
                wave_wait -= 1
                if wave_wait <= 0:
                    score += 1
                    enemy_queue = [ enemy_tank(*rand_loc(), *res) 
                                        for i in range(score)]
                    wave_wait, score_notif.show = 200, False
        
        game_win.blit(background, (0, 0))

        for enemy in enemy_queue:
            enemy.draw(game_win)

        for bullet in bullet_queue:
            bullet.draw(game_win)

        player.draw(game_win)

        if score_notif.show:
            score_notif.draw(game_win)
        
        pg.display.flip()

        t = pg.time.get_ticks()
import sys
import pygame
import random
from pygame.constants import MOUSEBUTTONDOWN, QUIT
from object import *

level = 1

#define game variables
rows = 0
cols = 0
alien_cooldown = 1000#bullet cooldown in milliseconds
boss_cooldown = 1500
last_alien_shot = pygame.time.get_ticks()
last_boss_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0#0 is no game over, 1 means player has won, -1 means player has lost



def draw_bg():
    screen.blit(bg, (0, 0))

#define function for creating text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#level
def lv1():
    global rows, cols, game_over
    rows = 1
    cols = 5
    game_over = 0
    create_aliens(1)
def lv2():
    global rows, cols, game_over
    rows = 3
    cols = 5
    game_over = 0
    create_aliens(2)
def lv3():
    boss_group.add(boss) 


def create_aliens(lv):
    #generate aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70,lv)
            alien_group.add(alien)
            
#create player
spaceship_group.add(spaceship)


lv1()
#level up
def level_up():
    global level
    level += 1
    if level == 2:
        lv2()
    elif level == 3:
        lv3()

def start_shooting():
    global level, time_now, last_alien_shot, last_boss_shot, alien_cooldown, boss_cooldown, alien_bullet_group, bosslaser_group,alien_group, Alien_Bullets, BossLaser, game_over, spaceship,bullet_group,countdown,level_up
    if level < 3:
        if time_now - last_alien_shot > alien_cooldown and len(alien_bullet_group) < 5*level and len(alien_group) > 0:
                    attacking_alien = random.choice(alien_group.sprites())
                    alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom, level)
                    alien_bullet_group.add(alien_bullet)
                    last_alien_shot = time_now
        game_over = spaceship.update()
                #update sprite groups
        bullet_group.update()
        alien_group.update()
        alien_bullet_group.update()
        if len(alien_group) == 0:
            level_up()
            countdown = 3
            bullet_group.empty()
            alien_bullet_group.empty()
            spaceship.reset()
    if level == 3:
          if time_now - last_boss_shot > boss_cooldown and len(bosslaser_group) < 10 and len(boss_group) > 0:
                    attacking_alien = random.choice(boss_group.sprites())
                    for i in range(-3, 4, 1):
                        alien_bullet = BossLaser(attacking_alien.rect.centerx, attacking_alien.rect.bottom, i * 12)
                        bosslaser_group.add(alien_bullet) 
                    last_boss_shot = time_now
          game_over = spaceship.update()
          #update sprite groups
          bullet_group.update()
          boss_group.update()
          bosslaser_group.update()
              
          if len(boss_group) == 0:
                    game_over = 1 

# level lable
def redraw_window():
    level_lable = main_font.render(f'LEVEL {level}',1,(255,255,255))
    screen.blit(level_lable, (screen_width / 2 - 100,10))
    pygame.display.flip()

run = False
click = False


#start window
while True:
    screen.fill((202, 228, 241))
    
    if start_button.draw(screen):
        if click:
            run = True
            break
    if exit_button.draw(screen):
        if click:
            pygame.quit()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    
    
    pygame.display.update()
    
    
while run:
    redraw_window()
    clock.tick(fps)
    #draw background
    draw_bg()
    if countdown == 0:
        #record current time
        time_now = pygame.time.get_ticks()
        if countdown > 0:
            draw_text('GET READY!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
        draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer
            
        
        if game_over == 0:
            if level == 1:
                start_shooting()
            elif level == 2 :
                start_shooting()
            elif level == 3 :
                start_shooting()
        else:
            if game_over == -1:
                draw_text('GAME OVER!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
                bullet_group.empty()
                alien_bullet_group.empty()
                alien_group.empty()
                boss_group.empty()
                bosslaser_group.empty()
                if try_again_button.draw(screen):
                    if click:
                        level = 1
                        countdown = 3
                        spaceship.revive()
                        spaceship.reset()
                        spaceship_group.add(spaceship)
                        game_over = spaceship.update()
                        lv1()
                        bullet_group.update()
                        alien_group.update()
                        alien_bullet_group.update()

                        
            if game_over == 1:
                draw_text('YOU WIN!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 - 100))
                bullet_group.empty()
                spaceship_group.empty()
                bosslaser_group.empty()
                if replay_button.draw(screen):
                    if click:
                        level = 1
                        countdown = 3
                        spaceship.revive()
                        spaceship.reset()
                        spaceship_group.add(spaceship)
                        game_over = spaceship.update()
                        lv1()
                        bullet_group.update()
                        alien_group.update()
                        alien_bullet_group.update()
                if exit_end_button.draw(screen):
                    if click:
                        pygame.quit()
                        
                

    


    #update explosion group 
    explosion_group.update()


    #draw sprite groups
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    alien_group.draw(screen)
    alien_bullet_group.draw(screen)
    explosion_group.draw(screen)
    boss_group.draw(screen)
    bosslaser_group.draw(screen)

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
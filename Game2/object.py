from boom import *
import math

#create spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Ship/4.png")
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()

    def reset(self):
        self.rect.x = int(screen_width / 2) - 18
        self.rect.y = screen_height - 100
    
    def revive(self):
        self.health_start = 5
        self.health_remaining = 5
    
    def update(self):
        #set movement speed
        speed = 8
        #set a cooldown variable
        cooldown = 500 #milliseconds
        game_over = 0


        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed

        #record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now


        #update mask
        self.mask = pygame.mask.from_surface(self.image)


        #draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            game_over = -1
        return game_over


#create Bullets class
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Shoot/3.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
        if pygame.sprite.spritecollide(self, boss_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion2_fx.play()
            #reduce spaceship health
            boss.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
                        
class Boss(pygame.sprite.Sprite):
    
    def __init__(self,x,y,health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Ship/8.png")
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.move_counter = 0
        self.move_direction = 1
    #update the boss
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 2
        if abs(self.move_counter) > 150:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
    #draw health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            self.kill()
            
class BossLaser(pygame.sprite.Sprite):
    def __init__(self, x, y, bend):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Shoot/4.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.bend = bend
    def update(self):
        self.rect.y += math.cos(self.bend * math.pi / 180) * 12
        self.rect.x -= math.tan(self.bend * math.pi / 180) * 15
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion3_fx.play()
            #reduce spaceship health
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)

#create Aliens class
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y,lv):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Ship/" + str(lv) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
#create Alien Bullets class
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y,lv):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Shoot/"+str(lv)+".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion3_fx.play()
            #reduce spaceship health
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosion_group.add(explosion)
            
boss = Boss(int(screen_width / 2), 100 , 10)
spaceship = Spaceship(int(screen_width / 2) - 10, screen_height - 100, 5)

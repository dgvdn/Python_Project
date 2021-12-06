import pygame
from pygame import mixer
import button

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

#define fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Shooter')

#define fonts
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)
main_font = pygame.font.SysFont("comicsans", 50)

#load image
bg = pygame.transform.scale(pygame.image.load("img/bg.png").convert(), (600,800)) 

#load sounds
explosion_fx = pygame.mixer.Sound("Sound/shoot-destroy-1.wav")
explosion_fx.set_volume(0.05)

explosion2_fx = pygame.mixer.Sound("Sound/shoot-destroy-2.wav")
explosion2_fx.set_volume(0.05)

explosion3_fx = pygame.mixer.Sound("Sound/shoot-destroy-3.wav")
explosion3_fx.set_volume(0.05)
laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.05)

#define colours
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

#create sprite groups
spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
bosslaser_group = pygame.sprite.Group()
    
start_img = pygame.image.load('img/play.png').convert_alpha()
exit_img = pygame.image.load('img/close_2.png').convert_alpha()
try_again_img = pygame.image.load('img/try_again.png').convert_alpha()
replay_img = pygame.image.load('img/replay.png').convert_alpha()
exit_end_img = pygame.image.load('img/exit.png').convert_alpha()

start_button = button.Button(int(screen_width / 2) - 111.6, 200, start_img, 0.8)
exit_button = button.Button(int(screen_width / 2) - 96, 400, exit_img, 0.8)
try_again_button = button.Button(210, int(screen_height / 2) + 100, try_again_img, 0.3)
replay_button = button.Button(223, int(screen_height / 2 ), replay_img, 0.1)
exit_end_button = button.Button(247.5, int(screen_height / 2 + 100 ), exit_end_img, 0.3)
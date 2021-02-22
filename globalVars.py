import pygame
import math

screenWidth = 1600
screenHeight = 800
gameWidth = 2200/5
gameHeight = 1500/5
compressedWidth = 300
compressedHeight = 150
button_surface_width = 300
button_surface_height = 300


win = False
loss = False

main_screen = pygame.display.set_mode((screenWidth, screenHeight))
screen = pygame.Surface((screenWidth, screenHeight))
button_screen = pygame.Surface((button_surface_width, button_surface_height))
pygame.display.update()

cameraX = gameWidth/2 - screenWidth/2 # centers camera
cameraY = gameHeight/2 - screenHeight/2

player = 0
humans = []
zombies = []
bullets = []

zombiesDead = 0
humansDead = 0
humansToZombie = 0



DIRECTION = {
    'x': 0,
    'y': 0
}


def dist(e1, e2):
    return math.sqrt((e2.x-e1.x)**2 + (e2.y-e1.y)**2)

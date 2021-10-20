import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 240 # frames per second setting
fpsClock = pygame.time.Clock()

# set up the window
WIDTH = 1000
HEIGHT = 1000
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Battleship')

OCEAN_COLOR = (0, 105, 148)
dogImg = pygame.image.load('dog.png')
dogx = WIDTH * 0.25
dogy = HEIGHT * 0.25


while True: # the main game loop
    SCREEN.fill(OCEAN_COLOR)
    mouseX = pygame.mouse.get_pos()[0]
    mouseY = pygame.mouse.get_pos()[1]
    SCREEN.blit(dogImg, (mouseX, mouseY))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)
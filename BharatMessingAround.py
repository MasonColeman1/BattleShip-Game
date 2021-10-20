## Execute  $ python ./BharatMessingAround.py
## to run this program
##
## NOTES AS OF:
##      OCTOBER 20, 2021
##      6:33PM
# As of now, the image can be clicked+dragged to follow the mouse and
# remains where ever the mouse is unclicked. The big issue is how to keep
# the image displayed even when the user is doing nothing.


import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30 # frames per second setting
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

drag = False

while True: # the main game loop
    SCREEN.fill(OCEAN_COLOR)

    # mouseX = pygame.mouse.get_pos()[0]
    # mouseY = pygame.mouse.get_pos()[1]
    # SCREEN.blit(dogImg, (mouseX-300, mouseY-250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Exit condition
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
        elif event.type == pygame.MOUSEMOTION and drag: # mouse is clicked and moving
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            SCREEN.blit(dogImg, (mouseX-300, mouseY-250))
            dogx, dogy = mouseX-300, mouseY-250
        elif event.type == pygame.MOUSEBUTTONUP: # mouse is unclicked
            drag = False
            SCREEN.blit(dogImg, (dogx, dogy))
        else:
            SCREEN.blit(dogImg, (dogx, dogy))

    pygame.display.update()
    fpsClock.tick(FPS)
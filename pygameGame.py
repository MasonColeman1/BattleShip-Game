import pygame
import sys
from enum import Enum

#defining all the colors
WHITE = (255,255,255)
LIGHT_GRAY = (170,170,170)
DARK_GRAY = (100,100,100)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (211, 211, 211)

#these probably shouldnt be global but im not gonna change that
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 70
HEIGHT = 70

# This sets the margin between each cell
MARGIN = 5

def main():
    pygame.init()

    #doing fps so my computer doesnt catch on fire
    clock = pygame.time.Clock()
    fps = 60

    screen = pygame.display.set_mode((1000,1000))
    global game_state
    game_state = GameState.TITLE

    while True:
        clock.tick(fps)

        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.PLAY:
            game_state = play_screen(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            sys.exit()
            return

def title_screen(screen):

    #background title screen if not work change reference to local
    bg_title = pygame.image.load(r"C:\Users\resur\OneDrive\Documents\School\CS 3100\group6-cs3100\title_art.png")

    # defining a font
    smallfont = pygame.font.SysFont('Corbel',35)

    # rendering a text written in this font
    quit_text = smallfont.render('quit' , True , WHITE)
    options_text = smallfont.render('options', True, WHITE)
    play_text = smallfont.render('play', True, WHITE)

    #MASONS BUTTONS BITCH
    #x pos, y pos, width, height
    quit_button = pygame.Rect(430,550,140,40)
    options_button = pygame.Rect(430,490,140,40)
    play_button = pygame.Rect(430,430,140,40)

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                #quits game when clicked on quit button
                if quit_button.collidepoint(mouse_pos):
                    return GameState.QUIT

                if play_button.collidepoint(mouse_pos):
                    return GameState.PLAY

        screen.blit(bg_title, (0,0))

        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()

        #draw buttons
        if quit_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, quit_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, quit_button)

        if options_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, options_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, options_button)

        if play_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, play_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, play_button)

        # superimposing the text onto buttons
        screen.blit(quit_text , (470,550))
        screen.blit(options_text, (450,490))
        screen.blit(play_text, (470,430))

        # updates the frames of the game
        pygame.display.update()

def play_screen(screen):
    p1grid = []
    for row in range(10):
        # Add an empty array that will hold each cell
        # in this row
        p1grid.append([])
        for column in range(10):
            p1grid[row].append(0)  # Append a cell

    WINDOW_SIZE = [WIDTH*10+MARGIN*10, HEIGHT*10+MARGIN*10]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Used to track current grid location mouse is in
    curr_column = 10
    curr_row = 10

    # Information on ship being placed
    placeable_ships = [2, 3, 3, 4, 5]
    ship_len = 0
    ship_orientation = [0, 0]
    # all_ships_placed = False

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)

                #makes sure player cannot shoot same square twice
                if ship_len == 0 or ship_orientation == [0, 0]: # Just in case they try to place without choosing anything
                    print("Invalid ship placement options")
                    continue
                else: print("ship will be " + ("vertical" if ship_orientation[0] else "horizontal") + " with length " + str(ship_len))
                for spot in range(ship_len):
                    if p1grid[row + (spot * ship_orientation[0])][column + (spot * ship_orientation[1])] == 0:
                        # Set that location to one
                        p1grid[row + (spot * ship_orientation[0])][column + (spot * ship_orientation[1])] = 1
                        print("Click ", pos, "Grid coordinates: ", row, column)
                    else: # overlap is detected
                        print("Overlap detected, but how do we \'roll back\' the changes??")
                        spot_to_keep = [row+(spot*ship_orientation[0]), column+(spot*ship_orientation[1])]
                        for spot in range(ship_len):
                            p1grid[row + (spot * ship_orientation[0])][column + (spot * ship_orientation[1])] = 0
                        p1grid[spot_to_keep[0]][spot_to_keep[1]] = 1
                        placeable_ships.append(ship_len)
                        break
                # Making sure the ship can't be placed a second time
                ship_len = 0
                ship_orientation = [0, 0]
            elif event.type == pygame.MOUSEMOTION: # Gets current mouse position
                pos = pygame.mouse.get_pos()

                curr_column = pos[0] // (WIDTH + MARGIN)
                curr_row = pos[1] // (HEIGHT + MARGIN)
            elif event.type == pygame.KEYDOWN: # Selects ships to place based off of user input
                if event.key == pygame.K_2 and 2 in placeable_ships: # if user presses "2", place the 2 ship
                    ship_len = 2
                    placeable_ships.remove(2)
                elif event.key == pygame.K_3 and 3 in placeable_ships: # if user presses "3", place the 3 ship
                    ship_len = 3
                    placeable_ships.remove(3)
                elif event.key == pygame.K_4 and 4 in placeable_ships: # if user presses "4", place the 4 ship
                    ship_len = 4
                    placeable_ships.remove(4)
                elif event.key == pygame.K_5 and 5 in placeable_ships: # if user presses "5", place the 5 ship
                    ship_len = 5
                    placeable_ships.remove(5)
                if event.key == pygame.K_v: # Set the ship to vertical orientation
                    ship_orientation = [1,0]
                elif event.key == pygame.K_h: # Set the ship to horizontal orientation
                    ship_orientation = [0,1]



        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        # if not all_ships_placed:
        for row in range(10):
            for column in range(10):
                color = WHITE
                if p1grid[row][column] == 1:
                    color = GREEN
                elif row == curr_row and column == curr_column:
                    color = GRAY
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
        #     if placeable_ships == []: all_ships_placed = True
        # else:
        #     print("Now the logic of the AI placing its ships needs to be implemented")
        #     time.sleep(3)
        #     done = True


        pygame.display.update()

        if placeable_ships == []: all_ships_placed = True


class GameState(Enum):
    QUIT = -1
    TITLE = 0
    PLAY = 1

if __name__ == "__main__":
    main()

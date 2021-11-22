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
ORANGE = (255,165,0)

#THESE ARE THE SETTINGS VARIABLES
#need to be global since settings mode and play mode need to access them
#I am going to follow the logic group and just make a choice var
#default is singleplayer (1 board)
choice = 1
debug = False
difficulty = 0 #0 - Easy, 1 - Normal, 2 - Hard, 3 - Impossible

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

    game_state = GameState.TITLE

    while True:
        clock.tick(fps)

        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.PLAY:
            game_state = play_screen(screen)

        if game_state == GameState.SETTINGS:
            game_state = settings_screen(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            sys.exit()
            return

def title_screen(screen):

    #background title screen if not work change reference to local
    bg_title = pygame.image.load('title_art.png')

    # defining a font
    smallfont = pygame.font.SysFont('Corbel',35)

    # rendering a text written in this font
    quit_text = smallfont.render('quit' , True , WHITE)
    settings_text = smallfont.render('settings', True, WHITE)
    play_text = smallfont.render('play', True, WHITE)

    #MASONS BUTTONS BITCH
    #x pos, y pos, width, height
    quit_button = pygame.Rect(430,550,140,40)
    settings_button = pygame.Rect(430,490,140,40)
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

                if settings_button.collidepoint(mouse_pos):
                    return GameState.SETTINGS

        screen.blit(bg_title, (0,0))

        # stores the (x,y) coordinates into
        # the variable as a tuple
        mouse = pygame.mouse.get_pos()

        #draw buttons
        if quit_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, quit_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, quit_button)

        if settings_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, settings_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, settings_button)

        if play_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, play_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, play_button)

        # superimposing the text onto buttons
        screen.blit(quit_text , (470,550))
        screen.blit(settings_text, (445,490))
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
                # Making sure the ship can't be placed a second time (resetting it essentially)
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


def settings_screen(screen):
    #must do this to change global variables without making them local
    global choice, debug, difficulty

    screen.fill(BLACK)

    #fonts
    header_font = pygame.font.SysFont('verdana', 90, bold=True)
    button_font = pygame.font.SysFont('arial', 50)

    #text
    header_text = header_font.render('Settings', True, WHITE)
    cpu_text = button_font.render('CPU Options:', True, WHITE)

    back_text = button_font.render('back', True, WHITE)

    singleplayer_text = button_font.render('singleplayer', True, WHITE)
    one_board_text = button_font.render('1 board', True, WHITE)
    two_board_text = button_font.render('2 boards', True, WHITE)

    multiplayer_text = button_font.render('multiplayer', True, WHITE)
    two_player_text = button_font.render('1 v 1', True, WHITE)
    three_player_text = button_font.render('1 v 1 v 1', True, WHITE)

    debug_text = button_font.render('debug', True, WHITE)
    debug_off_text = button_font.render('off', True, WHITE)
    debug_on_text = button_font.render('on', True, WHITE)

    difficulty_text = button_font.render('difficulty', True, WHITE)
    easy_text = button_font.render('easy', True, WHITE)
    normal_text = button_font.render('normal', True, WHITE)
    hard_text = button_font.render('hard', True, WHITE)
    impossible_text = button_font.render('impossible', True, WHITE)

    #button time
    #x pos, y pos, width, height
    back_button = pygame.Rect(20,20,200,75)

    singleplayer_button = pygame.Rect(50,150,350,100)
    one_board_button = pygame.Rect(500,150,220,100)
    two_board_button = pygame.Rect(750,150,220,100)

    multiplayer_button = pygame.Rect(50,300,350,100)
    two_player_button = pygame.Rect(500,300,220,100)
    three_player_button = pygame.Rect(750,300,220,100)

    debug_button = pygame.Rect(50,600,350,100)
    debug_off_button = pygame.Rect(500,600,220,100)
    debug_on_button = pygame.Rect(750,600,220,100)

    difficulty_button = pygame.Rect(50,750,350,100)
    easy_button = pygame.Rect(500,750,220,100)
    normal_button = pygame.Rect(750,750,240,100)
    hard_button = pygame.Rect(500,875,220,100)
    impossible_button = pygame.Rect(750,875,240,100)


    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #checks if a mouse is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if back_button.collidepoint(mouse_pos):
                    return GameState.TITLE

                if singleplayer_button.collidepoint(mouse_pos):
                    #prevents clicking singleplayer and changing from 2 boards to 1 board
                    if choice != 1 and choice != 2:
                        choice = 1 #1 by default

                if multiplayer_button.collidepoint(mouse_pos):
                    #prevents clicking multiplayer and changing from 1v1v1 to 1v1
                    if choice != 3 and choice != 4:
                        choice = 3 #3 by default

                if one_board_button.collidepoint(mouse_pos):
                    choice = 1
                if two_board_button.collidepoint(mouse_pos):
                    choice = 2

                if two_player_button.collidepoint(mouse_pos):
                    choice = 3
                if three_player_button.collidepoint(mouse_pos):
                    choice = 4

                if debug_off_button.collidepoint(mouse_pos):
                    debug = False
                if debug_on_button.collidepoint(mouse_pos):
                    debug = True

                if easy_button.collidepoint(mouse_pos):
                    difficulty = 0
                if normal_button.collidepoint(mouse_pos):
                    difficulty = 1
                if hard_button.collidepoint(mouse_pos):
                    difficulty = 2
                if impossible_button.collidepoint(mouse_pos):
                    difficulty = 3


        #get mouse position
        mouse = pygame.mouse.get_pos()

        #draw buttons
        if back_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, back_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, back_button)
        #selectable buttons
        #singleplayer
        if choice == 1 or choice == 2:
            pygame.draw.rect(screen, ORANGE, singleplayer_button)
        elif singleplayer_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, singleplayer_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, singleplayer_button)
        #multiplayer
        if choice == 3 or choice == 4:
            pygame.draw.rect(screen, ORANGE, multiplayer_button)
        elif multiplayer_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, multiplayer_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, multiplayer_button)
        #one board
        if choice == 1:
            pygame.draw.rect(screen, GREEN, one_board_button)
        elif one_board_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, one_board_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, one_board_button)
        #two board
        if choice == 2:
            pygame.draw.rect(screen, GREEN, two_board_button)
        elif two_board_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, two_board_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, two_board_button)
        #two player/1v1
        if choice == 3:
            pygame.draw.rect(screen, GREEN, two_player_button)
        elif two_player_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, two_player_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, two_player_button)
        #three player/1v1v1
        if choice == 4:
            pygame.draw.rect(screen, GREEN, three_player_button)
        elif three_player_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, three_player_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, three_player_button)

        #debug
        if debug:
            pygame.draw.rect(screen, GREEN, debug_button)
            pygame.draw.rect(screen, GREEN, debug_on_button)
            if debug_off_button.collidepoint(mouse):
                pygame.draw.rect(screen, LIGHT_GRAY, debug_off_button)
            else:
                pygame.draw.rect(screen, DARK_GRAY, debug_off_button)
        else:
            pygame.draw.rect(screen, RED, debug_button)
            pygame.draw.rect(screen, RED, debug_off_button)
            if debug_on_button.collidepoint(mouse):
                pygame.draw.rect(screen, LIGHT_GRAY, debug_on_button)
            else:
                pygame.draw.rect(screen, DARK_GRAY, debug_on_button)

        pygame.draw.rect(screen, DARK_GRAY, difficulty_button)
        if difficulty == 0:
            pygame.draw.rect(screen, ORANGE, easy_button)
        elif easy_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, easy_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, easy_button)
        if difficulty == 1:
            pygame.draw.rect(screen, ORANGE, normal_button)
        elif normal_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, normal_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, normal_button)
        if difficulty == 2:
            pygame.draw.rect(screen, ORANGE, hard_button)
        elif hard_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, hard_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, hard_button)
        if difficulty == 3:
            pygame.draw.rect(screen, ORANGE, impossible_button)
        elif impossible_button.collidepoint(mouse):
            pygame.draw.rect(screen, LIGHT_GRAY, impossible_button)
        else:
            pygame.draw.rect(screen, DARK_GRAY, impossible_button)

        #superimposing text
        screen.blit(header_text, (300,0))
        screen.blit(cpu_text, (70,475))

        screen.blit(back_text, (65,30))

        screen.blit(singleplayer_text, (90,175))
        screen.blit(multiplayer_text, (100,325))

        screen.blit(one_board_text, (525,175))
        screen.blit(two_board_text, (765,175))

        screen.blit(two_player_text, (555,325))
        screen.blit(three_player_text, (765,325))

        screen.blit(debug_text, (150, 625))
        screen.blit(debug_off_text, (580, 625))
        screen.blit(debug_on_text, (835, 625))

        screen.blit(difficulty_text, (130, 775))
        screen.blit(easy_text, (560, 775))
        screen.blit(normal_text, (795, 775))
        screen.blit(hard_text, (560, 900))
        screen.blit(impossible_text, (750, 900))


        pygame.display.update()




class GameState(Enum):
    QUIT = -1
    TITLE = 0
    PLAY = 1
    SETTINGS = 2

if __name__ == "__main__":
    main()

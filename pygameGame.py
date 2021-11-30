import pygame
import sys
from enum import Enum
import random
import time

#defining all the colors
WHITE = (255,255,255)
LIGHT_GRAY = (170,170,170)
DARK_GRAY = (100,100,100)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (211, 211, 211)
ORANGE = (255,165,0)
PINK = (255,105,180)
LIGHT_PINK = (255,182,193)
BLUE = (0,105,148)

#THESE ARE THE SETTINGS VARIABLES
#need to be global since settings mode and play mode need to access them
#I am going to follow the logic group and just make a choice var
#default is singleplayer (1 board)
choice = 2 #1 - One board, 2 - Two boards, 3 - PvP, 4 - PvPvP
debug = True
difficulty = 3 #0 - Easy, 1 - Normal, 2 - Hard, 3 - Impossible
difficulty_dict = {0:100, 1:60, 2:30, 3:17}

#these probably shouldnt be global but im not gonna change that
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 70
HEIGHT = 70

# This sets the margin between each cell
MARGIN = 10

def main():
    pygame.init()

    #doing fps so my computer doesnt catch on fire
    clock = pygame.time.Clock()
    fps = 60

    screen = pygame.display.set_mode((1000,1000))
    pygame.display.set_caption('Battleship')

    game_state = GameState.TITLE

    p1grid = []
    oppgrid = []
    winner = ""

    while True:
        clock.tick(fps)

        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if choice == 1:
            if game_state == GameState.AI_PLACE_SHIPS:
                game_state = create_ai_grid_screen(screen, oppgrid)

            if game_state == GameState.P1_TURN:
                for turn in range(difficulty_dict[difficulty]):
                    game_state = p1_turn(screen, oppgrid)
                if winner == "":
                    winner = "Tie"
                game_state = GameState.GAME_OVER

        if choice == 2:
            if game_state == GameState.PLACE_SHIPS:
                game_state = place_ships_screen(screen, p1grid)

            if game_state == GameState.AI_PLACE_SHIPS:
                game_state = create_ai_grid_screen(screen, oppgrid)

            if game_state == GameState.P1_TURN or game_state == GameState.P2_AI_TURN:
                for turn in range(difficulty_dict[difficulty]*2):
                    if turn%2 == 0 and game_state == GameState.P1_TURN: # Even turns is player one
                        game_state = p1_turn(screen, oppgrid)
                    elif turn%2 == 1 and game_state == GameState.P2_AI_TURN: # Odd turns is player two/AI
                        game_state = p2_ai_turn(screen, p1grid)
                if winner == "":
                    winner = "Tie"
                game_state = GameState.GAME_OVER

        if game_state == GameState.GAME_OVER:
            game_state = game_end_screen(screen)

        if game_state == GameState.SETTINGS:
            game_state = settings_screen(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            sys.exit()
            return

def title_screen(screen):

    #background title screen if not work change reference to local
    bg_title = pygame.image.load(r"C:\Users\jchri\Documents\S&T\FALL 21\CS 3100\Project Code\group6-cs3100\title_art.png")

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
                    if choice == 1:
                        return GameState.AI_PLACE_SHIPS
                    elif choice == 2:
                        return GameState.PLACE_SHIPS

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

def place_ships_screen(screen, p1grid):
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

                # handle invalid selections
                if ship_len == 0 or ship_orientation == [0, 0]: # Just in case they try to place without choosing anything
                    print("Invalid ship placement options")
                    continue
                else: print("Ship will be " + ("vertical" if ship_orientation[0] else "horizontal") + " with length " + str(ship_len))

                # Handle the ship being out of bounds
                if ship_orientation == [1,0] and row > 10-ship_len:
                    print("Ship would go off the bottom of the screen")
                    placeable_ships.append(ship_len)
                    break
                elif ship_orientation == [0,1] and column > 10-ship_len:
                    print("Ship would go off the right side of the screen")
                    placeable_ships.append(ship_len)
                    break
                else: print("Should be all good!")

                # Change all spots on the grid corresponding to the ship
                overlap_flag = False
                prev_values = []
                for spot in range(ship_len):

                    # Set that location to one
                    prev_values.append(p1grid[row + (spot * ship_orientation[0])][column + (spot * ship_orientation[1])])
                    p1grid[row + (spot * ship_orientation[0])][column + (spot * ship_orientation[1])] = ship_len
                    print("Click ", pos, "Grid coordinates: ", row, column)
                    if prev_values[spot] == 1: # overlap is detected
                        overlap_flag = True

                if overlap_flag: # Roll back all changes
                    print("There was an overlap, let's roll everything back")
                    for space_to_revert in range(ship_len):
                        p1grid[row + (space_to_revert * ship_orientation[0])][column + (space_to_revert * ship_orientation[1])] = prev_values.pop(0)
                    placeable_ships.append(ship_len)
                else:
                    print("Ship fully placed!")


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
                if event.key == pygame.K_d and placeable_ships == [] and choice == 2:
                    # User is all done placing ships. Move on to AI ships
                    return GameState.AI_PLACE_SHIPS



        # Set the screen background
        screen.fill(BLACK)
        
        # Draw the grid

        # Load ocean tile image here to avoid loading each loop
        oceanTile = pygame.image.load(r"C:\Users\jchri\Documents\S&T\FALL 21\CS 3100\Project Code\group6-cs3100\cs3100_Group-6 Ships\cs3100_oceanFloor.png")
        carrier = []
        battleship = []
        submarine = []        
        cruiser = []
        destroyer = []
        cruiserCount = 0 # counter for determining cruiser and sub placement
        for ship in placeable_ships:
            for i in range(ship):
                if ship == 2: # Load destroyer images
                    shipTile = pygame.image.load(r"C:\Users\jchri\Documents\S&T\FALL 21\CS 3100\Project Code\group6-cs3100\cs3100_Group-6 Ships\Destroyer\blue\destroyerBlue"+str(i)+r".png")
                    destroyer.append(shipTile)
                elif ship == 3: # Load cruiser images
                    shipTile = pygame.image.load(r"C:\Users\jchri\Documents\S&T\FALL 21\CS 3100\Project Code\group6-cs3100\cs3100_Group-6 Ships\Cruiser\blue\cruiserBlue"+str(i)+r".png")
                    cruiser.append(shipTile)
                    cruiserCount += 1
                    if(cruiserCount >= 3): # Load submarine images
                        shipTile = pygame.image.load(r"C:\Users\jchri\Documents\S&T\FALL 21\CS 3100\Project Code\group6-cs3100\cs3100_Group-6 Ships\Submarine\blue\subBlue"+str(i)+r".png")
                        submarine.append(shipTile)
                elif ship == 4: # Load battleship images
                    shipTile = pygame.image.load(r"C:\Users\jchri\Documents\S&T\FALL 21\CS 3100\Project Code\group6-cs3100\cs3100_Group-6 Ships\Battleship\blue\battleshipBlue"+str(i)+r".png")
                    battleship.append(shipTile)
                else: # Load carrier images
                    shipTile = pygame.image.load(r"C:\Users\jchri\Documents\S&T\FALL 21\CS 3100\Project Code\group6-cs3100\cs3100_Group-6 Ships\Carrier\blue\CarrierBlue"+str(i)+r".png")
                    carrier.append(shipTile)
        
        carrierCount = 0
        battleshipCount = 0
        cruiserCount = 0
        submarineCount = 0
        destroyerCount = 0
        # if not all_ships_placed:
        for row in range(10):
            for column in range(10):
                if p1grid[row][column] == 2:
                    currTile = destroyer[destroyerCount]
                    destroyerCount +=1
                elif p1grid[row][column] == 3:
                    currTile = cruiser[cruiserCount]
                    cruiserCount += 1
                    if(cruiserCount > 3):
                        currTile = submarine[submarineCount]
                        submarineCount += 1
                elif p1grid[row][column] == 4:
                    currTile = battleship[battleshipCount]
                    battleshipCount += 1
                elif p1grid[row][column] == 5:
                    currTile = carrier[carrierCount]
                    carrierCount += 1
                else:
                    currTile = oceanTile
                
                screen.blit(currTile, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])
                
                #pygame.draw.rect(screen,
                #                color,
                #                [(MARGIN + WIDTH) * column + MARGIN,
                #                (MARGIN + HEIGHT) * row + MARGIN,
                #                WIDTH,
                #                HEIGHT])


        pygame.display.update()

def create_ai_grid_screen(screen, aigrid):
    for row in range(10):
        # Add an empty array that will hold each cell
        # in this row
        aigrid.append([])
        for column in range(10):
            aigrid[row].append(0)  # Append a cell

    WINDOW_SIZE = [WIDTH*10+MARGIN*10, HEIGHT*10+MARGIN*10]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Used to track current grid location mouse is in
    curr_column = 10
    curr_row = 10

    # Dropping some real quick logic for placing ships
    #   Information on ship being placed
    placeable_ships = [2, 3, 3, 4, 5]
    ship_len = 0
    ship_orientation = [0, 0]
    overlap = False
    while placeable_ships:
        # Select the first ship in the list to place
        ship = placeable_ships[0]
        # Give it a random position and orientation
        col, row = random.randint(0,10-ship-1), random.randint(0,10-ship-1)
        ship_orientation = [1,0] if random.randint(0,1) else [0,1]
        # Check for overlaps
        for square in range(ship):
            if aigrid[row+(square*ship_orientation[0])][col+(square*ship_orientation[1])] == 1:
                overlap = True
        # Place the ship in the aigrid only if no overlap
        if overlap == False:
            for square in range(ship):
                aigrid[row+(square*ship_orientation[0])][col+(square*ship_orientation[1])] = 1
            placeable_ships.remove(ship)
        else:
            overlap = False

    # Print the aigrid in console (For debugging purposes)
    # print(placeable_ships)
    # for i in aigrid:
    #     for j in i:
    #         print(j, end="")
    #     print()


    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION: # Gets current mouse position
                pos = pygame.mouse.get_pos()

                curr_column = pos[0] // (WIDTH + MARGIN)
                curr_row = pos[1] // (HEIGHT + MARGIN)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    print("Acknowledged that player saw AI place ships")
                    return GameState.P1_TURN

        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        # if not all_ships_placed:
        for row in range(10):
            for column in range(10):
                color = WHITE
                if aigrid[row][column] == 1 and debug: # Showing ships in Debug mode
                    if row == curr_row and column == curr_column:
                        color = LIGHT_PINK
                    else:
                        color = PINK
                elif row == curr_row and column == curr_column:
                    color = GRAY
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])


        pygame.display.update()

def p1_turn(screen, aigrid):
    print("Entering p1 turn")
    WINDOW_SIZE = [WIDTH*10+MARGIN*10, HEIGHT*10+MARGIN*10]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Used to track current grid location mouse is in
    curr_column = 10
    curr_row = 10

    # Tracks if the move has been made
    move_made = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not move_made:
                    # User clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // (WIDTH + MARGIN)
                    row = pos[1] // (HEIGHT + MARGIN)

                    if aigrid[row][column] == 1: # If there's a ship, it's a hit
                        aigrid[row][column] = 2
                    elif aigrid[row][column] == 0: # Otherwise it's a miss
                        aigrid[row][column] = -1
                    move_made = True
                else:
                    print("You've made your move! Press 'D' to complete your turn.")
            elif event.type == pygame.MOUSEMOTION: # Gets current mouse position
                pos = pygame.mouse.get_pos()
                curr_column = pos[0] // (WIDTH + MARGIN)
                curr_row = pos[1] // (HEIGHT + MARGIN)
            elif event.type == pygame.KEYDOWN: # The move has been made and turn is over
                if event.key == pygame.K_d and move_made:
                    print("Move made, it's the opponents turn")
                    # Parse through the player's board to see if P1 won
                    win_flag = True
                    for row in aigrid:
                        for col in row:
                            if col == 1: win_flag = False
                    if win_flag:
                        print("You have sunk all of P2/AI's ships! Congratulations!")
                        winner = "P1"
                        return GameState.GAME_OVER
                    else:
                        if choice == 1:
                            time.sleep(1)
                            return GameState.P1_TURN
                        elif choice == 2:
                            time.sleep(2) # A small delay so they can see what they've done
                            return GameState.P2_AI_TURN

        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        # if not all_ships_placed:
        for row in range(10):
            for column in range(10):
                color = WHITE
                if aigrid[row][column] == 1 and debug: # Showing ships in Debug mode
                    if row == curr_row and column == curr_column:
                        color = LIGHT_PINK
                    else:
                        color = PINK
                elif aigrid[row][column] == 2: # Hits in red
                    color = RED
                elif aigrid[row][column] == -1: # misses in blue
                    color = BLUE
                elif row == curr_row and column == curr_column:
                    color = GRAY
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])


        pygame.display.update()

def p2_ai_turn(screen, p1grid):
    print("Entering p2/ai turn")
    WINDOW_SIZE = [WIDTH*10+MARGIN*10, HEIGHT*10+MARGIN*10]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Used to track current grid location mouse is in
    curr_column = 10
    curr_row = 10

    # AI picks a random spot to hit
    while True:
        row_shot, col_shot = random.randint(0,9), random.randint(0,9) # Pick a random spot to hit
        if p1grid[row_shot][col_shot] != 2 or p1grid[row_shot][col_shot] != -1: # If spot hasn't been shot at yet
            if p1grid[row_shot][col_shot] == 1: # If there's a ship, mark as hit
                p1grid[row_shot][col_shot] = 2
                break
            elif p1grid[row_shot][col_shot] == 0: # If there's water, mark as miss
                p1grid[row_shot][col_shot] = -1
                break

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    print("Acknowledged that player saw AI turn")
                    # Parse through the player's board to see if P2/AI won
                    win_flag = True
                    for row in p1grid:
                        for col in row:
                            if col == 1: win_flag = False
                    if win_flag:
                        print("P2/AI has sunk all of your ships, better luck next time!")
                        winner = "P2/AI"
                        return GameState.GAME_OVER
                    else:
                        return GameState.P1_TURN

        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        # if not all_ships_placed:
        for row in range(10):
            for column in range(10):
                color = WHITE
                if p1grid[row][column] == 1: # Showing ships in Debug mode
                    color = GREEN
                elif p1grid[row][column] == 2: # Hits in red
                    color = RED
                elif p1grid[row][column] == -1: # misses in blue
                    color = BLUE
                elif row == curr_row and column == curr_column:
                    color = GRAY
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])


        pygame.display.update()

def game_end_screen(screen):
    # WINDOW_SIZE = [WIDTH*10+MARGIN*10, HEIGHT*10+MARGIN*10]
    # screen = pygame.display.set_mode(WINDOW_SIZE)
    # pygame.font.init()

    # myfont = pygame.font.SysFont('Comic Sans MS', 30)

    # if winner == "P1":
    #     text = myfont.render("Congratulations! P1 has won!", False, (0, 0, 0))
    # elif winner == "P2/AI":
    #     text = myfont.render("Sorry, P2/AI won this time, but try again!", False, (0, 0, 0))
    # elif winner = "Tie":
    #     text = myfont.render("Whoa, a tie! Nobody managed to sink all of their opponent's ships.", False, (0, 0, 0))

    # textRect = text.get_rect()

    # # set the center of the rectangular object.
    # textRect.center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)

    # # infinite loop
    # while True:

    #     # completely fill the surface object
    #     # with white color
    #     screen.fill(BLACK)

    #     # copying the text surface object
    #     # to the display surface object
    #     # at the center coordinate.
    #     screen.blit(text, textRect)

    #     # iterate over the list of Event objects
    #     # that was returned by pygame.event.get() method.
    #     for event in pygame.event.get():

    #         # if event object type is QUIT
    #         # then quitting the pygame
    #         # and program both.
    #         if event.type == pygame.QUIT:

    #             # deactivates the pygame library
    #             pygame.quit()

    #             # quit the program.
    #             quit()

    #         # Draws the surface object to the screen.
    #         pygame.display.update()

    return GameState.TITLE

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
    GAME_OVER = -2
    QUIT = -1
    TITLE = 0
    PLACE_SHIPS = 1
    SETTINGS = 2
    AI_PLACE_SHIPS = 3
    P1_TURN = 4
    P2_AI_TURN = 5

if __name__ == "__main__":
    main()

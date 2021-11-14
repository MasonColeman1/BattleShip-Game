import pygame
# Since we might need these later
from Game import Game
from Player import Player
from Board import Board
from Ship import Ship

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (211, 211, 211)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 70
HEIGHT = 70

# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(10):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(10):
        grid[row].append(0)  # Append a cell

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [WIDTH*10+MARGIN*10, HEIGHT*10+MARGIN*10]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Grid with Clicks")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Used to track current grid location mouse is in
curr_column = 10
curr_row = 10

# Information on ship being placed
placeable_ships = [2, 3, 3, 4, 5]
ship_len = 0
ship_orientation = [0, 0]

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
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
            else: print("ship will be " + str(ship_orientation[0]) + " with length " + str(ship_len))
            for spot in range(ship_len):
                if grid[row + (spot * ship_orientation[0])][column + (spot * ship_orientation[1])] == 0:
                    # Set that location to one
                    grid[row + (spot * ship_orientation[0])][column + (spot * ship_orientation[1])] = 1
                    print("Click ", pos, "Grid coordinates: ", row, column)
                else: # overlap is detected
                    print("Overlap detected, but how do we \'roll back\' the changes??")
                    spot_to_keep = [row+(spot*ship_orientation[0]), column+(spot*ship_orientation[1])]
                    for spot in range(ship_len):
                        grid[row + (spot * ship_orientation[0])][column + (spot * ship_orientation[1])] = 0
                    grid[spot_to_keep[0]][spot_to_keep[1]] = 1
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
    for row in range(10):
        for column in range(10):
            color = WHITE
            if grid[row][column] == 1:
                color = GREEN
            elif row == curr_row and column == curr_column:
                color = GRAY
            pygame.draw.rect(screen,
                            color,
                            [(MARGIN + WIDTH) * column + MARGIN,
                            (MARGIN + HEIGHT) * row + MARGIN,
                            WIDTH,
                            HEIGHT])

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.
pygame.quit()

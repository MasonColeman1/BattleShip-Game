from Player import Player
from Board import Board
from Ship import Ship


TEST = True

Turns = 40          #Number of Turns
reshoot = True      #In case you input an improper coordinate or duplicate coordinate
debug = True        #Variable that controls whether debug information is printed


# Function to create player and have them fill in their board.
def createPlayerWithBoard() :
    player = Player()
    player.fillBoard()

    return player

# Function to shoot a bullet at the (x, y) coordinate of playerShotAt board.
def shoot(playerShotAt, x, y) :
    hit = playerShotAt.board.bulletShot(x, y)
    
    if TEST :
        if hit == 1 :
            print("You shot: (" + str(x+1) + ", " + str(y+1) + ") you hit a ship.")
        else :
            print("You shot: (" + str(x+1) + ", " + str(y+1) + ") you did not hit a ship.")

    return hit

# Function to convert ordered pair needed from command line to array elements.
# Ordered pairs are allowed to range from (A, 1) to (H, 8)
# This should not be needed once point and click is functional in py game.
#def convertShotToElements(shot) :
#   if shot[0] == "(" and shot[2] == "," and shot[3] == " " and shot[5] == ")" and shot[1] >= 'A' and shot[1] <= 'H' and shot[4] >= '1' and shot[4] <= '8' :
#        return ord(shot[1]) - 65, ord(shot[4]) - 49
#    else :
#        return -1, -1


def getRow(): #Function to get user input for row coordinate
    good = False
    row_data = 0
    while(good == False):
        row = input("Set the row (y) coordinate you would like to shoot at. Can be 'A' to 'h' or '1' to '10': ")
        if (len(row) > 1):
            if((ord(row[0])==49) and (ord(row[1])==48)):
                row_data = 9
                good = True
            else:
                good = False
        else:
            if ((ord(row) >= 65) and (ord(row) <= 74)):
                row_data = ord(row) - 65
                good = True
            elif ((ord(row) >= 97) and (ord(row) <= 106)):
                row_data = ord(row) - 97
                good = True
            elif ((ord(row) >= 49) and (ord(row) <= 58)):
                row_data = ord(row) - 49
                good = True
            else:
                good = False

    return row_data

def getCol(): #Function to get user input for column coordinate
    good = False
    col_data = 0
    while(good == False):
        col = input("Set the column (x) coordinate you would like to shoot at. Can be '1' to '10': ")
        if (len(col) > 1):
            if((ord(col[0])==49) and (ord(col[1])==48)):
                col_data = 9
                good = True
            else:
                good = False
        else:
            if ((ord(col) >= 49) and (ord(col) <= 57)):
                col_data = ord(col) - 49
                good = True
            else:
                good = False

    return col_data
    

def main() :
    turn_num = 0        #Number of turns played
    game_over = False   #Used to check if game should end before turn limit
   
    computer = createPlayerWithBoard()

    if (debug == True):
        computer.board.printShipPosits()

    while((turn_num < Turns) and (game_over == False)):
        print("\n")
        print("Turn: ", turn_num + 1, " of ", Turns)
        if ((computer.board.getShipTotal() - computer.board.checkDestroyList()) == 1):
            print("There is", computer.board.getShipTotal() - computer.board.checkDestroyList(), "enemy ship still in the water.")
        else:
            print("There are ", computer.board.getShipTotal() - computer.board.checkDestroyList(), "enemy ships still in the water.")
        print("You have sunk", computer.board.checkDestroyList(), "enemy ships.\n")
        reshoot = True

        computer.board.updateDisplayBoard(debug)
        computer.board.printDisplayBoard()

        while(reshoot == True):
            #shot = input("Enter the cooridinate you would like to shoot at. Ex (B, 4)")
            x = getRow()
            y = getCol()   #Yes x and y are backwards. It makes sense on board
            if x != -1 :
                if (computer.board.checkCoordDouble(x, y) == True):
                    print("You have already shot there. Please try again.")
                    reshoot = True
                else:
                    shoot(computer, x, y);
                    reshoot = False
            else :
               print("You input wrong coordinates. Please try again.")
               reshoot = True

        computer.board.updateShipDestroy()
        if (computer.board.checkDestroyList() == computer.board.getShipTotal()):
            game_over = True
        else:
            turn_num += 1

    print("/n")
    computer.board.updateDisplayBoard(debug)
    computer.board.printDisplayBoard()

    print("/n")
    if (computer.board.checkDestroyList() == computer.board.getShipTotal()):
        print("Congrats! You won! You have sunk all the enemy ships.")
    else:
        print("Sorry! You lose. You failed to sink all the enemy ships.")
        if ((computer.board.getShipTotal() - computer.board.checkDestroyList()) == 1):
            print("There was", computer.board.getShipTotal() - computer.board.checkDestroyList(), "enemy ship still in the water.")
        else:
            print("There were", computer.board.getShipTotal() - computer.board.checkDestroyList(), "enemy ships still in the water.")
            
    print("You sunk", computer.board.checkDestroyList(), "enemy ships in", turn_num, "turns.\n")
    accuracy = computer.board.calcAccuracy()
    print("You had an accuracy of", round((accuracy[3] * 100),2), "% with", accuracy[0], "hits,", accuracy[1], "misses, and", accuracy[2], "total shots.") 
    

if __name__ == "__main__":
    main()

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
def convertShotToElements(shot) :
    if shot[0] == "(" and shot[2] == "," and shot[3] == " " and shot[5] == ")" and shot[1] >= 'A' and shot[1] <= 'H' and shot[4] >= '1' and shot[4] <= '8' :
        return ord(shot[1]) - 65, ord(shot[4]) - 49
    else :
        return -1, -1

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
            shot = input("Enter the cooridinate you would like to shoot at. Ex (B, 4)")
            x, y = convertShotToElements(shot)
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
    print("You had an accuracy of", round(accuracy[3], 2), "with", accuracy[0], "hits,", accuracy[1], "misses, and", accuracy[2], "total shots.") 
    

if __name__ == "__main__":
    main()

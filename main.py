from Player import Player
from Board import Board
from Ship import Ship


TEST = True

Turns = 65          #Number of Turns
reshoot = True      #In case you input an improper coordinate or duplicate coordinate
debug = True        #Variable that controls whether debug information is printed



    #CREATE GAME CLASS????


# Function to shoot a bullet at the (x, y) coordinate of playerShotAt board.
def shoot(attPlayer, playerShotAt, x, y) :
    hit = playerShotAt.board.bulletShot(x, y)
    
    if TEST :
        if hit == 1 :
            print(attPlayer.name, "shot: (" + str(x+1) + ", " + str(y+1) + ").", attPlayer.name, "hit a ship.")
        else :
            print(attPlayer.name, "shot: (" + str(x+1) + ", " + str(y+1) + ").", attPlayer.name, "did not hit a ship.")

    #return hit



#SinglePlayer Function (One AI Board that Player shoots at
def singlePlayerOneBoard():
    turn_num = 0        #Number of turns played
    game_over = False   #Used to check if game should end before turn limit

    Player_1 = Player()
    AI_Player = Player()
    AI_Player.createWithBoard(True)

    if (debug == True):                     #Debug to print list of AI ships at beginning of game
        print("AI Ship List (DEBUG): ")
        AI_Player.board.printShipPosits()

    while((turn_num < Turns) and (game_over == False)): #TURN LOOP

        game_over = turn(Player_1, AI_Player, turn_num) #Turn Function Call
        if (game_over == False):
            turn_num += 1

    print(" ")
    AI_Player.board.updateDisplayBoard(True)  #Print Debug version so player can see AI ships after game
    AI_Player.board.printDisplayBoard()         #If they still exist, otherwise will not change print

    print(" ")
    if (AI_Player.board.checkDestroyList() == AI_Player.board.getShipTotal()):
        print("Congrats! You won! You have sunk all the enemy ships.")
    else:
        print("Sorry! You lose. You failed to sink all the enemy ships.")
        if ((AI_Player.board.getShipTotal() - AI_Player.board.checkDestroyList()) == 1):
            print("There was", AI_Player.board.getShipTotal() - AI_player.board.checkDestroyList(), "enemy ship still in the water.")
        else:
            print("There were", AI_Player.board.getShipTotal() - AI_Player.board.checkDestroyList(), "enemy ships still in the water.")
            
    print("You sunk", AI_Player.board.checkDestroyList(), "enemy ships in", turn_num, "turns.\n")
    accuracy = AI_Player.board.calcAccuracy()
    print("You had an accuracy of", round((accuracy[3] * 100),2), "% with", accuracy[0], "hits,", accuracy[1], "misses, and", accuracy[2], "total shots.") 
    



#SinglePlayer Function (AI and Player Board)
    #WILL CREATE ONCE ABILITY TO PLACE SHIPS IS WORKING
def singlePlayerTwoBoards():
    pass


#Turn Function
def turn(attPlayer, defPlayer, turn_num):
    print("\n")
    print("Turn: ", turn_num + 1, " of ", Turns)
    if (attPlayer.ai_value == False):
        if ((defPlayer.board.getShipTotal() - defPlayer.board.checkDestroyList()) == 1):
            print("There is", defPlayer.board.getShipTotal() - defPlayer.board.checkDestroyList(), "enemy ship still in the water.")
        else:
            print("There are ", defPlayer.board.getShipTotal() - defPlayer.board.checkDestroyList(), "enemy ships still in the water.")
        print("You have sunk", defPlayer.board.checkDestroyList(), "enemy ships.\n")

    reshoot = True

    print(defPlayer.name, "'s Board:")
    defPlayer.board.updateDisplayBoard(debug)
    defPlayer.board.printDisplayBoard()

    while(reshoot == True):
        #shot = input("Enter the cooridinate you would like to shoot at. Ex (B, 4)")
        x = attPlayer.getRow()
        y = attPlayer.getCol()   #Yes x and y are backwards. It makes sense on board
        if x != -1 :
            if (defPlayer.board.checkCoordDouble(x, y) == True):
                print("You have already shot there. Please try again.")
                reshoot = True
            else:
                shoot(attPlayer, defPlayer, x, y);
                reshoot = False
        else :
            print("You input wrong coordinates. Please try again.")
            reshoot = True

    defPlayer.board.updateShipDestroy()
    if (defPlayer.board.checkDestroyList() == defPlayer.board.getShipTotal()):
        return True
    else:
        return False
    
    
    
    

def main() :

    #Main Menu Function?
    
    singlePlayerOneBoard()
    
    

if __name__ == "__main__":
    main()




    #OLD MAIN FUNCTION
#def main() :
#    turn_num = 0        #Number of turns played
#    game_over = False   #Used to check if game should end before turn limit
#
#    Player1 = Player()
#    Player1.createWithBoard(False)
#    computer = Player()
#    computer.createWithBoard(True)
#
#    if (debug == True):
#        computer.board.printShipPosits()
#
#    while((turn_num < Turns) and (game_over == False)):
#        print("\n")
#        print("Turn: ", turn_num + 1, " of ", Turns)
#        if ((computer.board.getShipTotal() - computer.board.checkDestroyList()) == 1):
#            print("There is", computer.board.getShipTotal() - computer.board.checkDestroyList(), "enemy ship still in the water.")
#        else:
#            print("There are ", computer.board.getShipTotal() - computer.board.checkDestroyList(), "enemy ships still in the water.")
#        print("You have sunk", computer.board.checkDestroyList(), "enemy ships.\n")
#        reshoot = True
#
#        computer.board.updateDisplayBoard(debug)
#        computer.board.printDisplayBoard()
#
#        while(reshoot == True):
#            #shot = input("Enter the cooridinate you would like to shoot at. Ex (B, 4)")
#            x = computer.getRow()
#            y = computer.getCol()   #Yes x and y are backwards. It makes sense on board
#            if x != -1 :
#                if (computer.board.checkCoordDouble(x, y) == True):
#                    print("You have already shot there. Please try again.")
#                    reshoot = True
#                else:
#                    shoot(computer, x, y);
#                    reshoot = False
#            else :
#               print("You input wrong coordinates. Please try again.")
#               reshoot = True
#
#        computer.board.updateShipDestroy()
#        if (computer.board.checkDestroyList() == computer.board.getShipTotal()):
#            game_over = True
#        else:
#            turn_num += 1
#
#    print("/n")
#    computer.board.updateDisplayBoard(debug)
#    computer.board.printDisplayBoard()
#
#    print("/n")
#    if (computer.board.checkDestroyList() == computer.board.getShipTotal()):
#        print("Congrats! You won! You have sunk all the enemy ships.")
#    else:
#        print("Sorry! You lose. You failed to sink all the enemy ships.")
#        if ((computer.board.getShipTotal() - computer.board.checkDestroyList()) == 1):
#            print("There was", computer.board.getShipTotal() - computer.board.checkDestroyList(), "enemy ship still in the water.")
#        else:
#            print("There were", computer.board.getShipTotal() - computer.board.checkDestroyList(), "enemy ships still in the water.")
#            
#    print("You sunk", computer.board.checkDestroyList(), "enemy ships in", turn_num, "turns.\n")
#    accuracy = computer.board.calcAccuracy()
#    print("You had an accuracy of", round((accuracy[3] * 100),2), "% with", accuracy[0], "hits,", accuracy[1], "misses, and", accuracy[2], "total shots.") 
    

    

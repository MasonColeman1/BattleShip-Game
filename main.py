from Game import Game
from Player import Player
from Board import Board
from Ship import Ship


TEST = True

def main() :

    game = Game()
    
    quit_game = False
    reinput = False

    #Main Menu

    while (quit_game == False):
        print("Welcome to Battleship!")
        while(reinput == False):
            print("Please Select an Option (1-5 or A-E or a-e): ")
            print("1. Singleplayer (1 Board)")
            print("2. Singleplayer (2 Boards)  NOT IMPLEMENTED YET")
            print("3. Multiplayer              NOT IMPLEMENTED YET")
            print("4. Options                  NOT IMPLEMENTED YET")
            print("5. Quit Game")
            print(" ")

            choice = input("Select an Option: ")
            print(" ")

            if (len(choice) > 1):
                reinput == True
            elif ((choice == "1") or (choice == "A") or (choice == "a")):
                game.singlePlayerOneBoard()
                reinput == False
            elif ((choice == "2") or (choice == "B") or (choice == "b")):
                #CALL SINGLEPLAYERTWOBOARD
                reinput == True
            elif ((choice == "3") or (choice == "C") or (choice == "c")):
                #CALL MULTIPLAYER
                reinput == True
            elif ((choice == "4") or (choice == "D") or (choice == "d")):
                game.options()
                reinput == True
            elif ((choice == "5") or (choice == "E") or (choice == "e")):
                quit_game == True
                reinput == False
            else:
                reinput == True

            
    
    

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
    

    

from Player import Player
from Board import Board

#GAME CLASS

class Game:
    debug = True        #Variable that controls whether debug information is printed
    difficulty = 1      #Variable to change game difficulty  ## 0 - Easy,  1 - Normal, 2 - Hard, 3 - Impossible



    # Function to shoot a bullet at the (x, y) coordinate of playerShotAt board.
    def shoot(self, attPlayer, defPlayer, x, y) :
        hit = defPlayer.board.bulletShot(x, y)
        
        if hit == 1 :
            print(" ")
            print(attPlayer.name, "shot: (" + str(x+1) + ", " + str(y+1) + ").", attPlayer.name, "hit a ship.")
        else :
            print(" ")
            print(attPlayer.name, "shot: (" + str(x+1) + ", " + str(y+1) + ").", attPlayer.name, "did not hit a ship.")

        #return hit



    #Turn Function
    def turn(self, attPlayer, defPlayer, turn_num, max_turn):
        print("\n")
        print("Turn: ", turn_num + 1, " of ", max_turn)
        if (attPlayer.ai_value == False):
            if ((defPlayer.board.getShipTotal() - defPlayer.board.checkDestroyList()) == 1):
                print("There is", defPlayer.board.getShipTotal() - defPlayer.board.checkDestroyList(), "enemy ship still in the water.")
            else:
                print("There are ", defPlayer.board.getShipTotal() - defPlayer.board.checkDestroyList(), "enemy ships still in the water.")
            print("You have sunk", defPlayer.board.checkDestroyList(), "enemy ships.\n")

        reshoot = True

        print(defPlayer.name, "'s Board:")
        defPlayer.board.updateDisplayBoard(self.debug)
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
                    self.shoot(attPlayer, defPlayer, x, y);
                    reshoot = False
            else :
                print("You input wrong coordinates. Please try again.")
                reshoot = True

        defPlayer.board.updateShipDestroy()
        if (defPlayer.board.checkDestroyList() == defPlayer.board.getShipTotal()):
            return True
        else:
            return False



    #SinglePlayer Function (One AI Board that Player shoots at
    def singlePlayerOneBoard(self):
        turn_num = 0        #Number of turns played
        game_over = False   #Used to check if game should end before turn limit
        turn_max = 65

        if (self.difficulty == 0):
            turn_max = 80
        elif (self.difficulty == 1):
            turn_max = 65
        elif (self.difficulty == 2):
            turn_max = 50
        elif (self.difficulty == 3):
            turn_max = 35
        else: #THIS CASE SHOULD NEVER HAPPEN
            turn_max = 65


        Player_1 = Player()
        Player_1.createWithBoard(False)
        AI_Player = Player()
        AI_Player.createWithBoard(True)

        if (self.debug == True):                     #Debug to print list of AI ships at beginning of game
            print("AI Ship List (DEBUG): ")
            AI_Player.board.printShipPosits()

        while((turn_num < turn_max) and (game_over == False)): #TURN LOOP

            game_over = self.turn(Player_1, AI_Player, turn_num, turn_max) #Turn Function Call
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
                
        print("You sunk", AI_Player.board.checkDestroyList(), "enemy ships in", turn_num+1, "turns.\n")
        accuracy = AI_Player.board.calcAccuracy()
        print("You had an accuracy of", round((accuracy[3] * 100),2), "% with", accuracy[0], "hits,", accuracy[1], "misses, and", accuracy[2], "total shots.") 
        print(" ")
        print(" ")
        


    #SinglePlayer Function (AI and Player Board)
        #WILL CREATE ONCE ABILITY TO PLACE SHIPS IS WORKING
    def singlePlayerTwoBoards(self):
        pass



    #Options Function - Change Game Function
    def options(self):
        quit_opt = False

        while (quit_opt == False):
            print("-- Options Menu --")
            print("Debug is: ", self.debug)
            print("Difficulty is: ", self.difficulty)
            print("Please Select an Option (1-3 or A-C or a-c): ")
            print("1. Toggle Debug")
            print("2. Toggle Difficulty")
            print("3. Return to Menu")
            print(" ")

            choice_opt = input("Select an Option: ")
            print(" ")

            if (len(choice_opt) > 1):
                quit_opt = False
            elif ((choice_opt == "1") or (choice_opt == "A") or (choice_opt == "a")):
                if (self.debug == True):
                    self.debug = False
                else:
                    self.debug == True
            elif ((choice_opt == "2") or (choice_opt == "B") or (choice_opt == "b")):
                if (self.difficulty < 3):
                    self.difficulty += 1
                else:
                    self.difficulty = 0
            elif ((choice_opt == "3") or (choice_opt == "C") or (choice_opt == "c")):
                quit_opt = True





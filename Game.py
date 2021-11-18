from Player import Player
from Board import Board
import random

#GAME CLASS

class Game:
    def __init__(self):
        self.debug = True        #Variable that controls whether debug information is printed
        self.difficulty = 1      #Variable to change game difficulty  ## 0 - Easy,  1 - Normal, 2 - Hard, 3 - Impossible



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
    def turn(self, attPlayer, defPlayer, out_value):
        if (attPlayer.ai_value == False):
            if (out_value == True):
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
                        self.shoot(attPlayer, defPlayer, x, y)
                        reshoot = False
                else :
                    print("You input wrong coordinates. Please try again.")
                    reshoot = True

        else:
            if (attPlayer.last_posit != []):
                print("Last Posit: ",attPlayer.last_posit[0],",",attPlayer.last_posit[1])
                print("Last Ori: ",attPlayer.last_ori)
            reshoot = True
            cancel_counter = 0
            new_posit = []
            if(self.difficulty == 0):       #Easy
                while(reshoot == True):
                    x = random.randint(0,9)
                    y = random.randint(0,9)
                    if (defPlayer.board.checkCoordDouble(x, y) == True):
                        reshoot = True
                    else:
                        self.shoot(attPlayer, defPlayer, x, y)
                        reshoot = False
            elif(self.difficulty == 1):     #Medium
                while(reshoot == True):
                    if (attPlayer.last_hit == True):
                        new_posit = []
                        if (attPlayer.last_ori == "None"):
                            r = random.randint(0,1)
                            if (r == 0):
                                attPlayer.last_ori = "Horizontal"
                            else:
                                attPlayer.last_ori = "Vertical"
                        print("Last Ori 2: ", attPlayer.last_ori)
                        if(attPlayer.last_ori == "Vertical"):
                            if((attPlayer.last_posit[0] > 0) and (attPlayer.last_posit[0]<9)):
                                s = random.randint(0,1)
                                if (s == 0):
                                    new_posit = [attPlayer.last_posit[0]-1, attPlayer.last_posit[1]]
                                else:
                                    new_posit = [attPlayer.last_posit[0]+1, attPlayer.last_posit[1]]
                            elif (attPlayer.last_posit[0] == 0):
                                new_posit = [attPlayer.last_posit[0]+1, attPlayer.last_posit[1]]
                            else:
                                new_posit = [attPlayer.last_posit[0]-1, attPlayer.last_posit[1]]
                        else:
                            if((attPlayer.last_posit[1] > 0) and (attPlayer.last_posit[1]<9)):
                                s = random.randint(0,1)
                                if (s == 0):
                                    new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]-1]
                                else:
                                    new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]+1]
                            elif (attPlayer.last_posit[1] == 0):
                                new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]+1]
                            else:
                                new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]-1]
                        if((defPlayer.board.board[new_posit[0]][new_posit[1]] == 2) or (defPlayer.board.board[new_posit[0]][new_posit[1]] == 3)):
                            if (cancel_counter == 2):
                                attPlayer.last_posit = []
                                attPlayer.last_hit = False
                                attPlayer.last_ori = "None"
                                cancel_counter = 0
                            else:
                                attPlayer.last_ori = "None"
                                cancel_counter += 1
                            reshoot = True
                        elif (defPlayer.board.board[new_posit[0]][new_posit[1]] == 1):
                            self.shoot(attPlayer, defPlayer, new_posit[0], new_posit[1])
                            attPlayer.last_posit[0] = new_posit[0]
                            attPlayer.last_posit[1] = new_posit[1]
                            attPlayer.last_hit = True
                            reshoot = False
                        else:
                            self.shoot(attPlayer, defPlayer, new_posit[0], new_posit[1])
                            attPlayer.last_ori = "None"
                            reshoot = False     

                    else: 
                        x = random.randint(0,9)
                        y = random.randint(0,9)
                        r = random.randint(0,4)
                        if (defPlayer.board.checkCoordDouble(x, y) == True):
                            reshoot = True
                        elif (defPlayer.board.board[x][y] != 1):
                            if (r <= 2):
                                reshoot = True
                            else:
                                self.shoot(attPlayer, defPlayer, x, y)
                                attPlayer.last_posit = [x,y]
                                attPlayer.last_hit = True
                                reshoot = False
                        else:
                            self.shoot(attPlayer, defPlayer, x, y)
                            attPlayer.last_posit = [x,y]
                            attPlayer.last_hit = True
                            reshoot = False

            elif(self.difficulty == 2):     #Hard
                while(reshoot == True):
                    if (attPlayer.last_hit == True):
                        new_posit = []
                        if (attPlayer.last_ori == "None"):
                            r = random.randint(0,1)
                            if (r == 0):
                                attPlayer.last_ori = "Horizontal"
                            else:
                                attPlayer.last_ori = "Vertical"
                        print("Last Ori 2: ", attPlayer.last_ori)
                        if(attPlayer.last_ori == "Vertical"):
                            if((attPlayer.last_posit[0] > 0) and (attPlayer.last_posit[0]<9)):
                                s = random.randint(0,1)
                                if (s == 0):
                                    new_posit = [attPlayer.last_posit[0]-1, attPlayer.last_posit[1]]
                                else:
                                    new_posit = [attPlayer.last_posit[0]+1, attPlayer.last_posit[1]]
                            elif (attPlayer.last_posit[0] == 0):
                                new_posit = [attPlayer.last_posit[0]+1, attPlayer.last_posit[1]]
                            else:
                                new_posit = [attPlayer.last_posit[0]-1, attPlayer.last_posit[1]]
                        else:
                            if((attPlayer.last_posit[1] > 0) and (attPlayer.last_posit[1]<9)):
                                s = random.randint(0,1)
                                if (s == 0):
                                    new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]-1]
                                else:
                                    new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]+1]
                            elif (attPlayer.last_posit[1] == 0):
                                new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]+1]
                            else:
                                new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]-1]
                        if((defPlayer.board.board[new_posit[0]][new_posit[1]] == 2) or (defPlayer.board.board[new_posit[0]][new_posit[1]] == 3)):
                            if (cancel_counter == 2):
                                attPlayer.last_posit = []
                                attPlayer.last_hit = False
                                attPlayer.last_ori = "None"
                                cancel_counter = 0
                            else:
                                attPlayer.last_ori = "None"
                                cancel_counter += 1
                            reshoot = True
                        elif (defPlayer.board.board[new_posit[0]][new_posit[1]] == 1):
                            self.shoot(attPlayer, defPlayer, new_posit[0], new_posit[1])
                            attPlayer.last_posit[0] = new_posit[0]
                            attPlayer.last_posit[1] = new_posit[1]
                            attPlayer.last_hit = True
                            reshoot = False
                        else:
                            self.shoot(attPlayer, defPlayer, new_posit[0], new_posit[1])
                            attPlayer.last_ori = "None"
                            reshoot = False     

                    else: 
                        x = random.randint(0,9)
                        y = random.randint(0,9)
                        r = random.randint(0,4)
                        if (defPlayer.board.checkCoordDouble(x, y) == True):
                            reshoot = True
                        elif (defPlayer.board.board[x][y] != 1):
                            if (r <= 1):
                                reshoot = True
                            else:
                                self.shoot(attPlayer, defPlayer, x, y)
                                attPlayer.last_posit = [x,y]
                                attPlayer.last_hit = True
                                reshoot = False
                        else:
                            self.shoot(attPlayer, defPlayer, x, y)
                            attPlayer.last_posit = [x,y]
                            attPlayer.last_hit = True
                            reshoot = False

            else:                           #Impossible
                while(reshoot == True):
                    if (attPlayer.last_hit == True):
                        new_posit = []
                        if (attPlayer.last_ori == "None"):
                            r = random.randint(0,1)
                            if (r == 0):
                                attPlayer.last_ori = "Horizontal"
                            else:
                                attPlayer.last_ori = "Vertical"
                        print("Last Ori 2: ", attPlayer.last_ori)
                        if(attPlayer.last_ori == "Vertical"):
                            if((attPlayer.last_posit[0] > 0) and (attPlayer.last_posit[0]<9)):
                                s = random.randint(0,1)
                                if (s == 0):
                                    new_posit = [attPlayer.last_posit[0]-1, attPlayer.last_posit[1]]
                                else:
                                    new_posit = [attPlayer.last_posit[0]+1, attPlayer.last_posit[1]]
                            elif (attPlayer.last_posit[0] == 0):
                                new_posit = [attPlayer.last_posit[0]+1, attPlayer.last_posit[1]]
                            else:
                                new_posit = [attPlayer.last_posit[0]-1, attPlayer.last_posit[1]]
                        else:
                            if((attPlayer.last_posit[1] > 0) and (attPlayer.last_posit[1]<9)):
                                s = random.randint(0,1)
                                if (s == 0):
                                    new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]-1]
                                else:
                                    new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]+1]
                            elif (attPlayer.last_posit[1] == 0):
                                new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]+1]
                            else:
                                new_posit = [attPlayer.last_posit[0], attPlayer.last_posit[1]-1]
                        if((defPlayer.board.board[new_posit[0]][new_posit[1]] == 2) or (defPlayer.board.board[new_posit[0]][new_posit[1]] == 3)):
                            if (cancel_counter == 2):
                                attPlayer.last_posit = []
                                attPlayer.last_hit = False
                                attPlayer.last_ori = "None"
                                cancel_counter = 0
                            else:
                                attPlayer.last_ori = "None"
                                cancel_counter += 1
                            reshoot = True
                        elif (defPlayer.board.board[new_posit[0]][new_posit[1]] == 1):
                            self.shoot(attPlayer, defPlayer, new_posit[0], new_posit[1])
                            attPlayer.last_posit[0] = new_posit[0]
                            attPlayer.last_posit[1] = new_posit[1]
                            attPlayer.last_hit = True
                            reshoot = False
                        else:
                            self.shoot(attPlayer, defPlayer, new_posit[0], new_posit[1])
                            attPlayer.last_ori = "None"
                            reshoot = False     

                    else: 
                        x = random.randint(0,9)
                        y = random.randint(0,9)
                        if (defPlayer.board.checkCoordDouble(x, y) == True):
                            reshoot = True
                        elif (defPlayer.board.board[x][y] != 1):
                            reshoot = True
                        else:
                            self.shoot(attPlayer, defPlayer, x, y)
                            attPlayer.last_posit = [x,y]
                            attPlayer.last_hit = True
                            reshoot = False
                     
                
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
        #Player_1.createWithBoard(False)
        AI_Player = Player()
        AI_Player.createWithBoard(True)

        if (self.debug == True):                     #Debug to print list of AI ships at beginning of game
            print("AI Ship List (DEBUG): ")
            AI_Player.board.printShipPosits()

        while((turn_num < turn_max) and (game_over == False)): #TURN LOOP

            print("\n")
            print("Turn: ", turn_num + 1, " of ", turn_max)

            game_over = self.turn(Player_1, AI_Player, True) #Turn Function Call
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
                print("There was", AI_Player.board.getShipTotal() - AI_Player.board.checkDestroyList(), "enemy ship still in the water.")
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
        turn_num = 0
        game_over = False   #Used to check if game should end with player win
        game_over_com = False   #Used to check if game should end with AI win

        #Create Players
        player1 = Player()
        player1.createWithBoard(False)
        AI_Player = Player()
        AI_Player.createWithBoard(True)

        if (self.debug == True):                     #Debug to print list of AI ships at beginning of game
            print("Player Ship List (DEBUG): ")
            player1.board.printShipPosits()
            print("AI Ship List (DEBUG): ")
            AI_Player.board.printShipPosits()

        game_over_p1y = False   #Used to check if game should end with player win
        game_over_com = False   #Used to check if game should end with AI win

        while((game_over == False) and (game_over_com == False)): #TURN LOOP

            print("\n")
            print("Turn: ", turn_num + 1)

            #Print Player1 Board
            print("\n")
            print("Your Board: ")
            player1.board.updateDisplayBoard(self.debug)
            player1.board.printDisplayBoard()
            if ((player1.board.getShipTotal() - player1.board.checkDestroyList()) == 1):
                print("There is", player1.board.getShipTotal() - player1.board.checkDestroyList(), "friendly ship still in the water.")
            else:
                print("There are ", player1.board.getShipTotal() - player1.board.checkDestroyList(), "friendly ships still in the water.")
            print(player1.board.checkDestroyList(), "friendly ships have been sunk.\n")

            #Print AI Board
            print("\n")
            print("AI Board: ")
            AI_Player.board.updateDisplayBoard(self.debug)
            AI_Player.board.printDisplayBoard()
            if ((AI_Player.board.getShipTotal() - AI_Player.board.checkDestroyList()) == 1):
                print("There is", AI_Player.board.getShipTotal() - AI_Player.board.checkDestroyList(), "enemy ship still in the water.")
            else:
                print("There are ", AI_Player.board.getShipTotal() - AI_Player.board.checkDestroyList(), "enemy ships still in the water.")
            print("You have sunk", AI_Player.board.checkDestroyList(), "enemy ships.\n")
            

            game_over_ply = self.turn(player1, AI_Player, False) #Turn Function Call
            if (game_over_ply == False):
                game_over_com = self.turn(AI_Player, player1, False)

            if ((game_over_ply == False) and (game_over_com == False)):
                turn_num += 1

        print(" ")
        if (AI_Player.board.checkDestroyList() == AI_Player.board.getShipTotal()):
            print("Congrats! You won! You have sunk all the enemy ships.")
        else:
            print("Sorry! You lose. You failed to sink all the enemy ships.")
            if ((AI_Player.board.getShipTotal() - AI_Player.board.checkDestroyList()) == 1):
                print("There was", AI_Player.board.getShipTotal() - AI_Player.board.checkDestroyList(), "enemy ship still in the water.")
            else:
                print("There were", AI_Player.board.getShipTotal() - AI_Player.board.checkDestroyList(), "enemy ships still in the water.")
        print(" ")
        print(" ")



    #Two player game
    def twoPlayer(self):
        turn_num = 0
        game_over_p1 = False   #Used to check if game should end with player1 win
        game_over_p2 = False   #Used to check if game should end with player2 win

        #Create Players
        print("Player 1 place ships:")
        player1 = Player()
        player1.createWithBoardAndName("Player 1")
        print("Player 2 place ships:")
        player2 = Player()
        player2.createWithBoardAndName("Player 2")

        while((game_over_p1 == False) and (game_over_p2 == False)): #TURN LOOP

            print("\n")
            print("Turn: ", turn_num + 1)

            temp = input("Press enter when player 1 is ready for turn.")

            #Print Player1 Board
            print("\n")
            print("Player 1: ")
            player1.board.updateDisplayBoard(self.debug)
            player1.board.printDisplayBoard()
            if ((player1.board.getShipTotal() - player1.board.checkDestroyList()) == 1):
                print("There is", player1.board.getShipTotal() - player1.board.checkDestroyList(), "friendly ship still in the water.")
            else:
                print("There are ", player1.board.getShipTotal() - player1.board.checkDestroyList(), "friendly ships still in the water.")
            print(player1.board.checkDestroyList(), "friendly ships have been sunk.\n")

            game_over_p1 = self.turn(player1, player2, False) #Turn Function Call

            temp = input("Press enter when player 2 is ready for turn.")

            #Print Player2 Board
            print("\n")
            print("Player 2: ")
            player2.board.updateDisplayBoard(self.debug)
            player2.board.printDisplayBoard()
            if ((player2.board.getShipTotal() - player2.board.checkDestroyList()) == 1):
                print("There is", player2.board.getShipTotal() - player2.board.checkDestroyList(), "friendly ship still in the water.")
            else:
                print("There are ", player2.board.getShipTotal() - player2.board.checkDestroyList(), "friendly ships still in the water.")
            print(player2.board.checkDestroyList(), "friendly ships have been sunk.\n")
            

            if (game_over_p1 == False):
                game_over_p2 = self.turn(player2, player1, False)

            if ((game_over_p1 == False) and (game_over_p2 == False)):
                turn_num += 1

        print(" ")
        if (player2.board.checkDestroyList() == player2.board.getShipTotal()):
            print("Player 1 won the game.")
        else:
            print("Player 2 won the game.")



    #Options Function - Change Game Function
    def options(self):
        quit_opt = False

        while (quit_opt == False):
            print("-- Options Menu --")
            print("Debug is: ", self.debug)
            print("Difficulty is: ", self.difficulty)
            print("   0 - Easy, 1 - Normal, 2 - Hard, 3 - Impossible")
            print(" ")
            print("Please Select an Option (1-3): ")
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





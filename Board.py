from Ship import Ship
import random

# I made this a class because evantually I am assuming we will want somthing other
# than integers. Maybe something like ship.
class Board :

    ship_num = 4
    max_ship_size = 5
    min_ship_size = 2

    ship_list = []
    posit_list = []
    
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    display_board = [[" O", " O", " O", " O", " O", " O", " O", " O", " O", " O"],
                     [" O", " O", " O", " O", " O", " O", " O", " O", " O", " O"],
                     [" O", " O", " O", " O", " O", " O", " O", " O", " O", " O"],
                     [" O", " O", " O", " O", " O", " O", " O", " O", " O", " O"],
                     [" O", " O", " O", " O", " O", " O", " O", " O", " O", " O"],
                     [" O", " O", " O", " O", " O", " O", " O", " O", " O", " O"],
                     [" O", " O", " O", " O", " O", " O", " O", " O", " O", " O"],
                     [" O", " O", " O", " O", " O", " O", " O", " O", " O", " O"],
                     [" O", " O", " O", " O", " O", " O", " O", " O", " O", " O"],
                     [" O", " O", " O", " O", " O", " O", " O", " O", " O", " O"]]

    def bulletShot(self, x, y) :
        self.posit_list.append([x,y])
        if self.board[x][y] == 1:
            self.board[x][y] = 2
            return 1
        else :
            self.board[x][y] = 3
            return 0


    def checkCoordDouble(self, x, y):  #Check if the player has already shot a location
            for p in self.posit_list:
                if ((x == p[0]) and (y == p[1])):
                    return True

            return False


    def randomPlaceShips(self):  #Randomly place ships
        temp = Ship(0, 2, "Vertical", [], False)
        for w in range(self.ship_num):
            
            temp.clear()
            temp.id = w+1
            
            #Ship Sizing
            if w >= 3:
                temp.size = 2
            elif w == 2:
                temp.size = 3
            elif w == 1:
                temp.size = 4
            elif w == 0:
                temp.size = 5

            #Ship Orientation

            rand_ori = random.randint(0,1)
            if (rand_ori == 0):
                temp.orientation = "Vertical"
            else:
                temp.orientation = "Horizontal"

            #Select Random Anchor Position
            check = True
            redo = False
            while((check) or (redo)):
                temp.positions = [] #Reset temp positions in case of redo or recheck
                
                rand_row = random.randint(0,9)
                rand_col = random.randint(0,9)

                #Add Positions
                if (temp.orientation == "Vertical"): #Vertical Ships
                    if (rand_row > 4):
                        for v in range(temp.size):
                            temp.positions.append([rand_row - v, rand_col])
                            if v < 0:
                                redo = True  #Check to see if posit is out of bounds
                            else:
                                redo = False
                    else:
                        for v in range(temp.size):
                            temp.positions.append([rand_row + v, rand_col])
                            if v > 9:
                                redo = True
                            else:
                                redo = False
                else: #Horizontal Ships
                    if (rand_col > 4):
                        for v in range(temp.size):
                            temp.positions.append([rand_row, rand_col - v])
                            if v < 0:
                                redo = True
                            else:
                                redo = False
                    else:
                        for v in range(temp.size):
                            temp.positions.append([rand_row, rand_col + v])
                            if v > 9:
                                redo = True
                            else:
                                redo = False

                #Check Positions
                check_temp = False
                for s in self.ship_list:
                    if (temp.checkPositOverride(s.positions)):
                        check_temp = True

                if (check_temp == True):
                    check = True
                else:
                    check = False

            #Add to shiplist     
            self.ship_list.append(Ship(temp.id, temp.size, temp.orientation, temp.positions, temp.destroyed))

        #Adding Ship Positions to board
        for s in self.ship_list:
            for p in s.positions:
                self.board[p[0]][p[1]] = 1



    def getShipTotal(self): #Returns total number of ships destroyed or not
        return self.ship_num

    def updateDisplayBoard(self, debug): #Updates the display version of the board
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if ((self.board[r][c] == 1) and (debug == True)):
                    self.display_board[r][c] = " S"
                elif self.board[r][c] == 2:
                    self.display_board[r][c] = " H"
                elif self.board[r][c] == 3:
                    self.display_board[r][c] = " M"

    def printDisplayBoard(self): #Prints the display version of the board
        letter_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        print("  1 2 3 4 5 6 7 8 9 10")
        for r in range(len(self.display_board)):
            print(letter_list[r], end="")
            for c in range(len(self.display_board)):
                if c != 9:
                    print(self.display_board[r][c], end="")
                else:
                    print(self.display_board[r][c], end='\n')


    def updateShipDestroy(self): #Checks whether ships are destroyed
        for s in self.ship_list:
            s.checkDestroy(self.posit_list)
            

    def checkDestroyList(self): #Checks to see how many ships are destroyed
        result = 0
        for s in self.ship_list:
            if (s.getDestroy() == True):
                result += 1

        return result


    def printShipPosits(self): #Debug Function to coordinates of ships in list.
        for s in self.ship_list:
            print("Ship ",s.id,":")
            print("Size: ",s.size)
            s.printPosit()


    def calcAccuracy(self): #Used to calculate player accuracy at the end of the game.
        hits = 0
        misses = 0
        total = 0
        temp_hit = False
        result = 0

        for p in self.posit_list:
            temp_hit = False
            for s in self.ship_list:
                for t in s.positions:
                    if (p == t):
                        temp_hit = True
            if (temp_hit == True):
                hits += 1
            else:
                misses += 1
            total += 1
        result = hits/total

        return [hits, misses, total, result]
        
            
        
            

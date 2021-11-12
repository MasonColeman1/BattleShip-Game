from Board import Board

# I made this a class because I assume at some point we will want other attributes
# such as name or shots fired.
class Player:
    def __init__(self) :
        self.board = Board()
        self.name = ""
        self.ai_value = False

    def __init__(self) -> None: # Default constructor
        self.board = Board()
        self.name = ""
        self.ai_value = False


    def fillBoardAI(self): # This will need to be updated to not be hard coded.
        self.board.randomPlaceShips()

    def fillBoardPlayer(self, custom):
        self.board.placeShips(custom)

    # Function to create player and have them fill in their board.
    def createWithBoard(self, value) :
        if (value == True):  #Create AI Player
            self.name = "AI"
            self.ai_value = True
            self.fillBoardAI()
        else:
            self.name = "Player 1"
            self.ai_value = False
            #Function call to have player create board
            self.fillBoardPlayer(False)


    #       OLD FUNCTION TO CREATE PLAYER W/ BOARD
    # Function to create player and have them fill in their board.
    #def createAIWithBoard() :
    #   player = Player()
    #    player.fillBoardAI()
    #
    #   return player


        #OLD PLAYER INPUT FUNCTION - MAY BE USEFUL FOR PYGAME
        # Function to convert ordered pair needed from command line to array elements.
    # Ordered pairs are allowed to range from (A, 1) to (H, 8)
    # This should not be needed once point and click is functional in py game.
    #def convertShotToElements(shot) :
    #   if shot[0] == "(" and shot[2] == "," and shot[3] == " " and shot[5] == ")" and shot[1] >= 'A' and shot[1] <= 'H' and shot[4] >= '1' and shot[4] <= '8' :
    #        return ord(shot[1]) - 65, ord(shot[4]) - 49
    #    else :
    #        return -1, -1



    def getRow(self): #Function to get user input for row coordinate
        good = False
        row_data = 0
        while(good == False):
            row = input("Set the row (y) coordinate you would like to shoot at. Can be 'A' to 'J', 'a' to 'j': ")
            if (len(row) > 1):
                if((ord(row[0])==49) and (ord(row[1])==48)):
                    row_data = 9
                    good = True
                else:
                    good = False
            elif (len(row) == 0):
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


    def getCol(self): #Function to get user input for column coordinate
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
            elif (len(col) == 0):
                good = False
            else:
                if ((ord(col) >= 49) and (ord(col) <= 57)):
                    col_data = ord(col) - 49
                    good = True
                else:
                    good = False

        return col_data

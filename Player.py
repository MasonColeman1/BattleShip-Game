from Board import Board

# I made this a class because I assume at some point we will want other attributes
# such as name or shots fired.
class Player:
    board = Board()

    def fillBoard(self): # This will need to be updated to not be hard coded.
        self.board.randomPlaceShips()

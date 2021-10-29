from Board import Board

# I made this a class because I assume at some point we will want other attributes
# such as name or shots fired.
class Player:
    board = Board()

    def fillBoard(self): # This will need to be updated to not be hard coded.
        self.board.board[0][0] = 1
        self.board.board[7][7] = 1
        self.board.board[3][7] = 1
        self.board.board[6][2] = 1
        self.board.board[5][1] = 1
        self.board.board[7][5] = 1
        self.board.board[3][6] = 1

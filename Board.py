# I made this a class because evantually I am assuming we will want somthing other
# than integers. Maybe something like ship.
class Board :
    board = [[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]]

    def bulletShot(self, x, y) :
        if self.board[x][y] == 1 :
            self.board[x][y] = 2
            return 1
        else :
            return 0

from Player import Player
from Board import Board

TEST = True


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
            print("You shot: (" + str(x) + ", " + str(y) + ") you hit a ship.")
        else :
            print("You shot: (" + str(x) + ", " + str(y) + ") you did not hit a ship.")

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
    computer = createPlayerWithBoard()

    while 1 :
        shot = input("Enter the cooridinate you would like to shoot at. Ex (B, 4)")
        x, y = convertShotToElements(shot)
        if x != -1 :
            shoot(computer, x, y);
        else :
            print("You input wrong coordinates. Try again.")

if __name__ == "__main__":
    main()



class Ship:
    ship_id = 0                 #Debug Var
    size = 2                    #Ship Size
    orientation = "Vertical"    #Ship Orientation
    positions = []              #List of Ship Positions
    destroyed = False           #Whether Ship is destroyed


    def __init__(self, s_id, size, ori, posit, destro):  #Constructor
        self.id = s_id
        self.size = size
        self.orientation = ori
        self.positions = posit
        self.destroyed = destro

    def clear(self):    #Function used to clear a ship to default state
        self.id = 0
        self.size = 2
        self.orientation = "Vertical"
        self.positions = []
        self.destroyed = False
    
    def getDestroy(self):   #Used to return whether a ship is destroyed
        return self.destroyed

    def checkDestroy(self, posit_list):  #Used to update whether ship is destroyed
        result = 0
        for p in posit_list:
            for q in self.positions:
                if(p==q):
                    result += 1

        if (result >= self.size):
            self.destroyed = True


        #Called during ship placement to ensure ships are not placed over each other
    def checkPositOverride(self, posit_list):
        for p in posit_list:
            for q in self.positions:
                if(p==q):
                    return True
        return False

    def printPosit(self):   #Called when board debug prints locations of ships
        for p in range(len(self.positions)):
            print("[",self.positions[p][0]+1,",",self.positions[p][1]+1,"]", end="")
            print()
            

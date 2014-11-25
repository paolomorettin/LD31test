

class Stage :
    def __init__(self,stagemap) :
        pass

            


    
class Bot :
    def __init__(self,program,position=None,orientation=None,FOV=2) :
        self.program = program
        self.position = position
        self.orientation = orientation
        self.FOV = FOV
        self.operative = True
        

    def move(self) :
        if self.orientation == 180 :
            self.position[0] -= 1
        elif self.orientation == 0 :
            self.position[0] += 1
        elif self.orientation == 90 :
            self.position[1] -= 1
        elif self.orientation == 270 :
            self.position[1] += 1
    
    def turn(self,direction) :
        self.orientation = (self.orientation + angle) % 360
        
    def execute(self) :
        for condition,action in self.program :
            if eval(condition) :
                eval(action)
                return

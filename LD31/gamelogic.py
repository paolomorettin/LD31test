
# directions (enum)
DIRECTION_UP, DIRECTION_LEFT, DIRECTION_DOWN, DIRECTION_RIGHT = range(4)

# walls: 0 = no wall, 1 = wall
# style: 0..n = colors
# type
CELLTYPE_NORMAL, CELLTYPE_START, CELLTYPE_END = range(3)

# map size in cells
MAPSIZE = (26,20)


# Single cell of the map
class Cell:
    def __init__(self):
        self.wall = [0]*4
        self.style = 0
        self.type = CELLTYPE_NORMAL


# Game state.
class Game:
    _instance = None

    @staticmethod
    def instance():
        if Game._instance is None:
            Game._instance = Game()
        return Game._instance
    
    def __init__(self):
        print "Creating a new Game."

    def load_from(self, fname):
        # TODO: Stub
        pass

    def get_cell(self,x,y):
        # returns the Cell at (x,y) or None
        # TODO: Stub
        return Cell()

    def enter_cell(self,x,y):
        # called when player enters a cell. May trigger some changes over the map.
        # returns list of NEW items to put on the map.
        # TODO: Stub
        return []

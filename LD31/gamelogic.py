from datastructures import GameMapData


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
        self.matrix = {}
        self.current_cell_level = {}
        self.cell_cache = {}
        self._all_data = None
        self.triggers = {}

    def load_from(self, fname):
        # loads from the specified filename
        self._all_data = GameMapData.load(fname)
        self.matrix = self._all_data.levels[0].matrix.copy()
        self.triggers = self._all_data.levels[0].triggers.copy()
        for x in range(MAPSIZE[0]):
            for y in range(MAPSIZE[1]):
                self.current_cell_level[(x,y)] = 0
        pass

    def get_cell(self,x,y):
        # returns the Cell at (x,y) or None
        c = Cell()
        c.style = self.current_cell_level[(x,y)]
        c.type = self.matrix[(x*2+1, y*2+1)]
        c.wall[DIRECTION_UP] =    self.matrix[(x*2+2, y*2+1)]
        c.wall[DIRECTION_DOWN] =  self.matrix[(x*2,   y*2+1)]
        c.wall[DIRECTION_RIGHT] = self.matrix[(x*2+1, y*2+2)]
        c.wall[DIRECTION_LEFT] =  self.matrix[(x*2+1, y*2  )]
        return c

    def enter_cell(self,x,y):
        # called when player enters a cell. May trigger some changes over the map.
        # returns list of NEW items to put on the map.
        # TODO: Stub
        return []


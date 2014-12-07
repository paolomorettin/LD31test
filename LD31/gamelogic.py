from datastructures import GameMapData
import maplayer
import player
import cocos


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

    def __str__(self):
        return "walls [up, left, down, right] = "+str(self.wall)+" type "+str(self.type)+" lev "+str(self.style)


# Game state.
class Game(object):
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
        # other classes. Set my the main when they are initialized
        self.maplayer = None
        self.keystate = None
        self.player = None

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
        c.wall[DIRECTION_UP] =    self.matrix[(x*2+1, y*2+2)]
        c.wall[DIRECTION_DOWN] =  self.matrix[(x*2+1, y*2+0)]
        c.wall[DIRECTION_RIGHT] = self.matrix[(x*2+2, y*2+1)]
        c.wall[DIRECTION_LEFT] =  self.matrix[(x*2+0, y*2+1)]
        return c

    def get_block_coords(self, idx):
        data = [(0,8,0,9),(9,16,0,9),(17,25,0,9),(0,8,10,19),(9,16,10,19),(17,25,10,19)]
        x1, x2, y1, y2 = data[idx]
        return (x1, x2+1, y1, y2+1)

    def enter_cell(self,x,y):
        # called when player enters a cell. May trigger some changes over the map.
        # returns list of NEW items to put on the map.
        if (x,y) not in self.triggers:
            return
        trigger = self.triggers[(x,y)]
        print "TRIGGER"
        newlevel = self._all_data.levels[trigger.newlevel]
        for bid in trigger.block_id:
            # x1 y1 x2 y2 are in cell space
            (x1, x2, y1, y2) =  self.get_block_coords(bid)
            
            # update the map for the target locations
            for x in range(x1, x2):
                for y in range(y1, y2):
                    # foreach cell, copy the cell inner value
                    self.matrix[(x*2+1, y*2+1)] = newlevel.matrix[(x*2+1, y*2+1)]
                    # and the surrounding walls
                    self.matrix[(x*2+2, y*2+1)] = newlevel.matrix[(x*2+2, y*2+1)]
                    self.matrix[(x*2,   y*2+1)] = newlevel.matrix[(x*2,   y*2+1)]
                    self.matrix[(x*2+1, y*2+2)] = newlevel.matrix[(x*2+1, y*2+2)]
                    self.matrix[(x*2+1, y*2  )] = newlevel.matrix[(x*2+1, y*2  )]

            # todo: aggiungi i trigger nuovi
            # # insert new triggers, if they are there
            # new_triggers = {t for t in newlevel.triggers
            #                 if t.from_cell[0] >= x1
            #                 and t.from_cell[1] >= y1
            #                 and t.to_cell[0] <= x2
            #                 and t.to_cell[1] <= y2}
            
            # survived_triggers = {t for t in self.triggers
            #                      if not (t.from_cell[0] >= x1
            #                              and t.from_cell[1] >= y1
            #                              and t.to_cell[0] <= x2
            #                              and t.to_cell[1] <= y2)}
        
            #new_triggers.update(survived_triggers)
            #self.triggers = survived_triggers

            if self.maplayer is not None:
                self.maplayer.update(bid, animation=False)

        return []


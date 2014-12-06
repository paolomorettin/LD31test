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
        self.maplayer = None

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
        return
        # called when player enters a cell. May trigger some changes over the map.
        # returns list of NEW items to put on the map.
        trigger = self.triggers[(x,y)]
        if trigger is None:
            return
        newlevel = self._all_data.levels[newlevel]
        # x1 y1 x2 y2 are in cell space
        (x1, y1) = (trigger.from_cell[0], trigger.from_cell[1])
        (x2, y2) = (trigger.to_cell[0]+1, trigger.to_cell[1]+1)
        
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

        # insert new triggers, if they are there
        new_triggers = {t for t in newlevel.triggers
                        if t.from_cell[0] >= x1
                        and t.from_cell[1] >= y1
                        and t.to_cell[0] <= x2
                        and t.to_cell[1] <= y2}
        
        survived_triggers = {t for t in self.triggers
                             if not (t.from_cell[0] >= x1
                                     and t.from_cell[1] >= y1
                                     and t.to_cell[0] <= x2
                                     and t.to_cell[1] <= y2)}

        new_triggers.update(survived_triggers)
        self.triggers = survived_triggers

        # now consider a bit larger area, since we need to redraw the
        # walls also of neighboring cells.
        if x1 >= 1:
            x1 -= 1
        if y1 >= 1:
            y1 -= 1
        if x2 <= MAPSIZE[0]:
            x2 += 1
        if y2 <= MAPSIZE[1]:
            y2 += 1

        if self.maplayer is not None:
            self.maplayer.update_view(x1, y1, x2, y2)

        return []


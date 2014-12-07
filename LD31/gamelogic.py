from datastructures import GameMapData
import maplayer
import player
import cocos
import itertools
import enemy, random
from splashes import DeathScreen, WinScreen

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
        self._all_data = None
        self.triggers ={}
        self.levelnr = 0
        # other classes. Set my the main when they are initialized
        self.maplayer = None
        self.keystate = None
        self.player = None

    def load_from(self, fname):
        # loads from the specified filename
        self._all_data = GameMapData.load(fname)
        self.matrix = self._all_data.levels[0].matrix.copy()
        self.triggers = self._all_data.levels[0].triggers.copy()
        self.refresh_level()

    def get_start_point(self):
        return self._all_data.levels[self.levelnr].start_point
        
    def get_cell(self,x,y):
        # returns the Cell at (x,y) or None
        c = Cell()
        c.style = 0
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

    def get_coords_block(self, x, y):
        for i in range(6):
            (x1, x2, y1, y2) =  self.get_block_coords(i)
            if x >= x1 and y >= y1 and x <= x2 and y <= y2:
                return i
        return None # WTF?

    def enter_cell(self,xc,yc):
        # called when player enters a cell. May trigger some changes over the map.
        # returns list of NEW items to put on the map.
        if (xc,yc) == self._all_data.levels[self.levelnr].end_point:
            self.win()
            return

        
        if (xc,yc) not in self.triggers:
            return
        trigger = self.triggers[(xc,yc)]
        print "TRIGGER"
        self.levelnr = trigger.newlevel
        self.refresh_level()

    def die(self):
        cocos.director.director.replace(DeathScreen(self.restart()))

    def win(self):
        cocos.director.director.replace(WinScreen(self.restart()))

    def restart(self):
        Game._instance = Game()
        game = Game.instance()
        game.load_from("level.dat")
        viewer = maplayer.MapLayer()
        game.maplayer = viewer
        game.player = player.Player()
        game.keystate = self.keystate

        main_scene = cocos.scene.Scene(viewer)
        main_scene.add(game.player)
        return main_scene

    
    def refresh_level(self):
        print self
        print "Going to level", self.levelnr
        newlevel = self._all_data.levels[self.levelnr]

        self.matrix = newlevel.matrix.copy()
        self.triggers = newlevel.triggers.copy()

        for k,v in self.triggers.iteritems():
            print "@pos ",k, " triggers block ",v.block_id," switch to ",v.newlevel

        end_x, end_y = self._all_data.levels[self.levelnr].end_point
        print "new end @",end_x, ",",end_y
        print "should start @",self._all_data.levels[self.levelnr].start_point
        self.matrix[(end_x*2+1, end_y*2+1)] = CELLTYPE_END
        end_block = self.get_coords_block(end_x, end_y)
        if self.maplayer is not None:
            self.maplayer.update()
        pass

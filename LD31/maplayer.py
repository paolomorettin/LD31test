import cocos
import pyglet
from pyglet.gl.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
import gamelogic

class MapLayer(cocos.layer.ColorLayer):
    SPRITE_SIZE = 30
    WALL_SIZE = 2

    def __init__(self):
        super(MapLayer, self).__init__(255, 255, 255, 255)
        self.game = gamelogic.Game.instance()
        self.update_view(0, 0, gamelogic.MAPSIZE[0], gamelogic.MAPSIZE[1])

    def _get_sprite_drawing_coors(self, cell_x, cell_y, side):
        base_x = cell_x * MapLayer.SPRITE_SIZE
        base_y = cell_y * MapLayer.SPRITE_SIZE
        if side == gamelogic.DIRECTION_LEFT:
            x_offset = MapLayer.WALL_SIZE / 2
            y_offset = MapLayer.SPRITE_SIZE / 2
        elif side == gamelogic.DIRECTION_RIGHT:
            x_offset = MapLayer.SPRITE_SIZE - (MapLayer.WALL_SIZE / 2)
            y_offset = MapLayer.SPRITE_SIZE / 2
        elif side == gamelogic.DIRECTION_DOWN:
            x_offset = MapLayer.SPRITE_SIZE / 2
            y_offset = MapLayer.WALL_SIZE / 2
        elif side == gamelogic.DIRECTION_UP:
            x_offset = MapLayer.SPRITE_SIZE / 2
            y_offset = MapLayer.SPRITE_SIZE - (MapLayer.WALL_SIZE / 2)
        else:
            print "MapLayer ERROR: Unknown side " + side
        return base_x + x_offset, base_y + y_offset


        offset = MapLayer.SPRITE_SIZE / 2
        return base_x + offset, base_y + offset

    def update_view(self, startx, starty, endx, endy):
        """
        Redraws a portion of the screen

        :param startx:
        :param starty:
        :param endx:
        :param endy:
        :return:
        """
        self.batchnode = cocos.batch.BatchNode()
        print "updating map"
        for x in range(startx, endx):
            for y in range(starty, endy):
                cell = self.game.get_cell(x, y)
                for side in range(4):
                    if cell.wall[side] == 1:
                        
                        image = pyglet.resource.image("img/wall.png")
       
                        glTexParameteri(image.texture.target,
                                        GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                        glTexParameteri(image.texture.target,
                                        GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                        wall = cocos.sprite.Sprite(image)
                        if side == gamelogic.DIRECTION_UP or side == gamelogic.DIRECTION_DOWN:
                            wall.rotation = 90
                        wall.position = self._get_sprite_drawing_coors(x, y, side)
                        self.batchnode.add(wall)

        self.add(self.batchnode)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1 or sys.argv[1] != "-debug":
        print "This class is not intended to be run in a main file."
        print "However, if you just want to run a test, use -debug option."
        sys.exit(0)
    cocos.director.director.init(width=800, height=600)
    g =gamelogic.Game.instance()
    g.load_from("level.dat")
    test_map = MapLayer()
    test = cocos.scene.Scene(test_map)
    test_map.update_view(0,0,gamelogic.MAPSIZE[0],gamelogic.MAPSIZE[1])
    cocos.director.director.run(test)


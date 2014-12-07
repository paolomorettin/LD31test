import cocos
import pyglet
from pyglet.gl.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
import gamelogic

class MapLayer(cocos.layer.Layer):
    SPRITE_SIZE = 30
    WALL_SIZE = 5

    BLOCK_NEIGHBOUR = [{1, 3}, {0, 2, 4}, {1, 5},
                       {0, 4}, {1, 3, 5}, {2, 4}]

    LEVEL_COLORS = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]

    def __init__(self):
        super(MapLayer, self).__init__()
        self.game = gamelogic.Game.instance()

        self.back = self.__load_sprite("img/back.png")
        self.back.position = (400, 300)
        self.add(self.back)

        self.block = [None] * 6
        self.wall_builders = [self.__wall_top, self.__wall_left,
                              self.__wall_bottom, self.__wall_right]
        for i in range(6):
            self.__update_block(i, False)

    def update_blocks(self, block_list):
        """
        :type block_list:   list of int
        :param block_list:  IDs of the blocks which need to be updated
        :return:
        """
        neighbours = set()
        for block_id in block_list:
            self.__update_block(block_id, True)
            neighbours.update(MapLayer.BLOCK_NEIGHBOUR[block_id])
        neighbours -= set(block_list)
        for neigh in neighbours:
            self.__update_block(neigh, False)

    def __load_sprite(self, path):
        img = pyglet.resource.image(path)
        glTexParameteri(img.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(img.texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        return cocos.sprite.Sprite(img)


    def __wall_top(self, x, y):
        wall = self.__load_sprite("img/ice_mid2.png")
        wall.rotation = 90
        wall.position = self._get_sprite_drawing_coors(x, y, gamelogic.DIRECTION_UP)
        return wall

    def __wall_bottom(self, x, y):
        wall = self.__load_sprite("img/ice_mid.png")
        wall.rotation = 90
        wall.position = self._get_sprite_drawing_coors(x, y, gamelogic.DIRECTION_DOWN)
        return wall

    def __wall_left(self, x, y):
        wall = self.__load_sprite("img/ice_mid2.png")
        wall.position = self._get_sprite_drawing_coors(x, y, gamelogic.DIRECTION_LEFT)
        return wall

    def __wall_right(self, x, y):
        wall = self.__load_sprite("img/ice_mid.png")
        wall.position = self._get_sprite_drawing_coors(x, y, gamelogic.DIRECTION_RIGHT)
        return wall

    def __get_center(self, startx, endx, starty, endy):
        cell_center_x = startx + (endx - startx) / 2
        cell_center_y = starty + (endy - starty) / 2
        return cell_center_x * MapLayer.SPRITE_SIZE, cell_center_y * MapLayer.SPRITE_SIZE


    def __move_sprite(self, sprite, posx, posy):
        sprite.do()

    def __update_block(self, idx, animation=False):
        new_batch = cocos.batch.BatchNode()
        startx, endx, starty, endy = self.game.get_block_coords(idx)
        for x in range(startx, endx):
            for y in range(starty, endy):
                cell = self.game.get_cell(x, y)
                if cell.type == gamelogic.CELLTYPE_END:
                    end_flag = self.__load_sprite("img/end.png")
                    x_pos = x * MapLayer.SPRITE_SIZE + MapLayer.SPRITE_SIZE / 2
                    y_pos = y * MapLayer.SPRITE_SIZE + MapLayer.SPRITE_SIZE / 2
                    end_flag.position = x_pos, y_pos
                    new_batch.add(end_flag)
                for side in range(4):
                    if cell.wall[side] == 1:
                        wall = self.wall_builders[side](x, y)
                        new_batch.add(wall)
        if not animation:
            if self.block[idx]:
                self.remove(self.block[idx])
            self.add(new_batch)
        else:
            clouds = self.__load_sprite("img/cloud.png")
            cloud_x, cloud_y = self.__get_center(startx, endx, starty, endy)
            clouds.position = (cloud_x-1000, cloud_y)
            self.add(clouds, z=1)
            clouds.do(cocos.actions.MoveTo((cloud_x, cloud_y), 3) +\
                      cocos.actions.CallFunc(self.remove, self.block[idx]) +\
                      cocos.actions.CallFunc(self.add, new_batch) +\
                      cocos.actions.MoveTo((cloud_x+1000, cloud_y), 3))

        self.block[idx] = new_batch

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


import cocos
import pyglet
from pyglet.gl.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
import gamelogic
import random, enemy, bomb

class MapLayer(cocos.layer.Layer):
    SPRITE_SIZE = 30
    WALL_SIZE = 5

    def __init__(self):
        super(MapLayer, self).__init__()
        self.game = gamelogic.Game.instance()

        self.back = self.__load_sprite("img/back.png")
        self.back.position = (400, 300)
        self.add(self.back)

        self.storm = None

        self.wall_builders = [self.__wall_top, self.__wall_left,
                              self.__wall_bottom, self.__wall_right]

        self.map = cocos.batch.BatchNode()
        self.add(self.map)
        self.update(False)

        self.mystery_sound = cocos.audio.pygame.mixer.Sound("sounds/mystery.wav")

    def update_blocks(self, block_list):
        self.update(True)

    def bombing(self, timedelta):
        nuke = bomb.Bomb()
        self.add(nuke)
        launch_pos = self.game.get_random_cell()
        nuke.launch(launch_pos)
        print "Bombing @ " + str(launch_pos)

    def explode(self, timedelta, bomb):
        self.remove(bomb)
        explosion = self.__load_sprite("img/explosion.gif")
        explosion.position = bomb.position
        self.add(explosion)

    def update(self, animation=True):
        """
        :type block_list:   list of int
        :param block_list:  IDs of the blocks which need to be updated
        :return:
        """
        self.unschedule(self.bombing)
        self.schedule_interval(self.bombing, 20 - self.game.get_cell(0, 0).style * 10)

        if animation:
            if self.storm is None:
                self.storm = Storm(self)
                self.parent.add(self.storm, z=1)
                self.storm_started()
            self.storm.activate()
            self.mystery_sound.play()
            return
        new_batch = cocos.batch.BatchNode()
        for x in range(gamelogic.MAPSIZE[0]):
            for y in range(gamelogic.MAPSIZE[1]):
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
        self.remove(self.map)
        self.add(new_batch)
        self.map = new_batch

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

    def map_covered(self):
        self.add_enemies()
        self.update(False)

    def storm_started(self):
        self.game.player.disable_controls()
        pass

    def storm_ended(self):
        self.game.player.enable_controls()
        pass
    
    def add_enemies(self):
        for idx in range(2):
            self.add(enemy.Enemy([random.randint(0, gamelogic.MAPSIZE[0]-1),
                                  random.randint(0, gamelogic.MAPSIZE[1]-1)]))

class Storm(cocos.sprite.Sprite):
    def __init__(self, maplayer):
        img = pyglet.resource.image("img/cloud.png")
        glTexParameteri(img.texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(img.texture.target, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        super(Storm, self).__init__(img)
        self.scale = 3
        self.maplayer = maplayer
        self.position = (-1000, 300)

    def activate(self):
        self.position = (-1000, 300)
        self.do(cocos.actions.MoveTo((400, 300), 3) +\
                cocos.actions.CallFunc(self.maplayer.map_covered) +\
                cocos.actions.MoveTo((2000, 300), 3) +\
                cocos.actions.CallFunc(self.maplayer.storm_ended))

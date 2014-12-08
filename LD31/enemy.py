import random
import cocos, pyglet
from pyglet.gl.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
import maplayer, gamelogic
from pyglet.window import key

class Enemy(cocos.layer.Layer):
    PLAYER_SIZE = 26

    def __init__(self, position) :
        super(Enemy, self).__init__()
                                
        image = pyglet.resource.image("img/enemy.png")
        self.growl_sound = cocos.audio.pygame.mixer.Sound("sounds/growl1.wav")
       
        glTexParameteri(image.texture.target,
                        GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(image.texture.target,
                        GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.sprite = cocos.sprite.Sprite(image)
        (self.cell_x,self.cell_y) = position
        self.sprite.position = self._get_drawing_coors()
        self.add(self.sprite)
        self.moving = False # currently moving
        self.game = gamelogic.Game.instance()

        self.schedule(self.update)
        self.target = self.__get_target()

    def __get_target(self):
        x = random.randint(0, gamelogic.MAPSIZE[0]-1)
        y = random.randint(0, gamelogic.MAPSIZE[1]-1)
        return x, y

    def _get_drawing_coors(self):
        base_x = maplayer.MapLayer.SPRITE_SIZE * self.cell_x
        base_y = maplayer.MapLayer.SPRITE_SIZE * self.cell_y
        offset = maplayer.MapLayer.SPRITE_SIZE / 2
        return base_x + offset, base_y + offset

    def _movement_allowed(self, direction):
        return self.game.get_cell(self.cell_x, self.cell_y).wall[direction] == 0

    def compute_distance(self, x, y):
        x_dis = abs(x - self.target[0])
        y_dis = abs(y - self.target[1])
        return x_dis + y_dis

    def getting_closer(self, direction):
        x = self.cell_x
        y = self.cell_y
        actual_dis = self.compute_distance(x, y)
        if direction == gamelogic.DIRECTION_LEFT: x -= 1
        elif direction == gamelogic.DIRECTION_UP: y += 1
        elif direction == gamelogic.DIRECTION_DOWN: y -= 1
        elif direction == gamelogic.DIRECTION_RIGHT: x += 1
        future_dis = self.compute_distance(x, y)
        return future_dis <= actual_dis


    def update(self, timedelta):
        if self.moving:
            return

        good_moves = []
        if self._movement_allowed(gamelogic.DIRECTION_LEFT) and self.getting_closer(gamelogic.DIRECTION_LEFT):
            good_moves.append(gamelogic.DIRECTION_LEFT)
        if self._movement_allowed(gamelogic.DIRECTION_RIGHT) and self.getting_closer(gamelogic.DIRECTION_RIGHT):
            good_moves.append(gamelogic.DIRECTION_RIGHT)
        if self._movement_allowed(gamelogic.DIRECTION_UP) and self.getting_closer(gamelogic.DIRECTION_UP):
            good_moves.append(gamelogic.DIRECTION_UP)
        if self._movement_allowed(gamelogic.DIRECTION_DOWN) and self.getting_closer(gamelogic.DIRECTION_DOWN):
            good_moves.append(gamelogic.DIRECTION_DOWN)
        if len(good_moves) == 0:
            self.target = self.__get_target()
            return

        ran_move = random.choice(good_moves)

        if ran_move == gamelogic.DIRECTION_LEFT:
            self.cell_x -= 1
        elif ran_move == gamelogic.DIRECTION_UP:
            self.cell_y += 1
        elif ran_move == gamelogic.DIRECTION_DOWN:
            self.cell_y -= 1
        elif ran_move == gamelogic.DIRECTION_RIGHT:
            self.cell_x += 1

        if random.randint(0,50) == 0 :
            self.growl_sound.play()

        self.moving = True
        self.sprite.do(cocos.actions.MoveTo(self._get_drawing_coors(), 0.5) + cocos.actions.CallFunc(self.stopped_moving))
        if self.cell_x == self.game.player.cell_x and self.cell_y == self.game.player.cell_y:
            self.game.die()

    def stopped_moving(self):
        self.moving = False















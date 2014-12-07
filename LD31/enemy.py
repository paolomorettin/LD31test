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

    def _get_drawing_coors(self):
        base_x = maplayer.MapLayer.SPRITE_SIZE * self.cell_x
        base_y = maplayer.MapLayer.SPRITE_SIZE * self.cell_y
        offset = maplayer.MapLayer.SPRITE_SIZE / 2
        return base_x + offset, base_y + offset

    def _movement_allowed(self, direction):
        return self.game.get_cell(self.cell_x, self.cell_y).wall[direction] == 0

    def _movement_allowed(self, direction):
        return self.game.get_cell(self.cell_x, self.cell_y).wall[direction] == 0

    def update(self, timedelta):
        if self.moving:
            return

        ran_move = random.choice([gamelogic.DIRECTION_LEFT, gamelogic.DIRECTION_RIGHT,
                                  gamelogic.DIRECTION_RIGHT, gamelogic.DIRECTION_DOWN])

        if ran_move == gamelogic.DIRECTION_LEFT and self._movement_allowed(gamelogic.DIRECTION_LEFT):
            self.cell_x -= 1
        elif ran_move == gamelogic.DIRECTION_UP and self._movement_allowed(gamelogic.DIRECTION_UP):
            self.cell_y += 1
        elif ran_move == gamelogic.DIRECTION_DOWN and self._movement_allowed(gamelogic.DIRECTION_DOWN):
            self.cell_y -= 1
        elif ran_move == gamelogic.DIRECTION_RIGHT and self._movement_allowed(gamelogic.DIRECTION_RIGHT):
            self.cell_x += 1

        self.moving = True
        self.sprite.do(cocos.actions.MoveTo(self._get_drawing_coors(), 0.2) + cocos.actions.CallFunc(self.stopped_moving))

    def stopped_moving(self):
        self.moving = False

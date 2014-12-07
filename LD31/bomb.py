import random
import cocos, pyglet
from pyglet.gl.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
import maplayer, gamelogic
from pyglet.window import key

class Bomb(cocos.sprite.Sprite):
    PLAYER_SIZE = 26

    def __init__(self) :
                                
        image = pyglet.resource.image("img/bomb.png")
        self.explosion_sound = cocos.audio.pygame.mixer.Sound("sounds/explosion.wav")
       
        glTexParameteri(image.texture.target,
                        GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(image.texture.target,
                        GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        super(Bomb, self).__init__(image)
        
        self.game = gamelogic.Game.instance()
        
    def _get_drawing_coors(self):
        base_x = maplayer.MapLayer.SPRITE_SIZE * self.cell_x
        base_y = maplayer.MapLayer.SPRITE_SIZE * self.cell_y
        offset = maplayer.MapLayer.SPRITE_SIZE / 2
        return base_x + offset, base_y + offset

    def launch(self,target) :
        self.position = target[0]*30 + 15, 700
        self.do(cocos.actions.MoveTo(target,1))
        self.schedule_interval(self.parent.explode,6)

    def explode(self) :
        self.parent.explode
        

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

        if self.cell_y > self.target :
            self.cell_y -= 1
            self.moving = True
            self.sprite.do(cocos.actions.MoveTo(self._get_drawing_coors(), 0.2) + cocos.actions.CallFunc(self.stopped_moving))
        else :
            

    def stopped_moving(self):
        self.moving = False















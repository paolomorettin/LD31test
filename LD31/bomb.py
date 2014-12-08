import cocos, pyglet
from pyglet.gl.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
import gamelogic

class Bomb(cocos.sprite.Sprite):
    PLAYER_SIZE = 26

    def __init__(self) :
                                
        image = pyglet.resource.image("img/fire.gif")
        #self.explosion_sound = cocos.audio.pygame.mixer.Sound("sounds/explosion.wav")
       
        glTexParameteri(image.texture.target,
                        GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(image.texture.target,
                        GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        super(Bomb, self).__init__(image)
        self.position = (1000, 1000)
        self.game = gamelogic.Game.instance()

    def launch(self, target) :
        target_x = target[0] * 30 + 15
        target_y = target[1] * 30 + 15
        self.position = target_x, 700
        self.do(cocos.actions.MoveTo((target_x, target_y), 1))
        self.schedule_interval(self.parent.explode, 6, self)













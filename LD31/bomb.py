import cocos, pyglet
from pyglet.gl.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
import gamelogic
import random
from cocos.actions import *

class Bomb(cocos.sprite.Sprite):
    PLAYER_SIZE = 26

    def __init__(self) :
                                
        image = pyglet.resource.image("img/bomb.png")
        self.sound = cocos.audio.pygame.mixer.Sound("sounds/explosion.wav")
       
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
        self.schedule_interval(self.explode, 1)


    def explode(self, timedelta):
        self.sound.play()
        self.game.kill(self.position)
        for i in range(6):
            explosion = BombExplosion(self.position)
            self.parent.add(explosion)
        self.kill()




class BombExplosion(cocos.sprite.Sprite):
    
    animation = pyglet.image.load_animation('img/explosion.gif')

    bin = pyglet.image.atlas.TextureBin()
    animation.add_to_texture_bin(bin)


    def __init__(self, pos):
        super(BombExplosion, self).__init__(BombExplosion.animation)
        
        self.position = pos
        self.scale = 1.5
        self.target_pos = (pos[0]+random.randrange(-40,40),pos[1]+random.randrange(-40,40))
        self.do(MoveTo(self.target_pos,0.4) + CallFunc(self.done_animation))
        self.do(FadeOut(0.4))

    def done_animation(self):
        self.kill()





import cocos, pyglet
from pyglet.gl.gl import glTexParameteri, GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MIN_FILTER, GL_NEAREST
import gamelogic
import random
from cocos.actions import *

class Bomb(cocos.sprite.Sprite):
    PLAYER_SIZE = 26

    def __init__(self) :
                                
        image = pyglet.resource.image("img/bomb.png")
        self.drop_sound = cocos.audio.pygame.mixer.Sound("sounds/bomb_drop.wav")
        self.explosion_sound = cocos.audio.pygame.mixer.Sound("sounds/explosion.wav")
       
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
        self.drop_sound.play()
        self.schedule_interval(self.explode, 5)


    def explode(self, timedelta):
        self.explosion_sound.play()
        self.game.kill(self.position)
        for i in range(5):
            pos = self.position
            explosion = BombExplosion((pos[0]+random.randrange(-40,40),pos[1]+random.randrange(-40,40)), self.game)
            self.parent.add(explosion)
            
        if self.game.is_player_in_range(self.position):
            explosion = BombExplosion(self.position, self.game, killplayer=True)
            self.parent.add(explosion)
            self.game.player.disable_controls()
            self.game.player.stop()
            self.game.player.stopped_moving()

        self.kill()




class BombExplosion(cocos.sprite.Sprite):
    # yes, it's doing what you are thinking.
    animation = pyglet.image.load_animation('img/explosion.gif')
    bin = pyglet.image.atlas.TextureBin()
    animation.add_to_texture_bin(bin)


    def __init__(self, pos, game, killplayer=False):
        super(BombExplosion, self).__init__(BombExplosion.animation)
        self.position = pos
        self.scale = 1.5
        self.game = game
        self.killplayer = killplayer
        self.target_pos = pos
        self.do(MoveTo(self.target_pos,0.4) + CallFunc(self.done_animation))
        self.do(FadeOut(0.4))

    def done_animation(self):
        if self.killplayer:
            self.game.die()
        self.kill()





import random
import cocos

STEP, FALLING_BOMB, EXPLOSION, GROWL, MONKEYS, MISTERY = range(6)

class SoundManager(object):
    __inst = None

    def __init__(self):
        self.initialized = False
        try:
            cocos.audio.pygame.mixer.init()

            self.music = cocos.audio.pygame.music.load("sounds/music.wav")

            self.sounds = [None] * 6
            self.sounds[STEP] = [cocos.audio.pygame.mixer.Sound("sounds/snow1.wav"),
                                cocos.audio.pygame.mixer.Sound("sounds/snow2.wav")]
            self.sounds[FALLING_BOMB] = [cocos.audio.pygame.mixer.Sound("sounds/bomb_drop.wav")]
            self.sounds[EXPLOSION] = [cocos.audio.pygame.mixer.Sound("sounds/explosion.wav")]
            self.sounds[GROWL] = [cocos.audio.pygame.mixer.Sound("sounds/growl1.wav")]
            self.sounds[MONKEYS] = [cocos.audio.pygame.mixer.Sound("sounds/splash.wav")]
            self.sounds[MISTERY] = [cocos.audio.pygame.mixer.Sound("sounds/mystery.wav")]
        except Exception as exc:
            print "ERROR: an error occurred while initializing the sound manager"
            print "Sound will not be available"
            print exc
            return
        self.initialized = True

    @staticmethod
    def instance():
        if not SoundManager.__inst:
            SoundManager.__inst = SoundManager()
        return SoundManager.__inst

    def play_music(self):
        cocos.audio.pygame.music.play(-1)

    def play(self, sound):
        if not self.initialized:
            print "SOUND ERROR: Unable to play sounds"
        random.choice(self.sounds[sound]).play()


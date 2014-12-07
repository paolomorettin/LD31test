import cocos
import gamelogic
import maplayer
import player
import pyglet

class SplashScreen(cocos.scene.Scene):
    def __init__(self, main_scene):
        splash_layer = cocos.layer.Layer()
        logo = cocos.sprite.Sprite("img/logo.png")
        logo.position = 400, 300
        splash_layer.add(logo)
        super(SplashScreen, self).__init__(splash_layer)
        cocos.audio.pygame.music.load("sounds/splash.wav")
        cocos.audio.pygame.music.play(0)
        self.schedule_interval(self.close, 3.5, main_scene)

    def close(self, timedelta, scene):
        cocos.audio.pygame.music.load("sounds/music.wav")
        cocos.audio.pygame.music.play(-1)
        cocos.director.director.replace(scene)


if __name__ == "__main__":
    cocos.director.director.init(width=800, height=600)
    cocos.audio.pygame.mixer.init()

    game = gamelogic.Game.instance()
    game.load_from("level.dat")
    viewer = maplayer.MapLayer()
    game.maplayer = viewer
    game.player = player.Player()
    game.keystate = pyglet.window.key.KeyStateHandler()
    cocos.director.director.window.push_handlers(game.keystate)

    main_scene = cocos.scene.Scene(viewer)
    main_scene.add(game.player)
    splash = SplashScreen(main_scene)
    cocos.director.director.run(splash)


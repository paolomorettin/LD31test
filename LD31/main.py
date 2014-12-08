import cocos
import lvlGenerator
import gamelogic
import maplayer
import player
import pyglet
from splashes import InitialSplashScreen

if __name__ == "__main__":
    cocos.director.director.init(width=780, height=600)
    cocos.audio.pygame.mixer.init()

    game = gamelogic.Game.instance()
    lvlGenerator.do_it_now()
    game.load_from("level.dat")
    viewer = maplayer.MapLayer()
    game.maplayer = viewer
    game.player = player.Player()
    game.keystate = pyglet.window.key.KeyStateHandler()
    cocos.director.director.window.push_handlers(game.keystate)

    main_scene = cocos.scene.Scene(viewer)
    main_scene.add(game.player)
    splash = InitialSplashScreen(main_scene)
    cocos.director.director.run(splash)


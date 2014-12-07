import cocos
import gamelogic
import maplayer
import player
import pyglet

if __name__ == "__main__":
    cocos.director.director.init(width=800, height=600)
    cocos.audio.pygame.mixer.init()

    try:
        cocos.audio.pygame.music.load("sounds/music.wav")
        cocos.audio.pygame.music.play(-1)
    except Error:
        print "Unable to play music"

    game = gamelogic.Game.instance()
    game.load_from("level.dat")
    viewer = maplayer.MapLayer()
    game.maplayer = viewer
    game.player = player.Player()
    game.keystate = pyglet.window.key.KeyStateHandler()
    cocos.director.director.window.push_handlers(game.keystate)

    main_scene = cocos.scene.Scene(viewer)
    main_scene.add(game.player)
    cocos.director.director.run(main_scene)

import cocos
import gamelogic
import maplayer
import player

if __name__ == "__main__":
    cocos.director.director.init(width=800, height=600)
    game = gamelogic.Game.instance()
    game.load_from("level.dat")
    viewer = maplayer.MapLayer()
    game.maplayer = viewer
    player = player.Player()
    main_scene = cocos.scene.Scene(viewer)
    main_scene.add(player)
    cocos.director.director.run(main_scene)
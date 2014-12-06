import cocos, pyglet
import maplayer, gamelogic

class Player(cocos.layer.ColorLayer):
    is_event_handler = True
    PLAYER_SIZE = 26

    def __init__(self):
        super(Player, self).__init__(255,255,255,0)
        self.game = gamelogic.Game.instance()
        self.sprite = cocos.sprite.Sprite("img/player.png")
        self.cell_x = 0
        self.cell_y = 0
        self.sprite.position = self._get_drawing_coors()
        self.add(self.sprite)

    def _get_drawing_coors(self):
        base_x = maplayer.MapLayer.SPRITE_SIZE * self.cell_x
        base_y = maplayer.MapLayer.SPRITE_SIZE * self.cell_y
        offset = maplayer.MapLayer.SPRITE_SIZE / 2
        return base_x + offset, base_y + offset

    def _movement_allowed(self, direction):
        return self.game.get_cell(self.cell_x, self.cell_y).wall[direction] == 0

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.LEFT and self._movement_allowed(gamelogic.DIRECTION_LEFT):
            self.cell_x -= 1
        elif key == pyglet.window.key.UP and self._movement_allowed(gamelogic.DIRECTION_UP):
            self.cell_y += 1
        elif key == pyglet.window.key.DOWN and self._movement_allowed(gamelogic.DIRECTION_DOWN):
            self.cell_y -= 1
        elif key == pyglet.window.key.RIGHT and self._movement_allowed(gamelogic.DIRECTION_RIGHT):
            self.cell_x += 1

        self.sprite.position = self._get_drawing_coors()

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1 or sys.argv[1] != "-debug":
        print "This class is not intended to be run in a main file."
        print "However, if you just want to run a test, use -debug option."
        sys.exit(0)
    cocos.director.director.init()
    player = Player()
    test = cocos.scene.Scene(player)
    cocos.director.director.run(test)
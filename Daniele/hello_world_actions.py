#
# cocos2d
# http://cocos2d.org
#

from __future__ import division, print_function, unicode_literals


import random
import math

import cocos
from cocos.actions import *
from cocos.collision_model import *

from game_entities import BasicMonster, Structure, TurretBase, BasicBullet, CityLayer, MonsterLayer

# A color layer  is a Layer with the a color attribute
class GameLayer(cocos.layer.ColorLayer):
    def __init__(self, city):
        # blueish color
        super( GameLayer, self ).__init__(0,0,10,255)

        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a CocosNode
        label = cocos.text.Label('Playing',
            font_name='Times New Roman',
            font_size=32,
            anchor_x='center', anchor_y='center')

        # set the label in the center of the screen
        label.position = 400,300
        self.add( label )


        self.city = city
        self.monsters = MonsterLayer()
        self.city.set_attackers_layes(self.monsters)
        self.city.set_game_layer(self)
        self.city.start()
        self.add(self.city)
        self.add(self.monsters)


        for i in range(10):
            m = BasicMonster((i*50, 500))
            self.monsters.schedule_monster(m , 1.0/(i+1))
        for i in range(10):
            m = BasicMonster((i*50, 550))
            self.monsters.schedule_monster(m , 0.1)
        for i in range(10):
            m = BasicMonster((i*50, 600))
            self.monsters.schedule_monster(m , 0.1)


        self.monsters.start_spawning()
        
        # create a ScaleBy action that lasts 2 seconds
        #scale = ScaleBy(3, duration=2)
        
        # tell the label to scale and scale back and repeat these 2 actions forever
        #label.do( Repeat( scale + Reverse( scale) ) )
        
        # tell the sprite to scaleback and then scale, and repeat these 2 actions forever
        #sprite.do( Repeat( Reverse(scale) + scale ) )


    def game_over(self):
        cocos.director.director.pop()
        self.city.stop()

    def get_game(self):
        return self

class SpriteButton(cocos.sprite.Sprite):
    def __init__(self, img, size, position, callback, data = None):
        super(SpriteButton, self).__init__(img, position=position)
        self.dimensions = size
        self.callback = callback
        self.data = data

    def notify_button_click(self):
        self.callback(self)
    
class PlanningLayer(cocos.layer.ColorLayer):
    is_event_handler = True
    available_spaces=[ (0,0), (50,0), (100,0), (200,0), (250,10), (400,0), (500,0), (600,0), (700,0) ]
    
    def __init__(self):
        super( PlanningLayer, self ).__init__(0,10,0,255)
        self.shown_turrets = []
        self.turrets = [None] * len(self.available_spaces)
        self.buttons = []
        self.refresh_ui()
        self.refresh_turrets()
        self.city = CityLayer()

    def refresh_ui(self):
        for b in self.buttons:
            self.remove(b)

        self.buttons = []
        for idx in range(len(self.available_spaces)):
            btnpos = self.available_spaces[idx]
            btnpos = (btnpos[0], btnpos[1] + 40)
            if self.turrets[idx] is None:
                btn = SpriteButton("repeatturret.png", (30,30), btnpos, self.create_turret, (idx, "repeat"))
                self.buttons.append(btn)
            elif self.turrets[idx].nrbullets != 3:
                btn = SpriteButton("upgrade1.png", (30,30), btnpos, self.upgrade_turret, (idx, 1))
                self.buttons.append(btn)

        self.buttons.append(SpriteButton("readybtn.png", (100,40), (400,500), self.start_game, None))
        for b in self.buttons:
            self.add(b)

    def refresh_turrets(self):
        for t in self.shown_turrets:
            self.remove(t)

        self.shown_turrets = []
        
        for t in self.turrets:
            if t is not None:
                self.add(t)
                self.shown_turrets.append(t)
        
    def create_turret(self, btn):
        (idx, type_) = btn.data
        pos = self.available_spaces[idx]
        if self.turrets[idx] is not None:
            # wtf?
            self.refresh_ui()
            return
        if type_ == "repeat":
            self.turrets[idx] = TurretBase(pos)
            self.refresh_ui()
            self.refresh_turrets()
        else:
            # wtf?
            self.refresh_ui()
            return

    def upgrade_turret(self, btn):
        (idx, level) = btn.data
        if self.turrets[idx] is None:
            # wtf?
            self.refresh_ui()
            return

        # TODO: Very stub. Much crash.
        self.turrets[idx].bulletinterval=0.1
        self.turrets[idx].nrbullets = 3
        self.turrets[idx].burstinterval = 1
        self.refresh_ui()
        self.refresh_turrets()

    def start_game(self, btn):
        self.city.structures = [t for t in self.turrets if t is not None]
        cocos.director.director.push(cocos.scene.Scene(GameLayer(self.city)))

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        for b in self.buttons:
            if b.get_rect().contains(x,y):
                b.notify_button_click()
        pass
    
class MenuLayer(cocos.layer.ColorLayer):
    def __init__(self):
        super( MenuLayer, self ).__init__(0,10,0,255)

        menutitems = []
        menutitems.append( cocos.menu.MenuItem('Level 1', self.on_new_game ) )
        menutitems.append( cocos.menu.MenuItem('Quit', self.on_quit ) )
        menu = cocos.menu.Menu("Main Menu")
        menu.create_menu( menutitems, cocos.menu.zoom_in(), cocos.menu.zoom_out())
        menu.on_quit = self.on_quit
        self.add(menu)

        for t in range(5):
            turret = TurretBase((100*t, 30))
            self.add(turret)

    def on_new_game(self):
        cocos.director.director.push(cocos.scene.Scene(PlanningLayer()))

    def on_quit(self):
        sys.exit(0)
    
if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(width=800, height=600)

    # We create a new layer, an instance of HelloWorld
    hello_layer = MenuLayer ()

    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene (hello_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run (main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )

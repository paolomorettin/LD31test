#
# cocos2d
# http://cocos2d.org
#

from __future__ import division, print_function, unicode_literals

# This code is so you can run the samples without installing the package
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cocos2d/cocos2d-0.6.0'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cocos2d/pyglet-1.1.4'))
#

import random
import math

import cocos
from cocos.actions import *
from cocos.collision_model import *

from game_entities import BasicMonster, Structure, TurretBase, BasicBullet, CityLayer, MonsterLayer

# A color layer  is a Layer with the a color attribute
class GameLayer(cocos.layer.ColorLayer):
    def __init__(self):
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


        self.city = CityLayer()
        self.monsters = MonsterLayer()
        self.city.set_attackers_layes(self.monsters)
        self.add(self.city)
        self.add(self.monsters)


        for t in range(5):
            turret = TurretBase((100*t, 30))
            self.city.add_structure(turret)
            turret.start()
            
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

    def get_game(self):
        return self

class PlanningLayer(cocos.layer.ColorLayer):
    def __init__(self):
        
        super( PlanningLayer, self ).__init__(0,10,0,255)

        menutitems = []
        menutitems.append( cocos.menu.MenuItem('Start', self.on_new_game ) )
        menutitems.append( cocos.menu.MenuItem('Quit', self.on_quit ) )
        menu = cocos.menu.Menu("Main Menu")
        menu.create_menu( menutitems, cocos.menu.zoom_in(), cocos.menu.zoom_out())
        self.add(menu)

        for t in range(5):
            turret = TurretBase((100*t, 30))
            self.add(turret)

    def on_new_game(self):
        cocos.director.director.push(cocos.scene.Scene(GameLayer()))

    def on_quit(self):
        sys.exit(0)
    
if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(width=800, height=600)

    # We create a new layer, an instance of HelloWorld
    hello_layer = PlanningLayer ()

    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene (hello_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run (main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )

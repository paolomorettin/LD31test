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

class BasicMonster(cocos.sprite.Sprite):
    def __init__(self, position):
        super(BasicMonster, self).__init__("enemy.png", position=position)

    def spawned(self):
        time = random.gauss(15, 10)
        if time < 1:
            time = 1
        self.do(MoveTo((400,0), time))


######
class Structure(cocos.sprite.Sprite):
    def __init__(self, image, dimensions, position):
        super(Structure, self).__init__(image, position=position)
        self.dimensions = dimensions
        self.city=None

    def set_city(self, city):
        self.city=city

class ShooterTurret(Structure):
    def __init__(self, position):
        super(ShooterTurret, self).__init__("shooter.png", (30,30), position)
        self.schedule_interval(self.reload_and_target, 3)
        self.bullets = []

    def reload_and_target(self, dt):
        #print("Check", self.city.attackers.spawned)
        if not self.city.attackers.spawned:
            return
        #print("Reloaded!")
        target = random.choice(self.city.attackers.spawned)
        my_pos = cocos.euclid.Vector2(*self.position)
        other_pos = cocos.euclid.Vector2(*target.position)
        direction = (other_pos - my_pos).normalize()
        direction *= 100
        while len(self.bullets) < 10:
            angle = -cocos.euclid.Vector2(1,0).angle(direction) * 180 / math.pi
            bullet = BasicBullet(self.position, direction,angle , self.city.attackers )
            self.bullets.append(bullet)
        self.schedule_interval(self.shoot_one_bullet, 0.1)


    def shoot_one_bullet(self, dt):
        bb = self.bullets.pop()
        self.city.add(bb)
        bb.shooted()
        if not self.bullets:
            self.unschedule(self.shoot_one_bullet)


######
class BasicBullet(cocos.sprite.Sprite):
    def __init__(self, position, speed, angle, targets):
        super(BasicBullet, self).__init__("bullet.png")
        self.rotation = angle
        self.targets = targets
        self.velocity = speed
        self.position = position

    def shooted(self):
        self.schedule(self.check_hits)
        self.do(Move())

    def check_hits(self, dt):
        # TODO: check if it hits with anybody and call kill
        # out of screen
        if self.position[0] < -100 or self.position[1] < -100 \
           or self.position[0] >900 or self.position[1] > 700:
            self.kill_bullet()

    def kill_bullet(self):
        # is unschedule necessary?
        self.unschedule(self.check_hits)
        self.kill()

#########
class CityLayer(cocos.layer.Layer):
    def __init__(self):
        super(CityLayer, self).__init__()
        self.structures = []
        self.attackers = None

    def add_structure(self, struct):
        self.add(struct)
        struct.set_city(self)
        self.structures.append(struct)

    def set_attackers_layes(self, layer):
        self.attackers = layer

class MonsterLayer(cocos.layer.Layer):
    def __init__(self):
        super(MonsterLayer, self).__init__()
        self.to_spawn = []
        self.delays = []
        self.spawned = []

    def schedule_monster(self, monster, delay):
        self.to_spawn.append(monster)
        self.delays.append(delay)

    def start_spawning(self):
        self.schedule_interval(self.generate_monster, self.delays[0])
        print("scheduled in % seconds" % self.delays[0])

    def generate_monster(self, dt):
        self.unschedule(self.generate_monster)
        print("spawning")
        timepassed=self.delays.pop(0)
        monster=self.to_spawn.pop(0)
        self.add(monster)
        monster.spawned()
        self.spawned.append(monster)
        if self.to_spawn and self.delays:
            self.schedule_interval(self.generate_monster, self.delays[0])
            print("scheduled in % seconds" % self.delays[0])

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

        
        self.city.add_structure(ShooterTurret((100,30)))
        self.city.add_structure(ShooterTurret((200,30)))
        self.city.add_structure(ShooterTurret((300,30)))
        self.city.add_structure(ShooterTurret((400,30)))
        self.city.add_structure(ShooterTurret((500,30)))
        
        for i in range(20):
            m = BasicMonster((i*50, 500))
            self.monsters.schedule_monster(m , 1.0/(i+1))


        self.monsters.start_spawning()
        
        # create a ScaleBy action that lasts 2 seconds
        #scale = ScaleBy(3, duration=2)
        
        # tell the label to scale and scale back and repeat these 2 actions forever
        #label.do( Repeat( scale + Reverse( scale) ) )
        
        # tell the sprite to scaleback and then scale, and repeat these 2 actions forever
        #sprite.do( Repeat( Reverse(scale) + scale ) )

if __name__ == "__main__":
    # director init takes the same arguments as pyglet.window
    cocos.director.director.init(width=800, height=600)

    # We create a new layer, an instance of HelloWorld
    hello_layer = GameLayer ()

    # A scene that contains the layer hello_layer
    main_scene = cocos.scene.Scene (hello_layer)

    # And now, start the application, starting with main_scene
    cocos.director.director.run (main_scene)

    # or you could have written, without so many comments:
    #      director.run( cocos.scene.Scene( HelloWorld() ) )

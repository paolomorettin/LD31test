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

def rect2cshape(rect):
    return AARectShape(rect.center, rect.size[0]/2, rect.size[1]/2)


class BasicMonster(cocos.sprite.Sprite):
    def __init__(self, position):
        super(BasicMonster, self).__init__("enemy.png", position=position)
        ## TODO: was doing collisions here
        self.cshape = rect2cshape(self.get_rect())

    def spawned(self):
        time = random.gauss(30, 10)
        if time < 5:
            time = 5
        self.do(MoveTo((self.position[0],30), time) +
                CallFunc(self.reached_target))

    def reached_target(self):
        print("you lose!")
        self.parent.child_killed(self)
        self.kill()

    def hit(self, bullet):
        print("AAARGH!")
        self.parent.child_killed(self)
        self.kill()

    def get_game():
        return self.parent.get_game()

######
class Structure(cocos.sprite.Sprite):
    def __init__(self, image, dimensions, position):
        super(Structure, self).__init__(image, position=position)
        self.dimensions = dimensions
        self.city=None

    def set_city(self, city):
        self.city=city

    def start(self):
        pass

    def stop(self):
        pass
    
    def get_game():
        return self.parent.get_game()

class TurretBase(Structure):
    def __init__(self, position):
        super(TurretBase, self).__init__("shooter.png", (30,30), position)
        self.bullets = []
        self.nrbullets = 5
        self.bulletinterval = 0.2
        self.burstinterval = 3

    def start(self):
        self.schedule_interval(self.reload_and_target, self.burstinterval)
        self.bullets = []

    def stop(self):
        self.unschedule(self.reload_and_target)
        self.unschedule(self.shoot_one_bullet)

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
        while len(self.bullets) < self.nrbullets:
            # la formula dell'angolo e' ottenuta con trial and error. non toccare piu' :)
            angle = -cocos.euclid.Vector2(1,0).angle(direction) * 180 / math.pi
            bullet = BasicBullet(self.position, direction, angle, self.city.attackers )
            self.bullets.append(bullet)
        self.schedule_interval(self.shoot_one_bullet, self.bulletinterval)


    def shoot_one_bullet(self, dt):
        bb = self.bullets.pop()
        self.city.add(bb)
        bb.shooted()
        if not self.bullets:
            self.unschedule(self.shoot_one_bullet)

    def get_game():
        return self.parent.get_game()
    
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
        self.cshape = rect2cshape(self.get_rect())
        colliding = self.targets.collision.objs_colliding(self)
        for m in colliding:
            m.hit(self)
        if colliding:
            self.kill_bullet()
            return
        # TODO: check if it hits with anybody and call kill
        # out of screen
        if self.position[0] < -100 or self.position[1] < -100 \
           or self.position[0] >900 or self.position[1] > 700:
            self.kill_bullet()

    def kill_bullet(self):
        # is unschedule necessary?
        self.unschedule(self.check_hits)
        self.kill()

    def get_game(self):
        return self.parent.get_game()
#########
class CityLayer(cocos.layer.Layer):
    def __init__(self):
        super(CityLayer, self).__init__()
        self.structures = []
        self.attackers = None

    def add_structure(self, struct):
        self.structures.append(struct)

    def set_attackers_layes(self, layer):
        self.attackers = layer

    def get_game(self):
        return self._game

    def set_game_layer(self, gl):
        self._game = gl

    def start(self):
        for s in self.structures:
            self.add(s)
            s.set_city(self)
            s.start()
    
    def stop(self):
        for s in self.structures:
            s.stop()
    
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
        self.schedule_interval(self.regen_collision_grid, 0.2) # not done every frame to speed up things
        print("scheduled in % seconds" % self.delays[0])

    def regen_collision_grid(self, dt):
        self.collision = CollisionManagerGrid(0,800,0,600, 100, 100)
        for m in self.spawned:
            m.cshape = rect2cshape(m.get_rect())
            self.collision.add(m)

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

    def child_killed(self, child):
        # poor child :'(
        self.collision.remove_tricky(child)
        self.spawned.remove(child)
        if (not self.spawned) and (not self.to_spawn):
            # finished all monsters :(
            self.get_game().game_over()

    def get_game(self):
        return self.parent.get_game()

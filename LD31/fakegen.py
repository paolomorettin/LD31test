
from datastructures import GameMapData, LevelData
import random

g = GameMapData()
l = LevelData()
for x in range(26):
    for y in range(20):
        l.matrix[(x*2+1,y*2+1)] = 0
        
        l.matrix[(x*2+2,y*2+1)] = random.choice([1,0,0,0,0])
        l.matrix[(x*2,  y*2+1)] = random.choice([1,0,0,0,0])
        l.matrix[(x*2+1,y*2  )] = random.choice([1,0,0,0,0])
        l.matrix[(x*2+1,y*2+2)] = random.choice([1,0,0,0,0])
g.levels[0] = l
g.save("level.dat")

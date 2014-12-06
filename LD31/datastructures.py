""" low level data structures for file saving/loading """

import pickle

class GameMapData:
    """ Holds the map of the entire game """
    def __init__(self):
        self.blocks = {} # int -> BlockData

    @classmethod
    def load(fname):
        with open(fname,"r") as f:
            return pickle.load(f)

    @classmethod
    def save(map, fname):
        with open(fname,"w") as f:
            return pickle.dump(f, map)

class BlockData:
    """ Holds the multiple versions of a block in the map """
    def __init__(self):
        self.level = {} # int -> BlockLevelData

class BlockLevelData:
    """ Holds the data of a single version of a block"""
    def __init__(self):
        self.matrix = {} # (int, int) -> int
        self.triggers = []

class TriggerData:
    """ Trigger that is present in a block """
    def __init__(self):
        self.block = 0
        self.newlevel = 0


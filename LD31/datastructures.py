""" low level data structures for file saving/loading """

import pickle

class GameMapData:
    """ Holds the map of the entire game """
    def __init__(self):
        # levelnumber -> LevelData
        self.levels = {} # int -> LevelData

    @staticmethod
    def load(fname):
        with open(fname,"r") as f:
            return pickle.load(f)

    def save(map, fname):
        with open(fname,"w") as f:
            pickle.dump(map, f)

class LevelData:
    """ All the data in a block """
    def __init__(self):
        self.matrix = {} # (int, int) -> int
        self.triggers = {} # (int, int) -> TriggerDatax

class TriggerData:
    """ Trigger that is present in a block """
    def __init__(self):
        self.block = 0
        self.newlevel = 0




class Stage :
    def __init__(self,stagemap) :
        
        if len(set(map(len,stagemap))) == 1 :
        self.size = len(stagemap[0]),len(stagemap)
        for y in xrange(self.size[1]) :
            for x in xrange(self.size[0]) :
                self.map[(x,y)] = 'FLOOR' if stagemap[y][x] == 0 else 'WALL'

class Game :
    def __init(self,stage) :
        self.stage = stage

    def executePrograms(self) :
        for bot in self.bots :
            bot.execute()

    def evaluateActions(self) :
        '''
        Evaluates the actions in the current turn. Actions are concurrent, and the evaluation order is the following:
        - move
        - shoot
        - turn
        - wait

        '''
        moving_bots = [bot for bot in self.bots if bot.action.startswith('MOVE')]
        shooting_bots = [bot for bot in self.bots if bot.action = 'SHOOT']
        turning_bots = [bot for bot in self.bots if bot.action.starstwith('TURN')]

        # evaluates MOVE actions
        destinations = {}

        # destination of not moving bots is their actual position
        for bot in [b for b in self.bots if not bot.action.startswith('MOVE')] :
            destinations[bot.position] = [bot]

        for bot in moving_bots :
            if bot.orientation == 0 :
                step = (1,0)
            elif bot.orientation == 90 :
                step = (0,-1)
            elif bot.orientation == 180 :
                step = (-1,0)
            elif bot.orientation == 270 :
                step = (0,1)
            else :
                raise ValueError("Orientation not in [0,90,180,270]")

            if bot.action.endswith('FORWARD') :
                next_pos = (bot.position[0]+step[0],bot.position[1]+step[1])
            elif bot.action.endswith('BACKWARD') :
                next_pos = (bot.position[0]-step[0],bot.position[1]-step[1])
            else :
                raise ValueError("MOVE ??")
                
            if next_pos in destinations :
                destinations[next_pos].append(bot)
            else :
                destinations[next_pos] = [bot]
        
        # computes the crashes happening (when destinations coincide or are outside the map)
        for crash in [d for d in destinations if len(destinations[d]) > 1 or d[0] < 0 or d[1] < 0 or d[0] >= self.stage.size[0] or d[1] >= self.stage.size[1]] :
            for bot in destination[crash] :
                bot.status = 'CRASHED'
                
        # evaluates the SHOOT actions
        for bot in shooting_bots :

            if bot.orientation == 0 :
                step = (1,0)
            elif bot.orientation == 90 :
                step = (0,-1)
            elif bot.orientation == 180 :
                step = (-1,0)
            elif bot.orientation == 270 :
                step = (0,1)
            else :
                raise ValueError("Orientation not in [0,90,180,270]")
            
            target = bot.position
            for i in xrange(bot.fire_range) :
                target = (target[0] + step[0],target[1] + step[1])
                if self.stage.map[target] == 'WALL' :
                    break
                elif target in destinations and len(destinations[target]) == 1 : # if there's only one coming, shoots it, otherwise they'll crash before
                    destinations[target][0].status = 'HIT'
                    break

        # evaluates the TURN actions
        for bot in turning_bots :
            if bot.action.endswith('LEFT') :
                bot.orientation = (bot.orientation + 90) % 360
            elif bot.action.endswith('RIGHT') :
                bot.orientation = (bot.orientation - 90) % 360
            else :
                raise ValueError("Direction to turn not in [LEFT,RIGHT]")        


    
class Bot :
    def __init__(self,program,position=None,orientation=None,FOV=2,fire_range=4) :
        self.program = program
        self.position = position
        self.orientation = orientation
        self.FOV = FOV
        self.fire_range = fire_range
        self.status = 'OPERATIVE'
        self.action = 'WAIT'
        
    def execute(self) :
        for condition,action in self.program :
            if eval(condition) :
                eval(action)
                return

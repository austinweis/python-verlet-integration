import math

def distance(p0, p1):
    dx = p1.x - p0.x
    dy = p1.y - p0.y
    return math.sqrt(dx * dx + dy * dy)

class Engine():
    def __init__(self, pos, followCursor = False, size = 4, color = (255, 0, 0)):
        self.offset = pos
        self.x = pos[0]
        self.y = pos[1]
        self.size = size
        self.color = color
        self.followCursor = followCursor


class Point():
    def __init__(self, pos, oldPos, size = 4, color = (255, 255, 255)):
        self.x = pos[0]
        self.y = pos[1]
        self.ox = oldPos[0]
        self.oy = oldPos[1]
        self.size = size
        self.color = color

class Stick():
    def __init__(self, p0, p1, thickness = 3, color = (255, 255, 255)):
        self.p0 = p0
        self.p1 = p1
        self.length = distance(p0, p1)
        self.thickness = thickness
        self.color = color

class Form():
    def __init__(self, fPoints, color = (255, 255, 255)):
        if type(fPoints) == type([Point]):  
            self.path = fPoints
        else:
            raise TypeError("Forms.path must be and array of Points")
        self.color = color
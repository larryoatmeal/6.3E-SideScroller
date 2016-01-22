from pygame import Rect
from collections import namedtuple

#Maintains aspect ratio at all times
# Vector = namedtuple('Vector', ['x', 'y'])
# class Vector(list):
#   def __init__(self, x, y):
#       self.x = x
#       self.y = y
#       self.append(x)
#       self.append(y)
#   def __repr__(self):
#       return "Vector(x = {}, y = {})".format(self.x, self.y)
#   def __iter__(self):
#       return iter([self.x, self.y])
# def subVector(v1, v2):
#   return Vector(v1.x - v2.x, v1.y - v2.y)

class Camera:
    #pixW: actual width of screen in pixels
    #pixH: actual height of screen in pixels
    #worldW: how many world units desired in viewport (worldH automatically calculated)
    #worldW should evenly divide both pixW and pixH
    def __init__(self, pixW, pixH, worldW):
        self.pixW = pixW
        self.pixH = pixH
        self.worldW = worldW
        self.worldH = pixH * worldW / pixW
        self.pixelsPerUnit = pixW/worldW
        #top left position in world coordinates
        self.pos = [0, 0]

    def transform(self, rect):
        x = (rect[0] - self.pos[0]) * self.pixelsPerUnit
        y = (rect[1] - self.pos[1]) * self.pixelsPerUnit
        w = rect[2] * self.pixelsPerUnit
        h = rect[3] * self.pixelsPerUnit
        return Rect(x, y, w, h)

    def transformPoint(self, point):
        x = (point[0] - self.pos[0]) * self.pixelsPerUnit
        y = (point[1] - self.pos[1]) * self.pixelsPerUnit
        return (int(x), int(y))

    def scale(self, units):
        return int(self.pixelsPerUnit * units)

    def getRect(self):
        return (self.pos[0], self.pos[1], self.worldW, self.worldH)

if __name__ == "__main__":
    print("Testing Camera.py class")
    cam = Camera(480, 320, 30)
    print(cam.worldW, cam.worldH)
    print("PPU", cam.pixelsPerUnit)
    print(cam.pos)

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)

    print(v1)

    v1.x = 7
    print(v1)
    print(list(v1))
    r = Rect(v1,v2)
    print(r)
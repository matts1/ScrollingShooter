import math
from pyglet.gl import GL_QUADS
import pyglet.graphics

ANGLE = 4
SPEEDMUL = 4


class Rectangle(object):
    def __init__(self, pos1, pos2, batch, group, rgb = [0, 0, 0]):
        [x1, y1] = pos1
        [x2, y2] = pos2
        [r, g, b] = rgb
        self.vertex_list = batch.add(4, GL_QUADS, group,
                                     ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
                                     ('c4B', [r, g, b, 255] * 4))

def DrawHealthBar(x, y, w, h, health, m = 2, maxhealth = 100):
    x -= w
    y -= h
    batch = pyglet.graphics.Batch()
    group = pyglet.graphics.OrderedGroup(1)
    outline = [200, 200, 200]
    color = [150 - health, health, 0]
    Rectangle([x - m, y - m], [x + w + m, y + m], batch, group, outline)
    Rectangle([x - m, y + h - m], [x + w + m, y + h + m], batch, group, outline)
    Rectangle([x - m, y], [x + m, y + h], batch, group, outline)
    Rectangle([x + w - m, y], [x + w + m, y + h], batch, group, outline)
    sides = [x + m, x + w - m]
    w = int(float(health) / maxhealth * (sides[1] - sides[0]))
    Rectangle([x + m, y + m], [x + w + m, y + h - m], batch, group, color)
    return batch

def rotate_movement(angle, x, y, dr = 1):
    angle = math.radians(angle)
    x += SPEEDMUL * (dr * ANGLE * math.sin(angle))
    y += SPEEDMUL * (dr * ANGLE * math.cos(angle))
    return [x, y]

def in_bounds(obj, h, w, xdis = 0, ydis = 0):
    x, y = obj.x, obj.y
    if 0 - xdis >= obj.x: x = 0 - xdis
    if obj.x >= w + xdis: x = w + xdis
    if 0 - ydis >= obj.y: y = 0 - ydis
    if obj.y >= h + ydis: y = h + ydis
    if y == obj.y and x == obj.x: return [1]
    return [0, x, y]

def highscore(score):
    highfile = open('high.txt', 'rU')
    high = int(highfile.read())
    highfile.close()
    print high, "was the highscore"
    print "Your score was", score
    if score > high:
        print "You beat the highscore"
        highfile = open('high.txt', 'w')
        highfile.write(str(score))
        highfile.close()
        
def detect_collision(x, y, obj):
    if obj.x - (obj.width / 2.0) < x < obj.x + (obj.width / 2.0):
        if obj.y < y < obj.y + obj.height:
            return 1
    return 0
    
GRAVITY = 1
FRICTION = 1

def force(vel, forcediff = 0, gravity = GRAVITY):
    return vel + forcediff - gravity
    
def pos(x):
    if x == abs(x):
        return True
    return False

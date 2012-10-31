import math
import pyglet
from pyglet.window import key
from functions import rotate_movement, in_bounds, force, pos

JUMPHEIGHT = 16

FLOOR = 220

SCALE = 0.2

class CharSprite(pyglet.sprite.Sprite):
    def __init__(self):
        self.yvel = 0
        self.dir = True
        self.wpressed = 0
        self.floor = FLOOR
        self.img = pyglet.resource.image('images/Character/animation/1.png')
        self.img.anchor_x = self.hwidth = self.img.width / 2
        self.img.anchor_y = 0
        self.imgrot = self.img.get_transform(True)
        super(CharSprite, self).__init__(self.img)
        self.scale = SCALE
        self.arm = CharArm()
        self.arm.x = self.x
        self.arm.y = self.y
        self.frames = 9
        self.currentframe = self.curanim = 0

    def update(self, keys, x, y):
#ANIMATION
        fpf = 5
        if keys[key.A] or keys[key.D]:
            self.currentframe += 1
            if self.currentframe > (self.frames - 1) * fpf:
                self.currentframe = 1
            if self.currentframe / fpf != self.curanim:
                self.curanim = self.currentframe / fpf
                back = [self.x, self.y, self.img.anchor_x, self.img.anchor_y]
                self.img = pyglet.resource.image('images/Character/animation/' + str(self.curanim+1) + '.png')
                self.imgrot = self.img.get_transform(True)
                if x > self.x:
                    super(CharSprite, self).__init__(self.img)
                else:
                    super(CharSprite, self).__init__(self.imgrot)
                    
                [self.x, self.y, self.img.anchor_x, self.img.anchor_y] = back
                self.imgrot.anchor_x = self.img.anchor_x
                self.imgrot.anchor_y = self.img.anchor_y

#MOVEMENT
        newforce = 0
        self.olddir = self.dir
        self.dir = x - self.x
        if self.dir == 0:
            self.dir = 1
        if (self.dir / abs(self.dir)) != (self.olddir / abs(self.olddir)):
            bx = self.x
            by = self.y
            barm = [self.arm.x, self.arm.y]
            self.arm.update(True)
            [self.arm.x, self.arm.y] = barm
            self.img = self.img.get_transform(True)
            super(CharSprite, self).__init__(self.img)
            self.x = bx
            self.y = by
#ARM            
        diffx = x - self.arm.x
        diffy = y - self.arm.y
        if diffx == 0: diffx = 1
        if diffy == 0: diffy = 1
        self.arm.rotation = -math.degrees(math.atan2(diffy, diffx))
        if not pos(diffx):
            self.arm.rotation += 180
#PHYSICS
        if keys[key.W] and self.wpressed == 0:
            newforce += JUMPHEIGHT
            self.wpressed = 1            
        self.yvel = force(self.yvel, newforce)
        self.y += self.yvel
        if self.y <= FLOOR:
            self.y = FLOOR
            self.wpressed = 0
            if self.yvel < 0:
                self.yvel = 0
        self.arm.x = self.x
        self.arm.y = self.y + (self.arm.img.anchor_y * SCALE)
        
class CharArm(pyglet.sprite.Sprite):
    def __init__(self):
        self.img = pyglet.resource.image('images/Character/weapons/pistol.png')
        self.img.anchor_x = 284
        self.img.anchor_y = 380
        super(CharArm, self).__init__(self.img)
        self.scale = SCALE
    def update(self, turn):
        if turn:
            self.img = self.img.get_transform(True)
            super(CharArm, self).__init__(self.img)
    def changeimg(self, new, dir):
        back = [self.x, self.y, self.img.anchor_x, self.img.anchor_y]
        self.img = pyglet.resource.image('images/Character/weapons/' + new + '.png')
        if pos(dir):
            self.img = self.img.get_transform(True)
        super(CharArm, self).__init__(self.img)
        [self.x, self.y, self.img.anchor_x, self.img.anchor_y] = back

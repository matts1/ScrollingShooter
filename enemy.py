import pyglet
from random import randint
from functions import rotate_movement, force, pos
import math

FLOOR = 215

def spawn_enemy(width):
        if randint(0, 20)== 0:
            enemy = Enemy()
            side = randint(0, 1)
            enemy.x = [width + enemy.width, -enemy.width][side]
            enemy.y = FLOOR
            return enemy
            
        return 0

class Enemy(pyglet.sprite.Sprite):
    def __init__(self):
        self.img = pyglet.resource.image('images/Enemy/animation/1.png')
        self.img.anchor_x, self.img.anchor_y = self.img.width / 2, 0
        self.imgrot = self.img.get_transform(True)
        super(Enemy, self).__init__(self.img)
        self.scale = 0.2
        self.frame = 1

        
        self.dir = True
        if self.x < 0:
            self.dir = False
        
        self.yvel = 0
        self.newforce = 0

        self.health = self.maxhealth = 100

        self.frames = 9
        self.currentframe = self.curanim = 0
        self.xvel = 0

    def update(self, speed, playerx, time):
        diffx = playerx - self.x
#ANIMATION  
        fpf = 5       
        self.currentframe += 1
        if self.currentframe > (self.frames - 1) * fpf:
            self.currentframe = 1
        if self.currentframe / fpf != self.curanim:
            self.curanim = self.currentframe / fpf             
            back = [self.x, self.y, self.img.anchor_x, self.img.anchor_y]
            self.img = pyglet.resource.image('images/Enemy/animation/' + str(self.curanim+1) + '.png')
            if not pos(diffx):
                self.img = self.img.get_transform(True)
 
            super(Enemy, self).__init__(self.img)
            [self.x, self.y, self.img.anchor_x, self.img.anchor_y] = back

#MOVEMENT
        self.olddir = self.dir
        self.x += (diffx / abs(diffx)) * (speed + (time / 1000))
        
        self.dir = pos(diffx)
        
        if self.olddir != pos(diffx):
            backup = [self.x, self.y]
            super(Enemy, self).__init__(self.img)
            [self.x, self.y] = backup
        
        self.yvel = force(self.yvel, self.newforce)
        self.y += self.yvel
        if self.y <= FLOOR:
            self.y = FLOOR
            self.wpressed = 0
            if self.yvel < 0:
                self.yvel = 0

        
        self.xvel = force(self.xvel, self.newforce)
        
        if self.y == FLOOR:
                self.xvel = 0
        self.x += self.xvel

    def fly(self, fx, fy):
        self.yvel += fy
        self.xvel += fx

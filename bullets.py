import pyglet
from functions import rotate_movement, force
VELMUL = 1

class BulletSprite(pyglet.sprite.Sprite):
    def __init__(self):
        image = pyglet.resource.image('images/Character/bullet.png')
        image.anchor_x = image.width / 2
        image.anchor_y = image.height / 2
        self.movex = self.movey = 0
        super(BulletSprite, self).__init__(image)

    def update(self):
        if not self.movex:
            self.movex, self.movey = rotate_movement(self.rotation, self.x, self.y, 3)
            self.movex -= self.x
            self.movey -= self.y
            self.movex *= VELMUL
            self.movey *= VELMUL
            
        self.movey = force(self.movey, 0, 0.25)
        self.x += self.movex
        self.y += self.movey

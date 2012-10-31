import pyglet

class BackGround(pyglet.sprite.Sprite):
    def __init__(self):
        image = pyglet.resource.image('images/back.png')
        #self.scale = 0.5
        super(BackGround, self).__init__(image)

class BACK(pyglet.sprite.Sprite):
    def __init__(self):
        image = pyglet.resource.image('images/back.jpg')
        #self.scale = 0.5
        super(BACK, self).__init__(image)

class Door(pyglet.sprite.Sprite):
    def __init__(self):
        self.img = pyglet.resource.image("images/door.png")
        self.img.anchor_x = self.img.anchor_y = 0
        super(Door, self).__init__(self.img)
        

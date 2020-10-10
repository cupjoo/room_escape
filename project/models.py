from abc import *
from bangtal import *


class Formatter:
    @staticmethod
    def get_image(name, idx):
        prefix = 'images/'
        postfix = '.png'
        return prefix + name + str(idx) + postfix

    @staticmethod
    def get_effect(name, idx):
        effect = '_effect'
        return Formatter.get_image(name+effect, idx)


class Creature(Object, metaclass=ABCMeta):
    def __init__(self, x, y, scene):
        super().__init__('')
        self.x = x
        self.y = y
        self.img = None
        self.handler = None
        self.scene = scene

    def add_handler(self, handler):
        self.handler = handler

    def remove(self):
        self.handler.remove_creature(self)

    def onMouseAction(self, x, y, action):
        self.handler.handle_action(self.x, self.y)

    @abstractmethod
    def action(self, x, y, damage):
        pass


class Monster(Creature):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.hp = 0
        self.status = 1
        self.dist = 15

    def action(self, x, y, damage):
        if self.x == x and self.y == y:
            self.move()
            self.hp -= damage
            if self.hp <= 0:
                super().remove()
                self.hide()

    def move(self):
        self.x -= self.dist
        self.status = 3-self.status
        super().locate(self.scene, self.x, self.y)
        super().setImage(Formatter.get_image(self.img, self.status))


class Boss(Monster):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.hp = 10
        self.img = 'boss'
        super().setImage(Formatter.get_image(self.img, 1))
        super().locate(scene, self.x, self.y)
        super().show()


class Warrior(Monster):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.hp = 3
        self.img = 'warrior'
        super().setImage(Formatter.get_image(self.img, 1))
        super().locate(scene, self.x, self.y)
        super().show()


class Zombie(Monster):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.hp = 1
        self.img = 'zombie'
        super().setImage(Formatter.get_image(self.img, 1))
        super().locate(scene, self.x, self.y)
        super().show()


class Tower(Creature):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.status = 3

    def onMouseAction(self, x, y, action):
        pass

    def action(self, x, y, damage):
        self.status = int(y/140)+1
        super().setImage(Formatter.get_image(self.img, self.status))
        Bomb(x, y, self.img, self.scene).start()


class Cannon(Tower):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.img = 'cannon'
        self.damage = 1
        super().setImage(Formatter.get_image(self.img, self.status))
        super().locate(scene, self.x, self.y)
        super().show()


class Tank(Tower):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.img = 'tank'
        self.damage = 3
        super().setImage(Formatter.get_image(self.img, self.status))
        super().locate(scene, self.x, self.y)
        super().show()


class Bomb(Timer):
    def __init__(self, x, y, img, scene):
        self.delay = 0.09
        super().__init__(self.delay)
        self.count = 1
        self.x = x-30
        self.y = y
        self.img = img
        self.scene = scene
        self.object= Object(Formatter.get_effect(img, self.count))
        self.object.locate(self.scene, self.x, self.y)
        self.object.show()

    def onTimeout(self):
        self.count += 1
        self.object.setImage(Formatter.get_effect(self.img, self.count))
        if self.count < 4:
            self.set(self.delay)
            self.start()
        else:
            self.object.hide()

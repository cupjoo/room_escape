from abc import *
from bangtal import *


class Formatter:
    @staticmethod
    def get_image(name, idx):
        prefix = 'images/'
        postfix = '.png'
        return prefix + name + str(idx) + postfix


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

    def is_bound(self, x, y):
        return True if self.x == x and self.y == y else False

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
        self.move()
        # self.hp -= damage
        # # print(str(self.x)+','+str(self.y)+' ('+str(self.hp)+')')
        # if self.hp <= 0:
        #     super().remove()
        #     self.hide()

    def move(self):
        self.x -= self.dist
        self.status = 3-self.status
        super().locate(self.scene, self.x, self.y)
        super().setImage(Formatter.get_image(self.img, self.status))
        pass


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


class Cannon(Creature):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.img = 'cannon'
        self.status = 3
        super().setImage(Formatter.get_image(self.img, 3))
        super().locate(scene, self.x, self.y)
        super().show()

    def is_bound(self, x, y):
        return True

    def action(self, x, y, damage):
        y_pos = 0
        for i in range(5):
            if y == y_pos:
                self.status = i+1
                super().setImage(Formatter.get_image(self.img, self.status))
            y_pos += 140

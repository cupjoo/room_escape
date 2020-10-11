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
        self.delay = 0
        self.damage = 0
        self.movable = True
        self.movement = None

    def start(self):
        self.movement = Movement(self, self.delay)
        self.movement.start()

    def hide(self):
        self.stop()
        super().hide()

    def stop(self):
        self.movable = False
        self.movement.stop()

    def action(self, x, y, damage):
        if self.x == x and self.y == y:
            self.hp -= damage
            if self.hp <= 0:
                self.handler.remove_creature(self)

    def move(self):
        if self.movable:
            self.x -= self.dist
            self.status = 3-self.status
            super().locate(self.scene, self.x, self.y)
            super().setImage(Formatter.get_image(self.img, self.status))
            self.handler.decrease_life(self)


class Movement(Timer):
    def __init__(self, monster, delay):
        self.delay = delay
        self.monster = monster
        super().__init__(self.delay)

    def onTimeout(self):
        self.monster.move()
        self.set(self.delay)
        self.start()


class Boss(Monster):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.hp = 8
        self.img = 'boss'
        self.delay = 0.15
        self.damage = self.hp
        super().setImage(Formatter.get_image(self.img, 1))
        super().locate(scene, self.x, self.y)
        super().show()
        super().start()


class Warrior(Monster):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.hp = 4
        self.img = 'warrior'
        self.delay = 0.125
        self.damage = self.hp
        super().setImage(Formatter.get_image(self.img, 1))
        super().locate(scene, self.x, self.y)
        super().show()
        super().start()


class Zombie(Monster):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.hp = 2
        self.img = 'zombie'
        self.delay = 0.2
        self.damage = self.hp
        super().setImage(Formatter.get_image(self.img, 1))
        super().locate(scene, self.x, self.y)
        super().show()
        super().start()


class Tower(Creature):
    def __init__(self, x, y, scene):
        super().__init__(x, y, scene)
        self.img = 'cannon'
        self.status = 3
        self.damage = 1
        self.size = 0.7
        self.diff = -20
        self.upgraded = False

        super().setImage(Formatter.get_image(self.img, self.status))
        super().locate(scene, self.x, self.y)
        super().show()

    def onMouseAction(self, x, y, action):
        pass

    def action(self, x, y, damage):
        self.status = int(y/140)+1
        super().setImage(Formatter.get_image(self.img, self.status))
        Bomb(x+self.diff, y, self.size, self.scene).start()

    def upgrade(self):
        if self.upgraded is False:
            self.img = 'tank'
            self.damage = 2
            self.size = 1.2
            self.diff = -60
            self.upgraded = True
            super().setImage(Formatter.get_image(self.img, self.status))


class Bomb(Timer):
    def __init__(self, x, y, size, scene):
        self.delay = 0.09
        super().__init__(self.delay)
        self.count = 1
        self.img = 'tower'
        self.object = Object(Formatter.get_effect(self.img, self.count))
        self.object.setScale(size)
        self.object.locate(scene, x, y)
        self.object.show()

    def onTimeout(self):
        self.count += 1
        self.object.setImage(Formatter.get_effect(self.img, self.count))
        if self.count < 4:
            self.set(self.delay)
            self.start()
        else:
            self.object.hide()

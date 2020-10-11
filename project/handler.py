from project.models import *
import random
import copy


class EventHandler:
    def __init__(self):
        self.life = 220
        self.line = 220
        self.max_life = self.life
        self.tower = None
        self.monsters = []

    def add_tower(self, tower):
        self.tower = tower

    def has_no_damage(self):
        return self.max_life == self.life

    def upgrade_tower(self):
        self.tower.upgrade()

    def add_creature(self, creature):
        creature.add_handler(self)
        self.monsters.append(creature)

    def remove_creature(self, creature):
        creature.hide()
        self.monsters.remove(creature)

    def handle_action(self, x, y):
        self.tower.action(x, y, 2)
        for c in self.monsters:
            c.action(x, y, self.tower.damage)

    def stop_monsters(self):
        for c in self.monsters:
            c.stop()

    def has_no_life(self):
        return self.life <= 0

    def decrease_life(self, monster):
        if self.line >= monster.x:
            self.life -= monster.damage
            self.remove_creature(monster)
            if self.has_no_life():
                self.stop_monsters()


class GameManager:
    def __init__(self, scene):
        self.scene = scene
        self.wave = 1
        self.monsters = [
            [],
            [10, 0, 0],
            [7, 3, 0],
            [4, 6, 0],
            [0, 8, 2],
            [0, 0, 10],
        ]
        self.mob_order = []
        self.pos_order = []
        self.handler = EventHandler()
        self.handler.add_tower(Tower(100, 280, self.scene))

    def generate_mob(self, idx):
        mob = self.mob_order[idx]
        pos = self.pos_order[(self.wave+idx) % 10]
        x = 1080
        y = 140 * pos
        monster = None

        if mob == 0:
            monster = Zombie(x, y, self.scene)
        elif mob == 1:
            monster = Warrior(x, y, self.scene)
        else:
            monster = Boss(x, y, self.scene)
        self.handler.add_creature(monster)

    def random_generate(self):
        self.mob_order = []
        self.pos_order = [0, 3, 1, 2, 4, 0, 3, 1, 2, 4]

        # set order of monster
        monsters = copy.deepcopy(self.monsters[self.wave])
        for idx in range(len(monsters)):
            for i in range(monsters[idx]):
                self.mob_order.append(idx)
        random.shuffle(self.mob_order)

        # generate monsters in positions
        self.upgrade_tower()
        print(self.wave)
        Generator(self).start()

    def has_no_life(self):
        return self.handler.has_no_life()

    def next_wave(self):
        if self.wave < 5:
            self.wave += 1
            self.random_generate()

    def upgrade_tower(self):
        if self.handler.has_no_damage() and self.wave > 2:
            self.handler.upgrade_tower()


class Generator(Timer):
    def __init__(self, manager):
        self.delay = 1.3
        self.count = 0
        self.manager = manager
        super().__init__(3)

    def onTimeout(self):
        if self.count < 10 and self.manager.has_no_life() is False:
            self.manager.generate_mob(self.count)
            self.count += 1
            self.set(self.delay)
            self.start()
        else:
            self.count = 0
            self.manager.next_wave()

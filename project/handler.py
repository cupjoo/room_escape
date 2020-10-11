from project.models import *
import copy


class EventHandler:
    def __init__(self):
        self.life = 10
        self.line = 220
        self.tower = None
        self.monsters = []

    def add_tower(self, tower):
        self.tower = tower

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

    def end_game(self):
        for c in self.monsters:
            c.stop()

    def check_life(self, monster):
        if self.line >= monster.x:
            self.life -= monster.damage
            self.remove_creature(monster)
            if self.life <= 0:
                self.end_game()


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
        self.handler.add_tower(Cannon(100, 280, self.scene))

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
        self.mob_order.sort()

        # generate monsters in positions
        Generator(self).start()

    def upgrade_tower(self):
        pass


class Generator(Timer):
    def __init__(self, manager):
        self.delay = 2.5
        self.count = 0
        self.manager = manager
        super().__init__(self.delay)

    def onTimeout(self):
        if self.count < 10:
            self.manager.generate_mob(self.count)
            self.count += 1
            self.set(self.delay)
            self.start()

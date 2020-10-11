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

    def check_life(self, monster):
        if self.line >= monster.x:
            self.life -= monster.damage
            self.remove_creature(monster)
            if self.life <= 0:
                self.end_game()

    def end_game(self):
        for c in self.monsters:
            c.stop()

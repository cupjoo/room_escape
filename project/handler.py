class EventHandler:
    def __init__(self):
        self.tower = None
        self.monsters = []

    def add_tower(self, tower):
        self.tower = tower

    def add_creature(self, creature):
        creature.add_handler(self)
        self.monsters.append(creature)

    def remove_creature(self, creature):
        self.monsters.remove(creature)

    def handle_action(self, x, y):
        self.tower.action(x, y, 2)
        for c in self.monsters:
            c.action(x, y, self.tower.damage)

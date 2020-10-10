class EventHandler:
    def __init__(self):
        self.creatures = []

    def add_creature(self, creature):
        creature.add_handler(self)
        self.creatures.append(creature)

    def remove_creature(self, creature):
        self.creatures.remove(creature)

    def handle_action(self, x, y):
        print(str(x)+','+str(y)+' clicked (rem : '+str(len(self.creatures))+')')
        for c in self.creatures:
            if c.is_bound(x, y):
                c.action(x, y, 2)

# Handles AI commands per entity

class UnitAI:
    def __init__(self, ent):
        self.ent = ent

    def tick(self, dt):
        if self.ent.command != None:
            self.ent.command.tick(dt)

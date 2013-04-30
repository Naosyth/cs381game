from vector import Vector3


class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        print "starting Game mgr"

    def init(self):
        self.loadLevel()

    def loadLevel(self):
        self.game1()

    def game1(self):
        x = 0
        for entType in self.engine.entityMgr.entTypes:
            print "GameMgr Creating", str(entType)
            ent = self.engine.entityMgr.createEnt(entType, pos = Vector3(x, 0, 0))
            print "GameMgr Created: ", ent.uiname, ent.eid
            x += 300

    def tick(self, dt):
        pass

    def stop(self):
        pass
        


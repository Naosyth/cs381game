from vector import Vector3
import command

class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        print "starting Game mgr"

    def init(self):
        self.loadLevel()

    def loadPlayer(self):
        self.engine.entityMgr.playerObject = self.engine.entityMgr.createEnt(self.engine.entityMgr.playerType, pos = Vector3(0, 0, 0))

    def loadLevel(self):
        self.loadPlayer()
        self.game1()

    def game1(self):
        x = 300
        for entType in self.engine.entityMgr.enemyTypes:
            ent = self.engine.entityMgr.createEnt(entType, pos = Vector3(x, 0, 0))
            ent.command = command.Chase(ent, self.engine.entityMgr.playerObject)
            x += 300
            
        for entType in self.engine.entityMgr.escortTypes:
            ent = self.engine.entityMgr.createEnt(entType, pos = Vector3(x, 0, 0))
            x += 300

    def tick(self, dt):
        pass

    def stop(self):
        pass
        


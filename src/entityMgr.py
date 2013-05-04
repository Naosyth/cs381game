# Entity Manager
# Stores the list of entities that will appear on the map, as well as the actual list of spawned entities

from vector import Vector3

class EntityMgr:
    def __init__(self, engine):
        print "starting ent mgr"
        self.engine = engine
                
    def init(self):
        self.ents = {}
        self.nEnts = 0
        import ent
        self.playerType = ent.PlayerShip
        self.escortTypes = [ent.EscortShip]
        self.enemyTypes = [ent.EnemyFighter, ent.EnemyFighter, ent.EnemyFighter, ent.EnemyFighter]
        
        self.playerObject = None

    def createEnt(self, entType, pos = Vector3(0,0,0)):
        ent = entType(self.engine, self.nEnts, pos = pos)
        print "EntMgr created: ", ent.uiname, ent.eid, self.nEnts
        ent.init()
        self.ents[self.nEnts] = ent;
        self.nEnts = self.nEnts + 1
        return ent

    def tick(self, dt):
        for eid, ent in self.ents.iteritems():
            ent.tick(dt)
        


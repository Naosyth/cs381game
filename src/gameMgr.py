# Game Manager
# Handle the creation of all ships involved in the game, and assign initial AI commands

import random
from vector import Vector3
import command

class GameMgr:
    def __init__(self, engine):
        self.engine = engine
        print "starting Game mgr"

    def init(self):
        self.loadLevel()

    # Load the player ship.
    def loadPlayer(self):
        self.engine.entityMgr.playerObject = self.engine.entityMgr.createEnt(self.engine.entityMgr.playerType)

    def loadLevel(self):
        self.loadPlayer()
        self.game1()

    # Load the various types of ships found in the game and assign AI commands as necessary
    def game1(self):
        self.engine.entityMgr.escortShip = self.engine.entityMgr.createEnt(self.engine.entityMgr.escortType, Vector3(900, -300, 500))
    
        x = 300
        for entType in self.engine.entityMgr.enemyTypes:
            ent = self.engine.entityMgr.createEnt(entType, Vector3(x, 0, 0))
            ent.command = command.Chase(ent, random.choice([self.engine.entityMgr.playerObject, self.engine.entityMgr.escortShip]))
            x += 300
        
        # Spawn 30 inactive bullets
        for i in xrange(30):
            ent = self.engine.entityMgr.createProjectile(self.engine.entityMgr.projectileTypes[0])
        for i in xrange(30):
            ent = self.engine.entityMgr.createProjectile(self.engine.entityMgr.projectileTypes[1])

    def tick(self, dt):
        pass

    def stop(self):
        pass
        


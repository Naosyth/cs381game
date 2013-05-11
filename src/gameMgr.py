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
        #self.loadLevel()
        self.totalTime = 0.0
        self.gameBottomText = ""
        self.won = False

    # Load the player ship.
    def loadPlayer(self):
        self.engine.entityMgr.playerObject = self.engine.entityMgr.createEnt(self.engine.entityMgr.playerType)

    def loadLevel(self):
        self.loadPlayer()
        self.game1()

    # Load the various types of ships found in the game and assign AI commands as necessary
    def game1(self):
        self.engine.entityMgr.escortShip = self.engine.entityMgr.createEnt(self.engine.entityMgr.escortType, Vector3(2700, -1500, 900))
    
        # Warp Gate
        self.engine.entityMgr.warpGate = self.engine.entityMgr.createObstacle(self.engine.entityMgr.warpGateType, Vector3(-900, 300, -500))
    
        # Asteroids
        self.engine.entityMgr.createObstacle(self.engine.entityMgr.asteroidType, Vector3(0, 900, 0))
        self.engine.entityMgr.createObstacle(self.engine.entityMgr.asteroidType, Vector3(400, 1200, -1000))
        self.engine.entityMgr.createObstacle(self.engine.entityMgr.asteroidType, Vector3(1900, -900, -500))
        self.engine.entityMgr.createObstacle(self.engine.entityMgr.asteroidType, Vector3(2300, -700, 700))
        self.engine.entityMgr.createObstacle(self.engine.entityMgr.asteroidType, Vector3(-1900, 1400, 500))
        self.engine.entityMgr.createObstacle(self.engine.entityMgr.asteroidType, Vector3(0, -800, -1300))
    
        for entType in self.engine.entityMgr.enemyTypes:
            ent = self.engine.entityMgr.createEnt(entType, self.engine.entityMgr.escortShip.pos + Vector3(random.randint(-2400, 2400), random.randint(-2400, 2400), random.randint(-2400, 2400)))
            ent.command = command.Chase(ent, random.choice([self.engine.entityMgr.playerObject, self.engine.entityMgr.escortShip]))
        
        # Spawn 30 inactive bullets
        for i in xrange(30):
            ent = self.engine.entityMgr.createProjectile(self.engine.entityMgr.projectileTypes[0])
        for i in xrange(30):
            ent = self.engine.entityMgr.createProjectile(self.engine.entityMgr.projectileTypes[1])

    def tick(self, dt):
        self.totalTime += dt
        if self.totalTime < 5:
            self.gameBottomText = "Welcome to NaoSpace!"
        elif self.totalTime < 10:
            self.gameBottomText = "You can press F1 for help"
        elif self.totalTime < 15:
            self.gameBottomText = "F1 will also pause the game"
        elif self.totalTime < 20:
            self.gameBottomText = "Good luck!"
        elif self.totalTime < 25:
            self.gameBottomText = ""

    def stop(self):
        pass
        


import ogre.renderer.OGRE as ogre
import math

import command

class NPCMgr:
    def __init__(self, engine):
        self.engine = engine
        print "NPC Manager Constructed"
        
    def init(self):
        self.escortShip = self.engine.entityMgr.escortShip
        self.escortPath = [command.Move(self.escortShip, ogre.Vector3(2300, -1200, 900), False), 
                           command.Move(self.escortShip, ogre.Vector3(0, 300, -500), False), 
                           command.Move(self.escortShip, ogre.Vector3(-900, 300, -500), False), 
                           command.Move(self.escortShip, ogre.Vector3(-1000, 300, -500), True)]
        self.escortPathStep = 0
        self.escortPathSize = 4
        
    def updateEscortShip(self):
        if not self.escortShip == None:
            if self.escortShip.command == None and self.escortPathStep < self.escortPathSize:
                self.escortShip.command = self.escortPath[self.escortPathStep]
                self.escortPathStep += 1
        
    def tick(self, dtime):
        # Game end cases
        if self.engine.entityMgr.escortShip.health <= 0:
            self.engine.pause()
            self.engine.overlayMgr.setOverlay("Credits")
            self.engine.gameMgr.won = False
        elif self.engine.entityMgr.playerObject.health <= 0:
            self.engine.pause()
            self.engine.overlayMgr.setOverlay("Credits")
            self.engine.gameMgr.won = False
        elif self.escortShip.command == None and self.escortPathStep >= self.escortPathSize:
            self.engine.pause()
            self.engine.overlayMgr.setOverlay("Credits")
            self.engine.gameMgr.won = True
        self.updateEscortShip()


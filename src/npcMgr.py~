import ogre.renderer.OGRE as ogre
import math

import command

class NPCMgr:
    def __init__(self, engine):
        self.engine = engine
        print "NPC Manager Constructed"
        
    def init(self):
        self.escortShip = self.engine.entityMgr.escortShip
        self.escortPath = [command.Move(self.escortShip, ogre.Vector3(100, 100, 100), False), 
                           command.Move(self.escortShip, ogre.Vector3(-700, 1300, 800), False), 
                           command.Move(self.escortShip, ogre.Vector3(0, -1500, 0), True)]
        self.escortPathStep = 0
        self.escortPathSize = 3
        
    def updateEscortShip(self):
        if not self.escortShip == None:
            if self.escortShip.command == None and self.escortPathStep < self.escortPathSize:
                self.escortShip.command = self.escortPath[self.escortPathStep]
                self.escortPathStep += 1
        
    def tick(self, dtime):
        self.updateEscortShip()


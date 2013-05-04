# Simple Collision for 381Engine
# 
# Oliver Yancey

import ogre.renderer.OGRE as ogre
import utils
import math

class Collision:
    def __init__(self, ent):
        self.ent = ent
        self.id = self.ent.eid
        self.collideRadius = ent.collideRadius
        
    def tick(self, dtime):
        for eid, ent in self.ent.engine.entityMgr.ents.iteritems():
            # Get distance of ent and compare to others.  Set collide flag if within radius
            if self.id != eid:
                self.distance = self.ent.pos.squaredDistance(ent.pos)
                if self.distance <= self.collideRadius:
                    pass #print "Collision detected"
                else:
                    pass #print "Distance: " + str(self.distance)

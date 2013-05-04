# Command Aspect
# Simple AI for 381 Engine
#
# Brandon Worl

import math

import ogre.renderer.OGRE as ogre
Quaternion = ogre.Quaternion

from vector import Vector3

class Command:
    def __init__(self):
        pass

    def tick(self, dt):
        pass

# Orient towards the target ship and move towards it.
class Chase(Command):
    def __init__(self, ent, target):
        self.ent = ent
        self.target = target

    def tick(self, dt):
        # Face the target ship
        dir = self.ent.pos-self.target.pos
        dir.normalise()
        right = Vector3(dir.z,0,-dir.x)
        right.normalise()
        up = dir.crossProduct(right)
        self.ent.orientation = Quaternion.Slerp(dt, self.ent.orientation, Quaternion(right,up,dir), True)
        
        # Accelerate towards the target ship
        self.ent.desiredSpeed = self.ent.maxSpeed
        
# Applied when an enemy ship is close enough to a target. Orients the ship towards the target and shoots at it
class Attack(Command):
    def __init__(self, ent, target):
        self.ent = ent
        self.target = target
    
    def tick(self, dt):
        pass

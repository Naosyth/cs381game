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
        
        if self.ent.pos.distance(self.target.pos) < self.ent.attackRange/2:
            self.ent.command = Attack(self.ent, self.target)
        
# Applied when an enemy ship is close enough to a target. Orients the ship towards the target and shoots at it
class Attack(Command):
    def __init__(self, ent, target):
        self.ent = ent
        self.target = target
    
    def tick(self, dt):
        self.ent.desiredSpeed = 0
        self.ent.vel *= 0.5
        
        # Face the target ship
        dir = self.ent.pos-self.target.pos
        dir.normalise()
        right = Vector3(dir.z,0,-dir.x)
        right.normalise()
        up = dir.crossProduct(right)
        self.ent.orientation = Quaternion.Slerp(dt, self.ent.orientation, Quaternion(right,up,dir), True)
        
        if self.ent.canFire:
            bullet = self.ent.engine.entityMgr.getNextProjectile("enemyBullet")
            bullet.fire(self.ent)
            self.ent.canFire = False
        
# Move an entity to a particular set of coordinates
class Move(Command):
    def __init__(self, ent, destination, stopAtDest=False):
        self.ent = ent
        self.destination = destination
        self.stopAtDest = stopAtDest
        
    def tick(self, dt):
        # Face the destination coordinates
        dir = self.ent.pos-self.destination
        dir.normalise()
        right = Vector3(dir.z,0,-dir.x)
        right.normalise()
        up = dir.crossProduct(right)
        self.ent.orientation = Quaternion.Slerp(dt, self.ent.orientation, Quaternion(right,up,dir), True)
        
        # Velocity
        # Figure out stopping distance
        distToDest = self.ent.pos.distance(self.destination)
        
        if self.stopAtDest:
            stopDist = self.ent.speed/(2*self.ent.acceleration*dt*dt)
            if distToDest > stopDist:
                self.ent.desiredSpeed = self.ent.maxSpeed
            else:
                self.ent.desiredSpeed = 0
        else:
            self.ent.desiredSpeed = self.ent.maxSpeed
            
        if distToDest < 10:
            self.ent.command = None
            self.ent.vel *= 0
            
    def isAtDestination(self):
        return self.ent.pos.distance(self.destination) < 30


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
        
        self.chaseTime = 0.0
        self.moveAway = True
        #self.randPreference = random.randint(0, 1)

    def tick(self, dt):
        if self.ent.health <= 0:
            return
            
        self.chaseTime += dt
        if self.chaseTime > 5.0:
            self.moveAway = False
            
        # Face the target ship
        dir = self.ent.pos-self.target.pos
        dir.normalise()
        if self.moveAway:
            dir *= -1
        right = Vector3(dir.z,0,-dir.x)
        right.normalise()
        up = dir.crossProduct(right)
        self.ent.orientation = Quaternion.Slerp(dt, self.ent.orientation, Quaternion(right,up,dir), True)
        
        # Accelerate towards the target ship
        self.ent.desiredSpeed = self.ent.maxSpeed
        
        if self.ent.pos.distance(self.target.pos) < self.ent.attackRange and self.moveAway == False:
            self.ent.command = Attack(self.ent, self.target)
        
# Applied when an enemy ship is close enough to a target. Orients the ship towards the target and shoots at it
class Attack(Command):
    def __init__(self, ent, target):
        self.ent = ent
        self.target = target
        
        self.attackTime = 0.0
    
    def tick(self, dt):
        if self.ent.health <= 0:
            return
            
        self.attackTime += dt
        if self.attackTime > 6.0:
            self.ent.command = Chase(self.ent, self.target)
            return
            
        self.ent.desiredSpeed = 0
        self.ent.vel *= 0.5
        
        # Estimate where the target will be
        projectileSpeed = 300.0
        dist = self.ent.pos.distance(self.target.pos)
        timeToTarget = dist/projectileSpeed+0.2
        targetPos = self.target.pos+(self.target.vel*timeToTarget)
        
        # Face the target ship
        dir = self.ent.pos-targetPos
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


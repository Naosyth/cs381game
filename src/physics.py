# Physics Aspect
# Simple oriented 3D physics
#
# Brandon Worl

#from vector import Vector3
import ogre.renderer.OGRE as ogre
import utils
import math

class ShipPhysics:
    def __init__(self, ent):
        self.ent = ent
        
    def tick(self, dtime):
        if self.ent.health <= 0:
            return
            
        #----------position-----------------------------------
        timeScaledAcceleration = self.ent.acceleration * dtime
        self.ent.speed += utils.clamp( self.ent.desiredSpeed - self.ent.speed, -timeScaledAcceleration, timeScaledAcceleration)
        
        forwardVec = ogre.Vector3(0, 0, -1)
        currentDirection = self.ent.orientation * forwardVec
        
        self.ent.vel.x = currentDirection.x * self.ent.speed
        self.ent.vel.y = currentDirection.y * self.ent.speed
        self.ent.vel.z = currentDirection.z * self.ent.speed
        
        self.ent.pos = self.ent.pos + (self.ent.vel * dtime)

        #------------heading----------------------------------
        timeScaledRotation = self.ent.turningRate * dtime
        
        temp = ogre.Quaternion()
        temp.FromAngleAxis((self.ent.yawRate*self.ent.turningRate)*dtime, ogre.Vector3(0, 1, 0))
        self.ent.orientation *= temp

        temp = ogre.Quaternion()
        temp.FromAngleAxis((self.ent.pitchRate*self.ent.turningRate)*dtime, ogre.Vector3(1, 0, 0))
        self.ent.orientation *= temp
        
class ProjectilePhysics:
    def __init__(self, ent):
        self.ent = ent
        
    def tick(self, dtime):
        if not self.ent.isActive:
            return
            
        #----------position-----------------------------------
        forwardVec = ogre.Vector3(0, 0, -1)
        currentDirection = self.ent.orientation * forwardVec
        
        self.ent.vel = currentDirection * self.ent.speed
        self.ent.pos = self.ent.pos + (self.ent.vel * dtime)

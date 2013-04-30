# Simple ORIENTED Physics for 38Engine
# vel is rate of change of pos
# Sushil Louis

#from vector import Vector3
import ogre.renderer.OGRE as ogre
import utils
import math

class Physics:
    def __init__(self, ent):
        self.ent = ent
        
    def tick(self, dtime):
        #----------position-----------------------------------
        timeScaledAcceleration = self.ent.acceleration * dtime
        self.ent.speed += utils.clamp( self.ent.desiredSpeed - self.ent.speed, -timeScaledAcceleration, timeScaledAcceleration)
        
        forwardVec = ogre.Vector3(1, 0, 0)
        currentDirection = self.ent.orientation * forwardVec
        
        self.ent.vel.x = currentDirection.x * self.ent.speed
        self.ent.vel.y = currentDirection.y * self.ent.speed
        self.ent.vel.z = currentDirection.z * self.ent.speed
        
        self.ent.pos = self.ent.pos + (self.ent.vel * dtime)

        #------------heading----------------------------------
        timeScaledRotation = self.ent.turningRate * dtime
        
        temp = ogre.Quaternion()
        temp.FromAngleAxis(ogre.Degree(self.ent.yawRate), ogre.Vector3(0, 1, 0))
        self.ent.orientation *= temp

        temp = ogre.Quaternion()
        temp.FromAngleAxis(ogre.Degree(self.ent.pitchRate), ogre.Vector3(0, 0, 1))
        self.ent.orientation *= temp

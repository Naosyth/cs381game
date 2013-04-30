# Entity class to hold information about entities for 38Engine
# Sushil Louis

import ogre.renderer.OGRE as ogre
Quaternion = ogre.Quaternion

from vector        import Vector3
from physics       import Physics
from render        import Renderer
from unitAI        import UnitAI

#-----------------------------------------------------------------------------------------
class Entity:
    pos  = Vector3(0, 0, 0)
    orientation = Quaternion(0, 0, 0, 1);
    vel  = Vector3(0, 0, 0)

    aspectTypes = [Physics, Renderer, UnitAI]
    
    def __init__(self, engine, id, mesh, pos = Vector3(0,0,0), orientation = Quaternion(0,0,0,1), vel = Vector3(0,0,0)):
        self.engine = engine
        self.uiname = str(id)
        self.eid = id
        self.mesh = mesh
        
        self.pos = pos
        self.orientation = orientation
        self.vel = vel
        self.speed = vel.length()
        
        self.aspects = []

    def init(self):
        self.initAspects()

    def initAspects(self):
        for aspType in self.aspectTypes:
            self.aspects.append(aspType(self))
        
    def tick(self, dtime):
        for aspect in self.aspects:
            aspect.tick(dtime)

    def __str__(self):
        x = "--------------------\nEntity: %s \nPos: %s, Vel: %s,  mesh = %s\nSpeed: %f, desiredSpeed: %f" % (self.uiname, str(self.pos), str(self.vel), self.mesh, self.speed, self.desiredSpeed)
        return x
#-----------------------------------------------------------------------------------------
class GenericShip(Entity):
    def __init__(self, engine, id, mesh, pos = Vector3(0,0,0), orientation = Quaternion(0,0,0,1), vel = Vector3(0,0,0)):
        Entity.__init__(self, engine, id, '', pos = Vector3(0,0,0), orientation = Quaternion(0,0,0,1), vel = Vector3(0,0,0))
        self.mesh = ''
        self.uiname = 'generic' + str(id)

        self.orientation = Quaternion()
        self.orientation.FromAngleAxis(ogre.Degree(0), Vector3(0, 0, 1))

        # Movement
        self.acceleration = 0.0
        self.turningRate  = 0.0
        self.maxSpeed = 0.0
        self.desiredSpeed = 0.0
        self.yawRate = 0.0
        self.pitchRate = 0.0
        self.speed = 0.0
        
        # Control
        self.isPlayerControlled = False
        self.command = None
        
        # Other ship related data
        self.isTargeted = False
        self.health = 100.0
        self.energy = 100.0
        self.fireRate = 10.0
#-----------------------------------------------------------------------------------------
class PlayerShip(GenericShip):
    def __init__(self, engine, id, pos = Vector3(0,0,0), orientation = Quaternion(0,0,0,1), vel = Vector3(0,0,0)):
        GenericShip.__init__(self, engine, id, 'fighter.mesh', pos, orientation, vel)
        self.mesh = 'fighter.mesh'
        self.uiname = 'fighter' + str(id)

        self.orientation = Quaternion()
        self.orientation.FromAngleAxis(ogre.Degree(0), Vector3(0, 0, 1))

        # Movement
        self.acceleration = 20.0
        self.turningRate  = 20.0
        self.maxSpeed = 200.0
        self.desiredSpeed = 0.0
        self.yawRate = 0.0
        self.pitchRate = 0.0
        self.speed = 0.0
        
        # Control
        self.isPlayerControlled = True
        self.command = None
        
        # Other ship related data
        self.isTargeted = False
        self.health = 100.0
        self.energy = 100.0
        self.fireRate = 10.0

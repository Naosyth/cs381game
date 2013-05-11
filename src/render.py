# Rendering Aspect
# Draw the entity with the correct position and orientation
# Also render any particles related to the entity
#
# Brandon Worl

import utils
import math
import ogre.renderer.OGRE as ogre

class ShipRenderer:
    def __init__(self, ent):
        self.ent = ent
        print "Rendering seting up for: ", str(self.ent)
        
        self.gent =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + "_ogreEnt", self.ent.mesh)
        self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname + 'node', ent.pos)
        self.node.attachObject(self.gent)
        self.node.scale(self.ent.scale)

        # Trail Particles
        self.trailNode = self.node.createChildSceneNode()
        self.trailParticle = self.ent.engine.gfxMgr.sceneManager.createParticleSystem(self.ent.uiname + "Trail_ogreEnt", 'Navitas/Trail')
        self.trailNode.attachObject(self.trailParticle)
        
        # Explosion Particles
        self.explosionNode = self.node.createChildSceneNode()
        self.explosionParticle = self.ent.engine.gfxMgr.sceneManager.createParticleSystem(self.ent.uiname + "Explosion_ogreEnt", 'NaoSpace/Explosion')
        self.explosionNode.attachObject(self.explosionParticle)
        self.explosionParticle.setEmitting(False)
        
        self.deathTimer = 0.0
        
        if self.ent.isPlayerControlled:
            self.dustNode = self.node.createChildSceneNode()
            self.dustParticle = self.ent.engine.gfxMgr.sceneManager.createParticleSystem(self.ent.uiname + "Dust_ogreEnt", 'Navitas/Dust')
            self.dustNode.attachObject(self.dustParticle)
        
    def tick(self, dtime):
        self.node.setPosition(self.ent.pos)
        self.node.setOrientation(self.ent.orientation)
        
        # Bounding box is visible if the entity is targeted
        self.node.showBoundingBox(self.ent.isTargeted)
        # Trail Node is visible if the entity is moving
        self.trailParticle.setEmitting(self.ent.speed > 0.05)
        
        if self.ent.health <= 0:
            self.deathTimer += dtime
            
            self.gent.setVisible(False)
            self.trailParticle.setEmitting(False)
            self.explosionParticle.setEmitting(True)
            if self.deathTimer > 2.0:
                self.explosionParticle.setEmitting(False)
        else:
            self.deathTimer = 0.0
            self.explosionParticle.setEmitting(False)
            self.gent.setVisible(True)

class ProjectileRenderer:
    def __init__(self, ent):
        self.ent = ent

        self.gent =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + "_ogreEnt", self.ent.mesh)
        self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname + 'node', ent.pos)
        self.node.attachObject(self.gent)
        self.node.scale(self.ent.scale)
        
    def tick(self, dtime):
        self.node.setPosition(self.ent.pos)
        self.node.setOrientation(self.ent.orientation)
        
        if not self.ent.isActive:
            self.node.setVisible(False)
        else:
            self.node.setVisible(True)
            
class ObstacleRenderer:
    def __init__(self, ent):
        self.ent = ent

        self.gent =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + "_ogreEnt", self.ent.mesh)
        self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname + 'node', ent.pos)
        self.node.attachObject(self.gent)
        self.node.scale(self.ent.scale)
        
    def tick(self, dtime):
        self.node.setPosition(self.ent.pos)
        self.node.setOrientation(self.ent.orientation)


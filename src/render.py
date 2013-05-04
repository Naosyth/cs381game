# Simple Rendering Aspect for 38Engine
# Sushil Louis

#from vector import Vector3
import utils
import math
import ogre.renderer.OGRE as ogre

class Renderer:
    def __init__(self, ent):
        self.ent = ent
        print "Rendering seting up for: ", str(self.ent)
        self.gent =  self.ent.engine.gfxMgr.sceneManager.createEntity(self.ent.uiname + "_ogreEnt", self.ent.mesh)
        self.node =  self.ent.engine.gfxMgr.sceneManager.getRootSceneNode().createChildSceneNode(self.ent.uiname + 'node', ent.pos)
        self.node.attachObject(self.gent)
        self.node.scale(self.ent.scale)

        # Wake Particles
        self.wakeNode = self.node.createChildSceneNode()
        self.wakeParticle = self.ent.engine.gfxMgr.sceneManager.createParticleSystem(self.ent.uiname + "Wake_ogreEnt", 'Navitas/Trail')
        self.wakeNode.attachObject(self.wakeParticle)
        
        self.dustNode = self.node.createChildSceneNode()
        self.dustParticle = self.ent.engine.gfxMgr.sceneManager.createParticleSystem(self.ent.uiname + "Dust_ogreEnt", 'Navitas/Dust')
        self.dustNode.attachObject(self.dustParticle)
        
        # Chase Camera
        self.camera = self.ent.engine.gfxMgr.sceneManager.createCamera(self.ent.uiname + "_camera")
        self.camera.position = self.ent.pos + ogre.Vector3(0, 0, 170)
        self.camera.lookAt(self.ent.pos)
        self.camera.position = self.ent.pos + ogre.Vector3(20, 25, 170)
        self.node.attachObject(self.camera)
        
    def tick(self, dtime):
        #----------update scene node position and orientation-----------------------------------
        self.node.setPosition(self.ent.pos)
        self.node.setOrientation(self.ent.orientation)

        if self.ent.isPlayerControlled:
            self.ent.engine.gfxMgr.viewPort.setCamera(self.camera)
        
        if self.ent.isTargeted:
            self.node.showBoundingBox(True)
        else:
            self.node.showBoundingBox(False)

        if self.ent.speed > 0.025:
            self.wakeNode.setVisible(True)
        else:
            self.wakeNode.setVisible(False)

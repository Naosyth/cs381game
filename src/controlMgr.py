# Simple Keyboard arrows based manual Control Aspect for 38Engine
# Sushil Louis

#from vector import Vector3
import utils
import math
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class ControlMgr:
    toggleMax = 0.1
    def __init__(self, engine):
        self.engine = engine
        print "Control Manager Constructed "
        
    def init(self):
        self.keyboard = self.engine.inputMgr.keyboard
        self.mouse = self.engine.inputMgr.mouse
        self.ms = self.mouse.getMouseState()
        self.toggle = self.toggleMax
        
        self.screenWidth = self.engine.gfxMgr.viewPort.getActualWidth()
        self.screenHeight = self.engine.gfxMgr.viewPort.getActualHeight()
        
        self.playerObject = self.engine.entityMgr.playerObject

    def stop(self):
        pass
        
    def tick(self, dtime):
        # ---------- Mouse Orientation ----------
        deltaX = self.ms.X.abs
        deltaY = self.ms.Y.abs
        
        if not self.playerObject == None:
            if (utils.distSquared2D(self.ms.X.abs, self.ms.Y.abs, self.screenWidth/2, self.screenHeight/2) > 1000):
                self.playerObject.yawRate = -1*float(self.ms.X.abs) / (self.screenWidth/2) + 1
                self.playerObject.pitchRate = -1*float(self.ms.Y.abs) / (self.screenHeight/2) + 1
            else:
                self.playerObject.yawRate = 0
                self.playerObject.pitchRate = 0
        
        #----------make selected ent respond to keyboard controls-----------------------------------
        if self.toggle >= 0:
            self.toggle = self.toggle - dtime

        if  self.toggle < 0:
            self.keyboard.capture()
            if not self.playerObject == None:
                # Speed Up
                if self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_W):
                    self.toggle = self.toggleMax
                    self.playerObject.desiredSpeed = utils.clamp(self.playerObject.desiredSpeed + self.playerObject.acceleration, 0, self.playerObject.maxSpeed)
                # Slow down
                if  self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_S):
                    self.toggle = self.toggleMax
                    self.playerObject.desiredSpeed = utils.clamp(self.playerObject.desiredSpeed - self.playerObject.acceleration, 0, self.playerObject.maxSpeed)
                # Strafe Left.
                if  self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_A):
                    pass
                # Strafe Right.
                if  self.toggle < 0 and self.keyboard.isKeyDown(OIS.KC_D):
                    pass
                # Roll Left.
                if  self.keyboard.isKeyDown(OIS.KC_Q):
                    temp = ogre.Quaternion()
                    temp.FromAngleAxis(self.playerObject.turningRate*dtime, ogre.Vector3(0, 0, 1))
                    self.playerObject.orientation *= temp
                # Roll Right.
                if  self.keyboard.isKeyDown(OIS.KC_E):
                    temp = ogre.Quaternion()
                    temp.FromAngleAxis(-self.playerObject.turningRate*dtime, ogre.Vector3(0, 0, 1))
                    self.playerObject.orientation *= temp


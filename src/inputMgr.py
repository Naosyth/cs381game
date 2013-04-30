# Input manager. Initialize and manage keyboard and mouse. Buffered and unbuffered input
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS


from vector import Vector3
from command       import *


import os


class InputMgr(OIS.KeyListener, OIS.MouseListener, OIS.JoyStickListener):
    def __init__(self, engine):
        self.engine = engine
        OIS.KeyListener.__init__(self)
        OIS.MouseListener.__init__(self)
        OIS.JoyStickListener.__init__(self)
        self.move = 250
        self.rotate = 0.01
        self.yawRot = 0.0
        self.pitchRot = 0.0
        self.transVector = ogre.Vector3(0, 0, 0)
        self.toggle = 0.1
        self.selectionRadius = 100


    def init(self):
        windowHandle = 0
        renderWindow = self.engine.gfxMgr.root.getAutoCreatedWindow()
        windowHandle = renderWindow.getCustomAttributeUnsignedLong("WINDOW")
        paramList = [("WINDOW", str(windowHandle))]

        if os.name == "nt":
            t = [("w32_mouse","DISCL_FOREGROUND"), ("w32_mouse", "DISCL_NONEXCLUSIVE")]
        else:
            t = [("x11_mouse_grab", "false"), ("x11_mouse_hide", "false")]
            #t = [("x11_mouse_grab", "false"), ("x11_mouse_hide", "true")]

        paramList.extend(t)

        self.inputManager = OIS.createPythonInputSystem(paramList)
 
        # Now InputManager is initialized for use. Keyboard and Mouse objects
        # must still be initialized separately
        self.keyboard = None
        self.mouse    = None
        try:
            self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, True)
            self.mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, True)
        except Exception, e:
            print "No Keyboard or mouse!!!!"
            raise e
        if self.keyboard:
            self.keyboard.setEventCallback(self)
        if self.mouse:
            self.mouse.setEventCallback(self)

        self.ms = self.mouse.getMouseState()
 
        self.transVector = ogre.Vector3(0, 0, 0)
        import random
        self.randomizer = random
        self.randomizer.seed(None)
        print "Initialized Input Manager"
        self.crosslink()

    def crosslink(self):
        self.camera = self.engine.gfxMgr.camera
        self.camYawNode = self.engine.gfxMgr.camYawNode
        self.camPitchNode = self.engine.gfxMgr.camPitchNode

    def stop(self):
        self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        self.inputManager.destroyInputObjectMouse(self.mouse)
        OIS.InputManager.destroyInputSystem(self.inputManager)
        self.inputManager = None
        
    def tick(self, dtime):
        self.keyboard.capture()
        self.mouse.capture()

        self.keyPressed(dtime)
        
        #self.camNode.yaw(ogre.Degree(-self.yawRot)
        self.camYawNode.yaw(ogre.Radian(self.yawRot))
        self.camPitchNode.pitch(ogre.Radian(self.pitchRot))

        # Translate the camera based on time.
        self.camYawNode.translate(self.camYawNode.orientation
                               * self.transVector
                               * dtime)

        # Rotate the camera when the Right mouse button is down.
        if self.ms.buttonDown(OIS.MB_Right):
            self.engine.gfxMgr.camYawNode.yaw(ogre.Degree(self.rotate * (-10*self.ms.X.rel)).valueRadians())
            self.engine.gfxMgr.camPitchNode.pitch(ogre.Degree(self.rotate * (-10*self.ms.Y.rel)).valueRadians())

        self.handleModifiers(dtime)
        self.handleCreateEnt(dtime)

    def handleModifiers(self, dtime):
        self.leftShiftDown = self.keyboard.isKeyDown(OIS.KC_LSHIFT)
        self.leftCtrlDown = self.keyboard.isKeyDown(OIS.KC_LCONTROL)

    def handleCreateEnt(self, dt):
        self.toggle = self.toggle - dt
        if self.keyboard.isKeyDown(OIS.KC_EQUALS) and self.toggle < 0.0:
            ent = self.engine.entityMgr.createEnt(self.randomizer.choice(self.engine.entityMgr.entTypes), pos = Vector3(0,0,0))
            self.toggle = 0.1

    def keyPressed(self, evt):
        if self.keyboard.isKeyDown(OIS.KC_ESCAPE):
            self.engine.stop()

        return True

    def keyReleased(self, evt):
        return True
    
       # MouseListener
    def mouseMoved(self, evt):
        return True

    def mousePressed(self, evt, id):
        if id == OIS.MB_Left:
            self.handleMouseSelection(evt)
        if id == OIS.MB_Right:
            self.handleMouseCommand(evt)
        return True

    def handleMouseSelection(self, evt):
        self.mouse.capture()
        self.ms = self.mouse.getMouseState()
        print str(self.ms)

        self.ms.width = self.engine.gfxMgr.viewPort.actualWidth 
        self.ms.height = self.engine.gfxMgr.viewPort.actualHeight
        self.mousePos = (self.ms.X.abs/float(self.ms.width), self.ms.Y.abs/float(self.ms.height))
        mouseRay = self.engine.gfxMgr.camera.getCameraToViewportRay(*self.mousePos)
        result  =  mouseRay.intersects(self.engine.gfxMgr.groundPlane)

        if result.first:
            pos =  mouseRay.getPoint(result.second)
            self.mousePosWorld = pos

            closest = None
            closestDistance = self.selectionRadius * self.selectionRadius
            for ent in self.engine.entityMgr.ents.values():
                distSquared =  ent.pos.squaredDistance(pos)
                if distSquared < closestDistance:
                    closest = ent
                    closestDistance = distSquared

            if closest: # One level deep
                if self.leftShiftDown:
                    self.engine.selectionMgr.addSelectedEnt(closest)
                else:
                    self.engine.selectionMgr.selectEnt(closest)
            else:
                self.engine.selectionMgr.killSelection()

    def handleMouseCommand(self, evt):
        self.mouse.capture()
        self.ms = self.mouse.getMouseState()
        #print str(self.ms)

        # If there is no selected ent, we won't need to apply any commands so we can stop.
        if self.engine.selectionMgr.selectedEnts == []:
            print "no selected ents to command!"
            return

        self.ms.width = self.engine.gfxMgr.viewPort.actualWidth 
        self.ms.height = self.engine.gfxMgr.viewPort.actualHeight
        self.mousePos = (self.ms.X.abs/float(self.ms.width), self.ms.Y.abs/float(self.ms.height))
        mouseRay = self.engine.gfxMgr.camera.getCameraToViewportRay(*self.mousePos)
        result  =  mouseRay.intersects(self.engine.gfxMgr.groundPlane)

        if result.first:
            pos =  mouseRay.getPoint(result.second)
            self.mousePosWorld = pos

            closest = None
            closestDistance = self.selectionRadius * self.selectionRadius
            for ent in self.engine.entityMgr.ents.values():
                distSquared =  ent.pos.squaredDistance(pos)
                if distSquared < closestDistance:
                    closest = ent
                    closestDistance = distSquared

            if closest: # One level deep
                # Clicked a boat, do whatever based on that.
                if self.leftCtrlDown:
                    for selectedEnt in self.engine.selectionMgr.selectedEnts:
                        selectedEnt.command = Intercept(selectedEnt, closest)
                else:
                    for selectedEnt in self.engine.selectionMgr.selectedEnts:
                        selectedEnt.command = Follow(selectedEnt, closest)
            else:
                # Move the selected boat to the clicked location
                for selectedEnt in self.engine.selectionMgr.selectedEnts:
                    selectedEnt.command = Move(selectedEnt, pos)

    def mouseReleased(self, evt, id):
        return True
    
       # JoystickListener
    def buttonPressed(self, evt, button):
        return True
    def buttonReleased(self, evt, button):
        return True
    def axisMoved(self, evt, axis):
        return True


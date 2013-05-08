import utils
import math
import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS

class CameraMgr:
    def __init__(self, engine):
        self.engine = engine
        print "Camera Manager Constructed"
        
    def init(self):
        self.keyboard = self.engine.inputMgr.keyboard
        self.mouse = self.engine.inputMgr.mouse
        self.ms = self.mouse.getMouseState()
        
        self.camera = self.engine.gfxMgr.sceneManager.createCamera("player_camera")
        self.engine.gfxMgr.viewPort.setCamera(self.camera)
        
        self.playerObject = self.engine.entityMgr.playerObject
        
        self.lookYaw = 0
        self.lookPitch = 0

    def stop(self):
        pass
        
    def tick(self, dtime):
        if self.playerObject == None:
            self.playerObject = self.engine.entityMgr.playerObject
            
        self.screenWidth = self.engine.gfxMgr.viewPort.getActualWidth()
        self.screenHeight = self.engine.gfxMgr.viewPort.getActualHeight()
        
        deltaX = self.ms.X.rel
        deltaY = self.ms.Y.rel
        
        if not self.playerObject == None and self.keyboard.isKeyDown(OIS.KC_LSHIFT):
            self.lookYaw = deltaX*0.01
            self.lookPitch = deltaY*0.01
        else:
            self.lookYaw = 0
            self.lookPitch = 0
        
        # Chase Camera
        forwardVec = ogre.Vector3(0, 0, -1)
        playerForwardVec = self.playerObject.orientation * forwardVec
        playerForwardVec.normalise()
        
        upVec = ogre.Vector3(0, 1, 0)
        playerUpVec = self.playerObject.orientation * upVec
        playerUpVec.normalise()
        
        rightVec = ogre.Vector3(1, 0, 0)
        playerRightVec = self.playerObject.orientation * rightVec
        playerRightVec.normalise()
        
        # Holding shift to look around the ship
        # This needs to be improved
        if self.keyboard.isKeyDown(OIS.KC_LSHIFT):
            dir = self.camera.position-self.playerObject.pos
            dir.normalise()
            right = ogre.Vector3(dir.z,0,-dir.x)
            right.normalise()
            up = dir.crossProduct(right)
            self.camera.orientation = ogre.Quaternion(right,up,dir)
            
            self.offsetVec = ogre.Quaternion(self.lookYaw, up) * ogre.Quaternion(self.lookPitch, right) * self.offsetVec
        else:
            self.offsetVec = playerForwardVec
            self.camera.orientation = ogre.Quaternion.Slerp(0.2, self.camera.orientation, self.playerObject.orientation, True)
            
        # Move the camera slightly above the top of the ship
        self.camera.position = self.playerObject.pos + -200*self.offsetVec
        self.camera.position += 30*playerUpVec


import ogre.renderer.OGRE as ogre
import math

class OverlayMgr:
    def __init__(self, engine):
        self.engine = engine
        print "Overlay Manager Constructed"
        
    def init(self):
        self.overlayManager = ogre.OverlayManager.getSingleton()
        
        self.overlayList = []
        self.loadOverlays()
        self.currentOverlay = ""
        self.setOverlay("Splash")
        
    def loadOverlays(self):
        self.overlayList.append(SplashOverlay(self.engine, self.overlayManager))
        self.overlayList.append(GameOverlay(self.engine, self.overlayManager))
        self.overlayList.append(CreditsOverlay(self.engine, self.overlayManager))
        
    def setOverlay(self, name):
        self.currentOverlay = name
        for overlay in self.overlayList:
            overlay.setVisible(overlay.name == name)
        
    def getOverlayByName(self, name):
        for overlay in self.overlayList:
            if overlay.name == self.currentOverlay:
                return overlay
        
    def tick(self, dtime):
        for overlay in self.overlayList:
            if overlay.name == self.currentOverlay:
                overlay.tick(dtime)
     
class Overlay:
    def __init__(self, engine, overlayManager, name):
        self.engine = engine
        
        self.name = name
        self.overlayManager = overlayManager
        self.overlay = self.overlayManager.create(self.name + "Overlay")
        
    def setVisible(self, isVisible):
        if isVisible:
            self.overlay.show()
        else:
            self.overlay.hide()
            
class SplashOverlay(Overlay):
    name = "Splash"
    def __init__(self, engine, overlayManager):
        Overlay.__init__(self, engine, overlayManager, self.name)

        self.loadOverlay()
        
    def loadOverlay(self):
        # Special Features
        # Rotating camera
        self.camera = self.engine.gfxMgr.sceneManager.createCamera(self.name+"_camera")
        self.engine.gfxMgr.viewPort.setCamera(self.camera)
        
        # Static ship
        
        # Static asteroids
        
        # ---------- Logo Graphic ----------------------------------------
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_Logo")
        panel.setPosition(0.1, 0.1)
        panel.setDimensions(0.8, 0.8)
        panel.setMaterialName("Splash_Logo")
        
        self.overlay.add2D(panel)
        # --------------------------------------------------
        
    def tick(self, dtime):
        self.camera.yaw(-3.14/60*dtime)
        
class GameOverlay(Overlay):
    name = "Game"
    def __init__(self, engine, overlayManager):
        Overlay.__init__(self, engine, overlayManager, self.name)

        self.loadOverlay()
        
        self.showHelp = False
        
    def loadOverlay(self):
        # ---------- GUI Background ----------------------------------------
        guiPanel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_GUIPanel")
        guiPanel.setPosition(0.835, 0.005)
        guiPanel.setDimensions(0.16, 0.12)
        guiPanel.setMaterialName("GUI_Grey_Background")
        guiPanel.setBorderMaterialName("GUI_Grey_Border")
        guiPanel.setBorderSize(0.003)
        
        self.overlay.add2D(guiPanel)
        # --------------------------------------------------
    
        # ---------- Health Bar ----------------------------------------
        healthPanel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_HealthPanel")
        healthPanel.setPosition(0.84, 0.01)
        healthPanel.setDimensions(0.15, 0.02)
        healthPanel.setMaterialName("GUI_Health_Bar")
        healthPanel.setBorderMaterialName("GUI_Grey_Border")
        healthPanel.setBorderSize(0.003)
        
        self.healthPanel = healthPanel
        self.overlay.add2D(healthPanel)
        # --------------------------------------------------
        
        # ---------- Energy Bar ----------------------------------------
        energyPanel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_EnergyPanel")
        energyPanel.setPosition(0.84, 0.04)
        energyPanel.setDimensions(0.15, 0.02)
        energyPanel.setMaterialName("GUI_Energy_Bar")
        energyPanel.setBorderMaterialName("GUI_Grey_Border")
        energyPanel.setBorderSize(0.003)
        
        self.energyPanel = energyPanel
        self.overlay.add2D(energyPanel)
        # --------------------------------------------------
        
        # ---------- Score Text ----------------------------------------
        scorePanel = self.overlayManager.createOverlayElement("Panel", self.name+"_ScorePanel")
        scorePanel.setPosition(0.845, 0.08)
        scorePanel.setDimensions(0.15, 0.04)
        
        scoreText = self.overlayManager.createOverlayElement("TextArea", self.name+"_ScoreText")
        scoreText.setMetricsMode(ogre.GMM_PIXELS)
        scoreText.setFontName("BlueHighway")
        scoreText.setCharHeight(20)
        scoreText.setColour(ogre.ColourValue(1, 1, 1))
        scorePanel.addChild(scoreText)
        
        self.scorePanel = scoreText
        self.scorePanel.textArea = scoreText
        self.overlay.add2D(scorePanel)
        # --------------------------------------------------
        
        # ---------- Escort Ship Health Bar ----------------------------------------
        escortHealthPanel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_EscortHealthPanel")
        escortHealthPanel.setPosition(0.25, 0.03)
        escortHealthPanel.setDimensions(0.50, 0.03)
        escortHealthPanel.setMaterialName("GUI_Objective_Bar")
        escortHealthPanel.setBorderMaterialName("GUI_Grey_Border")
        escortHealthPanel.setBorderSize(0.003)
        
        self.escortHealthPanel = escortHealthPanel
        self.overlay.add2D(escortHealthPanel)
        # --------------------------------------------------
        
        # ---------- Crosshair ----------------------------------------
        crosshairPanel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_CrosshairPanel")
        crosshairPanel.setPosition(0.495, 0.53)
        crosshairPanel.setDimensions(0.01, 0.01)
        crosshairPanel.setBorderMaterialName("GUI_Objective_Bar")
        crosshairPanel.setBorderSize(0.0015)
        
        self.crosshairPanel = crosshairPanel
        self.overlay.add2D(crosshairPanel)
        # --------------------------------------------------
        
        # ---------- Bottom Text ----------------------------------------
        bottomPanel = self.overlayManager.createOverlayElement("Panel", self.name+"_BottomPanel")
        bottomPanel.setPosition(0.25, 0.90)
        bottomPanel.setDimensions(0.50, 0.06)
        
        bottomText = self.overlayManager.createOverlayElement("TextArea", self.name+"_BottomText")
        bottomText.setMetricsMode(ogre.GMM_PIXELS)
        bottomText.setFontName("BlueHighway")
        bottomText.setCharHeight(30)
        bottomText.setColour(ogre.ColourValue(1, 1, 1))
        bottomPanel.addChild(bottomText)
        
        self.bottomPanel = bottomText
        self.bottomPanel.textArea = bottomText
        self.overlay.add2D(bottomPanel)
        # --------------------------------------------------
        
        # ---------- Help Screen ----------------------------------------
        help = self.overlayManager.createOverlayElement("Panel", self.name+"_Help")
        help.setPosition(0.1, 0.1)
        help.setDimensions(0.8, 0.8)
        help.setMaterialName("Game_Help")
        help.hide()
        
        self.help = help
        self.overlay.add2D(help)
        # --------------------------------------------------
        
    def tick(self, dtime):
        self.playerObject = self.engine.entityMgr.playerObject
        self.escortShip = self.engine.entityMgr.escortShip
    
        if self.showHelp:    
            self.help.show()
        else:
            self.help.hide()
        
        if not self.playerObject == None and not self.escortShip == None:
            # Ship and player info
            self.healthPanel.setBorderSize(0.003, 0.003+0.144*(1-(self.playerObject.health/self.playerObject.maxHealth)), 0.003, 0.003)
            self.energyPanel.setBorderSize(0.003, 0.003+0.144*(1-(self.playerObject.energy/self.playerObject.maxEnergy)), 0.003, 0.003)
            self.scorePanel.textArea.setCaption("Score: " + str(self.playerObject.score))
            
            # Escort ship's health
            self.escortHealthPanel.setBorderSize(0.003, 0.003+0.49544*(1-(self.escortShip.health/self.escortShip.maxHealth)), 0.003, 0.003)
            
            # Bottom text
            self.bottomPanel.textArea.setCaption(self.engine.gameMgr.gameBottomText)

class CreditsOverlay(Overlay):
    name = "Credits"
    def __init__(self, engine, overlayManager):
        Overlay.__init__(self, engine, overlayManager, self.name)

        self.loadOverlay()
        
    def loadOverlay(self):        
        # ---------- Winner Graphic ----------------------------------------
        winPanel = self.overlayManager.createOverlayElement("Panel", self.name+"_Win")
        winPanel.setPosition(0.1, 0.1)
        winPanel.setDimensions(0.8, 0.8)
        winPanel.setMaterialName("Credits_Win")
        winPanel.hide()
        
        self.winPanel = winPanel
        
        self.overlay.add2D(winPanel)
        # --------------------------------------------------
        
        # ---------- Loser Graphic ----------------------------------------
        losePanel = self.overlayManager.createOverlayElement("Panel", self.name+"_Lose")
        losePanel.setPosition(0.1, 0.1)
        losePanel.setDimensions(0.8, 0.8)
        losePanel.setMaterialName("Credits_Lose")
        losePanel.hide()
        
        self.losePanel = losePanel
        
        self.overlay.add2D(losePanel)
        # --------------------------------------------------
        
    def tick(self, dtime):
        if self.engine.gameMgr.won == True:
            self.winPanel.show()
        else:
            self.losePanel.show()
        pass

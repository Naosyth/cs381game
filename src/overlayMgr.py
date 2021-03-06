import ogre.renderer.OGRE as ogre
import math

class OverlayMgr:
    def __init__(self, engine):
        self.engine = engine
        print "Overlay Manager Constructed"
        
    def init(self):
        self.overlayManager = ogre.OverlayManager.getSingleton()
        
        self.showAboutPage = False
        self.selection = 1
        
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
        
        # ---------- Logo Graphic ----------------------------------------
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_Logo")
        panel.setPosition(0.1, 0.1)
        panel.setDimensions(0.8, 0.8)
        panel.setMaterialName("Splash_Logo")
        
        self.logo = panel
        
        self.overlay.add2D(panel)
        # --------------------------------------------------
        
        # ---------- About Button ----------------------------------------
        panel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_About_Button")
        panel.setPosition(0.45, 0.65)
        panel.setDimensions(0.12, 0.08)
        panel.setMaterialName("Splash_About_Button")
        panel.setBorderMaterialName("GUI_Grey_Border")
        panel.setBorderSize(0.003)
        
        self.aboutButton = panel
        
        self.overlay.add2D(panel)
        # --------------------------------------------------
        
        # ---------- Start Button ----------------------------------------
        panel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_Start_Button")
        panel.setPosition(0.45, 0.5)
        panel.setDimensions(0.12, 0.08)
        panel.setMaterialName("Splash_Start_Button")
        panel.setBorderMaterialName("GUI_Grey_Border")
        panel.setBorderSize(0.003)
        
        self.playButton = panel
        
        self.overlay.add2D(panel)
        # --------------------------------------------------
        
        # ---------- About Graphic ----------------------------------------
        panel = self.overlayManager.createOverlayElement("Panel", self.name+"_About")
        panel.setPosition(0.1, 0.1)
        panel.setDimensions(0.8, 0.8)
        panel.setMaterialName("Splash_About")
        
        self.about = panel
        
        self.overlay.add2D(panel)
        # --------------------------------------------------
        
    def tick(self, dtime):
        self.camera.yaw(-3.14/60*dtime)
        
        if self.engine.overlayMgr.selection == 1:
            self.playButton.setBorderMaterialName("GUI_Red_Border")
            self.aboutButton.setBorderMaterialName("GUI_Grey_Border")
        elif self.engine.overlayMgr.selection == 0:
            self.playButton.setBorderMaterialName("GUI_Grey_Border")
            self.aboutButton.setBorderMaterialName("GUI_Red_Border")
        
        if self.engine.overlayMgr.showAboutPage:
            self.playButton.hide()
            self.aboutButton.hide()
            self.logo.hide()
            self.about.show()
        else:
            self.playButton.show()
            self.aboutButton.show()
            self.logo.show()
            self.about.hide()
        
class GameOverlay(Overlay):
    name = "Game"
    def __init__(self, engine, overlayManager):
        Overlay.__init__(self, engine, overlayManager, self.name)

        self.loadOverlay()
        
        self.showHelp = False
        
    def loadOverlay(self):
        # ---------- GUI Background ----------------------------------------
        background = self.overlayManager.createOverlayElement("Panel", self.name+"_Background")
        background.setPosition(0.0, 0.0)
        background.setDimensions(1.0, 1.0)
        background.setMaterialName("GUI_Background")
        
        self.background = background
        self.overlay.add2D(background)
        # --------------------------------------------------
    
        # ---------- Health Bar ----------------------------------------
        healthPanel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_HealthPanel")
        healthPanel.setPosition(0.77, 0.015)
        healthPanel.setDimensions(0.21, 0.04)
        healthPanel.setMaterialName("GUI_Health_Bar")
        healthPanel.setBorderMaterialName("GUI_Grey_Border")
        healthPanel.setBorderSize(0.003)
        
        self.healthPanel = healthPanel
        self.overlay.add2D(healthPanel)
        # --------------------------------------------------
        
        # ---------- Energy Bar ----------------------------------------
        energyPanel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_EnergyPanel")
        energyPanel.setPosition(0.02, 0.015)
        energyPanel.setDimensions(0.21, 0.04)
        energyPanel.setMaterialName("GUI_Energy_Bar")
        energyPanel.setBorderMaterialName("GUI_Grey_Border")
        energyPanel.setBorderSize(0.003)
        
        self.energyPanel = energyPanel
        self.overlay.add2D(energyPanel)
        # --------------------------------------------------
        
        # ---------- Score Text ----------------------------------------
        scorePanel = self.overlayManager.createOverlayElement("Panel", self.name+"_ScorePanel")
        scorePanel.setPosition(0.45, 0.02)
        scorePanel.setDimensions(0.15, 0.04)
        
        scoreText = self.overlayManager.createOverlayElement("TextArea", self.name+"_ScoreText")
        scoreText.setMetricsMode(ogre.GMM_PIXELS)
        scoreText.setFontName("BlueHighway")
        scoreText.setCharHeight(20)
        scoreText.setColour(ogre.ColourValue(1, 1, 1))
        scorePanel.addChild(scoreText)
        
        self.scorePanel = scorePanel
        self.scorePanel.textArea = scoreText
        self.overlay.add2D(scorePanel)
        # --------------------------------------------------
        
        # ---------- Escort Ship Health Bar ----------------------------------------
        escortHealthPanel = self.overlayManager.createOverlayElement("BorderPanel", self.name+"_EscortHealthPanel")
        escortHealthPanel.setPosition(0.35, 0.07)
        escortHealthPanel.setDimensions(0.30, 0.03)
        escortHealthPanel.setMaterialName("GUI_Objective_Bar")
        escortHealthPanel.setBorderMaterialName("GUI_Grey_Border")
        escortHealthPanel.setBorderSize(0.003)
        
        self.escortHealthPanel = escortHealthPanel
        self.overlay.add2D(escortHealthPanel)
        # --------------------------------------------------
        
        # ---------- Speed Text ----------------------------------------
        speedPanel = self.overlayManager.createOverlayElement("Panel", self.name+"_SpeedPanel")
        speedPanel.setPosition(0.04, 0.95)
        speedPanel.setDimensions(0.15, 0.04)
        
        speedText = self.overlayManager.createOverlayElement("TextArea", self.name+"_SpeedText")
        speedText.setMetricsMode(ogre.GMM_PIXELS)
        speedText.setFontName("BlueHighway")
        speedText.setCharHeight(20)
        speedText.setColour(ogre.ColourValue(1, 1, 1))
        speedPanel.addChild(speedText)
        
        self.speedPanel = speedPanel
        self.speedPanel.textArea = speedText
        self.overlay.add2D(speedPanel)
        # --------------------------------------------------
        
        # ---------- Crosshair ----------------------------------------
        crosshairPanel = self.overlayManager.createOverlayElement("Panel", self.name+"_CrosshairPanel")
        crosshairPanel.setMetricsMode(ogre.GMM_PIXELS)
        crosshairPanel.setLeft(-20)
        crosshairPanel.setTop(-12)
        crosshairPanel.setHorizontalAlignment(ogre.GHA_CENTER)
        crosshairPanel.setVerticalAlignment(ogre.GVA_CENTER)
        crosshairPanel.setDimensions(40, 40)
        crosshairPanel.setMaterialName("GUI_Reticle")
        
        self.crosshairPanel = crosshairPanel
        self.overlay.add2D(crosshairPanel)
        # --------------------------------------------------
        
        # ---------- Bottom Text ----------------------------------------
        bottomPanel = self.overlayManager.createOverlayElement("Panel", self.name+"_BottomPanel")
        bottomPanel.setPosition(0.50, 0.94)
        bottomPanel.setDimensions(0.40, 0.06)
        
        bottomText = self.overlayManager.createOverlayElement("TextArea", self.name+"_BottomText")
        bottomText.setMetricsMode(ogre.GMM_PIXELS)
        bottomText.setFontName("BlueHighway")
        bottomText.setCharHeight(30)
        bottomText.setColour(ogre.ColourValue(1, 1, 1))
        bottomText.setAlignment(ogre.TextAreaOverlayElement.Alignment.Center)
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
        
        # ---------- Mouse ----------------------------------------
        mousePanel = self.overlayManager.createOverlayElement("Panel", self.name+"_MousePanel")
        mousePanel.setMetricsMode(ogre.GMM_PIXELS)
        mousePanel.setDimensions(32, 32)
        mousePanel.setMaterialName("GUI_Mouse")
        
        self.mousePanel = mousePanel
        self.overlay.add2D(mousePanel)
        # --------------------------------------------------
        
    def tick(self, dtime):
        self.playerObject = self.engine.entityMgr.playerObject
        self.escortShip = self.engine.entityMgr.escortShip
    
        if self.showHelp:    
            self.help.show()
        else:
            self.help.hide()
        
        if not self.playerObject == None and not self.escortShip == None:
            # Cursor
            self.mousePanel.setPosition(self.engine.controlMgr.ms.X.abs-8, self.engine.controlMgr.ms.Y.abs-8)
               
            # Ship and player info
            self.healthPanel.setBorderSize(0.003, 0.003+0.204*(1-(self.playerObject.health/self.playerObject.maxHealth)), 0.003, 0.003)
            self.energyPanel.setBorderSize(0.003, 0.003+0.204*(1-(self.playerObject.energy/self.playerObject.maxEnergy)), 0.003, 0.003)
            self.scorePanel.textArea.setCaption("Score: " + str(self.playerObject.score))
            
            # Escort ship's health
            self.escortHealthPanel.setBorderSize(0.003, 0.003+0.294*(1-(self.escortShip.health/self.escortShip.maxHealth)), 0.003, 0.003)
            
            # Bottom text
            self.bottomPanel.textArea.setCaption(self.engine.gameMgr.gameBottomText)
            
            # Velocity display
            self.speedPanel.textArea.setCaption(str(math.floor(self.playerObject.speed)) + " m/s")

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

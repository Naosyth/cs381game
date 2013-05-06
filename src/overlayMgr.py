import ogre.renderer.OGRE as ogre
import math

class OverlayMgr:
    def __init__(self, engine):
        self.engine = engine
        print "Overlay Manager Constructed"
        
    def init(self):
        self.overlayManager = ogre.OverlayManager.getSingleton()
        self.overlay = self.overlayManager.create("GUIOverlay")
    
        self.playerObject = self.engine.entityMgr.playerObject
        self.escortShip = self.engine.entityMgr.escortShip
        
        # Create overlays
        self.createPlayerGUI()     
        
    def createPlayerGUI(self):
        # ---------- GUI Background ----------------------------------------
        # GUI panel
        guiPanel = self.overlayManager.createOverlayElement("BorderPanel", "GUIPanel")
        guiPanel.setPosition(0.835, 0.005)
        guiPanel.setDimensions(0.16, 0.12)
        guiPanel.setMaterialName("GUI_Grey_Background")
        guiPanel.setBorderMaterialName("GUI_Grey_Border")
        guiPanel.setBorderSize(0.003)
        
        # Add panel to overlay
        self.overlay.add2D(guiPanel)
        self.overlay.show()
        # --------------------------------------------------
    
        # ---------- Health Bar ----------------------------------------
        # Health panel
        healthPanel = self.overlayManager.createOverlayElement("BorderPanel", "HealthPanel")
        healthPanel.setPosition(0.84, 0.01)
        healthPanel.setDimensions(0.15, 0.02)
        healthPanel.setMaterialName("GUI_Health_Bar")
        healthPanel.setBorderMaterialName("GUI_Grey_Border")
        healthPanel.setBorderSize(0.003)
        
        self.healthPanel = healthPanel
        
        # Add panel to overlay
        self.overlay.add2D(healthPanel)
        self.overlay.show()
        # --------------------------------------------------
        
        # ---------- Energy Bar ----------------------------------------
        # Energy Panel
        energyPanel = self.overlayManager.createOverlayElement("BorderPanel", "EnergyPanel")
        energyPanel.setPosition(0.84, 0.04)
        energyPanel.setDimensions(0.15, 0.02)
        energyPanel.setMaterialName("GUI_Energy_Bar")
        energyPanel.setBorderMaterialName("GUI_Grey_Border")
        energyPanel.setBorderSize(0.003)
        
        self.energyPanel = energyPanel
        
        # Add panel to overlay
        self.overlay.add2D(energyPanel)
        self.overlay.show()
        # --------------------------------------------------
        
        # ---------- Score Text ----------------------------------------
        # Score panel
        scorePanel = self.overlayManager.createOverlayElement("Panel", "ScorePanel")
        scorePanel.setPosition(0.845, 0.08)
        scorePanel.setDimensions(0.15, 0.04)
        
        # Score panel text
        scoreText = self.overlayManager.createOverlayElement("TextArea", "ScoreText")
        scoreText.setMetricsMode(ogre.GMM_PIXELS)
        scoreText.setFontName("BlueHighway")
        scoreText.setCharHeight(20)
        scoreText.setColourBottom(ogre.ColourValue(1, 1, 1))
        scoreText.setColourTop(ogre.ColourValue(1, 1, 1))
        scoreText.show()
        
        # Link panel to text
        self.scorePanel = scoreText
        self.scorePanel.textArea = scoreText
        scorePanel.addChild(scoreText)
        
        # Add panel to overlay
        self.overlay.add2D(scorePanel)
        self.overlay.show()
        # --------------------------------------------------
        
        # ---------- Escort Ship Health Bar ----------------------------------------
        # Energy Panel
        escortHealthPanel = self.overlayManager.createOverlayElement("BorderPanel", "EscortHealthPanel")
        escortHealthPanel.setPosition(0.25, 0.03)
        escortHealthPanel.setDimensions(0.50, 0.03)
        escortHealthPanel.setMaterialName("GUI_Objective_Bar")
        escortHealthPanel.setBorderMaterialName("GUI_Grey_Border")
        escortHealthPanel.setBorderSize(0.003, 0.00156+0.144*(1/(self.playerObject.energy)), 0.003, 0.003)
        escortHealthPanel.setBorderSize(0.003)
        
        self.escortHealthPanel = escortHealthPanel
        
        # Add panel to overlay
        self.overlay.add2D(escortHealthPanel)
        self.overlay.show()
        # --------------------------------------------------
        
        # ---------- Bottom Text ----------------------------------------
        # Bottom panel
        bottomPanel = self.overlayManager.createOverlayElement("Panel", "BottomPanel")
        bottomPanel.setPosition(0.25, 0.90)
        bottomPanel.setDimensions(0.50, 0.06)
        
        # Score panel text
        bottomText = self.overlayManager.createOverlayElement("TextArea", "BottomText")
        bottomText.setMetricsMode(ogre.GMM_PIXELS)
        bottomText.setFontName("BlueHighway")
        bottomText.setCharHeight(30)
        bottomText.setColourBottom(ogre.ColourValue(1, 1, 1))
        bottomText.setColourTop(ogre.ColourValue(1, 1, 1))
        bottomText.show()
        
        # Link panel to text
        self.bottomPanel = bottomText
        self.bottomPanel.textArea = bottomText
        bottomPanel.addChild(bottomText)
        
        # Add panel to overlay
        self.overlay.add2D(bottomPanel)
        self.overlay.show()
        # --------------------------------------------------
        
    def tick(self, dtime):
        if not self.playerObject == None:
            # Ship and player info
            self.healthPanel.setBorderSize(0.003, 0.003+0.144*(1-(self.playerObject.health/self.playerObject.maxHealth)), 0.003, 0.003)
            self.energyPanel.setBorderSize(0.003, 0.003+0.144*(1-(self.playerObject.energy/self.playerObject.maxEnergy)), 0.003, 0.003)
            self.scorePanel.textArea.setCaption("Score: " + str(self.playerObject.score))
            
            # Escort ship's health
            self.escortHealthPanel.setBorderSize(0.003, 0.003+0.49544*(1-(self.escortShip.health/self.escortShip.maxHealth)), 0.003, 0.003)
            
            # Bottom text
            #self.bottomPanel.textArea.setCaption("Protect the cargo ship from enemy fighters!")


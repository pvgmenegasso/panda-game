from typing import Tuple
from direct.showbase.ShowBase import ShowBase
from entities.world.level import gen_level

from graphics.model_loader import load_model

from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
import sys
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode, NodePath, LightAttrib
from panda3d.core import LVector3





class World(DirectObject):

    def __init__(self, base : ShowBase):  # The initialization method caused 
        # The standard camera position and background initialization
        base.setBackgroundColor(0, 0, 0)
        base.disable_mouse()

        self.setupLights()

        taskMgr.add(self.move_light)

        # The standard title text that's in every tutorial
        # Things to note:
        #-fg represents the forground color of the text in (r,g,b,a) format
        #-pos  represents the position of the text on the screen.
        #      The coordinate system is a x-y based wih 0,0 as the center of the
        #      screen
        #-align sets the alingment of the text relative to the pos argument.
        #      Default is center align.
        #-scale set the scale of the text
        #-mayChange argument lets us change the text later in the program.
        #       By default mayChange is set to 0. Trying to change text when
        #       mayChange is set to 0 will cause the program to crash.
        self.title = OnscreenText(
            text="Untitled RTS game",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07)


        self.model = gen_level()

        self.timer = 0
        
    def setupLights(self):  # Sets up some default lighting
        self.ambientLight = AmbientLight("ambientLight")
        self.ambientLight.setColor((.4, .4, .35, 1))
        self.directionalLight = DirectionalLight("directionalLight")
        self.directionalLight.setDirection(LVector3(0, 8, -2.5))
        self.directionalLight.setColor((0.9, 0.8, 0.9, 1))
        render.setLight(render.attachNewNode(self.directionalLight))
        render.setLight(render.attachNewNode(self.ambientLight))

    def move_light(self, task):
        if self.timer >= 30:
            self.timer = 0
            if self.directionalLight.getDirection()[1] < 30:
                self.directionalLight.setDirection(self.directionalLight.getDirection()+LVector3(1, 1, 0))
            else:
                self.directionalLight.setDirection(LVector3(0, 0, -2.5))
        else:
            self.timer += 1
        return task.cont

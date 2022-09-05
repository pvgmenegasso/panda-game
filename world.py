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
        camera.setPos(0, 0, 125)
        camera.setHpr(0, -60, 0)
        self.cam_vec = (0, 0)
        self.setupLights()

        taskMgr.add(self.move_cam, "moveTask")
        taskMgr.add(self.move_light)


        # # The global variables we used to control the speed and size of objects
        # self.yearscale = 60
        # self.dayscale = self.yearscale / 365.0 * 5
        # self.orbitscale = 10
        # self.sizescale = 0.6sss

        #self.loadPlanets()  # Load, texture, and position the planets
        #self.rotatePlanets()  # Set up the motion to start them moving

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

        # self.mouse1EventText = self.genLabelText(
        #     "Mouse Button 1: Toggle entire Solar System [RUNNING]", 1)
        # self.skeyEventText = self.genLabelText("[S]: Toggle Sun [RUNNING]", 2)
        # self.ykeyEventText = self.genLabelText("[Y]: Toggle Mercury [RUNNING]", 3)
        # self.vkeyEventText = self.genLabelText("[V]: Toggle Venus [RUNNING]", 4)
        # self.ekeyEventText = self.genLabelText("[E]: Toggle Earth [RUNNING]", 5)
        # self.mkeyEventText = self.genLabelText("[M]: Toggle Mars [RUNNING]", 6)
        # self.yearCounterText = self.genLabelText("0 Earth years completed", 7)

        # self.yearCounter = 0  # year counter for earth years
        # self.simRunning = True  # boolean to keep track of the
        # # state of the global simulation


        # Now that we have finished basic initialization, we call loadPlanets which
        # will handle actually getting our objects in the world
        self.model = gen_level()

        self.timer = 0

        self.accept("w", self.delta_cam, [(0, 1)])
        self.accept("s", self.delta_cam, [(0, -1)])
        self.accept("a", self.delta_cam, [(-1, 0)])
        self.accept("d", self.delta_cam, [(1, 0)])
        self.accept("w-up", self.delta_cam, [(0, 0)])
        self.accept("s-up", self.delta_cam, [(0, 0)])
        self.accept("a-up", self.delta_cam, [(0, 0)])
        self.accept("d-up", self.delta_cam, [(0, 0)])
        

        

    def setupLights(self):  # Sets up some default lighting
        self.ambientLight = AmbientLight("ambientLight")
        self.ambientLight.setColor((.4, .4, .35, 1))
        self.directionalLight = DirectionalLight("directionalLight")
        self.directionalLight.setDirection(LVector3(0, 8, -2.5))
        self.directionalLight.setColor((0.9, 0.8, 0.9, 1))
        render.setLight(render.attachNewNode(self.directionalLight))
        render.setLight(render.attachNewNode(self.ambientLight))


    def move_cam(self, task):
        camera.setX(camera.getX()+2*self.cam_vec[0])
        camera.setY(camera.getY()+2*self.cam_vec[1])

        return task.cont

    def move_light(self, task):
        print(self.directionalLight.get_direction())
        if self.timer >= 30:
            self.timer = 0
            if self.directionalLight.getDirection()[1] < 30:
                self.directionalLight.setDirection(self.directionalLight.getDirection()+LVector3(1, 1, 0))
            else:
                self.directionalLight.setDirection(LVector3(0, 0, -2.5))
        else:
            self.timer += 1
        return task.cont

    def delta_cam(self, direction : Tuple[int, int]):
        if direction[0] > 0:
            if self.cam_vec[0] < 1:
                self.cam_vec = (1, self.cam_vec[1])
        elif direction[0] < 0:
            if self.cam_vec[0] > -1:
                self.cam_vec  = (-1, self.cam_vec[1])
        elif direction[1] > 0:
            if self.cam_vec[1] < 1:
                self.cam_vec = (self.cam_vec[0], 1)
        elif direction[1] < 0:
            if self.cam_vec[0] > -1:
                self.cam_vec = (self.cam_vec[0], -1)
        else:
            self.cam_vec = (0,0)




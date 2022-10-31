import copy
from dataclasses import InitVar, dataclass, field
from typing import Any, ClassVar, Optional, Tuple
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase, builtins
from direct.task.Task import Task
from direct.gui.DirectGui import *
from panda3d.core import TextNode, NodePath
from entities.buildings.building import Building
from entities.world.resource import Resource
from graphics.model_loader import load_model

# A simple function to make sure a value is in a given range, -1 to 1 by
# default
def clamp(i, mn=-1, mx=1) -> int:
    return min(max(i, mn), mx)

@dataclass
class Player(DirectObject):
    
    base : InitVar[ShowBase]
    resources          : dict[int, Resource] = field(default_factory=Resource.load_resources)
    player_buildings   : dict[int, list[Any]] = field(default_factory=dict)
    resource_texts     : dict[int, OnscreenText] = field(default_factory=dict)
    default_buildings  : ClassVar[list[Building]] = Building.load_buildings()
    selected_building  : int = 0
    object             : Optional[Any] = field(default=None)
    camera             : NodePath = camera
    

    def __post_init__(self, base: ShowBase) -> None:
        
        self.base = base

        print(self.resources.items())

        index = 0
        for id, res in self.resources.items():
            self.resource_texts[id] = OnscreenText(
                text=str(res),
                parent=self.base.a2dTopLeft, align=TextNode.A_left,
                style=1, fg=(1, 1, 1, 1), pos=(0, -0.1-(0.1*index)), scale=.07)
            index += 1

        
        self.camera.setPos(0, 0, 125)
        self.camera.setHpr(0, -60, 0)
        self.cam_vec = (0, 0)

        self.set_obj()

        # Now we add a task that will take care of turning the head
        taskMgr.add(self.move_obj, "move_obj")
        taskMgr.add(self.move_cam, "moveTask")
        taskMgr.add(self.set_housing)
        taskMgr.add(self.show_res)

        self.accept("w", self.delta_cam, [(0, 1)])
        self.accept("s", self.delta_cam, [(0, -1)])
        self.accept("a", self.delta_cam, [(-1, 0)])
        self.accept("d", self.delta_cam, [(1, 0)])
        self.accept("escape", self.unset_obj)
        self.accept("mouse1", self.place_obj)
        self.accept("wheel_up", self.next_obj)
        self.accept("wheel-down", self.next_obj, [False])
        self.accept("w-up", self.delta_cam, [(0, 0)])
        self.accept("s-up", self.delta_cam, [(0, 0)])
        self.accept("a-up", self.delta_cam, [(0, 0)])
        self.accept("d-up", self.delta_cam, [(0, 0)])



        super().__init__()

    def show_res(self, task) -> None:
        for id, res in self.resources.items():
            self.resource_texts[id].setText(str(res))
        return task.cont

    def place_obj(self) -> None:
        object = filter(lambda x: x.id==self.selected_building, Player.default_buildings).__next__()
        cost = object.cost
        can_buy = True
        for id, value in object.cost.items():
            if self.resources[id].value < value:
                can_buy = False
                break

        if can_buy:
            for id, value in object.cost.items():
                self.resources[id].use(value)
            if not self.player_buildings.get(id):
                self.player_buildings[id] = []
            self.player_buildings[id].append(
                load_model(
                    object.model_file,
                    render,
                    position=(self.object.getX(), self.object.getY(), self.object.getZ())
                )
            )


    def next_obj(self, backwards : bool = False) -> None:
        direction = 1
        if not self.selected_building:
            self.selected_building = 0
        else:
            if backwards:
                direction = -1
            if self.selected_building + direction < 0:
                self.selected_building = len(self.default_buildings)
            elif self.selected_building +  direction > len(self.default_buildings) -1 :
                self.selected_building = 0
        self.set_obj()

    def move_cam(self, task):
        self.camera.setX(self.camera.getX()+2*self.cam_vec[0])
        self.camera.setY(self.camera.getY()+2*self.cam_vec[1])

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

    def move_obj(self, task):
        if self.object:
            # Check to make sure the mouse is readable
            if self.base.mouseWatcherNode.hasMouse():
                # get the mouse position as a LVector2. The values for each axis are from -1 to
                # 1. The top-left is (-1,-1), the bottom right is (1,1)
                mpos = self.base.mouseWatcherNode.getMouse()
                self.object.setX(clamp(mpos.getX()) * 50 + self.camera.getX() )
                self.object.setY(clamp(mpos.getY()) * 50 + self.camera.getY() + 70)

        return Task.cont  # Task continues infinitely

    def unset_obj(self) -> None:
        self.object.hide()

    def set_obj(self) -> None:
        if self.object:
            self.object.hide()
        self.object = self.default_buildings[self.selected_building].model
        self.object.show()

    def set_housing(self, task) -> None:
        houses = 0
        if self.player_buildings.get(0):
            houses = len(self.player_buildings[0])

        self.resources[3].value = 35+(10*houses)

        return task.cont
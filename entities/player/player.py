from typing import Tuple
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from entities.world.resource import Resource
from graphics.model_loader import load_model

# A simple function to make sure a value is in a given range, -1 to 1 by
# default
def clamp(i, mn=-1, mx=1) -> int:
    return min(max(i, mn), mx)


class Player(DirectObject):
    
    def __init__(self, base: ShowBase) -> None:
        self.object = load_model(
            model_file = 'entities/buildings/house.obj',
            parent = render
        )
        
        self.base = base
        self.camera = camera
        self.objects = []
        self.resources = []

        self.resources.append(
            Resource.load_resource_from_file('example.cfg')
        )

        print(self.resources[0].value)

        self.camera.setPos(0, 0, 125)
        self.camera.setHpr(0, -60, 0)
        self.cam_vec = (0, 0)

        # Now we add a task that will take care of turning the head
        taskMgr.add(self.move_obj, "move_obj")
        taskMgr.add(self.move_cam, "moveTask")

        self.accept("w", self.delta_cam, [(0, 1)])
        self.accept("s", self.delta_cam, [(0, -1)])
        self.accept("a", self.delta_cam, [(-1, 0)])
        self.accept("d", self.delta_cam, [(1, 0)])
        self.accept("mouse1", self.place_obj)
        self.accept("w-up", self.delta_cam, [(0, 0)])
        self.accept("s-up", self.delta_cam, [(0, 0)])
        self.accept("a-up", self.delta_cam, [(0, 0)])
        self.accept("d-up", self.delta_cam, [(0, 0)])

        super().__init__()

    def place_obj(self):
        self.objects.append(
            load_model(
            model_file = 'entities/buildings/house.obj',
            parent = render,
            position=(self.object.getX(), self.object.getY(), self.object.getZ())
            )

        )
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
        # Check to make sure the mouse is readable
        if self.base.mouseWatcherNode.hasMouse():
            # get the mouse position as a LVector2. The values for each axis are from -1 to
            # 1. The top-left is (-1,-1), the bottom right is (1,1)
            mpos = self.base.mouseWatcherNode.getMouse()
            self.object.setX(clamp(mpos.getX()) * 50 + self.camera.getX() )
            self.object.setY(clamp(mpos.getY()) * 50 + self.camera.getY() + 70)

        return Task.cont  # Task continues infinitely
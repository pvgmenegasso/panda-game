



from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
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
        # Now we add a task that will take care of turning the head
        taskMgr.add(self.move_obj, "move_obj")
        super().__init__()


    def move_obj(self, task):
        # Check to make sure the mouse is readable
        if self.base.mouseWatcherNode.hasMouse():
            # get the mouse position as a LVector2. The values for each axis are from -1 to
            # 1. The top-left is (-1,-1), the bottom right is (1,1)
            mpos = self.base.mouseWatcherNode.getMouse()
            # Here we multiply the values to get the amount of degrees to turn
            # Restrain is used to make sure the values returned by getMouse are in the
            # valid range. If this particular model were to turn more than this,
            # significant tearing would be visable
            self.object.setX(clamp(mpos.getX()) * 50)
            self.object.setY(clamp(mpos.getY()) * 20)

        return Task.cont  # Task continues infinitely
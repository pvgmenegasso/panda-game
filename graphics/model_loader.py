from typing import Tuple
from panda3d.core import NodePath

def load_model(
    model_file : str, 
    parent, 
    scale : float | None = None, 
    position : Tuple[int, int, int] | None = None
    ) -> NodePath:

    object = loader.loadModel(modelPath = model_file)
    object.reparentTo(parent)

    if scale:
        object.setScale(scale)
    if position:
        object.setX(position[0])
        object.setY(position[1])
        object.setZ(position[2])


    # Very often, the egg file will know what textures are needed and load them
    # automatically. But sometimes we want to set our textures manually, (for
    # instance we want to put different textures on the same planet model)
    # Loading textures works the same way as loading models, but instead of
    # # calling loader.loadModel, we call loader.loadTexture
    # sky_tex = loader.loadTexture("sun_1k_tex.jpg")

    # Finally, the following line sets our new sky texture on our sky model.
    # # The second argument must be one or the command will be ignored.
    # object.setTexture(sky_tex, 1)

    return object

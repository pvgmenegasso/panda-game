from typing import Tuple
from panda3d.core import NodePath

def load_model(
    model_file : str, 
    parent, 
    scale : float | None = None, 
    position : Tuple[int, int, int] | None = None
    ) -> NodePath:
    # Here, inside our class, is where we are creating the loadPlanets function
    # For now we are just loading the star-field and sun. In the next step we
    # will load all of the planets

    # Loading objects in Panda is done via the command loader.loadModel, which
    # takes one argument, the path to the model file. Models in Panda come in
    # two types, .egg (which is readable in a text editor), and .bam (which is
    # not readable but makes smaller files). When you load a file you leave the
    # extension off so that it can choose the right version

    # Load model returns a NodePath, which you can think of as an object
    # containing your model

    # Here we load the sky model. For all the planets we will use the same
    # sphere model and simply change textures. However, even though the sky is
    # a sphere, it is different from the planet model because its polygons
    #(which are always one-sided in Panda) face inside the sphere instead of
    # outside (this is known as a model with reversed normals). Because of
    # that it has to be a separate model.
    object = loader.loadModel(modelPath = model_file)

    # After the object is loaded, it must be placed in the scene. We do this by
    # changing the parent of self.sky to render, which is a special NodePath.
    # Each frame, Panda starts with render and renders everything attached to
    # it.
    object.reparentTo(parent)

    # You can set the position, orientation, and scale on a NodePath the same
    # way that you set those properties on the camera. In fact, the camera is
    # just another special NodePath
    if scale:
        object.setScale(scale)

    if position:
        object.setPos(position)


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

from random import Random, random, randrange
from typing import Any, Tuple

from graphics.model_loader import load_model

def gen_scenery(
    amount : int, 
    model : str, 
    parent : Any | None = None,
    x_bounds : Tuple[int, int] | None = None, 
    y_bounds : Tuple[int, int] | None = None,
    z_bounds : Tuple[int, int] | None = None,
    rotate : bool = True
    ):
    object = []
    for i in range(amount):
        x_pos: int = 0
        y_pos: int = 0
        z_pos: int = 0
        if x_bounds:
            x_pos = randrange(x_bounds[0], x_bounds[1])
        if y_bounds:
            y_pos = randrange(y_bounds[0], y_bounds[1])
        if z_bounds:
            z_pos = randrange(z_bounds[0], z_bounds[1])

        object.append(load_model(
            model_file=model,
            parent=parent if parent else render,
            scale=1,
            position=(x_pos, y_pos, z_pos)
        ))
        if rotate:
            object[i-1].setHpr(randrange(0,364), 0, 0)
        scale = Random().uniform(0.2, 1)
        object[i-1].setColorScale(scale, scale, scale, 0)
    return object

def gen_level():
    trees = []
    rocks = []
    bushes = []

    ground = load_model(
        model_file="entities/world/ground.obj",
        parent=render,
        scale=1,
        position=(0, 0, 0)
    )

    trees = gen_scenery(
        amount = 20,
        model = "entities/world/tree.obj",
        parent=ground,
        x_bounds=(-64, 64),
        y_bounds=(-64, 64),
        z_bounds=(-2, 4)
    )

    rocks = gen_scenery(
        amount = 40,
        model = "entities/world/rock.obj",
        parent=ground,
        x_bounds=(-64, 64),
        y_bounds=(-64, 64),
        z_bounds=(0, 2)
    )
    bushes = gen_scenery(
        amount = 40,
        model = "entities/world/bush.obj",
        parent=ground,
        x_bounds=(-64, 64),
        y_bounds=(-64, 64),
        z_bounds=(0, 2)
    )
        

    return trees, rocks, bushes, ground
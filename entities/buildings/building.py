from __future__ import annotations
from types import MethodType
from typing import Any, Callable, Dict, List, Tuple
from direct.showbase.DirectObject import DirectObject

from entities.world.resource import Resource



class Building(DirectObject):

    def __init__(
        self,
        cost       : Tuple[int, int],
        name       : str,
        id         : int,
        model_file : str,
        action     : Callable,
        args       : List[Any]
        ) -> None:

        self.cost: Tuple[int, int]   = cost
        self.name: str               = name
        self.id: int                 = id
        self.model_file: str         = model_file
        self.action  = action    
        self.args: List[Any]         = args
                

        super().__init__()


    @classmethod
    def load_resource_from_file(cls, filename : str) -> Building:
        config = ConfigParser()
        config.read(f'entities/buildings/{filename}')
        new_building = Building(
            icon = config['resource']['icon'],
            name = config['resource']['name'],
            id   = int(config['resource']['id'])
        )
        for atr, value in config['resource'].items():
            new_building.__setattr__(atr, value)
        return new_building
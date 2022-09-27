from __future__ import annotations
from configparser import ConfigParser
from dataclasses import dataclass
from glob import glob
from types import MethodType
from typing import Any, Callable, Dict, List, Optional, Tuple
from direct.showbase.DirectObject import DirectObject

from entities.world.resource import Resource

class Building(DirectObject):

    def __init__(
        self,
        cost       : dict[int, int],
        name       : str,
        id         : int,
        model_file : str,
        icon       : str,
        action     : Optional[Callable] = None,
        args       : Optional[List[Any]] = None
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
        config.read(f'{filename}')
        modelstr = config['building']['model_file']
        new_building = Building(
            icon = config['building']['icon'],
            name = config['building']['name'],
            id   = int(config['building']['id']),
            cost = dict(config['cost']),
            model_file = f'entities/buildings/{modelstr}' 
        )
        for atr, value in config['building'].items():
            new_building.__setattr__(atr, value)
        return new_building

    @classmethod
    def load_buildings(cls) -> List[Building]:
        return_list = []
        for file in glob('entities/buildings/*.cfg'):
            return_list.append(cls.load_resource_from_file(file))
        return return_list

default_buildings = Building.load_buildings()
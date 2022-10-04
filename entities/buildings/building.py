from __future__ import annotations
from configparser import ConfigParser
from dataclasses import dataclass
from glob import glob
from logging import debug
from types import MethodType
from typing import Any, Callable, Dict, List, Optional, Tuple
from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase
from entities.world.resource import Resource
from graphics.model_loader import load_model

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

        self.cost: dict[int, int]   = cost
        self.name: str               = name
        self.id: int                 = id
        self.icon:str                = icon
        self.model_file: str         = model_file
        self.action  = action    
        self.args: List[Any]         = args
                
        self.model = load_model(
            model_file = self.model_file,
            parent=render
        )
        self.model.hide()

        super().__init__()

    def __repr__(self) -> str:
        return f'  \n\
            self,                           \n\
            cost       : {self.cost}        \n\
            name       : {self.name}        \n\
            id         : {self.id}          \n\
            model_file : {self.model_file}  \n\
            icon       : {self.icon}        \n\
            action     : {self.action}      \n\
            args       : {self.args} \n '

    @classmethod
    def load_building_from_file(cls, filename : str) -> Building:
        config = ConfigParser()
        config.read(f'{filename}')
        modelstr = config['building']['model_file']
        costs: dict[int, int] = dict()
        for item, value in config['cost'].items():
            costs[int(item)] = int(value)
        new_building = Building(
            icon = config['building']['icon'],
            name = config['building']['name'],
            id   = int(config['building']['id']),
            cost = costs,
            model_file = f'entities/buildings/{modelstr}'
        )
        return new_building

    @classmethod
    def load_buildings(cls) -> List[Building]:
        return_list = []
        for file in glob('entities/buildings/*.cfg'):
            building = cls.load_building_from_file(file)
            debug('loaded building !')
            debug(building)
            return_list.append(building)
        return return_list

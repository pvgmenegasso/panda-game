from __future__ import annotations
from configparser import ConfigParser
from pycolorlogs import debug
from glob import glob
from math import ceil
from direct.showbase.DirectObject import DirectObject

class Resource(DirectObject):
    
    def __init__(
        self,
        icon         : str,
        name         : str,
        id           : int,
        value        : int        = 0,
        delta        : int        = 0,
        cap          : int        = 5000,
        is_phisical  : bool       = False,
        model        : str | None = None,
        ) -> None:

        self.icon: str         = icon
        self.name: str         = name
        self.id: int           = id
        self.value: int        = value
        self.delta: int        = delta
        self.cap: int          = cap
        self.is_phisical: bool = is_phisical
        self.model: str | None = model     

        super().__init__()

    def __repr__(self) -> str:
        return f'{self.name}: {self.value}'

    def process(self, task):
        if self.delta > 0:
            self.add(self.delta)
        if self.delta < 0:
            self.use(self.delta)

    def add(self, amount : int):
        self.value = min(self.value+amount, self.cap)

    def use(self, amount : int) -> bool:
        if self.value >= amount:
            self.value -= amount
            return True
        else:
            return False

    @classmethod
    def load_resource_from_file(cls, filename : str) -> Resource:
        config = ConfigParser()
        config.read(filename)
        new_resource = Resource(
            icon  = config['resource']['icon'],
            name  = config['resource']['name'],
            id    = int(config['resource']['id']),
            value = int(config['resource']['value']),
            cap   = int(config['resource']['cap'])
        )
        return new_resource

    @classmethod
    def load_resources(cls):
        return_dict = dict()
        for file in glob("entities/world/*.cfg"):
            debug('Loading resource')
            resource = cls.load_resource_from_file(file)
            debug(resource)
            return_dict[resource.id]= resource
        return return_dict
from __future__ import annotations
from configparser import ConfigParser
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
        config.read(f'entities/world/{filename}')
        new_resource = Resource(
            icon = config['resource']['icon'],
            name = config['resource']['name'],
            id   = int(config['resource']['id'])
        )
        for atr, value in config['resource'].items():
            new_resource.__setattr__(atr, value)
        return new_resource
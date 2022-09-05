from direct.showbase.ShowBase import ShowBase
base: ShowBase = ShowBase()

from panda3d.core import *
from direct.gui.DirectGui import OnscreenText
from dataclasses import dataclass
from typing import Tuple

from panda3d.core import TextNode

@dataclass 
class UI:
    ''' This class defines a base class for
        elements of the user interface on the game

    '''
    text   : str
    parent : float
    style  : int
    fg     : Tuple[int, int, int, int]
    pos    : Tuple[float, float]
    scale  : float
 
 
    def genLabelText(self, text : str, i : int) -> OnscreenText:
        return OnscreenText(
            text   = text, 
            pos    = (0.06, -.06 * (i + 0.5)), 
            fg     = (1, 1, 1, 1),
            parent = base.a2dTopLeft,
            align  = base.TextNode.ALeft, scale=.05)
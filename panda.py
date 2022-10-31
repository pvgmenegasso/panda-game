# Start logging capabilities
from pycolorlogs import init_logs, DEBUG, debug, info

from entities.actors.cat import get_cat
init_logs(DEBUG)
# Initialize Panda and create a window
from direct.showbase.ShowBase import ShowBase
base = ShowBase()
from entities.player.player import Player
from world import World

from panda3d.core import *  # Contains most of Panda's modules
from direct.gui.DirectGui import *  # Imports Gui objects we use for putting


x = World(base)
p = Player(base) 
cat = get_cat()
cat.setCenter(p.camera.getPos())
debug(cat.get_actor_info())
debug(cat.get_anim_control_dict())
base.run()
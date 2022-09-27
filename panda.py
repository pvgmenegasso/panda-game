# Start logging capabilities
from pycolorlogs import init_logs, DEBUG, INFO, debug, info
init_logs(DEBUG)
# Initialize Panda and create a window
from direct.showbase.ShowBase import ShowBase
from entities.player.player import Player
from world import World
base = ShowBase()
from panda3d.core import *  # Contains most of Panda's modules
from direct.gui.DirectGui import *  # Imports Gui objects we use for putting


x = World(base)
p = Player(base) 
base.run()
"""
FGA + Arcade: A simple abstraction on top of the Arcade library to easily create
platformers and other kinds of games.
"""
from .fix import fix_all as _fix_all
from .game import *
from .physics import PhysicsEnginePlatformer
from .utils import run, create_platformer, hex_to_color

__version__ = '0.1.1'
_fix_all()

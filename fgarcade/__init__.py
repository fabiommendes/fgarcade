"""
FGA + Arcade: A simple abstraction on top of the Arcade library to easily create
platformers and other kinds of games.
"""
from .fix import fix_all as _fix_all
from .physics import PhysicsEnginePlatformer
from .platformer import Platformer
from .utils import run, create_platformer, hex_to_color

__version__ = '0.1.0'
_fix_all()

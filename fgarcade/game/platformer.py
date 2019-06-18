from fgarcade.game.physics import HasPhysicsMixin
from .background import HasBackgroundMixin
from .base import GameWindow
from .camera import HasScrollingCameraMixin
from .platforms import HasPlatformsMixin
from .player import HasPlayerMixin


class Platformer(HasPhysicsMixin,
                 HasBackgroundMixin,
                 HasPlatformsMixin,
                 HasPlayerMixin,
                 HasScrollingCameraMixin,
                 GameWindow):
    """
    Base class for platformer games.
    """

    # Sprite lists
    items = None
    enemies = None
    animated = None
def hex_to_color(color):
    """Convert color in the "#rrggbb" format to a color tuple."""
    red = color[1:3]
    green = color[3:5]
    blue = color[5:7]
    return int(red, 16), int(green, 16), int(blue, 16)


def run(window, title=None, width=None, height=None):
    if isinstance(window, type):
        window = window(width, height, title)
    window.run()


def create_platformer(title='FGArcade Game', width=800, height=600):
    """
    Crete a new Window class for a platformer game.
    """
    from .platformer import Platformer

    def decorator(func):
        game_cls = type('Game', (Platformer,), {'init': func})
        return game_cls(width, height, title)

    return decorator

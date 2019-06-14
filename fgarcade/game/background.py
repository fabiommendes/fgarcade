from math import ceil

from sidekick import lazy

import arcade
from .base import GameWindow
from ..assets import get_sprite_path
from ..utils import hex_to_color

BACKGROUND_COLOR_MAP = {
    'brown': hex_to_color('#d8bf9e'),
    'blue': hex_to_color('#ffefbd'),
    'green': hex_to_color('#8e6e53'),
    'yellow': hex_to_color('#54447b'),
}


class HasBackgroundMixin(GameWindow):
    """
    Defines a world with a given background color.
    """

    #: Background color
    @lazy
    def background_color(self):
        return BACKGROUND_COLOR_MAP[self.background_theme]

    #: Background theme name. Usually same as world_theme, or defaults to "blue"
    @lazy
    def background_theme(self):
        return getattr(self, 'world_color', 'blue')

    #: Near/fixed background sprite lists.
    #: Near background moves with parallax, while far background is fixed.
    @lazy
    def background_near(self):
        path = f'background/{self.background_theme}/hills'
        return repeat(get_sprite_path(path), self.width)

    @lazy
    def background_fixed(self):
        path = f'background/{self.background_theme}/tiles'
        width = self.scene_horizontal_end * self.parallax_ratio
        return repeat(get_sprite_path(path), width)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        arcade.set_background_color(self.background_color)

    def on_viewport_changed(self):
        """
        Hook called when viewport changes. Update background using parallax.
        """
        # Adjust fixed background parallax
        dx = self.background_fixed[0].left - \
             self.viewport_horizontal_start
        dy = self.background_fixed[0].bottom - \
             self.viewport_vertical_start
        self.background_fixed.move(round(-dx), round(-dy))

        # Adjust hills parallax
        dx = self.background_near[0].left - \
             self.viewport_horizontal_start * (1 - self.parallax_ratio)
        dy = self.background_near[0].bottom - \
             self.viewport_vertical_start * (1 - self.parallax_ratio)
        self.background_near.move(round(-dx), round(-dy))

    def draw_background(self):
        """
        Draw background.
        """
        self.background_fixed.draw()
        self.background_near.draw()

    def draw_background_elements(self):
        super().draw_elements()
        self.draw_background()


#
# Auxiliary functions
#
def repeat(img, total_width):
    """
    Repeat background tiles
    """
    lst = arcade.SpriteList(use_spatial_hash=False)
    tile = arcade.Sprite(img)
    width = tile.right - tile.left
    repeat_n = int(ceil(total_width / width))
    tile.left = tile.bottom = 0
    lst.append(tile)

    for n in range(1, repeat_n + 1):
        tile = arcade.Sprite(img)
        tile.bottom = 0
        tile.left = n * width
        lst.append(tile)
    return lst

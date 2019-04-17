import os
from functools import lru_cache
from pathlib import Path

import arcade

#
# PATHS
#
# Global paths

assets_dir = Path(__file__).parent / 'data'
images_dir = assets_dir / 'images'
theme_dir = assets_dir / 'themes' / 'abstract'

# Local paths
local_assets_dir = Path('.') / 'assets'
local_images_dir = Path('.') / 'images'

#
# Constants
#
EXTENSIONS = ('png', 'jpeg', 'svg')
IMAGE_SEARCH_PATHS = [local_images_dir, images_dir, theme_dir]


def get_tile(kind, color='blue', **kwargs):
    """
    Return tile for given color and kind.
    """
    return get_sprite(f'tile/{color}/{kind}', **kwargs)


def get_sprite(name, scale=1.0, role=None, position=None, **kwargs):
    """
    Return sprite for image with the given name.
    """
    sprite = arcade.Sprite(get_sprite_path(name), scale=scale, **kwargs)
    if role is not None:
        sprite.role = role
    if position is not None:
        x, y = position
        sprite.position = (x, y)
    return sprite


@lru_cache(maxsize=256)
def get_sprite_path(name, extensions=EXTENSIONS):
    """
    Return file path for a given sprite name.

    >>> get_sprite_path('player/blue/up1')
    PosixPath('.../player/blue/up1.png')
    """
    name = os.path.sep.join(name.split('/'))
    file_names = [f'{name}.{ext}' for ext in extensions]
    for path in IMAGE_SEARCH_PATHS:
        for filename in file_names:
            full_path = path / filename
            if full_path.exists():
                return full_path
    raise FileNotFoundError(f'no image found for {name}')

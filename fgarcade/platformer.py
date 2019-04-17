import os
import sys
from math import ceil

import arcade
from sidekick import lazy

from .assets import get_sprite_path
from .enums import Command
from .level_factory import LevelFactoryMixin
from .physics import PhysicsEnginePlatformer
from .sprites import AnimatedWalkingSprite
from .utils import hex_to_color


class Platformer(LevelFactoryMixin, arcade.Window):
    """
    Base class for platformer games.
    """

    path = None

    # Configuration
    world_color = 'blue'
    player_color = 'red'
    scaling = 1.0
    width = 800
    height = 600
    title = 'FGArcade Game'

    # Basic elements
    player = None
    physics_engine = None

    # Sprite lists
    player_list = None
    platforms = None
    items = None
    background_near = None
    background_fixed = None
    decorations = None
    enemies = None
    animated = None

    # Player options
    player_initial_position = 1.5, 1.5
    jump_cooldown = 0.125

    # Camera options
    viewport_margin_horizontal = 200
    viewport_margin_vertical = 150
    viewport_horizontal_start = 0
    viewport_vertical_start = 0
    viewport_horizontal_end = property(
        lambda self: self.viewport_horizontal_start + self.width)
    viewport_vertical_end = property(
        lambda self: self.viewport_vertical_start + self.height)
    parallax_ratio = 0.1

    # Geometric properties
    @lazy
    def viewport_horizontal_limit(self):
        return max(max(x.right for x in self.platforms), self.width)

    @lazy
    def viewport_vertical_limit(self):
        return max(max(x.top for x in self.platforms), self.height) + 128

    # Constants
    _has_setup_platformer = False
    _last_time_jumped = -1
    _background_color_map = {
        'brown': hex_to_color('#d8bf9e'),
        'blue': hex_to_color('#ffefbd'),
        'green': hex_to_color('#8e6e53'),
        'yellow': hex_to_color('#54447b'),
    }
    _default_commands = {
        arcade.key.LEFT: Command.LEFT,
        arcade.key.RIGHT: Command.RIGHT,
        arcade.key.UP: Command.UP,
        arcade.key.DOWN: Command.DOWN,
        arcade.key.SPACE: Command.SPACE,
    }

    def __init__(self, width, height, title, background_color=None,
                 command_map=_default_commands, **kwargs):
        super().__init__(width or self.width, height or self.height,
                         title or self.title)
        self.time = 0
        self.active_commands = Command.NONE
        self.command_map = command_map

        for k, v in kwargs.items():
            if not hasattr(self, k):
                raise TypeError(f'invalid argument: {k}')
            setattr(self, k, v)

        # Adjust path
        if self.path is None:
            mod_name = type(self).__module__
            mod = sys.modules[mod_name]
            try:
                self.path = os.path.dirname(mod.__file__)
            except AttributeError:
                pass

        # Set color configurations
        if background_color is None:
            self.background_color = self._background_color_map[self.world_color]
        else:
            self.background_color = background_color

        # Initialize variables and player sprite
        self.player_list = arcade.SpriteList()
        self.platforms = arcade.SpriteList()
        self.items = arcade.SpriteList()
        self.background_near = arcade.SpriteList(use_spatial_hash=False)
        self.background_fixed = arcade.SpriteList(use_spatial_hash=False)
        self.decorations = arcade.SpriteList()
        self.enemies = arcade.SpriteList()
        self.animated = arcade.SpriteList()
        self.player = self.setup_player()
        self.player_list.append(self.player)

    #
    # Initialize game
    #
    def setup(self):
        # Execute only once!
        if self._has_setup_platformer:
            return

        # User hook
        self.init()

        # Adjust player position
        x, y = self.player_initial_position
        self.player.center_x, self.player.center_y = int(64 * x), int(64 * y)
        self.player.last_texture_change_center_x = x
        self.player.last_texture_change_center_y = y

        # Adjust background
        arcade.set_background_color(self.background_color)

        def repeat(img, lst, total_width):
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

        repeat(get_sprite_path(f'background/{self.world_color}/tiles'),
               self.background_fixed, self.width)
        repeat(get_sprite_path(f'background/{self.world_color}/hills'),
               self.background_near, self.viewport_horizontal_limit * self.parallax_ratio)

        self.physics_engine = PhysicsEnginePlatformer(self.player, self.platforms)

        # Prevent multiple executions
        self._has_setup_platformer = True

    def setup_player(self):
        """
        Return a sprite representing a Player.
        """

        def load(which, mirrored=False):
            path = get_sprite_path(f"player/{self.player_color}/{which}")
            return arcade.load_texture(path, scale=self.scaling, mirrored=mirrored)

        mirror = lambda x: load(x, mirrored=True)

        # Create animated sprite
        player = AnimatedWalkingSprite(
            stand_left=mirror('walk1'),
            stand_right=load('walk1'),
            left=[mirror(f'walk{i}') for i in (2, 3, 2, 1)],
            right=[load(f'walk{i}') for i in (2, 3, 2, 1)],
            up=[load(f'up{i}') for i in (2,)],
            down=[load('fall')],
            step=20,
        )
        return player

    def init(self):
        """
        Overridden by child classes.

        Used to initialize world.
        """

    def run(self):
        """
        Run platformer.
        """
        self.setup()
        arcade.run()

    #
    # Control and events
    #
    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        self.background_fixed.draw()
        self.background_near.draw()
        self.platforms.draw()
        self.items.draw()
        self.decorations.draw()
        self.animated.draw()
        self.enemies.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        try:
            self.active_commands |= self.command_map[key]
        except KeyError:
            pass

    def on_key_release(self, key, modifiers):
        try:
            self.active_commands ^= self.command_map[key]
        except KeyError:
            self.handle_key(key, modifiers)

    def handle_key(self, key, modifiers):
        pass

    def handle_space(self):
        pass

    #
    # Update logic
    #
    def update(self, delta_time):
        self.time += delta_time
        self.update_player(delta_time)
        self.physics_engine.update()
        self.update_viewport(delta_time)
        self.player.update()
        self.player.update_animation()
        self.player_list.update_texture(self.player)

    def update_player(self, delta_time):
        change_x = self.player.change_x
        change_y = self.player.change_y
        can_jump = abs(change_y) <= 2 * \
                   abs(change_x) and self.physics_engine.can_jump()
        if abs(change_y) > 1:
            self._last_time_jumped = self.time

        max_speed = 4.5
        delta = 1.25 if can_jump else 0.5
        jump = 10
        cmd = Command
        active = self.active_commands
        go_left = active & cmd.LEFT
        go_right = active & cmd.RIGHT
        change_x *= 0.95

        # Change speeds
        if active & cmd.UP and can_jump:
            if not (self.time < self._last_time_jumped + self.jump_cooldown):
                self._last_time_jumped = self.time
                self.player.change_y = jump
        if go_left and go_right:
            pass
        elif go_right and change_x >= 0:
            change_x += delta
        elif go_left and change_x <= 0:
            change_x -= delta
        else:
            change_x = 0

        # Set maximum speed
        if change_x > 0:
            change_x = min(change_x, max_speed)
        elif change_x < 0:
            change_x = max(change_x, -max_speed)
        self.player.change_x = change_x

        # Handle special keys
        if active & cmd.SPACE:
            self.handle_space()

    def update_viewport(self, dt):
        changed = False

        x_view = self.viewport_horizontal_start
        y_view = self.viewport_vertical_start
        dx = self.viewport_margin_horizontal
        dy = self.viewport_margin_vertical

        # Check if player changed the viewport
        if self.player.left < x_view + dx:
            self.viewport_horizontal_start = \
                max(0.0, self.player.left - dx)
            changed = True
        if self.player.right > x_view + self.width - dx:
            self.viewport_horizontal_start = min(self.viewport_horizontal_limit - self.width,
                                                 self.player.right + dx - self.width)
            changed = True
        if self.player.bottom < y_view + dy:
            self.viewport_vertical_start = \
                max(0.0, self.player.bottom - dy)
            changed = True
        if self.player.top > y_view + self.height - dy:
            self.viewport_vertical_start = min(self.viewport_vertical_limit - self.height,
                                               self.player.top + dy - self.height)
            changed = True

        if changed:
            # Adjust fixed background parallax
            if self.background_fixed:
                dx = self.background_fixed[0].left - \
                     self.viewport_horizontal_start
                dy = self.background_fixed[0].bottom - \
                     self.viewport_vertical_start
                self.background_fixed.move(round(-dx), round(-dy))

            # Adjust hills parallax
            if self.background_near:
                dx = self.background_near[0].left - \
                     self.viewport_horizontal_start * (1 - self.parallax_ratio)
                dy = self.background_near[0].bottom - \
                     self.viewport_vertical_start * (1 - self.parallax_ratio)
                self.background_near.move(round(-dx), round(-dy))

            # Adjust viewport
            arcade.set_viewport(round(self.viewport_horizontal_start),
                                round(self.viewport_horizontal_end),
                                round(self.viewport_vertical_start),
                                round(self.viewport_vertical_end))

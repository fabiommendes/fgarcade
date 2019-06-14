from sidekick import record, lazy

import arcade
from .base import GameWindow
from ..assets import get_sprite_path
from ..enums import Command
from ..sprites import AnimatedWalkingSprite


class HasPlayerMixin(GameWindow):
    """
    Mixin that adds a player element into the class.
    """

    #: Scaling for assets
    scaling = 1.0

    #: Player theme
    player_theme = 'red'

    #: Initial player position (measured in tiles)
    player_initial_tile = 1, 1

    #: Dummy physics engine
    physics_engine = record(can_jump=lambda: True, update=lambda *args: None)

    #: Default player class
    player_class = lazy(lambda _: Player)

    @lazy
    def player(self):
        x, y = self.player_initial_tile
        x, y = int(64 * x + 32), int(64 * y + 32)
        player = self.player_class(self.player_theme, scaling=self.scaling,
                                   center_x=x, center_y=y)
        self.__dict__['player'] = player
        self.on_player_init(player)
        return player

    #
    # Base implementations for class hooks
    #
    def on_player_init(self, player):
        """
        Hook called when player is first created with the player as single
        argument.
        """

    #
    # Hooks and methods overrides
    #
    def get_viewport_focus(self):
        player = self.player
        return player.left, player.bottom, player.right, player.top

    def update_player(self, dt):
        """
        Update player element after a time increment of dt.
        """
        self.player.update_clock(dt)
        self.player.update_actions(self.commands, self.physics_engine)
        self.player.update()
        self.player.update_animation()

    def update_elements(self, dt):
        super().update_elements(dt)
        self.update_player(dt)

    def draw_player(self):
        """
        Draw player on screen.
        """
        return self.player.draw_sprites()

    def draw_elements(self):
        super().draw_elements()
        self.draw_player()

class Player(AnimatedWalkingSprite):
    """
    Represents a simple player.
    """

    #: Player internal clock
    time = 0

    #: Player options
    jump_cooldown = 0.125
    last_time_jumped = -float('inf')

    #: Commands bound to movement actions such as go left, right and jump
    command_left = Command.LEFT
    command_right = Command.RIGHT
    command_jump = Command.UP

    def __init__(self, theme, scaling=1.0, center_x=0, center_y=0, **kwargs):
        self.theme = theme
        self.scaling = scaling

        load = self._load
        mirror = lambda x: load(x, mirrored=True)

        # Create animated sprite
        super().__init__(
            stand_left=mirror('walk1'),
            stand_right=load('walk1'),
            left=[mirror(f'walk{i}') for i in (2, 3, 2, 1)],
            right=[load(f'walk{i}') for i in (2, 3, 2, 1)],
            up=[load(f'up{i}') for i in (2,)],
            down=[load('fall')],
            step=20,
        )

        # Move it to correct position
        self.center_x = center_x
        self.center_y = center_y
        self.last_texture_change_center_x = center_x
        self.last_texture_change_center_y = center_y

        # Add to sprite list
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self)

        # Add extra attributes
        for k, v in kwargs.items():
            if hasattr(self, k) and not k.startswith('_'):
                setattr(self, k, v)
            else:
                raise TypeError(f'invalid argument: {k}')

    def _load(self, which, mirrored=False):
        path = get_sprite_path(f"player/{self.theme}/{which}")
        return arcade.load_texture(path, scale=self.scaling, mirrored=mirrored)

    def draw_sprites(self):
        return self.sprite_list.draw()

    def update_clock(self, dt):
        self.time += dt

    def update_animation(self):
        super().update_animation()
        self.sprite_list.update_texture(self)

    def update_actions(self, commands, physics):
        """
        Update internal state from given commands.

        It must pass the PhysicsEngine object with a can_jump method that tests
        if jumps are allowed or not.
        """

        change_x = self.change_x
        change_y = self.change_y
        can_jump = abs(change_y) <= 2 * abs(change_x) and physics.can_jump()
        if abs(change_y) > 1:
            self.last_time_jumped = self.time

        max_speed = 4.5
        delta = 1.25 if can_jump else 0.5
        jump = 10
        go_left = commands & self.command_left
        go_right = commands & self.command_right
        change_x *= 0.95

        # Change speeds
        if commands & self.command_jump and can_jump:
            if not (self.time < self.last_time_jumped + self.jump_cooldown):
                self.last_time_jumped = self.time
                self.change_y = jump
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
        self.change_x = change_x

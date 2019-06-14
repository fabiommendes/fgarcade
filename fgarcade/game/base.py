import arcade
from ..enums import Command

COMMAND_MAP = {
    arcade.key.LEFT: Command.LEFT,
    arcade.key.RIGHT: Command.RIGHT,
    arcade.key.UP: Command.UP,
    arcade.key.DOWN: Command.DOWN,
    arcade.key.SPACE: Command.SPACE,
    arcade.key.RETURN: Command.RETURN,
    arcade.key.A: Command.ASDW_LEFT,
    arcade.key.D: Command.ASDW_RIGHT,
    arcade.key.W: Command.ASDW_UP,
    arcade.key.S: Command.ASDW_DOWN,
}


class GameWindow(arcade.Window):
    """
    Base class for all kind of games.
    """

    #: Scale factor for all game graphics
    scaling = 1.0

    #: Screen width
    width = 800

    #: Screen height
    height = 600

    #: Window title
    title = 'FGArcade Game'

    #: Simulation time
    time = 0

    #: Initial command
    commands = Command.NONE

    #: Mapping between keys and commands
    command_map = COMMAND_MAP

    def __init__(self, width=None, height=None, title=None, **kwargs):
        super().__init__(width or self.width,
                         height or self.height,
                         title or self.title)

        for k, v in kwargs.items():
            if hasattr(self, k) and not k.startswith('_'):
                setattr(self, k, v)
            else:
                raise TypeError('invalid argument: %s' % k)
        self._has_init = False

    #
    # Components
    #
    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        self.draw_background_elements()
        self.draw_elements()
        self.draw_foreground_elements()
        arcade.finish_render()

    def draw_elements(self):
        """
        Hook called to draw all elements that compose the game world.

        Subclasses should override this function instead of on_draw.
        """

    def draw_background_elements(self):
        """
        Called before draw_elements()
        """

    def draw_foreground_elements(self):
        """
        Called after draw_elements()
        """

    def update(self, dt):
        """
        Update simulation by interval dt.
        """
        self.start_update(dt)
        self.update_elements(dt)
        self.finish_update(dt)

    def start_update(self, dt):
        """
        Updates the clock tick and performs any other work before updating
        elements when frame starts.
        """
        self.time += dt

    def finish_update(self, dt):
        """
        Hook that subclasses may override to make any action after all elements
        are updated.
        """

    def update_elements(self, dt):
        """
        Hook called to update all elements that compose the game world.

        Subclasses usually should override this function instead of update()
        """

    #
    # Keyboard interaction
    #
    def on_key_press(self, key, modifiers):
        """
        Hook called when some key is pressed.
        """
        try:
            self.commands |= self.command_map[key]
        except KeyError:
            pass

    def on_key_release(self, key, modifiers):
        """
        Hook called when some key is release.
        """
        try:
            self.commands ^= self.command_map[key]
        except KeyError:
            self.handle_key(key, modifiers)

    def handle_key(self, key, modifiers):
        """
        Hook used to handle keys that are not associated with commands.
        """

    #
    # Initialization hooks
    #
    def init(self):
        """
        Overridden by child classes.

        Used to initialize world.
        """

    def run(self):
        """
        Run platformer.
        """
        if not self._has_init:
            self.init()
            self._has_init = True
        arcade.run()

from sidekick import lazy

import arcade
from .base import GameWindow


class HasScrollingCameraMixin(GameWindow):
    """
    A basic game window that has a scrolling camera.
    """

    #: The ratio of movement for background/foreground.
    #: ratio = 0 => no move, ratio = 1 => sync with the foreground
    parallax_ratio = 0.1

    #: Tolerance of the reference point for the camera. It moves camera if
    #: the reference point (usually the player) moves beyond those margins
    #: Measured in pixels.
    viewport_margin_horizontal = 200
    viewport_margin_vertical = 120

    #: x, y coordinates for the start of viewport area
    viewport_horizontal_start = 0
    viewport_vertical_start = 0

    #: Automatically computed viewport end coordinates
    @property
    def viewport_horizontal_end(self):
        return self.viewport_horizontal_start + self.width

    @property
    def viewport_vertical_end(self):
        return self.viewport_vertical_start + self.height

    #: Min/max coordinates of the viewport in both directions
    scene_horizontal_start = 0
    scene_horizontal_end = lazy(lambda _: _.width)
    scene_vertical_start = 0
    scene_vertical_end = lazy(lambda _: _.height)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._viewport_focus = (
            self.viewport_horizontal_start,
            self.viewport_vertical_start,
            self.viewport_horizontal_end,
            self.viewport_vertical_end,
        )

    def move_with_parallax(self, obj, parallax=None, left=0, bottom=0):
        """
        Move object relative to viewport using paralax effect.

        Args:
            obj:
                Displaced object
            parallax:
                Ratio between [0, 1] of paralax. If not given, uses the default
                parallax.
            left:
            bottom:
                Initial displacements of obj in respect with the current
                viewport.
        """
        parallax = self.parallax_ratio if parallax is None else parallax
        viewport_x = self.viewport_horizontal_start
        viewport_y = self.viewport_vertical_start
        dx = obj[0].left - left - viewport_x * (1 - parallax)
        dy = obj[0].bottom - bottom - viewport_y * (1 - parallax)
        obj.move(round(-dx), round(-dy))

    def move_with_viewport(self, obj, left=0, bottom=0):
        """
        Move an object fixed with the background.
        """
        self.move_with_parallax(obj, parallax=1.0, left=left, bottom=bottom)

    #
    # Register base implementations for class hooks
    #
    def on_viewport_changed(self):
        """
        Hook that is executed when viewport is changed
        """

    def get_viewport_focus(self):
        """
        Return a bounding box of (x_min, y_min, x_max, y_max) with the region
        that the viewport should try to focus.
        """
        return self.width, self.height, self.width, self.height

    #
    # Override base class methods
    #
    def update_elements(self, dt):
        super().update_elements(dt)
        self.update_viewport()

    def update_viewport(self):
        """
        Update viewport to include the focused viewport area.
        """
        xmin, ymin, xmax, ymax = self.get_viewport_focus()
        changed = False

        dx = self.viewport_margin_horizontal
        dy = self.viewport_margin_vertical

        v_xmin = self.viewport_horizontal_start
        v_xmax = self.viewport_horizontal_end
        v_ymin = self.viewport_vertical_start
        v_ymax = self.viewport_vertical_end

        # Check if player changed the viewport
        if xmin < v_xmin + dx:
            self.viewport_horizontal_start = \
                max(self.scene_horizontal_start, xmin - dx)
            changed = True

        if xmax > v_xmax - dx:
            self.viewport_horizontal_start = \
                min(self.scene_horizontal_end - self.width,
                    xmax + dx - self.width)
            changed = True

        if ymin < v_ymin + dy:
            self.viewport_vertical_start = \
                max(self.scene_vertical_start, ymin - dy)
            changed = True

        if ymax > v_ymax - dy:
            self.viewport_vertical_start = \
                min(self.scene_vertical_end - self.width,
                    ymax + dy - self.height)
            changed = True

        if changed:
            self.on_viewport_changed()
            arcade.set_viewport(round(self.viewport_horizontal_start),
                                round(self.viewport_horizontal_end),
                                round(self.viewport_vertical_start),
                                round(self.viewport_vertical_end))

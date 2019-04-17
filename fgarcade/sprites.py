import arcade
from arcade import FACE_RIGHT, FACE_DOWN, FACE_UP, FACE_LEFT


class AnimatedWalkingSprite(arcade.Sprite):
    def __init__(self, scale: float = 1,
                 image_x: float = 0, image_y: float = 0,
                 center_x: float = 0, center_y: float = 0, *,
                 stand_left, stand_right, left, right, up, down, step=20):
        super().__init__(scale=scale, image_x=image_x, image_y=image_y,
                         center_x=center_x, center_y=center_y)
        self.state = FACE_RIGHT
        self.stand_right_texture = stand_right
        self.stand_left_texture = stand_left
        self.walk_left_textures = left
        self.walk_right_textures = right
        self.walk_up_textures = up
        self.walk_down_textures = down
        self.cur_texture_index = 0
        self.texture_change_distance = step
        self.last_texture_change_center_x = 0
        self.last_texture_change_center_y = 0
        self._update_direction(FACE_RIGHT, self.stand_right_texture)
        self.textures = [self._texture]

    def _update_direction(self, state, texture):
        self.last_texture_change_center_x = self.center_x
        self.last_texture_change_center_y = self.center_y
        self.state = state
        self.cur_texture_index = 0
        self._texture = texture

    def _rotate(self, delta, list):
        if abs(delta) >= self.texture_change_distance:
            self.cur_texture_index += 1
            self.last_texture_change_center_x = self.center_x
            self.last_texture_change_center_y = self.center_y
        self._texture = list[self.cur_texture_index % len(list)]

    def update_animation(self):
        tol = 1.

        # Falling
        if self.change_y <= -tol:
            if self.state != FACE_DOWN:
                self._update_direction(FACE_DOWN, self.walk_down_textures[0])
            else:
                self._rotate(self.center_y - self.last_texture_change_center_y,
                             self.walk_down_textures)

        # Jumping
        elif self.change_y >= tol:
            if self.state != FACE_UP:
                self._update_direction(FACE_UP, self.walk_up_textures[0])
            else:
                self._rotate(self.center_y - self.last_texture_change_center_y,
                             self.walk_up_textures)

        # Going left
        elif self.change_x <= -tol:
            if self.state != FACE_LEFT:
                self._update_direction(FACE_LEFT, self.stand_left_texture)
            else:
                self._rotate(self.center_x - self.last_texture_change_center_x,
                             self.walk_left_textures)

        # Going right
        elif self.change_x >= tol:
            if self.state != FACE_RIGHT:
                self._update_direction(FACE_RIGHT, self.stand_right_texture)
            else:
                self._rotate(self.center_x - self.last_texture_change_center_x,
                             self.walk_right_textures)

        elif abs(self.change_x) < tol and self.state == FACE_DOWN:
            self._update_direction(FACE_RIGHT, self.stand_right_texture)

        self.textures[0] = self._texture
        self.width = self._texture.width * self.scale
        self.height = self._texture.height * self.scale
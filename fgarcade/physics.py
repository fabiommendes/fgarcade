from math import sqrt

import arcade

from fgarcade.enums import Role


class PhysicsEnginePlatformer(arcade.PhysicsEnginePlatformer):
    """
    This class is responsible for move everything and take care of collisions.
    """

    def can_jump(self) -> bool:
        """
        Method that looks to see if there is a floor under
        the player_sprite. If there is a floor, the player can jump
        and we return a True.
        """
        self.player_sprite.center_y -= 2
        bottom = self.player_sprite.bottom
        top = self.player_sprite.top
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.platforms)
        self.player_sprite.center_y += 2

        for other in hit_list:
            if bottom < other.top and top > other.center_y:
                return True
        else:
            return False

    def update(self):
        """
        Move everything and resolve collisions.
        """
        max_speed = 10
        check_for_collision_with_list = arcade.check_for_collision_with_list
        player = self.player_sprite

        # Add gravity and move
        player.change_y -= self.gravity_constant
        speed = sqrt(player.change_x ** 2 + player.change_y ** 2)
        if speed > max_speed:
            ratio = max_speed / speed
            player.change_x *= ratio
            player.change_y *= ratio

        player.center_y += player.change_y
        player.center_x += player.change_x

        # Check for wall hit
        hit_list = check_for_collision_with_list(player, self.platforms)
        recover = 0.666
        min_shadow_x = 12
        min_shadow_y = 6

        for hit in hit_list:
            shadow_x = min(player.right, hit.right) - \
                       max(player.left, hit.left)
            shadow_y = min(player.top, hit.top) - \
                       max(player.bottom, hit.bottom)
            role = getattr(hit, 'role', Role.OBJECT)
            collision_role = Role.OBJECT

            shift_y = 0
            if role == Role.RAMP_DOWN:
                shift_y = player.center_x - hit.left
            elif role == Role.RAMP_UP:
                shift_y = max(player.center_x - hit.left, 0) - 64

            # Falling down...
            if (player.change_y < 0
                    and player.bottom < hit.top + shift_y < player.center_y
                    and shadow_x > min_shadow_x
                    and shadow_y < 24 + abs(shift_y)):
                player.bottom += max(recover *
                                     (hit.top + shift_y - player.bottom), 0.5)
                player.change_y = 0

            # Going up
            elif (player.change_y > 0
                  and role == collision_role
                  and player.top > hit.bottom > player.center_y
                  and shadow_x > min_shadow_x
                  and shadow_y < 24):
                player.top -= max(recover * (player.top - hit.bottom), 0.5)
                player.change_y = 0

            # Going right...
            if (player.change_x > 0
                    and (role == collision_role or role == Role.RAMP_UP)
                    and player.right > hit.left
                    and player.center_x < hit.center_x
                    and shadow_y > min_shadow_y
                    and shadow_x < 24):
                if role == Role.RAMP_UP:
                    player.change_x /= 2
                    player.change_y += 4 * player.change_y
                    player.center_y += 64 + shift_y
                else:
                    player.right -= max(recover *
                                        (player.right - hit.left), 0.5)
                    player.change_x = 0

            # Going left...
            elif (player.change_x < 0
                  and role == collision_role
                  and player.left < hit.right
                  and player.center_x > hit.center_x
                  and shadow_y > min_shadow_y
                  and shadow_x < 24):
                player.left += max(recover * (hit.right - player.left), 0.5)
                player.change_x = 0

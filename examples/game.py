import fgarcade as ge


@ge.create_platformer('Simple game')
def game(world):
    """
    Create game and initialize the variables.
    """
    world.player_initial_position = (5, 1.5)
    
    world.create_tower(10, 2, coords=(0, 1))
    world.create_ground(3, coords=(2, 3))
    world.create_ground(3, coords=(6, 1))
    world.create_platform(3, coords=(4, 5))
    world.create_platform(3, coords=(12, 4))
    world.create_ground(35, coords=(0, 0), smooth_ends=False)
    world.create_ramp('up', 6, coords=(15, 1))
    world.create_ground(5, coords=(21, 6), smooth_ends=False, height=6)
    world.create_ramp('down', 6, coords=(26, 7))
    world.create_tower(10, coords=(34, 1))


if __name__ == "__main__":
    game.run()
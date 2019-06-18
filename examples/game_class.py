import fgarcade as ge


class Game(ge.Platformer):
    """
    Simple platformer example
    """

    title = 'Simple platformer'
    player_initial_tile = 4, 1

    def init_world(self):
        self.create_tower(10, 2, coords=(0, 1))
        self.create_ground(3, coords=(2, 3))
        self.create_ground(3, coords=(6, 1))
        self.create_platform(3, coords=(4, 5))
        self.create_platform(3, coords=(12, 4))
        self.create_ground(35, coords=(0, 0), smooth_ends=False)
        self.create_ramp('up', 6, coords=(15, 1))
        self.create_ground(5, coords=(21, 6), smooth_ends=False, height=6)
        self.create_ramp('down', 6, coords=(26, 7))
        self.create_tower(10, coords=(34, 1))

        self.create_block('green', (5, 8))
        self.create_block('red', (6, 8))
        self.create_block('grey', (7, 8))
        self.create_block('brown', (8, 8))
        self.create_block('red-lock', (9, 8))

        self.create_arrow('right', (3, 1))


        self.create_fence('left', (10, 1))
        self.create_fence('middle', (11, 1))
        self.create_fence('middle', (12, 1))
        self.create_fence('right', (13, 1))

        self.create_foreground('other/plant/blue-3', (4, 1))
        self.create_foreground('other/plant/blue-1', (7, 2))
        self.create_foreground('other/plant/blue-5', (9, 2))

    def init_enemies(self):
        pass

    def init_items(self):
        pass


    def init(self):
        self.init_world()
        self.init_items()
        self.init_enemies()


if __name__ == "__main__":
    Game().run()

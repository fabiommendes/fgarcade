from sidekick import lazy

from fgarcade import GameWindow, PhysicsEnginePlatformer


class HasPhysicsMixin(GameWindow):
    """
    Base class for all games that have a Physics Engine attribute.
    """
    #: Class that implements the physics engine
    physics_engine_class = PhysicsEnginePlatformer

    #: Gravity constant
    gravity_constant = 0.5

    #: Initializes the physics engine object
    @lazy
    def physics_engine(self):
        return self.physics_engine_class(self)

    def update_physics(self, dt):
        """
        Main loop for physics update.
        """
        self.physics_engine.update(dt)

    def update_elements(self, dt):
        super().update_elements(dt)
        self.update_physics(dt)
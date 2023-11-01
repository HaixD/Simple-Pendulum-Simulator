import math
import physics.force as force
import physics.gravity as gravity
import physics.pendulum as pendulum

class PendulumTension(force.Force):
    """PendulumTension represents the Tension Force on a Body.

    PendulumTension represents the Tension Force of a pendulum on a
    Body. The difference between PendulumTension and Tension is that
    PedulumTension only accounts for scenarios with a pivot such that
    you end up with circular motion.
    """

    def __init__(self, body: pendulum.Pendulum):
        """Initializes a PendulumTension that is applied on a Pendulum.

        Args:
            body (Pendulum): The Body to apply PendulumTension on.
        """
        super(PendulumTension, self).__init__(body)
    
    def get_magnitude(self) -> float:
        """Returns the magnitude of PendulumTension.

        Calculates and returns the magnitude of PendulumTension. The
        magnitude of this force depends on the angle between the 
        Pendulum Body and the pivot.

        Returns:
            The magnitude of PendulumTension.
        """
        gravitational_tension = self.body.forces[gravity.Gravity].get_magnitude() * math.sin(self.get_direction())

        velocity = self.body.velocity.seek(-1)
        centripetal_tension = self.body.mass * ((velocity[0][1] ** 2 + velocity[1][1] ** 2) / self.body.distance_from_pivot())

        return gravitational_tension + centripetal_tension
    
    def get_direction(self) -> float:
        """Returns the direction of PendulumTension.

        Returns the direction of PendulumTension.The direction of 
        PendulumTension will always point towards the pivot 
        (from the Pendulum Body).

        Returns:
            float: The direction of PendulumTension
        """
        position_vs_time = self.body.position.seek(-1)
        position = (position_vs_time[0][1], position_vs_time[1][1])

        return math.atan2(self.body.pivot[1] - position[1], self.body.pivot[0] - position[0])
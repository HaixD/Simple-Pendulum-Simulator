import math
import physics.force as force
import physics.body as body

class Gravity(force.Force):
    """Gravity represents a constnat downwards Force.

    While gravity points to the center of a body of mass, for the 
    purposes of this simulation, it will always point downwards with
    an almost constant Force.

    Attributes:
        source_mass (float): The mass of the seperate body that is 
        causing gravity to pull on the applied Body.
        source_radius (float): the radius of the body that is causing
        gravity to pull on the applied Body.
    """
    
    gravitational_constant = 6.674 * 10 ** -11

    def __init__(self, body: body.Body, source_mass: float, source_radius: float):
        """Initializes a Gravity Force caused by a given mass and radius.

        Initializes a Gravity Force caused by an external mass and 
        radius. The source_mass and source_radius is not the mass and
        radius of the body. It is an external actor.

        Args:
            body (Body): The Body to apply the Gravity Force on.
            source_mass (float): The mass of the external actor.
            source_radius (float): The radius of the external actor.
        """
        super(Gravity, self).__init__(body)

        self.source_mass: float = source_mass
        self.source_radius: float = source_radius

    def get_magnitude(self) -> float:
        """Returns a magnitude based on the external actor and the body.

        Returns a magnitude based on the external actor and the body.
        See Newton's law of universal gravitation:
        https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation

        Returns:
            float: The magnitude of Gravity Force applied on the body.
        """
        height = self.body.position.seek(-1)[1][1]
        freefall_acceleration = Gravity.gravitational_constant * self.source_mass / ((self.source_radius + height) ** 2)

        return self.body.mass * freefall_acceleration

    def get_direction(self) -> float:
        """Returns the direction of the Gravity Force on the Body.

        Returns the direction of the Gravity Force on the Body. The
        direction is always downwards (-90 degrees).

        Returns:
            Always -90 degrees.
        """
        return -math.pi/2
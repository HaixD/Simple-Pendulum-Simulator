from __future__ import annotations
import math
from json import dumps
from dataclasses import dataclass, field
import physics.force as force
import graph.vector_function as vector_function

@dataclass
class Body:
    """Body represents anything that is affected by physics.

    Body is a collection of variables that are useful in calculating
    the physics (kinematics) of anything.

    Attributes:
        mass (float): The mass of the Body.
        forces (dict[type, Force]): The forces applied on the Body.
        position(VectorFunction): The Function for the Body's position
        velocity(VectorFunction): The function for the Body's velocity
        acceleration(VectorFunction): The function for the Body's
        acceleration
    """

    mass: float
    forces: dict[type, force.Force] = field(init = False)
    position: vector_function.VectorFunction = field(init = False)
    velocity: vector_function.VectorFunction = field(init = False)
    acceleration: vector_function.VectorFunction = field(init = False)

    def __post_init__(self) -> None:
        """Ensures forces, position, velocity, and acceleration are not None
        """
        self.forces = {}
        self.position = vector_function.VectorFunction()
        self.velocity = vector_function.VectorFunction()
        self.acceleration = vector_function.VectorFunction()

    def get_net_force(self) -> tuple[float, float]:
        """Calculates the total forces applied to this Body.

        Calculates the net force applied on this Body. The return
        is a tuple containing the magnitudes of the net force in the
        positive x direction and position y direction respectively.
        
        Returns:
            The net force applied on this Body
        """
        net_force_x = 0
        net_force_y = 0

        for force in self.forces.values():
            magnitude = force.get_magnitude()
            direction = force.get_direction()

            net_force_x += math.cos(direction) * magnitude
            net_force_y += math.sin(direction) * magnitude

        return (net_force_x, net_force_y)
    
    def add_force(self, force: type, *args, **kwargs) -> None:
        """Adds a given force to this Body.

        Creates a force instance from the given args and kwargs and 
        applies it to this Body.

        Args:
            force (type): A Force subclass.

        Returns:
            This Body object.
        """
        self.forces[force] = force(self, *args, **kwargs)
        return self

    def save(self, file_name: str, framerate: int = 60) -> None:
        """Saves the data of this Body to a JSON file.

        Saves the data of this Body to a JSON file.

        Args:
            file_name (str): The file name to save in 
            (should end with .json).
            framerate (int, optional): The framerate/interval to save 
            the vector functions. Defaults to 60.
        """
        position = ([item[0] for item in iter(self.position)], [item[1] for item in iter(self.position)])
        velocity = ([item[0] for item in iter(self.velocity)], [item[1] for item in iter(self.velocity)])    
        acceleration = ([item[0] for item in iter(self.acceleration)], [item[1] for item in iter(self.acceleration)])

        frame_dt = round((self.dt ** -1) / framerate)
        
        json = dumps({'position': {'x': position[0][::frame_dt],
                                   'y': position[1][::frame_dt]},
                      'velocity': {'x': velocity[0][::frame_dt],
                                   'y': velocity[1][::frame_dt]},
                      'acceleration': {'x': acceleration[0][::frame_dt],
                                       'y': acceleration[1][::frame_dt]}},
                     indent = 2)
        
        with open(file_name, 'w') as file:
            file.write(json)
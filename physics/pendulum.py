import math
from dataclasses import dataclass
from .animated_body import AnimatedBody

@dataclass
class Pendulum(AnimatedBody):
    """PendulumBody represents a Body bound by a hypothetical rope.

    PendulumBody represents a Body bound by a hypothetical rope. This 
    hypothetical rope is bound to an immovable pivot point.

    Attributes:
        pivot (list[float, float]): The coordinates of the pivot point.
        length (float): The length of the rope attached to the pivot.
    """

    pivot: list[float, float]
    length: float

    def angle_from_pivot(self) -> float:
        """Returns the angle from the pivot to the Body in radians.

        Returns the angle from the Body to the pivot in radians.
        0 rad means the Body is to the right of the pivot.

        Returns:
            float: The angle from the pivot to the Body in radians.
        """
        position_vs_time = self.position.seek(-1)
        position = (position_vs_time[0][1], position_vs_time[1][1])
        
        return math.atan2(position[1] - self.pivot[1], position[0] - self.pivot[0])
    
    def distance_from_pivot(self) -> float:
        """Returns the distance between the Body and the pivot.

        Returns the distance between the Body and the pivot.

        Returns:
            float: The distance between the Body and the pivot.
        """
        position_vs_time = self.position.seek(-1)
        position = (position_vs_time[0][1], position_vs_time[1][1])

        return math.sqrt((position[0] - self.pivot[0]) ** 2 + (position[1] - self.pivot[1]) ** 2)

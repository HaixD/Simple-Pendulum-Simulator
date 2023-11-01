from __future__ import annotations
from abc import ABC
import physics.body as body

class Force(ABC):
    """Force represents a Force that can be applied to any "body".

    Force represents a Force that can be applied to any body/object 
    that is affected by physics.
    """

    def __init__(self, body: body.Body):
        """Initializes a Force that is applied on the given body.

        Args:
            body (Body): The body that the force is applied on.
        """
        self.body = body
    
    def get_magnitude(self) -> float:
        """Returns the magnitude of the force that is applied to the 
        body.

        Returns the magnitude of the force that is applied to the 
        body. Depending on the child class, the magnitude will be 
        calculated differently.

        Raises:
            NotImplementedError: The get_magnitude function called 
            belongs to the Force abstract base class.

        Returns:
            The magnitude of the force that is applied to the body.
        """
        raise NotImplementedError()

    def get_direction(self) -> float:
        """Returns the direction of the force that is applied to the
        body.

        Returns the direction of the force that is applied to the
        body. Depending on the child class, the direction will be 
        calculated differently.

        Raises:
            NotImplementedError: The get_magnitude function called 
            belongs to the Force abstract base class.

        Returns:
            float: The angle (in radians) relative to 0 degrees or 
            to the right/east.
        """
        raise NotImplementedError()
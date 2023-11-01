from __future__ import annotations
from json import loads
from dataclasses import dataclass, field
from graph.vector_function import VectorFunction

@dataclass
class BodyReplay:
    """BodyReplay represents a body after loading from a JSON file.

    BodyReplay exists for the purposes of replaying/loading saved
    data on the original Body. The original Body cannot be restored
    from this class alone. Information such as the mass and forces
    are not loaded because they are unnecessary for replaying a Body. 

    Attributes:
        position(VectorFunction): The Function for the Body's position
        velocity(VectorFunction): The function for the Body's velocity
        acceleration(VectorFunction): The function for the Body's
        acceleration
    """

    position: VectorFunction = field(init = False)
    velocity: VectorFunction = field(init = False)
    acceleration: VectorFunction = field(init = False)
    index: int = field(init = False, default = 0)
    time: float = field(init = False, default = 0)

    def __post_init__(self) -> None:
        """Ensures Position, velocity, and acceleration are not None.
        """
        self.position = VectorFunction()
        self.velocity = VectorFunction()
        self.acceleration = VectorFunction()
    
    def step(self) -> bool:
        """Steps the state of the Body to the next recorded point.

        Steps the state of the Body to the next recorded point.
        Returns True if there is still more data, and False otherwise.

        Returns:
            True if there is still more data, and False otherwise.
        """
        self.index += 1

        try:
            self.time = self.position.x.seek(self.index)[0]
        except Exception:
            return False

        return True

    def get_state(self) -> tuple[float, float, float]:
        """Returns the current state of this BodyReplay.

        Returns the current state of this BodyReplay.

        Returns:
            The current position, 
            velocity, and acceleration.
        """
        return self.position.seek(self.index), self.velocity.seek(self.index), self.acceleration.seek(self.index)

    @staticmethod
    def load(file_name: str) -> BodyReplay:
        """Loads data from the given file and creates a BodyReplay.

        Loads data from the given file and creates a BodyReplay.
        
        Args:
            file_name (str): The file name of the desired JSON file
            (should end with '.json').

        Returns:
            The loaded BodyReplay
        """
        output = BodyReplay()

        with open(file_name, 'r') as file:
            data = loads(file.read())
        
        output.position = VectorFunction.from_iter(data['position']['x'], data['position']['y'])
        output.velocity = VectorFunction.from_iter(data['velocity']['x'], data['velocity']['y'])
        output.acceleration = VectorFunction.from_iter(data['acceleration']['x'], data['acceleration']['y'])

        output.time = output.position.x.seek(0)[0]

        return output
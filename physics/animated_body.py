from __future__ import annotations
from dataclasses import dataclass, field
import physics.body as body
from graph.integration_method import IntegrationMethod

@dataclass
class AnimatedBody(body.Body):
    """AnimatedBody represents a body that moves.

    AnimatedBody represents a body that moves. It can step/increment
    by a given dt (delta time). The lower dt is, the more accurate 
    AnimatedBody will be after each step. Lower dt values also cost
    more to compute. In terms of game engines, stepping can be seen
    as equivalent to the update function, except stepping is done 
    when it is necessary, not as often as possible at every moment
    in time.

    Attributes:
        dt (float): The change in time between steps.
        time (float): The initial/starting time.
        pre_step (list[callable[[AnimatedBody], None]]): functions to
        run at the start of every step
        post_step (list[callable[[AnimatedBody], None]]): functions to
        run at the end of every step.
    """
    
    dt: float
    time: float = field(init = False, default = 0)
    pre_step: list[callable[[AnimatedBody], None]] = field(init = False)
    post_step: list[callable[[AnimatedBody], None]] = field(init = False)

    def __post_init__(self) -> None:
        """Ensures pre_step and post_step are not None.
        """
        super(AnimatedBody, self).__post_init__()

        self.pre_step = []
        self.post_step = []

    def set_state(self, v_ix: float = 0, v_iy: float = 0, x_i: float = 0, y_i: float = 0, integration_method = IntegrationMethod.EULER) -> AnimatedBody:
        """Sets the state (position, velocity, etc) at time=0.

        Sets the state (position, velocity, etc) at time=0 to the 
        given values.

        Args:
            v_ix (int, optional): The initial velocity in the x 
            direction. Defaults to 0.
            v_iy (int, optional): The initial velocity in the y 
            direction. Defaults to 0.
            x_i (int, optional): The initial position along the x 
            axis. Defaults to 0.
            y_i (int, optional): The initial position along the y 
            axis. Defaults to 0.
            integration_method (_type_, optional): The default 
            integration method. Defaults to IntegrationMethod.EULER.

        Returns:
            This AnimatedBody object.
        """
        self.acceleration.insert(0, *self.generate_acceleration())
        
        self.velocity = self.acceleration.integrate(0, v_ix, v_iy, integration_method)
        self.position = self.velocity.integrate(0, x_i, y_i, integration_method)

        return self

    def __step_acceleration(self) -> None:
        """Updates acceleration to account for the current time.

        Stepping the acceleration means to append new data into the 
        acceleration VectorFunction. This will also propagate "down"
        to the velocity VectorFunction, and then the position
        VectorFunction such that velocity and position will also have
        new data appended.
        """
        self.acceleration.insert(self.time, *self.generate_acceleration())

    def step(self) -> None:
        """Steps/increments time by dt and updates acceleration.

        Stepping will trigger all pre_step functions, and then 
        proceed with updating the acceleration 
        (after incrementing time). Once this process is done,
        all post_step functions will be executed.
        """
        for function in self.pre_step:
            function(self)
        
        self.time += self.dt

        self.__step_acceleration()
        
        for function in self.post_step:
            function(self)

    def generate_acceleration(self) -> float:
        """Calculates acceleration caused by Forces applied.

        Calculates acceleration caused by Forces applied. For 
        information on how this is calculated, see Newton's 
        second law:
        https://www.britannica.com/science/Newtons-laws-of-motion/Newtons-second-law-F-ma

        Returns:
            The current acceleration.
        """
        forces = self.get_net_force()
        
        return (forces[0] / self.mass, forces[1] / self.mass)
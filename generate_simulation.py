import math
from sys import argv
import multiprocessing as mp
import physics.pendulum as pendulum
import physics.gravity as gravity
import physics.pendulum_tension as pendulum_tension
import graph.integration_method as integration_method

def lock_distance(body: pendulum.Pendulum) -> None:
    """post-step function to ensure distance from pivot stays constant.

    post-step function to ensure distance from pivot stays constant 
    by resetting the distance.

    Args:
        body (pendulum.Pendulum): The Pendulum Body to reset.
    """
    if (body.distance_from_pivot() - body.length < 0.01) or (abs(body.position.seek(-1)[0][1]) > 0.1):
        return
    
    angle = body.angle_from_pivot()
    body.position.pop()
    body.position.insert(body.time, math.cos(angle) * body.length, 
                                    math.sin(angle) * body.length)

class ResetVelocity:
    """ResetVelocity represents a function that resets a Pendulum's velocity.

    ResetVelocity represents a function that sets a Pendulum's 
    velocity to an expected velocity when it reaches its lowest point
    (also referred to as the base).
    
    """

    def __init__(self, base_velocity: float):
        """Initializes ResetVelocity with a base velocity.

        Initializes ResetVelocity with a base velocity.

        Args:
            base_velocity (float): The velocity of the pendulum at 
            its base.
        """
        self.base_velocity = base_velocity

    def __call__(self, body: pendulum.Pendulum) -> None:
        """post-step function to ensure a Pendulum's velocity is correct.
        
        post-step function to ensure a Pendulum's velocity is correct
        when it is at its base (-90 degrees).

        Args:
            body (Pendulum): The Pendulum Body that is being reset.
        """
        if abs(body.angle_from_pivot() + math.pi/2) > 0.01: #
            return
        
        velocity = abs(body.velocity.x.seek(-1)[1])
        
        if self.base_velocity:
            time, v = body.velocity.x.pop()
            if v > 0:
                body.velocity.x.insert(time, self.base_velocity)
            else:
                body.velocity.x.insert(time, -self.base_velocity)
        else:
            self.base_velocity = velocity

def compile_simulation(degrees: int):
    """simulates a default Pendulum.

    Creates and simulates a default Pendulum (unless parameters are 
    passed) with the Gravity and PendulumTension forces added.

    Args:
        angle (float, optional): The initial angle of the Pendulum. 
        Defaults to 0.
        mass (float, optional): The mass of the Pendulum. Defaults
        to 1.
        dt (float, optional): The delta-time of the Pendulum. 
        Defaults to 10**-3.
        length (float, optional): The length of the Pendulum. 
        Defaults to 1.
        gravitational_source_mass (float, optional): The mass of the 
        external actor. Defaults to 5.9722*10**24
        (mass of earth).
        gravitational_source_radius (float, optional): The radius of 
        the external actor. Defaults to 6.371*10**6 (radius of earth).
        integration_method (IntegrationMethod, optional): The default 
        integration method. Defaults to 
        integration_method.IntegrationMethod.EULER.
    """
    #SIMULATION PARAMETERS
    angle = math.radians(-90 + degrees)
    mass = 0.1
    dt = 10 ** -3 * 1/2
    length = 0.1476
    gravitational_source_mass = 5.9722 * 10 ** 24 #Earth's mass
    gravitational_source_radius = 6.371 * 10 ** 6 #Earth's radius
    seconds = 3
    numerical_approximation = integration_method.IntegrationMethod.RK4

    #SAVE FILE'S PARAMETERS
    save_folder = argv[4]
    save_file_name = f'{save_folder}/{degrees} degrees.json'
    save_framerate = 60

    pendulum_obj = pendulum.Pendulum(
        mass = mass,
        dt = dt,
        pivot = [0, 0],
        length = length
    ).set_state(
        x_i = length * math.cos(angle),
        y_i = length * math.sin(angle),
        integration_method = numerical_approximation
    ).add_force(
        gravity.Gravity, gravitational_source_mass, gravitational_source_radius
    ).add_force(
        pendulum_tension.PendulumTension
    )

    for iterations in range(int((dt ** -1) * seconds)):
        if iterations % (dt ** -1) == 0:
            print(f'{int(iterations // (dt ** -1)) + 1}/{seconds} sec compiled for {degrees} degrees')
        pendulum_obj.step()

    pendulum_obj.save(save_file_name, framerate = save_framerate)
        
if __name__ == '__main__':
    #SIMULATE MULTIPLE ANGLES (RANGING FROM START TO STOP) SIMULTANEOUSLY 
    start = int(argv[1])
    stop = int(argv[2])
    increment = int(argv[3])
    
    with mp.Pool() as pool:
        pool.map(compile_simulation, range(start, stop + increment, increment))
    print('Compilation finished')

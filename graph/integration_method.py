from __future__ import annotations
from enum import Enum, auto

class IntegrationMethod(Enum):
    """IntegrationMethod represents implemented numerical approximations.

    IntegrationMethod represents implemented numerical approximations.
    """
    EULER = auto()       #Euler's Method
    TRAPEZOIDAL = auto() #Trapezoidal Rule
    RK4 = auto()         #Runge-Kutta 4
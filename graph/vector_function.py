from __future__ import annotations
from dataclasses import dataclass, field
import graph.function as function
import graph.integration_method as integration_method

@dataclass
class VectorFunction:
    """VectorFunction represents a Function with 2 components, x and y.

    VectorFunction represents a Function with 2 components, x with
    respect to time, and y with respect to time. Changes done to the 
    x Function are independent from the changes done with the y 
    Function.

    Attributes:
        x (Function): The Function that represents x with respect to 
        time.
        y (Function): The Function that represents y with respect to 
        time.
    """

    x: function.Function = field(default = None)
    y: function.Function = field(default = None)

    def __iter__(self) -> iter[tuple[float, float], tuple[float, float]]:
        """Returns a generator used to iterate both x and y at once.

        Returns a generator used to iterate both x and y at once.

        Returns:
            iter[tuple[float, float], tuple[float, float]]: A 
            generator used to iterate both x and y at once.
        """
        return zip(self.x, self.y)
    
    def __post_init__(self) -> None:
        """Ensures that the x and y Functions are not None.
        """
        self.x = self.x or function.Function()
        self.y = self.y or function.Function()

    def insert(self, time: float, x: float, y: float) -> None:
        """Inserts an x and y value with respect to time.

        Inserts (time, x) into the Function for x and (time, y) into
        the function for y.

        Args:
            t (float): The time that corresponds with the given 
            (x, y) coordinate .
            x (float): The x value of the (x, y) coordinate.
            y (float): The y value of the (x, y) coordinate.
        """
        self.x.insert(time, x)
        self.y.insert(time, y)

    def append(self, dt: float, dx: float, dy: float) -> None:
        """Appends a change in x and y with respect to the change in time.

        Adds a new coordinate to both the x Function and y Function 
        based on their respective last element.

        Args:
            dt (float): The change in time from the last coordinate.
            dx (float): The change in x from the last coordinate.
            dy (float): the change in y from the last coordinate.
        """
        self.x.append(dt, dx)
        self.y.append(dt, dy)

    def pop(self, index: int = -1) -> tuple[float, float]:
        """Pops the x and y coordinate at the given index, disregarding time.

        Pops the x and y coordinate at the given index, disregarding time.

        Args:
            index (int, optional): The index of the desired x and y 
            coordinate. Defaults to -1.

        Returns:
            The popped x and y coordinate.
        """
        return (self.x.pop(index), self.y.pop(index))

    def seek(self, index: int):
        """Gets the x and y coordinate stored at the given index.

        Gets the x and y coordinate stored at the given index.

        Args:
            index (int): The index of the desired coordinate.

        Returns:
            The x and y coordinate stored at the desired index.
        """
        return (self.x.seek(index), self.y.seek(index))
    
    def integrate(self, t_i: float = 0, x_i: float = 0, y_i: float = 0, method: integration_method.IntegrationMethod = integration_method.IntegrationMethod.TRAPEZOIDAL) -> VectorFunction:
        """Integrates both the x and y Functions.

        Integrates both the x and y Functions with the given initial 
        points time (t_i), x (x_i), and y (y_i).

        Args:
            t_i (float, optional): The initial value for time. 
            Defaults to 0.
            x_i (float, optional): The initial value for x. 
            Defaults to 0.
            y_i (float, optional): The initial value for y. 
            Defaults to 0.
            method (IntegrationMethod, optional): The desired 
            integration method. Defaults to IntegrationMethod.TRAPEZOIDAL.

        Returns:
            A VectorFunction that contains both the 
            integral/anti-derivative Function of this VectorFunction.
        """
        x_integral = self.x.integral(method, t_i, x_i)
        y_integral = self.y.integral(method, t_i, y_i)

        return VectorFunction(x_integral, y_integral)
    
    @staticmethod
    def from_iter(x_iterable: iter[tuple[float, float]], y_iterable: iter[tuple[float, float]]) -> VectorFunction:
        """Creates a VectorFunction from the given x and y coordinates.

        Creates a VectorFunction from the given x and y coordinates.
        This function does not assume that the x values for x_iterable
        and y_iterable represents time.

        Args:
            x_iterable (iter[tuple[float, float]]): The x Function's 
            contents.
            y_iterable (iter[tuple[float, float]]): The y Function's 
            contents.

        Returns:
            A new VectorFunction created from the given x and y data.
        """
        output = VectorFunction()

        output.x = function.Function.from_iter(x_iterable)
        output.y = function.Function.from_iter(y_iterable)

        return output
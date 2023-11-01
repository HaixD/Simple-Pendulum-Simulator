from __future__ import annotations
import graph.integration_method as integration_method

class Function:
    """Function represents a mathematical function.

    Function represents a mathematical function where all values (y) 
    for x are implied if it is not given. It will assume between all 
    stored points there is a linear relationship.

    Attributes:
        __points (list[tuple[float, float]]): A list of (x, y) 
        coordinates.
        __integral (Function): A function that represents this 
        function's integral.
        __integration_method: The desired method to calculate
        the integral function.
    """
    
    def __init__(self):
        """Initizalizes a Function with no stored points.
        """
        self.__points: list[tuple[float, float]] = []
        self.__integral: Function = None
        self.__integration_method: integration_method.IntegrationMethod = None

    def __repr__(self) -> str:
        """Returns a string useful for debugging Function.

        Returns:
            A string useful for debugging Function.
        """
        return f'Function({str(self.__points)})'

    def __call__(self, x: float) -> float:
        """Returns the y value at the given x.

        Calculates the y value at the given x based on existing 
        points (assuming 1 or more points is stored). If there is 
        only 1 stored point, the entire function is implied to be a 
        flat horizontal line where all y values are equal. If there
        is multiple points, a slope will be made connecting relevant 
        points and the y value will be obtained from that slope.

        Args:
            x (float): The x value of the desired y.

        Raises:
            ValueError: There are no coordinates stored in the 
            function.

        Returns:
            A y value at the given x.
        """
        if not self.__points:
            raise ValueError('Function object has no stored points.')
        
        if len(self.__points) == 1:
            return self.__points[0][1] #slope formed by y value of only point
        elif x > self.__points[-1][0]:
            index = len(self.__points) - 1 #slope formed by 2 right-most points
        elif x < self.__points[0][0]:
            index = 1 #slope formed by 2 left-most points
        else:
            #sloped formed by closest points
            index = self.search_best_index(x, slice(0, len(self.__points)))
        
        a = self.__points[index - 1]
        b = self.__points[index]

        slope = (b[1] - a[1]) / (b[0] - a[0])
        
        return slope * (x - a[0]) + a[1]

    def __iter__(self) -> iter[tuple[float, float]]:
        """Returns a generator to iterate stored points.

        Returns a generator to iterate stored points.

        Yields:
            The points stored within this Function object.
        """
        for point in self.__points:
            yield point

    def search_best_index(self, x: float, section: slice) -> int:
        """Finds where x should be stored if it were added.

        Performs a binary search to find the correct index to store x.

        Args:
            x (float): The x value to be inserted.
            section (slice): The slice of the points array to be searched.

        Returns:
            An index representing where x should be stored.
        """
        if section.start == section.stop:
            return section.start
        
        offset = section.start + (section.stop - section.start) // 2
        middle = self.__points[offset][0]

        if x > middle:
            return self.search_best_index(x, slice(offset + 1, section.stop))
        elif x < middle:
            return self.search_best_index(x, slice(section.start, offset))
        elif x == middle:
            return offset

    def insert(self, x: float, y: float, check: bool = False) -> None:
        """Inserts the (x, y) coordinate into the function

        Automatically finds the correct index and inserts the (x, y)
        coordinate into the list of stored points. This will modify 
        the behavior of this object when it is called as more points
        allow for higher accuracy. This function will also update the
        integral if possible. By default, this function will not
        check if the given point is already stored.

        Args:
            x (float): The x value of the new coordinate.
            y (float): The y value of the new coordinate.
            check (bool, optional): True if the x value should be 
            checked to see if it collides with any other point, and 
            False otherwise. Defaults to False.
        """
        if check and x in set(point[0] for point in self.__points):
            raise ValueError(f'Point at x={x} already exists in points list')
        
        index = self.search_best_index(x, slice(0, len(self.__points)))
        self.__points.insert(index, (x, y))

        if self.__integral is not None:
            if index == len(self.__points) - 1:
                self.__update_integral()
            else:
                self.__integral = self.integral(self.__integral.__integration_method, *self.__integral.__points[0])

    def append(self, dx: float, dy: float) -> None:
        """Inserts a new point based on the last point.

        Adds a new point to the points list based on the 
        last point + (dx, dy). This coordinate is not guaranteed to 
        be at the end of the points list.

        Args:
            dx (float): The change in x from the last stored point.
            dy (float): The change in y from the last stored point.
        """
        self.insert(self.__points[-1][0] + dx, self.__points[-1][1] + dy)

    def pop(self, index: int = -1) -> tuple[float, float]:
        """Pops a coordinate from the points list at the given index.

        Pops a coordinate from the points list at the given index.

        Args:
            index (int, optional): The index to pop. Defaults to -1.

        Returns:
            The coordinates stored at the given index.
        """
        return self.__points.pop(index)

    def seek(self, index: int) -> tuple[float, float]:
        """Returns the coordinate stored at the given index.

        Returns the coordinate stored at the given index.

        Args:
            index (int): The index of the desired coordinate.

        Returns:
            The coordinate stored at the given index.
        """
        return self.__points[index]

    def integral(self, method: integration_method.IntegrationMethod, x_i: float = 0, y_i: float = 0) -> Function:
        """Creates an integral function of this Function.

        Creates an integral function of this Function starting at 
        the initial x (x_i) and y (y_i). The integration method will 
        vary depending on the passed method parameter.

        Args:
            method (IntegrationMethod): The integration method.
            x_i (float, optional): The initial x coordinate. Defaults 
            to 0.
            y_i (float, optional): The initial y coordinate. Defaults 
            to 0.

        Returns:
            The integral/anti-derivative Function.
        """
        self.__integral = Function()
        self.__integral.__integration_method = method

        self.__integral.insert(x_i, y_i)
        
        match method:
            case integration_method.IntegrationMethod.TRAPEZOIDAL:
                for i, point in enumerate(self.__points[1:], 1):
                    _integrate_trapezoidal(self.__integral, self, point[0] - self.__points[i - 1][0])
            case integration_method.IntegrationMethod.EULER:
                for i, point in enumerate(self.__points[1:], 1):
                    _integrate_euler(self.__integral, self, point[0] - self.__points[i - 1][0])
            case integration_method.IntegrationMethod.RK4:
                for i, point in enumerate(self.__points[1:], 1):
                    _integrate_rk4(self.__integral, self, point[0] - self.__points[i - 1][0])

        return self.__integral
    
    def __update_integral(self):
        match self.__integral.__integration_method:
            case integration_method.IntegrationMethod.TRAPEZOIDAL:
                _integrate_trapezoidal(self.__integral, self, self.__points[-1][0] - self.__points[-2][0] if len(self.__points) > 1 else 0)
            case integration_method.IntegrationMethod.EULER:
                _integrate_euler(self.__integral, self, self.__points[-1][0] - self.__points[-2][0] if len(self.__points) > 1 else 0)
            case integration_method.IntegrationMethod.RK4:
                _integrate_rk4(self.__integral, self, self.__points[-1][0] - self.__points[-2][0] if len(self.__points) > 1 else 0)

    @staticmethod
    def from_iter(iterable: iter[tuple[float, float]]) -> Function:
        """Creates a Function from an iterable of coordinates.

        Iterates through iterable to create a Function. The 
        coordinates with iterable do not have to be sorted.

        Args:
            iterable (iter[tuple[float, float]]): The iterable to 
            obtain coordinates from.

        Returns:
            A function formed by the points within iterable.
        """
        output = Function()
        
        for x, y in iterable:
            output.insert(x, y)

        return output
    
def _integrate_trapezoidal(f: Function, derivative: Function, dx: float, splits: int = 1) -> None:
    """Appends a new point to the integral function, f.

    Using the derivative function and dx, a new coordinate is 
    estimated for the given integral function using trapezoidal rule.

    Args:
        f (Function): The integral/anti-derivative function.
        derivative (Function): The derivative function of the 
        integral/anti-derivative function.
        dx (float): The change in x from the right-most coordinate
        of the integral/anti-derivative function.
        splits (int, optional): Amount of splits to perform with 
        Trapezoidal rule. More splits means more accuracy. 
        Defaults to 1.
    """
    width = dx/splits
    x = derivative.seek(-1)[0]

    area = 0
    for _ in range(splits):
        area += (width / 2) * (derivative(x - width) + derivative(x))
        x -= width

    f.append(dx, area)

def _integrate_euler(f: Function, derivative: Function, dx: float) -> None:
    """Appends a new point to the integral function, f.

    Using the derivative function and dx, a new coordinate is 
    estimated for the given integral function using Euler's method.


    Args:
        f (Function): The integral/anti-derivative function.
        derivative (Function): The derivative function of the 
        integral/anti-derivative function.
        dx (float): The change in x from the right-most coordinate
        of the integral/anti-derivative function.
    """
    f.append(dx, dx * derivative(f.seek(-1)[0]))

def _integrate_rk4(f: Function, derivative: Function, dx: float) -> None:
    """Appends a new point to the integral function, f.

    Using the derivative function and dx, a new coordinate is 
    estimated for the given integral function using Runge-Kutta 4.

    Args:
        f (Function): The integral/anti-derivative function.
        derivative (Function): The derivative function of the 
        integral/anti-derivative function.
        dx (float): The change in x from the right-most coordinate
        of the integral/anti-derivative function.
    """
    x = derivative.seek(-1)[0]

    k1 = derivative(x)
    k23 = 2 * derivative(x + dx / 2)
    k4 = derivative(x + dx)

    f.append(dx, dx / 6 * (k1 + 2 * k23 + k4))
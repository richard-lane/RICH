import numpy as np
from math import sqrt


class Ring:
    """
    Class representing a Cherenkov ring
    
    Unit radius, centred at the point (x, y) provided to the ctor

    """

    _x = 0.0
    _y = 0.0

    # Angle between the horizontal and the line joining the centre to the origin
    _alpha = 0.0

    # Distance of centre from the origin
    _d = 0.0

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._alpha = np.arctan2(y, x)
        self._d = sqrt(x ** 2 + y ** 2)

    def _r(self, phi):
        """
        Returns the distance from the origin to the edge of the ring, looking along a line at an angle phi
        from the horizontal.

        phi in rad

        """
        # Our distance is the positive solution to the quadratic equation r^2 + br + c = 0
        # This just comes out of some geometry if you draw the triangles
        b = -2 * self._d * np.cos(phi - self._alpha)
        c = (self._d * self._d) - 1

        return (-b + sqrt(b * b - 4 * c)) / 2

    def misalignment(self, n):
        """
        Returns an array of n distances from the origin to the edge of the ring, equally spaced in angle
        between 0 and 2 pi

        Returns also an array of n array equally spaced between 0 and 2pi

        """
        angles = np.linspace(0, 2 * np.pi)

        # Could make this faster, don't need to
        return np.array([self._r(angle) for angle in angles]), angles

    def centre(self):
        return self._x, self._y

    def boundary(self, n):
        """
        Returns two n-length arrays (x, y) of x and y co-ordinates of the ring edges
        
        Not guaranteed to start at any particular angle - i.e. 
        
        """
        angles = np.linspace(0, 2 * np.pi)
        return (
            np.array([self._x + np.cos(x) for x in angles]),
            np.array([self._y + np.sin(x) for x in angles]),
        )

    def move(self, x, y):
        """
        Move this ring to be centred on (x, y)

        """
        self.__init__(x, y)


class Noisy_Ring(Ring):

    # Cache positional errors
    _noise = None
    _x_error = None
    _y_error = None

    def _set_error(self, n, level=0.05):
        self._noise = level

        noise_mag = np.random.normal(scale=self._noise, size=n)
        noise_angle = 2 * np.pi * np.random.uniform(size=n)

        self._x_error = noise_mag * np.cos(noise_angle)
        self._y_error = noise_mag * np.sin(noise_angle)

    def _should_find_errors(self, force, n, noise_level):
        """
        Find whether we need to recalculate the errs

        """
        # If we haven't yet calculated them, we have changed n or the noise level or if we explicitly asked to
        return bool(
            force
            or (self._x_error is None)
            or len(self._x_error) != n
            or self._noise != noise_level
        )

    def __init__(self, x, y):
        super().__init__(x, y)

    def boundary(self, n, noise=0.05, new_errors=False):
        """
        Returns two n-length arrays (x, y) of x and y co-ordinates of the ring edges, with some random noise

        Not guaranteed to start at any particular angle - i.e.

        """
        if self._should_find_errors(new_errors, n, noise):
            self._set_error(n, noise)

        exact_x, exact_y = super().boundary(n)

        return exact_x + self._x_error, exact_y + self._y_error

    def misalignment(self, n, noise=0.05):
        """
        Returns distance from origin of these points

        """
        if self._should_find_errors(False, n, noise):
            self._set_error(n, noise)

        x, y = self.boundary(n, noise)

        return np.sqrt(boundary_x ** 2 + boundary_y ** 2)

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from math import sqrt


class Point:
    """
    Class representing a point within the unit circle

    """

    _x = 0.0
    _y = 0.0

    # Angle between the horizontal and the line joining this point to the origin
    _phi = 0.0

    # Distance to the origin
    _d = 0.0

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._phi = np.arctan2(y, x)
        self._d = sqrt(x ** 2 + y ** 2)

    def _r(self, theta):
        """
        Returns the distance from this point to the edge of the unit circle, looking along a line at an angle theta from the horizontal.

        theta in rad

        """
        # This just comes out of some geometry if you draw the triangles
        chi = self._phi + np.pi - theta
        b = -2 * self._d * np.cos(chi)
        c = (self._d * self._d) - 1

        return (-b + sqrt(b * b - 4 * c)) / 2

    def misalignment(self, n):
        """
        Returns an array of n distances to the edge of a unit circle, equally spaced in angle between 0 and 2 pi

        Returns an array of n angles equally spaced between 0 and 2pi

        """
        angles = np.linspace(0, 2 * np.pi)

        # Could make this faster, don't need to
        return np.array([self._r(angle) for angle in angles]), angles

    def coords(self):
        return self._x, self._y

    def move(self, x, y):
        """
        Move this point to (x, y)

        """
        self.__init__(x, y)


def main():
    My_Point = Point(0.0, 0.0)
    distances, angles = My_Point.misalignment(50)

    fig, _ = plt.subplots(figsize=(18.0, 6.0))
    ax = plt.subplot2grid((1, 3), (0, 0))
    ax2 = plt.subplot2grid((1, 3), (0, 1), colspan=2)

    circle = np.array([(np.cos(x), np.sin(x)) for x in angles])
    ax.plot(circle[:, 0], circle[:, 1])
    point, = ax.plot(*My_Point.coords(), "r.")
    ax.axis("off")

    line, = ax2.plot(angles, distances)
    print(line)
    ax2.set_xlabel(r"$\theta\ /rad$")
    ax2.set_ylabel(r"$r$")
    ax2.set_ylim(0, 2)
    x_tick = np.linspace(0, 2, 5)
    ax2.set_xticks(x_tick * np.pi)
    ax2.set_xticklabels([fr"${x}\pi$" for x in x_tick])

    ax_x_slider = plt.axes([0.05, 0.1, 0.3, 0.03])
    x_slider = Slider(ax_x_slider, "x", -1.0, 1.0, 0.0)

    ax_y_slider = plt.axes([0.05, 0.05, 0.3, 0.03])
    y_slider = Slider(ax_y_slider, "y", -1.0, 1.0, 0.0)

    def update(val):
        x = x_slider.val
        y = y_slider.val
        My_Point.move(x, y)
        line.set_ydata(My_Point.misalignment(50)[0])
        point.set_data(*My_Point.coords())

    x_slider.on_changed(update)
    y_slider.on_changed(update)
    plt.show()


if __name__ == "__main__":
    main()

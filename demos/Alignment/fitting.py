import scipy.optimize
from numpy import cos


def ring_fit(angle, distance):
    """
    Fit an iterable of distances and angles to 1+Acos(angle - B)

    returns (A, B)

    """

    def f(a, A, B):
        return 1 + A * cos(a - B)

    return scipy.optimize.curve_fit(f, angle, distance)[0]

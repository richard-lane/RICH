"""
Some functions for creating a plot

"""
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Arc
import numpy as np


def _empty_figure(figsize):
    """
    Create a blank figure for visualising the RICH alignment procedure
    
    Returns two axis handles as (ax1, ax2) for the ring image + a plot of distance against angle, respectively
    
    """
    plt.subplots(figsize=figsize)
    ax = plt.subplot2grid((1, 3), (0, 0))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.axis("off")

    ax2 = plt.subplot2grid((1, 3), (0, 1), colspan=2)
    ax2.set_ylim(0, 2)
    ax2.set_yticks([])
    ax2.set_ylabel(r"$r\ (\phi)$")

    x_tick = np.linspace(0, 2, 5)
    ax2.set_xticks(x_tick * np.pi)
    ax2.set_xlim(0, x_tick[-1] * np.pi)
    ax2.set_xticklabels([fr"${x}\pi$" for x in x_tick])
    ax2.tick_params(direction="in")
    ax2.text(np.pi, 0.1, r"$\phi\ /rad$", horizontalalignment="center")

    return ax, ax2


def _setup_diagram(ax, style="k--"):
    """
    Init all the components in the ring diagram
    
    Returns ring, ring_centre, horizontal, angled_line, phi_label, r_label
    
    """
    # Cherenkov Ring
    ring, = ax.plot(0, 0, style)

    # Tracking spot and ring centre
    ax.plot(0, 0, "r.", label="Tracking Spot")
    ring_centre, = ax.plot(0, 0, "bx", label="Cherenkov Ring Centre")
    ax.legend(loc=(-0.5, 0.9))

    # Horizontal line from the tracking spot
    horizontal, = ax.plot(0, 0, "k")

    # Angle to illustrate what we're doing
    angled_line, = ax.plot(0, 0, "k")

    # Labels
    phi_label = ax.text(0, 0, "$\\phi$")
    r_label = ax.text(0, 0, "r")

    return ring, ring_centre, horizontal, angled_line, phi_label, r_label


def _setup_plot(ax2, markerstyle=None, linestyle="-"):
    """
    Init all the components in the r(phi) plot
    
    Returns line, plot title
    
    """
    # Plot the distance from the tracking spot to the ring as a function of angle
    line, = ax2.plot((0, np.pi), (0, 2))
    if markerstyle is not None:
        line.set_marker(markerstyle)
    if linestyle is not None:
        line.set_ls(linestyle)

    title = ax2.set_title("")

    return line, title


def _create_sliders(starting_x, starting_y):
    ax_x_slider = plt.axes([0.05, 0.1, 0.3, 0.03])
    ax_y_slider = plt.axes([0.05, 0.05, 0.3, 0.03])
    x_slider = Slider(ax_x_slider, "x", -1.0, 1.0, starting_x)
    y_slider = Slider(ax_y_slider, "y", -1.0, 1.0, starting_y)

    return x_slider, y_slider


def _draw_diagram(
    ring_boundary_coords,
    ring_centre_coords,
    r0,
    n,
    horizontal_line,
    angled_line,
    ring,
    ring_centre,
    r_label,
    phi_label,
):
    """
    Draw the diagram showing the Cherenkov ring, the tracking spot and an angle originating at the tracking spot on ax
    
    Modifies the features in place 
    
    ring_boundary_coords as (ring_x, ring_y); ring_centre_coords as (x, y)
    
    """
    circle_x, circle_y = ring_boundary_coords

    # Move the ring and its central dot
    ring_centre.set_data(*ring_centre_coords)
    ring.set_data(circle_x, circle_y)

    # Update the geometric bits (horizontal line, line at an angle phi, etc.)
    horizontal_line.set_xdata((0, r0))
    angled_line.set_data((0, circle_x[n // 5]), (0, circle_y[n // 5]))
    r_label.set_position((-0.2 + circle_x[n // 5] / 2, circle_y[n // 5] / 2))

    phi = np.arctan2(circle_y[n // 5] / 5, circle_x[n // 5] / 5)
    phi_label.set_position((0.2 * np.cos(phi / 2.0), 0.2 * np.sin(phi / 2.0)))


def _draw_plot(r, phi, ring_centre_coords, n, line, title):
    """
    Draw the plot showing r(phi)
    
    """
    line.set_data(phi, r)

    x, y = ring_centre_coords
    m = 100 * np.sqrt(x ** 2 + y ** 2)
    title.set_text(f"Total Misalignment: {m:.2f}%")

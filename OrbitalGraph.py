import Satellite as Orbiter
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import math

matplotlib.use("TkAgg")
import numpy as np

# Plots orbit and displays satellite in static position
def graph_orbit(sat):
    fig = plt.figure(figsize=(8, 8))
    n = 1000
    theta = [None] * n
    r = [None] * n
    for i in range(n):
        theta[i] = (.36 * i) * (np.pi / 180)
        r[i] = (int)(sat.calculator.calculate_Gposition(theta[i]))

    x = [None] * n
    y = [None] * n
    for i in range(n):
        x[i] = r[i] * math.cos(theta[i])
        y[i] = r[i] * math.sin(theta[i])
    plt.plot(x, y)

    ax = plt.gca()
    planet = plt.Circle((0, 0), sat.planet.radius, color="g")
    ax.add_artist(planet)
    ax.set_aspect('equal', adjustable='box')
    ax.plot(sat.get_x(), sat.get_y(), marker='o', color=sat.color,
            ms=sat.size, label=sat.name)
    plt.show()

# Creates and animates the orbit of a satellite
def animate(sat):
    lines = [None]*1

    fig = plt.figure(figsize=(8,8))

    n = 1000
    theta = [None] * n
    r = [None] * n
    for i in range(n):
        theta[i] = (.36 * i) * (np.pi / 180)
        r[i] = (int)(sat.calculator.calculate_Gposition(theta[i]))

    x = [None] * n
    y = [None] * n
    for i in range(n):
        x[i] = r[i] * math.cos(theta[i])
        y[i] = r[i] * math.sin(theta[i])
    plt.plot(x, y)

    ax = plt.gca()
    planet = plt.Circle((0, 0), sat.planet.radius, color="g")
    ax.add_artist(planet)
    ax.set_aspect('equal', adjustable='box')
    for i in range(1):
        lines[i], = ax.plot(sat.get_x(), sat.get_y(), marker='o', color=sat.color,
                ms=sat.size, label=sat.name)

    ani = FuncAnimation(fig, animation, np.arange(1, 5000), fargs=[sat, lines], interval=5, blit=True, repeat=True)
    plt.show()


# Function that is repeatedly called implicitly to animate graph
def animation(i, sat, line):
    sat.update_pos()
    '''print(sat.get_position())
    print(sat.get_true_anomaly())
    print(sat.before_apoapsis)
    print(sat.get_time())
    print()'''
    for i in range(1):
        line[i].set_data(sat.rx, sat.ry)

    return line




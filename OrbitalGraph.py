import Satellite as Orbiter
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import math

matplotlib.use("TkAgg")
import numpy as np

def orbits(sats):
    lines = [None] * len(sats)
    x = [None] * len(sats)
    y = [None] * len(sats)
    positions = [None] * len(sats)

    fig = plt.figure(figsize=(8, 8))

    n = 1000
    theta = [None] * n
    for j in range(len(sats)):
        r = [None] * n
        for i in range(n):
            theta[i] = (.36 * i) * (np.pi / 180)
            r[i] = (int)(sats[j].calculator.calculate_Gposition(theta[i]))
        positions[j] = r

    for j in range(len(sats)):
        x_list = [None] * n
        y_list = [None] * n
        for i in range(n):
            pos = positions[j]
            x_list[i] = pos[i] * math.cos(theta[i])
            y_list[i] = pos[i] * math.sin(theta[i])
        x[j] = x_list
        y[j] = y_list
        plt.plot(x[j], y[j])

    ax = plt.gca()
    planet = plt.Circle((0, 0), sats[0].planet.radius, color="g")
    ax.add_artist(planet)
    ax.set_aspect('equal', adjustable='box')
    for i in range(len(sats)):
        lines[i], = ax.plot(sats[i].get_x(), sats[i].get_y(), marker='o', color=sats[i].color,
                            ms=sats[i].size, label=sats[i].name)

# Plots orbit and displays satellite in static position
def graph_orbit(sats):
    orbits(sats)
    plt.show()

def graph_transfer(sats, transfering):
    orbits(sats)
    if sats[0] is transfering:
        trans_orbit = transfering.hohmann_transfer(other_sat=sats[1])  # will not always be sats[0]
    else:
        trans_orbit = transfering.hohmann_transfer(other_sat=sats[0])

    n = 1000
    theta = [None] * n
    r = [None] * n
    for i in range(n):
        theta[i] = (.36 * i) * (np.pi / 180)
        r[i] = (int)(trans_orbit.calculator.calculate_Gposition(theta[i]))

    x_list = [None] * (n//2)
    y_list = [None] * (n//2)

    if trans_orbit.t_anomalies[0] > 0:
        for i in range(len(x_list)):
            x_list[i] = r[i+500] * math.cos(theta[i+500])
            y_list[i] = r[i+500] * math.sin(theta[i+500])
    else:
        for i in range(len(x_list)):
            x_list[i] = r[i] * math.cos(theta[i])
            y_list[i] = r[i] * math.sin(theta[i])

    plt.plot(x_list,y_list, '--')
    plt.show()



# Creates and animates the orbit of a satellite
def animate(sats):
    lines = [None] * len(sats)
    x = [None] * len(sats)
    y = [None] * len(sats)
    positions = [None] * len(sats)

    fig = plt.figure(figsize=(8, 8))

    n = 1000
    theta = [None] * n
    for j in range(len(sats)):
        r = [None] * n
        for i in range(n):
            theta[i] = (.36 * i) * (np.pi / 180)
            r[i] = (int)(sats[j].calculator.calculate_Gposition(theta[i]))
        positions[j] = r

    for j in range(len(sats)):
        x_list = [None] * n
        y_list = [None] * n
        for i in range(n):
            pos = positions[j]
            x_list[i] = pos[i] * math.cos(theta[i])
            y_list[i] = pos[i] * math.sin(theta[i])
        x[j] = x_list
        y[j] = y_list
        plt.plot(x[j], y[j])

    ax = plt.gca()
    planet = plt.Circle((0, 0), sats[0].planet.radius, color="g")
    ax.add_artist(planet)
    ax.set_aspect('equal', adjustable='box')
    for i in range(len(sats)):
        lines[i], = ax.plot(sats[i].get_x(), sats[i].get_y(), marker='o', color=sats[i].color,
                ms=sats[i].size, label=sats[i].name)

    ani = FuncAnimation(fig, animation, np.arange(1, 5000), fargs=[sats, lines], interval=5, blit=True, repeat=True)
    plt.show()


# Function that is repeatedly called implicitly to animate graph
def animation(i, sat, line):

    '''print(sat.get_position())
    print(sat.get_true_anomaly())
    print(sat.before_apoapsis)
    print(sat.get_time())
    print()'''
    for i in range(len(sat)):
        sat[i].update_pos()
        line[i].set_data(sat[i].rx, sat[i].ry)


    return line




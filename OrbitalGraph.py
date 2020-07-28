import Satellite as Orbiter
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import math
import numpy as np

matplotlib.use("TkAgg")


# Creates a figure object and plots the orbits of satellites in 'sats'
def orbits(sats):
    lines = [None] * len(sats)
    x = [None] * len(sats)
    y = [None] * len(sats)
    positions = [None] * len(sats)

    fig = plt.figure(figsize=(8, 8))

    # Calculates position in orbit at a specified angle
    # Angle ranges from 0 - 2 pi radians incrementing by 2pi/1000
    n = 1000
    theta = [None] * n
    for j in range(len(sats)):
        r = [None] * n
        for i in range(n):
            theta[i] = (.36 * i) * (np.pi / 180)
            r[i] = (int)(sats[j].calculator.calculate_position(theta[i]))
        positions[j] = r

    # Calculates components to each position calculated
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

    # Plot
    ax = plt.gca()
    planet = plt.Circle((0, 0), sats[0].planet.radius, color="g")
    ax.add_artist(planet)
    ax.set_aspect('equal', adjustable='box')
    for i in range(len(sats)):
        lines[i], = ax.plot(sats[i].get_x(), sats[i].get_y(), marker='o', color=sats[i].color,
                            ms=sats[i].size, label=sats[i].name)

    return [fig, lines]

# Plots orbit and displays satellite in static position
def graph_orbit(sats):
    orbits(sats)
    plt.show()

# Plots orbits and displays transfer orbit with satellites at position right before transfer
def graph_transfer(sats, transfering):

    if sats[0] is transfering:
        other_sat=sats[1]
    else:
        other_sat = sats[0]

    trans_orbit = transfering.hohmann_transfer(other_sat)
    intercept_values = transfering.hohmann_intercept(other_sat)

    orbits(sats)

    # Calculates position in transfer orbit at a specified angle
    # Angle ranges from 0 - 2pi radians incrementing by 2pi/1000
    n = 1000
    theta = [None] * n
    r = [None] * n
    for i in range(n):
        theta[i] = (.36 * i) * (np.pi / 180)
        r[i] = (int)(trans_orbit.calculator.calculate_position(theta[i]))

    x_list = [None] * (n//2)
    y_list = [None] * (n//2)

    # Position components for decreasing transfer (large orbit to small orbit)
    if trans_orbit.t_anomalies[0] > 0:
        for i in range(len(x_list)):
            x_list[i] = r[i+500] * math.cos(theta[i+500])
            y_list[i] = r[i+500] * math.sin(theta[i+500])

    # Position components for increasing transfer (small orbit to large orbit)
    else:
        for i in range(len(x_list)):
            x_list[i] = r[i] * math.cos(theta[i])
            y_list[i] = r[i] * math.sin(theta[i])

    print(intercept_values)
    plt.plot(x_list,y_list, '--')
    plt.show()

# Plots orbits and displays transfer orbit with animated satellites
def animate_transfer(sats, transferring):
    values = orbits(sats)
    fig = values[0]
    lines = values[1]

    if sats[0] is transferring:
        other_sat=sats[1]
        original_orbit = sats[0]
        trans_orbit = transferring.hohmann_transfer(other_sat)
        sats[0] = trans_orbit
    else:
        other_sat = sats[0]
        original_orbit = sats[1]
        trans_orbit = transferring.hohmann_transfer(other_sat)
        sats[1] = trans_orbit

    intercept_values = transferring.hohmann_intercept(other_sat)

    # Calculates position in transfer orbit at a specified angle
    # Angle ranges from 0 - 2pi radians incrementing by 2pi/1000
    n = 1000
    theta = [None] * n
    r = [None] * n
    for i in range(n):
        theta[i] = (.36 * i) * (np.pi / 180)
        r[i] = (int)(trans_orbit.calculator.calculate_position(theta[i]))

    x_list = [None] * (n // 2)
    y_list = [None] * (n // 2)

    # Position components for decreasing transfer (large orbit to small orbit)
    if trans_orbit.t_anomalies[0] > 0:
        for i in range(len(x_list)):
            x_list[i] = r[i + 500] * math.cos(theta[i + 500])
            y_list[i] = r[i + 500] * math.sin(theta[i + 500])

    # Position components for increasing transfer (small orbit to large orbit)
    else:
        for i in range(len(x_list)):
            x_list[i] = r[i] * math.cos(theta[i])
            y_list[i] = r[i] * math.sin(theta[i])

    plt.plot(x_list, y_list, '--')
    print(intercept_values)
    total_frames = intercept_values[2]-5

    ani = FuncAnimation(fig, animation, np.arange(1, total_frames), fargs=[sats, lines], interval=1, blit=True, repeat=False)
    plt.show()

# Plots orbit and displays satellite in static position
def animate_orbit(sats):
    values = orbits(sats)
    fig = values[0]
    lines = values[1]
    ani = FuncAnimation(fig, animation, np.arange(1, 500), fargs=[sats, lines], interval=1, blit=True, repeat=True)
    plt.show()


# Function that is repeatedly called implicitly to animate graph
def animation(i, sat, line):

    for i in range(len(sat)):
        sat[i].update_pos()
        line[i].set_data(sat[i].rx, sat[i].ry)


    return line




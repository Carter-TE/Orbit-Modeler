import Satellite as Orbiter
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import math

matplotlib.use("TkAgg")
import numpy as np


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
    '''ax.plot(sat.get_x(), sat.get_y(), marker='o', color=sat.color,
            ms=sat.size, label=sat.name)'''
    #plt.show()

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

    ani = FuncAnimation(fig, animation, np.arange(1, 5000), fargs=[sat, lines], interval=20, blit=True, repeat=True)
    plt.show()


def graph_future_orbit(sat):
    graph_orbit(sat)
    ax = plt.gca()
    # r = sat.predict_pos()
    # x =
    ax.plot(sat.get_x(), sat.get_y(), marker='o', color='r',
            ms=sat.size, label=sat.name)




# def ani_graph(satellites):
def main():
    sat_num = 1
    mass = 2.646e19
    radius = 60000
    apo = 117674
    peri = 6701
    pos = 91065

    planet = Orbiter.Body(radius, mass)

    s1 = Orbiter.Satellite(planet, pos, apo, peri, bapo=True)
    s1.name = 'Sat 1'

    satellites = [None] * sat_num
    for i in range(sat_num):
        satellites[i] = s1  # will change this later to be able to add different satellites

    lines = [None] * (len(satellites))
    fig = plt.figure(figsize=(5, 5))
    ax = plt.subplot()
    planet = plt.Circle((0, 0), satellites[0].planet.radius, color="g")
    ax.add_artist(planet)
    ax.set_aspect('equal', adjustable='box')

    count = 0
    for sat in satellites:
        x = sat.get_x()
        y = sat.get_y()
        lines[count], = ax.plot(x, y, marker='o', color=sat.color,
                               ms=sat.size, label=sat.name)
        graph(sat)
        count += 1


    ani = FuncAnimation(fig, animation, np.arange(1, 1000), fargs=[satellites, lines],
                                  interval=20, blit=True, repeat=True)

    plt.show()




def animation(i, sat, line):
    '''
    Calls update_parameters on a given particle
    :return:
    '''

    sat.pos_update()
    print(sat.get_position())
    print(sat.get_true_anomaly())
    print(sat.before_apoapsis)
    print(sat.get_time())
    print()
    for i in range(1):
        line[i].set_data(sat.rx, sat.ry)

    return line


if __name__ == '__main__':
    at_num = 1
    mass = 2.646e19
    radius = 60000
    apo = 117674
    peri = 6701
    pos = 91065

    planet = Orbiter.Body(radius, mass)

    s1 = Orbiter.Satellite(planet, pos, apo, peri, bapo=True)
    s1.name = 'Sat 1'
    graph(s1)
    plt.show()


import Satellite
import OrbitalGraph as grapher
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import math


def main():
    sat_num = 1
    mass = 2.646e19
    radius = 60000
    apo = 23813
    peri = 13106
    pos = 23094

    planet = Satellite.Body(radius, mass)
    s1 = Satellite.Satellite(planet, apo, peri, pos=apo-500, bapo=True)
    #s1.update_pos(1641)
    print(s1.true_anomaly)
    print(s1.get_position())
    print()

    '''for i in range(100):
        s1.pos_update()
        print(s1.true_anomaly)
        print(s1.get_position())'''

    grapher.animate(s1)




    '''for i in range(1642):
        print(i)
        s1.pos_update()
        print("Position:\t\t\t\t",s1.get_position())
        print("True anom:\t\t\t\t",s1.true_anomaly)
        print("Time:\t\t\t\t\t",s1.get_time())
        print()
        #grapher.graph_orbit(s1)'''



    #print(s1.predict_pos(3193))
    #print(s1.get_position())




if __name__ == '__main__':
    main()

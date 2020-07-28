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
    apo = 117674
    peri = 6701
    pos = 6701

    planet = Satellite.Body(radius, mass)
    s1 = Satellite.Satellite(planet, pos, apo, peri, True)
    s1.update_pos(3193)
    print(s1.true_anomaly)

    s1.update_pos(3100)
    print("Position: ", s1.get_position())
    print("True anom: ", s1.true_anomaly)

    '''for i in range(3193):
        s1.update_pos()
        print(i)
        print("Position: ",s1.get_position())
        print("True anom: ",s1.true_anomaly)
        print()'''



    #print(s1.predict_pos(3193))
    #print(s1.get_position())




if __name__ == '__main__':
    main()

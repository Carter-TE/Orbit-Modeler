import OrbitalPositionCalculator as calc
import OrbitalGraph as grapher
from matplotlib import pyplot as plt
import matplotlib
import math
matplotlib.use("TkAgg")


class Body(object):

    def __init__(self, rad, mass):
        self.radius = rad
        self.mass = mass


class Satellite(object):

    def __init__(self, planet, apo, peri, pos = None, bapo=True):



        self.before_apoapsis = bapo
        # self.period = (int)(2*math.pi*(self.a**3/(6.673e-11*planet.mass))**.5)

        self.periapsis = peri
        self.apoapsis = apo
        if pos is None:
            self.pos = peri
        else:
            self.pos = pos
        self.rx = 0
        self.ry = 0


        self.planet = planet
        self.calculator = calc.Orbit_Calculator(self.planet, self.pos, apo, peri,)

        self.del_t = self.calculator.elapsed_time(bapo)+1
        self.true_anomaly = self.calculator.calc_true_anom(bapo = self.before_apoapsis)


        self.color = 'k'
        self.size = 5
        self.name = None

    def calc_bapo(self):
        if self.del_t >= self.calculator.T/2 and self.del_t < self.calculator.T:
            self.before_apoapsis = False

        elif self.del_t >= self.calculator.T:
            time = self.del_t - self.calculator.T
            self.del_t = 0
            self.update_del_t(time)
            self.calc_bapo()

        else:
            self.before_apoapsis = True


    # Updates elapsed time
    def update_del_t(self, time):
        self.del_t = self.del_t + time

    def update_pos(self, time=5):
        self.pos = self.calculator.calculate_position(time, self.before_apoapsis)
        self.calculator.pos = self.pos
        self.update_del_t(time)
        self.calc_bapo()
        self.true_anomaly = self.calculator.calc_true_anom(bapo=self.before_apoapsis)
        self.rx = self.get_x()
        self.ry = self.get_y()

    def predict_pos(self, time=1):
        values = [None]*4
        self.pos = self.calculator.calculate_position(time, self.before_apoapsis)
        values[0] = self.pos
        values[1] = self.calculator.true_anomaly
        values[2] = values[0] * math.cos(values[1])
        values[3] = values[0] * math.sin(values[1])
        self.pos = self.calculator.pos
        self.calculator.true_anomaly = self.true_anomaly
        return values

    def pos_update(self):
        time = 1
        nu = self.calculator.approx_tru_anom(time, self.before_apoapsis, self.true_anomaly)
        self.true_anomaly = self.calculator.true_anomaly = nu
        self.pos = self.calculator.calculate_Gposition(nu)
        self.calculator.pos = self.pos
        self.update_del_t(time)
        self.calc_bapo()
        self.rx = self.get_x()
        self.ry = self.get_y()




    def get_time(self):
        return self.del_t

    def get_position(self):
        return self.calculator.pos - self.planet.radius

    def get_eccentricity(self):
        return self.calculator.e

    def get_semimajor_axis(self):
        return self.calculator.a

    def get_apoapsis(self):
        return self.calculator.apo - self.planet.radius

    def get_periapsis(self):
        return self.calculator.peri - self.planet.radius

    def get_period(self):
        return self.calculator.T

    def get_true_anomaly(self):
        return self.true_anomaly

    def get_x(self):
        x = self.calculator.pos * math.cos(self.get_true_anomaly())
        return x

    def get_y(self):
        y = self.calculator.pos * math.sin(self.get_true_anomaly())
        return y


if __name__ == '__main__':
    '''
    mass = float(input("Enter mass of primary body: "))
    radius = float(input("Enter radius of primary body: "))
    apo = float(input("Enter distance from Apoapsis to surface (m): "))
    peri = float(input("Enter distance from Periapsis to surface (m): "))
    pos = float(input("Enter satellites initial position: "))
    del_t = float(input("Enter change in time: "))
    bapo = input("Before apoapsis: (T/F)")

    #  TEST 1 VALUES
    '''
    sat_num = 1
    mass = 2.646e19
    radius = 60000
    apo = 117674
    peri = 6701
    pos = 6701
    #del_t = 3193


    #a = calc.calc_semimajor_axis(radA, radP)  # Semi-major axis
   # e = calc.calc_eccentricity(radA, radP)

    planet = Body(radius, mass)

    s1 = Satellite(planet, pos, apo, peri, bapo=True)
    s1.name = 'Sat 1'

    satellites = [None] * sat_num
    for i in range(sat_num):
        satellites[i] = s1  # will change this later to be able to add different satellites


    '''s1.update_pos(3193)
    print(s1.get_position())
    print(s1.get_time())'''

    '''satellites[0].update_pos(3193)
    print(satellites[0].get_position())
    print(satellites[0].get_time())'''  # TEST CASE: GOOD

    #grapher.graph(s1)


    grapher.ani_graph(satellites)
    plt.show()



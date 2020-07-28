import OrbitalPositionCalculator as calc
import matplotlib
import math

class Body(object):
    def __init__(self, rad, mass):
        self.radius = rad
        self.mass = mass


class Satellite(object):
    def __init__(self, planet, apo, peri, pos = None, bapo=True, transfer=False):

        self.before_apoapsis = bapo
        self.periapsis = peri
        self.apoapsis = apo
        if pos is None:
            self.pos = peri
        else:
            self.pos = pos
        self.rx = 0
        self.ry = 0
        self.planet = planet
        self.calculator = calc.Orbit_Calculator(self.planet, self.pos, apo, peri, bapo)

        self.calculator.area = self.calculator.calculate_area(0, self.calculator.approx_tru_anom(1, True, 0))
        self.calculator.init_t_anon = self.calculator.approx_tru_anom(1, True, 0)
        self.t_anomalies = self.calculator.init_angles(transfer)

        self.del_t = self.calculator.elapsed_time(bapo)
        self.true_anomaly = self.calculator.calc_true_anom(bapo=self.before_apoapsis)


        self.color = 'k'
        self.size = 5
        self.name = None

    # Calculates whether the satellite is before or after the apoapsis
    # Updates before_apoapsis value
    def calc_bapo(self):
        if self.del_t >= self.calculator.T/2 and self.del_t < self.calculator.T:
            self.before_apoapsis = self.calculator.bapo = False

        elif self.del_t >= self.calculator.T:
            time = self.del_t - self.calculator.T
            self.del_t = 0
            self.update_del_t(time)
            self.calc_bapo()

        else:
            self.before_apoapsis = self.calculator.bapo = True


    # Updates elapsed time
    def update_del_t(self, time):
        self.del_t = self.calculator.del_t = self.del_t + time

    # Updates satellite position given a change in time
    def update_pos(self, time=1):
        self.update_del_t(time)
        self.pos = self.calculator.calculate_Gposition(self.t_anomalies[self.del_t])
        self.calculator.pos = self.pos
        self.calc_bapo()
        self.true_anomaly = self.calculator.true_anomaly = self.t_anomalies[self.del_t]
        self.rx = self.get_x()
        self.ry = self.get_y()

    # Predicts satellite position values given a change in time
    # Returns list [position, true anomaly, x-component, y-component]
    def predict_pos(self, time=1):
        values = [None]*4
        pos = self.calculator.calculate_Gposition(self.t_anomalies[self.del_t+time])
        values[0] = pos
        values[1] = self.t_anomalies[self.del_t+time]
        values[2] = values[0] * math.cos(values[1])
        values[3] = values[0] * math.sin(values[1])
        return values

    # Creates transfer orbit from peri of one orbit to apo of ther
    def hohmann_transfer(self, n_peri=None, n_apo=None, other_sat=None):
        if n_apo is None:
            n_apo = other_sat.get_apoapsis()
            n_peri = other_sat.get_periapsis()
        if n_apo > self.apoapsis:
            transfer_orbit = Satellite(self.planet, n_apo, self.periapsis, transfer=True)
        else:
            transfer_orbit = Satellite(self.planet, self.apoapsis, n_peri)
            temp_anomalies = [None] * ((transfer_orbit.get_period() //2)+1)
            for i in range(((transfer_orbit.get_period() //2))):
                num = i + ((transfer_orbit.get_period() //2))
                temp_anomalies[i] = transfer_orbit.t_anomalies[num]
            transfer_orbit.t_anomalies = temp_anomalies
        return transfer_orbit


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





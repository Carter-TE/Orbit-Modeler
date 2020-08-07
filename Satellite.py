import OrbitalPositionCalculator as calc
import matplotlib
import math

class Body(object):
    def __init__(self, rad, mass):
        self.radius = rad
        self.mass = mass

    def __eq__(self, other):
        return self.radius == other.radius and self.mass == other.mass


class Satellite(object):
    def __init__(self, planet, apo, peri, pos = None, bapo=True, transfer=False):

        self.before_apoapsis = bapo # Before APOapsis
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

        self.calculator.area = self.calculator.calculate_area(0, 2*math.pi) / self.calculator.T
        self.calculator.init_t_anon = self.calculator.approx_tru_anom(1, True, 0)
        self.t_anomalies = self.calculator.init_angles(transfer)

        self.del_t = self.calculator.elapsed_time(bapo)
        self.orbit_delta_t = self.del_t

        self.color = 'k'
        self.size = 5
        self.name = None

    def __eq__(self, other):
        if self.apoapsis == other.apoapsis and self.periapsis == other.periapsis:
            return self.planet == other.planet
        return False

    # Calculates whether the satellite is before or after the apoapsis
    # Updates before_apoapsis value
    def calc_bapo(self):
        if self.orbit_delta_t >= self.calculator.T/2 and self.orbit_delta_t < self.calculator.T:
            self.before_apoapsis = self.calculator.bapo = False

        elif self.orbit_delta_t >= self.calculator.T:
            time = self.orbit_delta_t - self.calculator.T
            self.orbit_delta_t = 0
            self.update_del_t(time)
            self.calc_bapo()

        else:
            self.before_apoapsis = self.calculator.bapo = True


    # Updates elapsed time
    def update_del_t(self, time):
        self.del_t = self.calculator.delta_t = self.del_t + time

    # Updates satellite position given a change in time
    def update_pos(self, time=1):
        self.update_del_t(time)

        orbit_del_t = self.orbit_delta_t
        while orbit_del_t + time > self.get_period():
            time = time - self.get_period()

        orbit_del_t = time + orbit_del_t

        self.pos = self.calculator.calculate_position(self.t_anomalies[orbit_del_t])
        self.calculator.pos = self.pos
        self.calc_bapo()
        self.orbit_delta_t = self.calculator.orbit_delta_t = orbit_del_t
        self.rx = self.get_x()
        self.ry = self.get_y()

    # Predicts satellite position values given a change in time
    # Returns list [position, elapsed time in current orbit, position x-component, position y-component]
    def predict_pos(self, time=1):
        values = [None]*4

        orbit_del_t = self.orbit_delta_t
        while orbit_del_t + time > self.get_period():
            time = time - self.get_period()

        orbit_del_t = time + orbit_del_t

        predicted_pos = self.calculator.calculate_position(self.t_anomalies[orbit_del_t])
        values[0] = predicted_pos
        values[1] = orbit_del_t
        values[2] = values[0] * math.cos(self.t_anomalies[orbit_del_t])
        values[3] = values[0] * math.sin(self.t_anomalies[orbit_del_t])
        return values

    # Creates transfer orbit from peri/apo of one orbit to apo/peri of other
    def hohmann_transfer(self, other_sat):
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

    # Calculates values for an intercept using a Hohmann transfer
    # Returns list
    # [initial pos of transferring, initial pos of other sat, delta t of the transfer, time until transfer]
    def hohmann_intercept(self, other_sat=None):
        values = [None] * 5
        transfer_orbit = self.hohmann_transfer(other_sat)


        # delta t of transfer
        transfer_time = len(transfer_orbit.t_anomalies) - 1
        values[2] = transfer_time

        # Position of transferring sat to intercept
        pos1 = transfer_orbit.calculator.calculate_position(transfer_orbit.t_anomalies[0])
        values[4] = transfer_orbit.calculator.transfer_dv(pos1)  # Delta v values for transfer
        pos1 = pos1 - self.planet.radius
        values[0] = pos1

        # Position of other sat to intercept
        if transfer_orbit.t_anomalies[0] > 0:
            time = other_sat.get_period() - transfer_time
            pos2 = other_sat.calculator.calculate_position(other_sat.t_anomalies[time])
        else:
            time = (other_sat.get_period()//2) - transfer_time
            pos2 = other_sat.calculator.calculate_position(other_sat.t_anomalies[time])
        pos2 = pos2 - self.planet.radius
        values[1] = pos2

        values[2] = transfer_time

        # Time until transfer
        time_2_transfer = 0
        count = 1
        while self.get_position() != values[0] or other_sat.get_position() != values[1]:
            if self.get_position() == values[0]:
                self.update_pos(self.get_period())
                other_sat.update_pos(self.get_period())
                time_2_transfer = time_2_transfer + self.get_period()
            else:
                self.update_pos()
                other_sat.update_pos()
                time_2_transfer = time_2_transfer + 1
            count = count+1

        values[3] = int(time_2_transfer)


        return values

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
        return self.orbit_delta_t

    def get_x(self):
        x = self.calculator.pos * math.cos(self.t_anomalies[self.get_true_anomaly()])
        return x

    def get_y(self):
        y = self.calculator.pos * math.sin(self.t_anomalies[self.get_true_anomaly()])
        return y





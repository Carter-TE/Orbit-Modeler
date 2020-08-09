import math as math
from scipy import integrate


''' For all calculations work from center of body
    i.e. always include radius in distances.
    All incoming values are expected to have radius measure included

        for x in times:
        print(x)
'''


class Orbit_Calculator():
    def __init__(self, body, pos, a, p, bapo=True):
        self.apo = a + body.radius  # Apoapsis to center
        self.peri = p + body.radius  # Periapsis to center

        self.mass = body.mass
        self.init_pos = self.pos = pos + body.radius
        self.a = (self.apo + self.peri) / 2  # Semi-major axis
        self.e = (self.apo - self.peri) / (self.apo + self.peri)
        self.T = (int)(2 * math.pi * (self.a ** 3 / (6.673e-11 * self.mass)) ** .5)
        self.delta_t = 0

        self.orbit_delta_t = 0
        self.area = 0
        self.bapo = bapo

    # Calculates ellapsed time in orbit using position values
    # Should only be used when delta_t is null
    def elapsed_time(self, bapo):
        if self.pos == self.peri:
            self.delta_t = 0
            return self.delta_t
        nu = self.calc_true_anom(self.pos, bapo)
        E = self.calc_ecc_anom(nu, bapo)
        M0 = self.calc_imean_anom(E)
        n = self.calc_mean_motion()
        time = int(((2 * math.pi) - M0) / n)
        self.delta_t = self.T - time
        return self.delta_t

    # Calculates the error for the true anomaly
    # The error is of the order e3
    def calc_error(self, nu=None, bapo=None):
        if nu is None:
            nu = self.calc_true_anom(self.pos, bapo)
        error = nu * (self.e ** 3)
        return error

    def calc_semimajor_axis(self, ra, rp):
        return (ra + rp) / 2

    def calc_eccentricity(self, ra, rp):
        return (ra - rp) / (ra + rp)

    #  Calculates the True anomaly using position
    #  Currently used to calculate initial true anomaly from initial position
    def calc_true_anom(self, p0=None, bapo=True):
        if p0 is None:
            p0 = self.pos
        num1 = (self.a * (1 - self.e ** 2)) / p0
        num1 = num1 - 1
        num1 = num1 * (1 / self.e)
        if (num1 > 1):
            num1 = 1
        elif (num1 < -1):
            num1 = -1
        nu = math.acos(num1)
        if bapo is False:
            nu = (2 * math.pi) - nu
        # print("Initial true anom: ", nu)
        return nu

    #  Calculates the eccentric anomaly using the true anomaly
    #  Currently used to calculate the initial eccentric anomaly using the initial true anomaly
    def calc_ecc_anom(self, nu, bapo):
        num1 = (self.e + math.cos(nu)) / (1 + (self.e * math.cos(nu)))
        eccentric_anom = math.acos(num1)
        if (bapo == False):
            return (2 * math.pi) - eccentric_anom
        return eccentric_anom

    def calc_mean_motion(self):
        num1 = self.mass * 6.67E-11
        num1 = num1 / (self.a ** 3)
        n = num1 ** (1 / 2)
        return n

    #  Calculates mean anomaly using the eccentric anomaly
    #  Currently used to calculate the initial mean anomaly based of the initial eccentric anomaly
    def calc_imean_anom(self, Eanom):
        return Eanom - (self.e * math.sin(Eanom))

    #  Calculates Mean anomaly after delta t
    def calc_mean_anom(self, t, bapo, nu0=None):
        if nu0 is None:
            nu0 = self.calc_true_anom(bapo=bapo)
        E0 = self.calc_ecc_anom(nu0, bapo)
        M0 = self.calc_imean_anom(E0)
        n = self.calc_mean_motion()
        M = (n * t) + M0
        return M

    #  Approximates true anomaly after delta t
    #  Used to calculate estimated position after delta t
    def approx_tru_anom(self, t, bapo, nu0=None):
        m = self.calc_mean_anom(t, bapo, nu0)
        # print("predicted mean anom", m)
        nu = m + (2 * self.e * math.sin(m)) + (1.25 * self.e ** 2 * math.sin(2 * m))
        return nu

    # Callable helper method to adjust accuracy of true anomalies
    def make_accurate(self, nu, prev):
        hi = nu + .001
        lo = nu - .001
        area = self.area  # * (self.del_t-1)
        if self.e >= .1:
            hi = hi + (nu*self.e)
            lo = lo - (nu*self.e)
        if self.calculate_area(prev, hi) < area:
            hi = hi+1
        accurate_nu = self.accuracy_BS(nu, hi, lo, area, prev)
        return accurate_nu

    # Uses a binary search to make approximated true anomaly more accurate
    # Not explicitly called
    def accuracy_BS(self, nu, hi, lo, area, prev):
        temp_area = self.calculate_area(prev, nu)
        if temp_area > area + 500:
            hi = nu
            nu = (hi + lo) / 2
            return self.accuracy_BS(nu, hi, lo, area, prev)

        elif temp_area < area - 500:
            lo = nu
            nu = (hi + lo) / 2
            return self.accuracy_BS(nu, hi, lo, area, prev)

        else:
            return nu

    #  Calculates future position based on change in time (essentially r(t), actually r(nu))
    def calculate_position(self, t, bapo):
        nu = self.approx_tru_anom(t, bapo)
        true_anon = self.make_accurate(nu, bapo)
        r = (self.a * (1 - (self.e ** 2))) / (1 + (self.e * math.cos(true_anon)))
        return round(r)

    # Calculates position given true anomaly
    # Used to draw ellipse of orbit in OrbitalGraph.py
    def calculate_Gposition(self, nu):
        r = (self.a * (1 - (self.e ** 2))) / (1 + (self.e * math.cos(nu)))
        return round(r)

    # Calculates area swept out in any part of the orbit
    # start and end are angles, specifically the initial and final true anomalies of a sector
    def calculate_area(self, start, end):
        eqs = lambda nu: .5 * ((self.a * (1 - (self.e ** 2))) / (1 + (self.e * math.cos(nu)))) ** 2
        ans = integrate.quad(eqs, start, end)
        return ans[0]

    # Creates an array of size T (period in seconds) and finds the true anomaly at every second in an orbit
    def init_angles(self, transfer):
        if transfer:
            t_anomalies = [None] * ((self.T //2)+1)
        else:
            t_anomalies = [None] * (self.T + 1)
            t_anomalies[self.T] = 2 * math.pi
        t_anomalies[0] = 0
        t_anomalies[self.T // 2] = math.pi

        bapo = True
        for i in range(len(t_anomalies)):
            if i == 0 or i == self.T // 2 or i == self.T:
                continue
            if i > self.T // 2:
                bapo = False
            prev = t_anomalies[i - 1]
            current = self.approx_tru_anom(1, bapo, prev)
            try:
                current = self.make_accurate(current, prev)
            except Exception as e:
                print(i, e)
            t_anomalies[i] = current

        return t_anomalies

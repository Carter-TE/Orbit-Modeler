import math as math
import OrbitalGraph


''' For all calculations work from center of body 
    i.e. always include radius in distances.
    All incoming values are expected to have radius measure included
    
        for x in times:
        print(x)
    '''

class Orbit_Calculator():
    def __init__(self, body, pos, a, p, ):
        self.apo = a + body.radius  # Apoapsis to center
        self.peri = p + body.radius  # Periapsis to center

        self.mass = body.mass
        self.init_pos = self.pos = pos + body.radius
        self.a = (self.apo + self.peri) / 2  # Semi-major axis
        self.e = (self.apo - self.peri) / (self.apo + self.peri)
        self.T = (int)(2 * math.pi * (self.a ** 3 / (6.673e-11 * self.mass)) ** .5)

        self.true_anomaly = 0


    # Calculates the estimated elapsed time since Periapsis
    # Used to help calculate orbital position given initial position
    '''def elapsed_time(self,bapo):
        # creates array of times where values are (index - 1) seconds
        # First half of orbit
        if bapo:
            count = 0
            times = range(1, (int)(self.T/2)+1)
            for x in times:
                print(x)
                count+=1
            print(count)
        # Second half of orbit
        else:
            times = [None]* ((int)(self.T+1)-(int)(self.T / 2) + 1)
            count = self.T
            print(times)

            for x in range(((int)(self.T+1)-(int)(self.T / 2) + 1)):
                times[(int)(x)] = count
                count -= 1

        # Binary search through possible times to find elapsed time
        print(times)
        delta_t = self.binary_search(times, 0, len(times)-1, self.init_pos, bapo)
        return delta_t

    # Helper method used to help calculate initial elapsed time
    # Use binary search on times array, comparing the position at a given delta t to the initial position inputted
    def binary_search(self, arr, lo, hi, ans, bapo):
        mid = (hi+lo)//2

        error = self.calc_error(bapo)
        nu = self.calc_true_anom(self.e, self.pos, bapo)

        upper_bound = self.calculate_Gposition(nu+error)  # position calculated using maximum error in true anomaly
        lower_bound = self.calculate_Gposition(nu-error)  # position calculated using minimum error in true anomaly
        temp_pos = self.pos_from_peri(arr[mid], bapo)     # estimated position based off of time from binary search

        # Binary search
        #  +- 5 meters to upper and lower bound (wiggle room)
        if temp_pos <= upper_bound+5 and temp_pos >=lower_bound-5:
            return arr[mid]
        elif temp_pos > upper_bound+5:
            return self.binary_search(arr, lo, mid-1, ans, bapo)
        else:
            return self.binary_search(arr, mid + 1, hi, ans, bapo)'''

    def elapsed_time(self, bapo):
        nu = self.calc_true_anom(self.pos, bapo)
        E = self.calc_ecc_anom(nu, bapo)
        M0 = self.calc_imean_anom(E)
        n = self.calc_mean_motion()
        time = int(((2 * math.pi) - M0)/n)
        return self.T - time

    # Helper method to estimate final position after a given change in time from periapsis
    def pos_from_peri(self, t, bapo):
        nu = self.approx_tru_anom(self.e, t)
        r = (self.a * (1 - (self.e ** 2))) / (1 + (self.e * math.cos(nu)))
        return (int)(r)

    # Calculates the error for the true anomaly
    # The error is of the order e3
    def calc_error(self, bapo):
        nu = self.calc_true_anom(self.pos, bapo)
        error = nu * (self.e**3)
        return error

    def calc_semimajor_axis(self, ra, rp):
        return (ra + rp) / 2


    def calc_eccentricity(self, ra, rp):
        return (ra - rp) / (ra + rp)


    #  Calculates the True anomaly using position
    #  Currently used to calculate initial true anomaly from initial position
    def calc_true_anom(self, p0 = None, bapo = True):
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
        self.true_anomaly = nu
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
    def calc_mean_anom(self, t, bapo, nu0 = None):
        if nu0 is None:
            nu0 = self.calc_true_anom(bapo=bapo)
        E0 = self.calc_ecc_anom(nu0, bapo)
        M0 = self.calc_imean_anom(E0)
        n = self.calc_mean_motion()
        M = (n * t) + M0
        # print("Initial Mean Anomaly:\t", M0)
        # print("Initial Eccentric Anom:\t",E0)
        # print("Final Mean Anomaly:\t\t",M)
        return M


    #  Approximates true anomaly after delta t
    #  Used to calculate estimated position after delta t
    def approx_tru_anom(self, t, bapo, nu0 = None):
        m = self.calc_mean_anom(t, bapo, nu0)
        #print("predicted mean anom", m)
        nu = m + (2 * self.e * math.sin(m)) + (1.25 * self.e ** 2 * math.sin(2 * m))
        return nu


    #  Calculates future position based on change in time (essentially r(t), actually r(nu))
    def calculate_position(self, t, bapo):
        nu = self.approx_tru_anom(t, bapo)
        r = (self.a * (1 - (self.e ** 2))) / (1 + (self.e * math.cos(nu)))
        return round(r)

    #Calculates position given true anomaly
    # Used to draw ellipse of orbit in OrbitalGraph.py
    def calculate_Gposition(self,  nu):
        r = (self.a * (1 - (self.e ** 2))) / (1 + (self.e * math.cos(nu)))
        return round(r)


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
    mass = 2.646e19
    radius = 60000
    apo = 117674
    peri = 6701
    pos = 117674
    del_t = 3193
    bapo = True
    #  Answer should be close to peri (current ans = 1709801)


    # radA = apo + radius     # Apoapsis to center
    # radP = peri + radius    # Periapsis to center
    p0 = pos + radius       # Initial position to center



    #OrbitalGraph.graph(a,e, radius)

    '''position = calculate_position(a, e, mass, del_t, p0, bapo)
    # print("Predicted position: ", round(position) - radius)
    itruanom = calc_true_anom(a, e, 91065+radius, True)
    print(itruanom)
    E = calc_ecc_anom(e, itruanom, True)
    print("Eccentric anomaly: ", E)
    print("Mean anomaly", calc_imean_anom(e, E))'''

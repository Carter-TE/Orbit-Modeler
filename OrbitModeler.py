import Satellite
import OrbitalGraph as grapher



def main():
    sat_num = 1
    mass = 2.646e19
    radius = 60000
    apo = 117674
    peri = 6701
    pos = 23094

    planet = Satellite.Body(radius, mass)
    sats = [None]*1
    s1 = Satellite.Satellite(planet, apo, peri, pos=apo, bapo=True)
    #s2 = Satellite.Satellite(planet, 23813, 13106, pos=13106, bapo=True)

    sats[0] = s1
    #sats[1] = s2

    #s2.hohmann_transfer(other_sat=s1)

    print(s1.t_anomalies)
    print(len(s1.t_anomalies))
    print(s1.get_period())
    grapher.graph_orbit(sats)










if __name__ == '__main__':
    main()
    '''
       mass = float(input("Enter mass of primary body: "))
       radius = float(input("Enter radius of primary body: "))
       apo = float(input("Enter distance from Apoapsis to surface (m): "))
       peri = float(input("Enter distance from Periapsis to surface (m): "))
       pos = float(input("Enter satellites initial position: "))
       del_t = float(input("Enter change in time: "))
       bapo = input("Before apoapsis: (T/F)")'''

import Satellite
import OrbitalGraph as grapher
import math



def main():
    sat_num = 1
    mass = 2.646e19
    radius = 60000
    apo = 117674
    peri = 40000
    pos = 523222

    planet = Satellite.Body(radius, mass)
    sats = [None]*2
    s1 = Satellite.Satellite(planet, apo, peri, pos=peri, bapo=True)
    print('Sat 1 status: Initialized')
    s2 = Satellite.Satellite(planet, 23813, 13106, pos=13106, bapo=True)
    print('Sat 2 status: Initialized')
    # s1 = Satellite.Satellite(planet, apo, 13106, pos=apo, bapo=True)
    print('Done')


    # s2.update_pos(7703000)



    grapher.animate_transfer(sats, s2)
    # grapher.graph_transfer(sats, s2)
    # grapher.animate_orbit(sats)
    # grapher.graph_orbit(sats)





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

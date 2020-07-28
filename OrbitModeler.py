import Satellite
import OrbitalGraph as grapher



def main():
    sat_num = 1
    mass = 5.2915158e22
    radius = 600000
    apo = 554526
    peri = 553941
    pos = 23094

    planet = Satellite.Body(radius, mass)
    s1 = Satellite.Satellite(planet, apo, peri, pos=peri, bapo=True)


    grapher.animate(s1)







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

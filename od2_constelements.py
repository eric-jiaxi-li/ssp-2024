"""
Calculate constant orbital elements

All testcases passed; runs fine

Eric Li
"""
import numpy as np
import odlib
from math import *

debug = True

def baby_od_const_elements(filename):
    """
    Params: Text file containing the input format specified below
    Return: PRINT orbital elements and error from true values
            Only works for the specified asteroid in LiInput.txt,
            NOT our group's asteroid
            Elements: everything except M
    """
    # Input format: X, Y, Z, VX, VY, VZ, LT, RG, RR
    # Units: AU and days (need to convert to Gaussian Days!)
    # Each value on a separate line
    fin = open(filename)
    x = float(fin.readline())
    y = float(fin.readline())
    z = float(fin.readline())
    vx = float(fin.readline())
    vy = float(fin.readline())
    vz = float(fin.readline())
    lt = float(fin.readline())
    rg = float(fin.readline())
    rr = float(fin.readline())

    # Convert to Gaussian days
    # 1 GD = 1/k_Gauss days
    k_Gauss = 0.0172020989484 # Units: Gaussian days/day
    mu = 1 # mu = G * M_sun = 1 in Gaussian days/AU
    # mu = 6.67430e-11 * 1.989e30 
    # mu = mu * (3600 * 24 * 1/k_Gauss) ** 2 / (149597870691 ** 3)

    vx /= k_Gauss
    vy /= k_Gauss
    vz /= k_Gauss

    r_vec = np.array([x, y, z]) # AU
    r_dot_vec = np.array([vx, vy, vz]) # AU/GD
    r = odlib.mag(r_vec)
    v = odlib.mag(r_dot_vec)



    ######################################################
    #
    #              Calculate orbital elements
    #
    ######################################################

    # Semimajor axis
    a = 1 / (2 / r - np.dot(r_dot_vec, r_dot_vec) / mu)



    # Eccentricity
    e = np.sqrt(1 - odlib.mag(np.cross(r_vec, r_dot_vec))**2 / (mu * a))



    # Inclination
    h = np.cross(r_vec, r_dot_vec) # Angular momentum
    i = degrees(acos(h[2] / odlib.mag(h)))



    # Longitude of ascending node
    sin_omega = h[0] / (odlib.mag(h) * sin(radians(i)))
    cos_omega = -h[1] / (odlib.mag(h) * sin(radians(i)))
    omega = odlib.quadrant_deg(sin_omega, cos_omega)



    # Argument of periapsis
    sin_nu = a / odlib.mag(h) * (1 - e**2) / e * np.dot(r_vec, r_dot_vec) / r
    cos_nu = 1 / e * (a * (1 - e**2) / r - 1)

    sin_u = r_vec[2] / (r * sin(radians(i)))
    cos_u = (r_vec[0] * cos(radians(omega)) + r_vec[1] * sin(radians(omega))) / r

    nu = odlib.quadrant_deg(sin_nu, cos_nu)
    u = odlib.quadrant_deg(sin_u, cos_u)
    w = (u - nu) % 360.0

    # if debug == True:
    #     print("u", u)
    #     print("nu", nu)
    #     print("h vector", h)

    #     print("sin_nu", sin_nu)
    #     print("cos_nu", cos_nu)

    #     print("sin_u", sin_u)
    #     print("cos_u", cos_u)


    # Mean anomaly
    # Not needed for this assignment




    # Correct values from JPL horizons:
    A_true = 1.056800055578855E+00
    EC_true = 3.442331103932664E-01
    IN_true = 2.515525144198502E+01
    OM_true = 2.362379803959657E+02
    W_true = 2.555046145241498E+02

    print()
    print("-----ANGULAR ELEMENTS-----")
    def check_error(my_val, true_val, element_name):
        percent_error = (my_val - true_val) / true_val * 100

        if abs(percent_error) < 0.02: # Threshold set by instructor
            status = "Passed"
        else:
            status = "Failed"

        print("{} {} | Calculated = {} | Actual = {} | Percent error = {} %".format(status, element_name, my_val, true_val, percent_error))

    check_error(a, A_true, "a")
    check_error(e, EC_true, "e")
    check_error(i, IN_true, "i")
    check_error(omega, OM_true, "omega")
    check_error(w, W_true, "w")

baby_od_const_elements("inputs/LiInput.txt")
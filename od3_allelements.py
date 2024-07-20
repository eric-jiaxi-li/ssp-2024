"""
Calculate variable orbital elements

Eric Li
"""

import numpy as np
import odlib
from math import *

debug = True


# Calculate Julian date from UTC year, month, day
# Using https://awb.fyi/ssp/exercises-1.html
Y, M, D = 2018, 7, 14
# J = 367*Y - 7 * (Y + (M+9)//12)//4 + (275*M)//9 + D + 1721013.5
J = odlib.julian(Y, M, D)
print()
print(odlib.get_orbital_elements(3.970631912189709E-01, -1.225073703123122E+00, 4.747425159692229E-01,
                                 1.139883471649287E-02, 2.679831533677191E-03, 3.750852804158524E-03))

    # A_true = 1.056800055578855E+00
    # EC_true = 3.442331103932664E-01
    # IN_true = 2.515525144198502E+01
    # OM_true = 2.362379803959657E+02
    # W_true = 2.555046145241498E+02
    # MA_true = 1.404194574969259E+02
    # Tp_true = 2458158.720849720296













# def baby_od_all_elements(filename, curr_date_julian):
    # """
    # Params: Text file containing the input format specified below
    #         Time of the observations in Julian Days
    # Return: PRINT variable orbital elements and error from true values
    #         Only works for the specified asteroid in LiInput.txt,
    #         NOT our group's asteroid
    #         Elements:   Everything in baby_od, plus:
    #                     Mean anomaly, time of last perehelion passage,
    #                     Julian date
    #                     last perehelion passage = periapsis
    # """
    
    # # Input format: X, Y, Z, VX, VY, VZ, LT, RG, RR
    # # Units: AU and days (need to convert to Gaussian Days!)
    # # Each value on a separate line
    # fin = open(filename)
    # x = float(fin.readline())
    # y = float(fin.readline())
    # z = float(fin.readline())
    # vx = float(fin.readline())
    # vy = float(fin.readline())
    # vz = float(fin.readline())
    # lt = float(fin.readline())
    # rg = float(fin.readline())
    # rr = float(fin.readline())

    # # Convert to Gaussian days
    # # 1 GD = 1/k_Gauss days
    # k_Gauss = 0.0172020989484 # Units: Gaussian days/day
    # mu = 1 # mu = G * M_sun = 1 in Gaussian days/AU
    # # mu = 6.67430e-11 * 1.989e30 
    # # mu = mu * (3600 * 24 * 1/k_Gauss) ** 2 / (149597870691 ** 3)

    # vx /= k_Gauss
    # vy /= k_Gauss
    # vz /= k_Gauss

    # r_vec = np.array([x, y, z]) # AU
    # r_dot_vec = np.array([vx, vy, vz]) # AU/GD
    # r = odlib.mag(r_vec)
    # # v = odlib.mag(r_dot_vec)






    # ######################################################
    # #
    # #              Calculate orbital elements
    # #
    # ######################################################

    # # Semimajor axis
    # a = 1 / (2 / r - np.dot(r_dot_vec, r_dot_vec) / mu)



    # # Eccentricity
    # e = np.sqrt(1 - odlib.mag(np.cross(r_vec, r_dot_vec))**2 / (mu * a))



    # # Inclination
    # h = np.cross(r_vec, r_dot_vec) # Angular momentum
    # i = degrees(acos(h[2] / odlib.mag(h)))



    # # Longitude of ascending node
    # sin_omega = h[0] / (odlib.mag(h) * sin(radians(i)))
    # cos_omega = -h[1] / (odlib.mag(h) * sin(radians(i)))
    # omega = odlib.quadrant_deg(sin_omega, cos_omega)



    # # Argument of periapsis
    # sin_nu = a / odlib.mag(h) * (1 - e**2) / e * np.dot(r_vec, r_dot_vec) / r
    # cos_nu = 1 / e * (a * (1 - e**2) / r - 1)

    # sin_u = r_vec[2] / (r * sin(radians(i)))
    # cos_u = (r_vec[0] * cos(radians(omega)) + r_vec[1] * sin(radians(omega))) / r

    # nu = odlib.quadrant_deg(sin_nu, cos_nu)
    # u = odlib.quadrant_deg(sin_u, cos_u)
    # w = (u - nu) % 360.0



    # # Mean anomaly
    # E = -1
    # if 0 <= nu and nu < 180:
    #     E = acos(1 / e * (1 - r / a))
    # elif 180 <= nu and nu < 360:
    #     E = 2 * pi - acos(1 / e * (1 - r / a))
    # M = degrees(E - e * sin(E)) % 360
    # M_rad = radians(M)

    
    
    # # Time of last perehelion passage
    # # M = M_0 + 2pi(t - t0)/P; at perehelion, M_0 = 0
    # # Calculate period in Gaussian days, then convert
    # # back to regular days to compare with Julian date
    # P = sqrt(4 * pi ** 2 * a ** 3) # Period in Gaussian days
    # P *= k_Gauss
    # t_0 = curr_date_julian - (M_rad * P) / (2 * pi)





    # ######################################################
    # #
    # #                      Check results
    # #
    # ######################################################
    # # Correct values from JPL horizons:
    # """
    # 2458313.500000000 = A.D. 2018-Jul-14 00:00:00.0000 TDB 
    # EC= 3.442331103932664E-01 QR= 6.930144853831691E-01 IN= 2.515525144198502E+01
    # OM= 2.362379803959657E+02 W = 2.555046145241498E+02 Tp=  2458158.720849720296
    # N = 9.072246309860561E-01 MA= 1.404194574969259E+02 TA= 1.589559248433168E+02
    # A = 1.056800055578855E+00 AD= 1.420585625774540E+00 PR= 3.968146230870281E+02
    # """
    # A_true = 1.056800055578855E+00
    # EC_true = 3.442331103932664E-01
    # IN_true = 2.515525144198502E+01
    # OM_true = 2.362379803959657E+02
    # W_true = 2.555046145241498E+02
    # MA_true = 1.404194574969259E+02
    # Tp_true = 2458158.720849720296

    # print("-----ANGULAR ELEMENTS-----")
    # # def check_error(my_val, true_val, element_name):
    # #     percent_error = (my_val - true_val) / true_val * 100

    # #     if abs(percent_error) < 0.02: # Threshold set by instructor
    # #         status = "Passed"
    # #     else:
    # #         status = "Failed"

    # #     print("{} {} | Calculated = {} | Actual = {} | Percent error = {} %".format(status, element_name, round(my_val, 5), round(true_val, 5), percent_error))

    # print("JULIAN DATE: {}".format(curr_date_julian))
    # odlib.check_error(a, A_true, "a")
    # odlib.check_error(e, EC_true, "e")
    # odlib.check_error(i, IN_true, "i")
    # odlib.check_error(omega, OM_true, "omega")
    # odlib.check_error(w, W_true, "w")
    # odlib.check_error(M, MA_true, "M")
    # odlib.check_error(t_0, Tp_true, "last periapsis")

"""
Ephemeris generation

Eric Li
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from math import *
import odlib

debug = False

"""
Correct input values:
3.442331103932664E-01
6.930144853831691E-01 
2.515525144198502E+01
2.362379803959657E+02 
2.555046145241498E+02 
2458158.720849720296
9.072246309860561E-01 
1.404194574969259E+02 
1.589559248433168E+02
1.056800055578855E+00 
1.420585625774540E+00 
3.968146230870281E+02
---
EC= 3.442331103932664E-01 QR= 6.930144853831691E-01 IN= 2.515525144198502E+01
OM= 2.362379803959657E+02 W = 2.555046145241498E+02 Tp=  2458158.720849720296
N = 9.072246309860561E-01 MA= 1.404194574969259E+02 TA= 1.589559248433168E+02
A = 1.056800055578855E+00 AD= 1.420585625774540E+00 PR= 3.968146230870281E+02
"""


# Earth to sun vector from JPL Horizons on Aug 3 2018
sun_vec = np.array([-6.573682734490408E-01, 
                    7.092594484733306E-01, 
                    3.074361163608106E-01])

use_jul_elements = True

if use_jul_elements == True:

    RA, DEC = odlib.gen_eph("inputs/LiInputElements20180714.txt", sun_vec, 23.4384987711, 2018, 8, 3, 2018, 7, 14) # Sun tilt from Dr. F

    # Astrometric, not apparent
    #  2018-Aug-03 00:00 *   17 42 21.20 +31 52 28.1  168.7875
    print()
    print("-----GENERATED EPHEMERIS USING 20180714 ELEMENTS-----")
    print(odlib.RA_decimal_to_HMS(RA), odlib.DEC_decimal_to_DMS(DEC))
    print("Actual: 17 42 21.20 and +31 52 28.1  168.7875")
    print()



















# if use_aug_elements == True:
#     # Try to use orbital elements from 20180803 since the elements change over time
#     RA, DEC = gen_eph("inputs/LiInputElements20180803.txt", sun_vec, 23.4384987711, 2018, 8, 3, 2018, 8, 3) # Sun tilt from Dr. F

#     # Astrometric, not apparent
#     #  2018-Aug-03 00:00 *   17 42 21.20 +31 52 28.1  168.7875
#     print()
#     print("-----GENERATED EPHEMERIS USING 20180803 ELEMENTS-----")
#     print(odlib.RA_decimal_to_HMS(RA), odlib.DEC_decimal_to_DMS(DEC))
#     print()



# def gen_eph(fits_file, sun_vec, earth_tilt_deg, eph_Y, eph_M, eph_D, obs_Y, obs_M, obs_D):
#     """
#     Params: Text file containing the orbital elements (Note:
#             may vary from time to time)
#             Earth-to-sun vector as a np array in equatorial coords
#             Tilt of earth in degrees
#             Date of desired ephemeris: Y, M, D at 0 UTC
#             Observation time in same format
#             All units AU, days
#     Return: RA/DEC of asteroid at the specified time
#     """

#     # if debug == True:
#     #     print()
#     #     print()
#     #     print()
#     #     print("-----DEBUGGING OUTPUT-----")

#     eph_time_julian = odlib.julian(eph_Y, eph_M, eph_D)
#     obs_time_julian = odlib.julian(obs_Y, obs_M, obs_D)
#     interval_Gaussian = odlib.days_to_GD(eph_time_julian - obs_time_julian)

#     # if debug == True:
#     #     print("Julian dates of ephemeris and observation")
#     #     print(eph_time_julian)
#     #     print(obs_time_julian)
#     #     print("Date difference in Gaussian days", interval_Gaussian)
    
#     # Each value on a separate line
#     """
#     EC= 3.442331103932664E-01 QR= 6.930144853831691E-01 IN= 2.515525144198502E+01
#     OM= 2.362379803959657E+02 W = 2.555046145241498E+02 Tp=  2458158.720849720296
#     N = 9.072246309860561E-01 MA= 1.404194574969259E+02 TA= 1.589559248433168E+02
#     A = 1.056800055578855E+00 AD= 1.420585625774540E+00 PR= 3.968146230870281E+02
#     """
#     fin = open(fits_file)
#     EC = float(fin.readline()) # Eccentricity
#     QR = float(fin.readline())
#     IN = float(fin.readline()) # Inclination (deg)
#     OM = float(fin.readline()) # Long of asc node (deg)
#     W = float(fin.readline()) # Arg of perifocus (deg)
#     Tp = float(fin.readline())
#     N = float(fin.readline())
#     MA = float(fin.readline()) # Mean anomaly (deg)
#     TA = float(fin.readline())
#     A = float(fin.readline()) # Semimajor axis (AU)
#     AD = float(fin.readline())
#     PR = float(fin.readline())
    
# 	# Rename variables, convert all to rad
#     a = A
#     e = EC
#     i = radians(IN)
#     omega = radians(OM)
#     w = radians(W)
#     M = radians(MA)
#     # M_obs = M # Mean anomaly at observing time

#     # Update mean anomaly
#     period_Gaussian = sqrt(4 * (pi ** 2) * (a ** 3))
#     M += 2 * pi * interval_Gaussian / period_Gaussian 
#     M = (M % (2 * pi)) # Correct value from Vince that gives the right numbers: 2.767463004482487

#     if debug == True:
#         print("Interval in GD", interval_Gaussian)
#         print("Period in GD", period_Gaussian)
#         print(radians(MA))

#     E = odlib.solve_kepler(M, e, threshold = 1e-9) # Eccentric anomaly, rad

#     # if debug == True:
#     #     print("Period in Gaussian days", period_Gaussian)
#     #     print()
#     #     print("Orbital elements", a, e, degrees(i), degrees(omega), degrees(w), degrees(M), M)

    
#     r = np.array([a * cos(E) - a * e, a * sqrt(1 - e ** 2) * sin(E), 0])
    
#     omega_spin = np.array([[cos(omega), -sin(omega), 0], 
#                            [sin(omega), cos(omega), 0], 
#                            [0, 0, 1]])
#     i_spin = np.array([[1, 0, 0], 
#                        [0, cos(i), -sin(i)], 
#                        [0, sin(i), cos(i)]])
#     w_spin = np.array([[cos(w), -sin(w), 0], 
#                        [sin(w), cos(w), 0], 
#                        [0, 0, 1]])
#     r_ec = omega_spin @ i_spin @ w_spin @ r

#     # if debug == True:
#     #     print()
#     #     print("Sun to ast vector ecliptic", r_ec)
#     #     print("JPL: [ 0.6145690626622695 -1.144703348784966 0.5386837813294618]" )

#     # Correct for tilt of earth
#     tilt = radians(earth_tilt_deg) # Angle of earth's axis
#     tilt_spin = np.array([[1, 0, 0], 
#                           [0, cos(tilt), -sin(tilt)], 
#                           [0, sin(tilt), cos(tilt)]])
#     r_eq = tilt_spin @ r_ec # r in equatorial coordinates

#     # if debug == True:
#     #     print()
#     #     print("Sun to asteroid vector", r_eq)
#     #     r_eq_JPL = np.array([6.145690626622695E-01, 
#     #                      -1.264520891384611E+00, 
#     #                      3.889586403195763E-02])
#     #     print("JPL sun->ast vector (equatorial)", r_eq_JPL)

#     # Range vector
#     rho = r_eq + sun_vec
#     rho_hat = rho / odlib.mag(rho)

#     # RA and DEC
#     DEC = degrees(asin(rho_hat[2]))
#     sin_RA = (rho_hat[1] / cos(radians(DEC)))
#     cos_RA = (rho_hat[0] / cos(radians(DEC)))
#     RA = odlib.quadrant_deg(sin_RA, cos_RA)
    
#     return RA, DEC
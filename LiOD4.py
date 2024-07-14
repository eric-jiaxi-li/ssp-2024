"""
Ephemeris generation

Eric Li
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from math import *
import odlib

debug = True

def gen_eph(fits_file, sun_vec, earth_tilt_deg, time_Y, time_M, time_D, obs_Y = 2018, obs_M = 7, obs_D = 14):
    """
    Params: Text file containing the orbital elements at specified time
            Earth-sun vector as a np array in equatorial coords
            Tilt of earth in degrees
            Date of desired ephemeris: Y, M, D at 0 UTC
            Observation time in same format
            All units AU, days
    Return: RA/DEC of asteroid at the specified time
    """

    eph_time_julian = odlib.julian(time_Y, time_M, time_D)
    obs_time_julian = odlib.julian(obs_Y, obs_M, obs_D)
    interval_Gaussian = odlib.days_to_GD(eph_time_julian - obs_time_julian)
    
    # Units: AU and days (need to convert to Gaussian Days!)
    # Each value on a separate line
    fin = open(fits_file)
    EC = float(fin.readline()) # Eccentricity
    QR = float(fin.readline())
    IN = float(fin.readline()) # Inclination (deg)
    OM = float(fin.readline()) # Long of asc node (deg)
    W = float(fin.readline()) # Arg of perifocus (deg)
    Tp = float(fin.readline())
    N = float(fin.readline())
    MA = float(fin.readline()) # Mean anomaly (deg)
    TA = float(fin.readline())
    A = float(fin.readline()) # Semimajor axis
    AD = float(fin.readline())
    PR = float(fin.readline())
    
	# Rename variables
    a = A
    e = EC
    i = IN
    omega = OM
    w = W
    M = MA

    # Update mean anomaly
    period_Gaussian = sqrt(4 * pi ** 2 * a ** 3)
    M += 360 * interval_Gaussian / period_Gaussian
    
    E = odlib.solve_kepler(radians(M), e) # Eccentric anomaly, rad
    
    r = np.array([a * cos(E) - a * e, a * sqrt(1 - e ** 2) * sin(E), 0])
    
    omega_spin = np.array([[cos(omega), -sin(omega), 0], 
                        [sin(omega), cos(omega), 0], 
                        [0, 0, 1]])
    i_spin = np.array([[1, 0, 0], 
                [0, cos(i), -sin(i)], 
                [0, sin(i), cos(i)]])
    w_spin = np.array([[cos(w), -sin(w), 0], 
                [sin(w), cos(w), 0], 
                [0, 0, 1]])
    r = omega_spin @ i_spin @ w_spin @ r

    # Correct for tilt of earth
    tilt = radians(earth_tilt_deg) # Angle of earth's axis
    tilt_spin = np.array([[1, 0, 0], 
                          [0, cos(tilt), -sin(tilt)], 
                          [0, sin(tilt), cos(tilt)]])
    r_eq = tilt_spin @ r # r in equatorial coordinates

    # Range vector
    rho = r_eq + sun_vec
    rho_hat = rho / odlib.mag(rho)

    # RA and DEC
    DEC = degrees(asin(rho_hat[2]))
    cos_RA = (rho_hat[0] / cos(radians(DEC)))
    sin_RA = (rho_hat[1] / cos(radians(DEC)))
    RA = odlib.quadrant_deg(sin_RA, cos_RA)
    
    return RA, DEC


sun_vec = np.array([-6.573682734490408E-01, 
                    7.092594484733306E-01, 
                    3.074361163608106E-01])
RA, DEC = gen_eph("inputs/LiInputElements.txt", sun_vec, 23.5)

print(odlib.RA_decimal_to_HMS(RA), odlib.DEC_decimal_to_DMS(DEC))
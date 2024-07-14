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

def gen_eph(fits_file, sun_vec, earth_tilt_deg):
    """
    Params: Text file containing the orbital elements at Jul 14, 2018 (0 UTC)
            Earth-sun vector as a np array in equatorial coords
            # Date of desired ephemeris: Y, M, D, time in decimal hrs UTC
            Tilt of earth in degrees
            All units AU, days
    Return: RA/DEC of asteroid at the specified time
    """
    
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
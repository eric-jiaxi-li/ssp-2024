"""
Method of Gauss OD code
"""

import numpy as np
import odlib
from math import *

debug == True

def mog(input_file):

    # Constants
    k_Gauss = 0.0172020989484
    c_AU = 173.144643267 # Speed of light in au/(mean solar)day
    eps = radians(23.4384668053) # Earth's obliquity

    ######################################################
    #
    #                    Read input
    #
    ######################################################

    fin = open(input_file)
    for line in fin.readlines():
        
        Y, M, D, hour, RA, DEC, sun_vec_0, sun_vec_1, sun_vec_2 = line.split()

        Y = int(Y) # Year of observation
        M = int(M) # Month of observation
        D = int(D) # Day of observation
        hour = odlib.time_string_to_decimals(hour) # Time in UTC of observation (decimal hours)
        T = odlib.julian(Y, M, D, hour) # Julian day of observation

        RA_components = map(float, RA.split(":"))
        RA = odlib.HMS_to_rad(RA_components[0], RA_components[1], RA_components[2]) # RA in rad
        DEC_components = map(float, DEC.split(":"))
        DEC = odlib.DMS_to_rad(DEC_components[0], DEC_components[1], DEC_components[2]) # DEC in rad
        sun_vec = np.array([sun_vec_0, sun_vec_1, sun_vec_2])

        if debug == True:
            print()

    return None


mog("inputs/LiInput_MOG.txt")
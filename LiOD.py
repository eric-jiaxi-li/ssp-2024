"""
Method of Gauss OD code
"""

import numpy as np
from math import *
import odlib

debug = True

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

    curr_line_number = 1
    fin = open(input_file)
    for line in fin.readlines():
        T, RA, DEC, sun_vec_0, sun_vec_1, sun_vec_2 = line.split()

        # Time of observation, JD
        T = float(T)

        # RA and DEC
        RA_components_0, RA_components_1, RA_components_2 = map(float, RA.split(":"))
        RA = odlib.HMS_to_rad(RA_components_0, RA_components_1, RA_components_2) # RA in rad
        DEC_components_0, DEC_components_1, DEC_components_2 = map(float, DEC.split(":"))
        DEC = odlib.DMS_to_rad(DEC_components_0, DEC_components_1, DEC_components_2) # DEC in rad
        
        # Earth-sun vector
        sun_vec = np.array([sun_vec_0, sun_vec_1, sun_vec_2]).astype(np.float64)

        # if debug == True:
        #     print("RA/DEC", RA, DEC)

        # Assign inputs to the right variables
        if curr_line_number == 1:
            rho_hat1 = np.array([cos(RA) * cos(DEC), sin(RA) * cos(DEC), sin(DEC)])
            R1 = sun_vec
            t1 = T
        if curr_line_number == 2:
            rho_hat2 = np.array([cos(RA) * cos(DEC), sin(RA) * cos(DEC), sin(DEC)])
            R2 = sun_vec
            t2 = T
        if curr_line_number == 3:
            rho_hat3 = np.array([cos(RA) * cos(DEC), sin(RA) * cos(DEC), sin(DEC)])
            R3 = sun_vec
            t3 = T

        curr_line_number += 1

    # Don't change these, these are the original observation times
    t01 = t1
    t02 = t2
    t03 = t3

    # if debug == True:
    #     print(rho_hat2)
    #     print(t1, R1)
    #     print(t2, R2)
    #     print(t3, R3)





    ######################################################
    #
    #                     First iteration
    #
    ######################################################
    

    D0 = np.dot(rho_hat1, np.cross(rho_hat2, rho_hat3))
    D11 = np.dot(np.cross(R1, rho_hat2), rho_hat3)
    D12 = np.dot(np.cross(R2, rho_hat2), rho_hat3)
    D13 = np.dot(np.cross(R3, rho_hat2), rho_hat3)
    D21 = np.dot(np.cross(rho_hat1, R1), rho_hat3)
    D22 = np.dot(np.cross(rho_hat1, R2), rho_hat3)
    D23 = np.dot(np.cross(rho_hat1, R3), rho_hat3)
    D31 = np.dot(rho_hat1, np.cross(rho_hat2, R1))
    D32 = np.dot(rho_hat1, np.cross(rho_hat2, R2))
    D33 = np.dot(rho_hat1, np.cross(rho_hat2, R3))

    tau1 = k_Gauss * (t1 - t2)
    tau3 = k_Gauss * (t3 - t2)
    tau0 = k_Gauss * (t3 - t1)

    c1 = tau3 / tau0
    c2 = -1
    c3 = -tau1 / tau0

    rho1 = (c1 * D11 + c2 * D12 + c3 * D13) / (c1 * D0)
    rho2 = (c1 * D21 + c2 * D22 + c3 * D23) / (c2 * D0)
    rho3 = (c1 * D31 + c2 * D32 + c3 * D33) / (c3 * D0)

    r1 = rho1 * rho_hat1 - R1
    r2 = rho2 * rho_hat2 - R2
    r3 = rho3 * rho_hat3 - R3

    r_dot12 = (r2 - r1) / (-tau1)
    r_dot23 = (r3 - r2) / (tau3)
    r_dot2 = tau3 / tau0 * r_dot12 - tau1 / tau0 * r_dot23

    last_iteration_r2 = np.copy(r2)
    last_iteration_r_dot2 = np.copy(r_dot2)

    # Lightspeed correction
    t1 = t01 - rho1 / c_AU
    t2 = t02 - rho2 / c_AU
    t3 = t03 - rho3 / c_AU


    while True:
        tau1 = k_Gauss * (t1 - t2)
        tau3 = k_Gauss * (t3 - t2)
        tau0 = k_Gauss * (t3 - t1)

        f1, f3, g1, g3 = odlib.get_fg(tau1, tau3, r2, r_dot2)
        c1 = g3 / (f1 * g3 - g1 * f3)
        c3 = -g1 / (f1 * g3 - g1 * f3)
        d1 = -f3 / (f1 * g3 - g1 * f3)
        d3 = f1 / (f1 * g3 - g1 * f3)

        rho1 = (c1 * D11 + c2 * D12 + c3 * D13) / (c1 * D0)
        rho2 = (c1 * D21 + c2 * D22 + c3 * D23) / (c2 * D0)
        rho3 = (c1 * D31 + c2 * D32 + c3 * D33) / (c3 * D0)

        r1 = rho1 * rho_hat1 - R1
        r2 = rho2 * rho_hat2 - R2
        r3 = rho3 * rho_hat3 - R3

        r_dot2 = d1 * r1 + d3 * r3

        # Lightspeed correction
        t1 = t01 - rho1 / c_AU
        t2 = t02 - rho2 / c_AU
        t3 = t03 - rho3 / c_AU

        # if debug == True:
        #     print(r2, r_dot2)

        if odlib.mag(r2 - last_iteration_r2) + odlib.mag(r_dot2 - last_iteration_r_dot2) < 1e-8:
            # Convert to ecliptic coordinates
            tilt_spin = np.linalg.inv(np.array([[1, 0, 0], 
                                                [0, cos(eps), -sin(eps)], 
                                                [0, sin(eps), cos(eps)]]))
            return tilt_spin @ r2, tilt_spin @ (r_dot2 * k_Gauss) # get_orbital_elements requires days, not Gaussian days
        else:
            last_iteration_r2 = np.copy(r2)
            last_iteration_r_dot2 = np.copy(r_dot2)

r2, r_dot2 = mog("inputs/LiInput_MOG.txt")
print("MOG output, ecliptic:", r2, r_dot2)
print()
print(odlib.get_orbital_elements(r2[0], r2[1], r2[2], r_dot2[0], r_dot2[1], r_dot2[2]))
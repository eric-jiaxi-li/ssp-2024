"""
Write a code that calls a function to determine f and g values. The functions should be able 
to return the f and g function values or f and g series values to 3rd or 4th order. This function 
will sit inside your larger OD code inside the MoG iteration.
a. required input:
- gaussian time interval from the current iteration
- r2 and r2dot vectors from the current iteration
- Flag specifying functions or 3rd, 4th order series
b. required output:
- the corresponding f and g values
"""

import numpy as np
from math import *
import odlib

debug = True

def get_fg(tau1, tau3, r2, r2_dot, flag, tolerance = 1e-12):
    """
    Params: Mostly self-explanatory. Flag: 3rd or 4th order, or
            function (OD Packet Appendix C) "3", "4", "f"
            Tolerance only needed for "f"
    Return: values of f1, f3, g1, g3
    """

    r2_mag = odlib.mag(r2)
    u = 1 / (r2_mag ** 3)
    z = np.dot(r2, r2_dot) / (r2_mag ** 2)
    q = np.dot(r2_dot, r2_dot) / (r2_mag ** 2) - u



    if flag == "3":
        f1 = 1 - 1/2*u*tau1**2 + 1/2*u*z*tau1**3
        f3 = 1 - 1/2*u*tau3**2 + 1/2*u*z*tau3**3
        g1 = tau1 - 1/6*u*tau1**3
        g3 = tau3 - 1/6*u*tau3**3

    elif flag == "4":
        f1 = 1 - 1/2*u*tau1**2 + 1/2*u*z*tau1**3 + 1/24*(3*u*q-15*u*z**2+u**2)*tau1**4
        f3 = 1 - 1/2*u*tau3**2 + 1/2*u*z*tau3**3 + 1/24*(3*u*q-15*u*z**2+u**2)*tau3**4
        g1 = tau1 - 1/6*u*tau1**3 + 1/4*u*z*tau1**4
        g3 = tau3 - 1/6*u*tau3**3 + 1/4*u*z*tau3**4

    elif flag == "f":
        # Appendix C of OD guide
        f1 = -1
        f3 = -1
        g1 = -1
        g3 = -1

    else:
        raise Exception("Invalid flag: only \"3\", \"4\", \"f\" allowed")
    


    return f1, f3, g1, g3



######################################################
#
#                   Run testcases
#
######################################################
# Correct so far: 2, 3


# TC 1
tau1 = -0.32618569435308475
tau3 = 0.050840808143482484
r2 = np.array([0.26640998194891174, -1.382856212643199, -0.505199925482389])
r2_dot = np.array([0.8439832722802604, -0.39937767878456487, 0.14200790188593015] )
print("Testcase 1 results:", get_fg(tau1, tau3, r2, r2_dot, "f"))

# TC 2
tau1 = -0.32618617484601165
tau3 = 0.0508408854033231
r2 = np.array([0.26799552002875776, -1.3726277901924608, -0.5026729612047128])
r2_dot = np.array([0.8456809141954584, -0.3838382184712308, 0.14215854191172816])
print("Testcase 2 results:", get_fg(tau1, tau3, r2, r2_dot, "3"))

# TC 3, correct
tau1 = -0.3261857571141891 
tau3 = 0.05084081855693949 
r2 = np.array([0.26662393644794813, -1.381475976476564, -0.5048589337503169])
r2_dot = np.array([0.8442117090940343, -0.39728396707075087, 0.14202728258915864])
print("Testcase 3 results:", get_fg(tau1, tau3, r2, r2_dot, "4"))
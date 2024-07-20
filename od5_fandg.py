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

Checked by Dr. F
"""

import numpy as np
from math import *
import odlib

debug = True


######################################################
#
#                   Run testcases
#
######################################################

# TC 1
# Not necessary, says Dr. F, until you need it

# TC 2
tau1 = -0.32618617484601165
tau3 = 0.0508408854033231
r2 = np.array([0.26799552002875776, -1.3726277901924608, -0.5026729612047128])
r2_dot = np.array([0.8456809141954584, -0.3838382184712308, 0.14215854191172816])
print("Testcase 2 results:", odlib.get_fg(tau1, tau3, r2, r2_dot, 3))

# TC 3, correct
tau1 = -0.3261857571141891 
tau3 = 0.05084081855693949 
r2 = np.array([0.26662393644794813, -1.381475976476564, -0.5048589337503169])
r2_dot = np.array([0.8442117090940343, -0.39728396707075087, 0.14202728258915864])
print("Testcase 3 results:", odlib.get_fg(tau1, tau3, r2, r2_dot, 4))

















# def get_fg(tau1, tau3, r2, r2_dot, flag):
#     """
#     Params: See OD Guide. Flag: 3rd or 4th order
#             approximation, 3 or 4
#             Functions not necessary, says Dr. F
#     Return: values of f1, f3, g1, g3
#     """

#     r2_mag = odlib.mag(r2)
#     u = 1 / (r2_mag ** 3)
#     z = np.dot(r2, r2_dot) / (r2_mag ** 2)
#     q = np.dot(r2_dot, r2_dot) / (r2_mag ** 2) - u



#     if flag == 3:
#         f1 = 1 - 1/2*u*tau1**2 + 1/2*u*z*tau1**3
#         f3 = 1 - 1/2*u*tau3**2 + 1/2*u*z*tau3**3
#         g1 = tau1 - 1/6*u*tau1**3
#         g3 = tau3 - 1/6*u*tau3**3

#     elif flag == 4:
#         f1 = 1 - 1/2*u*tau1**2 + 1/2*u*z*tau1**3 + 1/24*(3*u*q-15*u*z**2+u**2)*tau1**4
#         f3 = 1 - 1/2*u*tau3**2 + 1/2*u*z*tau3**3 + 1/24*(3*u*q-15*u*z**2+u**2)*tau3**4
#         g1 = tau1 - 1/6*u*tau1**3 + 1/4*u*z*tau1**4
#         g3 = tau3 - 1/6*u*tau3**3 + 1/4*u*z*tau3**4

#     else:
#         raise Exception("Invalid flag: only 3 and 4 allowed")
    


#     return f1, f3, g1, g3

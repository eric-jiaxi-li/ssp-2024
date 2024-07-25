"""
Method of Gauss OD code
"""

import numpy as np
from math import *
import odlib

np.random.seed(777)

debug = False

only_run_monte_carlo = False

######################################################
#
#                  MOG on 2012 FN62
#
######################################################
if only_run_monte_carlo == False:
    """
    Observation times:
    2024-06-28 08:15:21 = 2460489.843993 ELP aqwa
    2024-07-10 12:00:16 = 2460502.000185 Q58 
    - (wasn't able to find exact on JPL, used 413)
    2024-07-18 12:24:29 = 2460510.017002 OGG
    """

    r2, r_dot2 = odlib.mog("inputs/2012FN62/2012FN62_MOGinput.txt")
    print("2012FN62 vectors at 2024-07-10 12:00:16:", r2, r_dot2)
    a, e, i, omega, w, m = odlib.get_orbital_elements(r2[0], r2[1], r2[2], r_dot2[0], r_dot2[1], r_dot2[2])

    # 2460502.000185000 = A.D. 2024-Jul-10 12:00:15.9840 TDB 
    #  EC= 6.162095989777298E-01 QR= 1.252863662837021E+00 IN= 1.000625206112275E+01
    #  OM= 1.479906043977145E+02 W = 1.424191318807842E+02 Tp=  2460506.980212359689
    #  N = 1.671050275387466E-01 MA= 3.591678123908871E+02 TA= 3.555537239548167E+02
    #  A = 3.264447624275831E+00 AD= 5.276031585714641E+00 PR= 2.154333746281372E+03

    print()
    print("Orbital elements at this time:")
    print("ALL ELEMENTS CORRECT WITH UNDER 1% ERROR (2012 FN62)")
    odlib.check_error(a, 3.264447624275831E+00, "a", threshold = 1)
    odlib.check_error(e, 6.162095989777298E-01, "e", threshold = 1)
    odlib.check_error(i, 1.000625206112275E+01, "i", threshold = 1)
    odlib.check_error(omega, 1.479906043977145E+02, "omega", threshold = 1)
    odlib.check_error(w, 1.424191318807842E+02, "w", threshold = 1)
    odlib.check_error(m, 3.591678123908871E+02, "m", threshold = 1)








######################################################
#
#                     Monte Carlo
#
######################################################


print()
print()
print("-----RUNNING MONTE CARLO-----")


##########################################
#            Setup for input
##########################################

"""
-----RESULTS FROM ASTROMETRY-----
REMEMBER THAT UNCERTAINTIES IN ARCSECONDS
6/27:
    Uncertainties RA 0.0141631310323522 DEC 0.30669045765817193
    RA 18.0 hours 2.0 minutes 55.378309 seconds  DEC 12 degrees 31 arcminutes 21.90406 arcseconds
7/10:
    Uncertainties RA 0.002782904700978816 DEC 0.0018046091182027507
    RA 18.0 hours 26.0 minutes 18.697729 seconds  DEC 8 degrees 50 arcminutes 58.523058 arcseconds
7/17:
    Uncertainties RA 0.0038768302232221144 DEC 0.00626199644260542
    RA 18.0 hours 45.0 minutes 2.783863 seconds  DEC 4 degrees 50 arcminutes 44.891622 arcseconds
"""

t1 = 2460489.843993
RA1_orig = odlib.HMS_to_rad(18, 2, 55.378309)
sigmaRA1 = radians(0.0141631310323522 / 3600)
DEC1_orig = odlib.DMS_to_rad(12, 31, 21.90406)
sigmaDEC1 = radians(0.30669045765817193 / 3600)
R1 = np.array([-1.202618669769325E-01, 9.262084923058235E-01, 4.014630144278040E-01])

t2 = 2460502.000185
RA2_orig = odlib.HMS_to_rad(18, 26, 18.697729)
sigmaRA2 = radians(0.002782904700978816 / 3600)
DEC2_orig = odlib.DMS_to_rad(8, 50, 58.523058)
sigmaDEC2 = radians(0.0018046091182027507 / 3600)
R2 = np.array([-3.206617972850214E-01, 8.851905880039788E-01, 3.837280260259753E-01])

t3 = 2460510.017002
RA3_orig = odlib.HMS_to_rad(18, 45, 2.783863)
sigmaRA3 = radians(0.0038768302232221144 / 3600)
DEC3_orig = odlib.DMS_to_rad(4, 50, 44.891622)
sigmaDEC3 = radians(0.00626199644260542 / 3600)
R3 = np.array([-4.460342859078354E-01, 8.378241050812248E-01, 3.631607209761045E-01])




##########################################
#            Run Monte Carlo
##########################################

a_all = []
e_all = []
i_all = []
omega_all = []
w_all = []
m_all = []

# # Test mog2
# print("MOG2", odlib.mog2(t1, RA1_orig, DEC1_orig, R1, t2, RA2_orig, DEC2_orig, R2, t3, RA3_orig, DEC3_orig, R3))
# print("MOG", odlib.mog("inputs/2012FN62/2012FN62_MOGinput.txt"))

n_iter = 1000

for iter in range(n_iter):
    # print("Running iteration", iter)

    # Choose random RA and DEC
    RA1 = np.random.normal(RA1_orig, sigmaRA1)
    DEC1 = np.random.normal(DEC1_orig, sigmaDEC1)
    RA2 = np.random.normal(RA2_orig, sigmaRA2)
    DEC2 = np.random.normal(DEC2_orig, sigmaDEC2)
    RA3 = np.random.normal(RA3_orig, sigmaRA3)
    DEC3 = np.random.normal(DEC3_orig, sigmaDEC3)

    r2, r_dot2, = odlib.mog2(t1, RA1, DEC1, R1, t2, RA2, DEC2, R2, t3, RA3, DEC3, R3)

    # print(r2, r_dot2)

    a, e, i, omega, w, m = odlib.get_orbital_elements(r2[0], r2[1], r2[2], r_dot2[0], r_dot2[1], r_dot2[2])

    a_all.append(a)
    e_all.append(e)
    i_all.append(i)
    omega_all.append(omega)
    w_all.append(w)
    m_all.append(m)


a_all = np.array(a_all)
e_all = np.array(e_all)
i_all = np.array(i_all)
omega_all = np.array(omega_all)
w_all = np.array(w_all)
m_all = np.array(m_all)

# Standard deviation of the mean (divide by number of iterations sqrt-ed)
print("Uncertainty for a: ", np.std(a_all) / np.sqrt(n_iter))
print("Uncertainty for e: ", np.std(e_all) / np.sqrt(n_iter))
print("Uncertainty for i: ", np.std(i_all) / np.sqrt(n_iter))
print("Uncertainty for omega: ", np.std(omega_all) / np.sqrt(n_iter))
print("Uncertainty for w: ", np.std(w_all) / np.sqrt(n_iter))
print("Uncertainty for m: ", np.std(m_all) / np.sqrt(n_iter))

# RESULTS:
# Uncertainty for a:  0.0015410949588008727
# Uncertainty for e:  0.00016744733104140217
# Uncertainty for i:  0.0018814274566339472
# Uncertainty for omega:  0.0012969136202898813
# Uncertainty for w:  0.0018636718958085986
# Uncertainty for m:  0.00038438592857694667





















# print()
# print("-----SAMPLE TESTCASE-----")
# r2, r_dot2 = odlib.mog("inputs/testcases/LiInput_MOG.txt")
# print("MOG output, ecliptic:", r2, r_dot2)
# print("Distance in AU: ", odlib.mag(r2))
# print(odlib.get_orbital_elements(r2[0], r2[1], r2[2], r_dot2[0], r_dot2[1], r_dot2[2]))

# """
# CORRECT: 
# Semimajor axis 2.30430 AU
# Eccentricity 0.54791
# Inclination 3.2412 degrees
# Longitude of the Ascending Node: 213.218 degrees
# Argument of the Perihelion: 98.1439 degrees
# Mean Anomaly at t2: 350.07 degrees
# """





# def mog(input_file):

#     # Constants
#     k_Gauss = 0.0172020989484
#     c_AU = 173.144643267 # Speed of light in au/(mean solar)day
#     eps = radians(23.4384668053) # Earth's obliquity

#     ######################################################
#     #
#     #                    Read input
#     #
#     ######################################################

#     curr_line_number = 1
#     fin = open(input_file)
#     for line in fin.readlines():
#         T, RA, DEC, sun_vec_0, sun_vec_1, sun_vec_2 = line.split()

#         # Time of observation, JD
#         T = float(T)

#         # RA and DEC
#         RA_components_0, RA_components_1, RA_components_2 = map(float, RA.split(":"))
#         RA = odlib.HMS_to_rad(RA_components_0, RA_components_1, RA_components_2) # RA in rad
#         DEC_components_0, DEC_components_1, DEC_components_2 = map(float, DEC.split(":"))
#         DEC = odlib.DMS_to_rad(DEC_components_0, DEC_components_1, DEC_components_2) # DEC in rad
        
#         # Earth-sun vector
#         sun_vec = np.array([sun_vec_0, sun_vec_1, sun_vec_2]).astype(np.float64)

#         # if debug == True:
#         #     print("RA/DEC", RA, DEC)

#         # Assign inputs to the right variables
#         if curr_line_number == 1:
#             rho_hat1 = np.array([cos(RA) * cos(DEC), sin(RA) * cos(DEC), sin(DEC)])
#             R1 = sun_vec
#             t1 = T
#         if curr_line_number == 2:
#             rho_hat2 = np.array([cos(RA) * cos(DEC), sin(RA) * cos(DEC), sin(DEC)])
#             R2 = sun_vec
#             t2 = T
#         if curr_line_number == 3:
#             rho_hat3 = np.array([cos(RA) * cos(DEC), sin(RA) * cos(DEC), sin(DEC)])
#             R3 = sun_vec
#             t3 = T


#         curr_line_number += 1

#     # Original observation times in Julian Days, don't change!
#     t01 = t1
#     t02 = t2
#     t03 = t3

#     # if debug == True:
#     #     print(rho_hat2)
#     #     print(t1, R1)
#     #     print(t2, R2)
#     #     print(t3, R3)





#     ######################################################
#     #
#     #                     First iteration
#     #
#     ######################################################
    

#     D0 = np.dot(rho_hat1, np.cross(rho_hat2, rho_hat3))
#     D11 = np.dot(np.cross(R1, rho_hat2), rho_hat3)
#     D12 = np.dot(np.cross(R2, rho_hat2), rho_hat3)
#     D13 = np.dot(np.cross(R3, rho_hat2), rho_hat3)
#     D21 = np.dot(np.cross(rho_hat1, R1), rho_hat3)
#     D22 = np.dot(np.cross(rho_hat1, R2), rho_hat3)
#     D23 = np.dot(np.cross(rho_hat1, R3), rho_hat3)
#     D31 = np.dot(rho_hat1, np.cross(rho_hat2, R1))
#     D32 = np.dot(rho_hat1, np.cross(rho_hat2, R2))
#     D33 = np.dot(rho_hat1, np.cross(rho_hat2, R3))

#     tau1 = k_Gauss * (t1 - t2)
#     tau3 = k_Gauss * (t3 - t2)
#     tau0 = k_Gauss * (t3 - t1)

#     # Initial guesses for c1, c3 using Kepler's Laws
#     c1 = tau3 / tau0
#     c2 = -1
#     c3 = -tau1 / tau0

#     # Scalar ranges of each observation
#     rho1 = (c1 * D11 + c2 * D12 + c3 * D13) / (c1 * D0)
#     rho2 = (c1 * D21 + c2 * D22 + c3 * D23) / (c2 * D0)
#     rho3 = (c1 * D31 + c2 * D32 + c3 * D33) / (c3 * D0)

#     # Position vector (sun to asteroid)
#     r1 = rho1 * rho_hat1 - R1
#     r2 = rho2 * rho_hat2 - R2
#     r3 = rho3 * rho_hat3 - R3

#     # Initial linear interpolation of velocity
#     r_dot12 = (r2 - r1) / (-tau1)
#     r_dot23 = (r3 - r2) / (tau3)
#     r_dot2 = tau3 / tau0 * r_dot12 - tau1 / tau0 * r_dot23

#     # Store vectors from previous iteration to check convergence
#     last_iteration_r2 = np.copy(r2)
#     last_iteration_r_dot2 = np.copy(r_dot2)

#     # Lightspeed correction
#     t1 = t01 - rho1 / c_AU
#     t2 = t02 - rho2 / c_AU
#     t3 = t03 - rho3 / c_AU



#     ######################################################
#     #
#     #                 Subsequent iterations
#     #
#     ######################################################

#     while True:
#         tau1 = k_Gauss * (t1 - t2)
#         tau3 = k_Gauss * (t3 - t2)
#         tau0 = k_Gauss * (t3 - t1)

#         f1, f3, g1, g3 = odlib.get_fg(tau1, tau3, r2, r_dot2)
#         c1 = g3 / (f1 * g3 - g1 * f3)
#         c3 = -g1 / (f1 * g3 - g1 * f3)
#         d1 = -f3 / (f1 * g3 - g1 * f3)
#         d3 = f1 / (f1 * g3 - g1 * f3)

#         # Scalar ranges of each observation
#         rho1 = (c1 * D11 + c2 * D12 + c3 * D13) / (c1 * D0)
#         rho2 = (c1 * D21 + c2 * D22 + c3 * D23) / (c2 * D0)
#         rho3 = (c1 * D31 + c2 * D32 + c3 * D33) / (c3 * D0)

#         # Position vector (sun to asteroid)
#         r1 = rho1 * rho_hat1 - R1
#         r2 = rho2 * rho_hat2 - R2
#         r3 = rho3 * rho_hat3 - R3

#         r_dot2 = d1 * r1 + d3 * r3

#         # Lightspeed correction
#         t1 = t01 - rho1 / c_AU
#         t2 = t02 - rho2 / c_AU
#         t3 = t03 - rho3 / c_AU

#         # if debug == True:
#         #     print(r2, r_dot2)

#         ##################################
#         #     Check for convergence
#         ##################################
#         if odlib.mag(r2 - last_iteration_r2) + odlib.mag(r_dot2 - last_iteration_r_dot2) < 1e-8:
#             # Convert to ecliptic coordinates
#             tilt_spin = np.linalg.inv(np.array([[1, 0, 0], 
#                                                 [0, cos(eps), -sin(eps)], 
#                                                 [0, sin(eps), cos(eps)]]))
#             return tilt_spin @ r2, tilt_spin @ (r_dot2 * k_Gauss) # get_orbital_elements requires days, not Gaussian days
        
#         else:
#             last_iteration_r2 = np.copy(r2)
#             last_iteration_r_dot2 = np.copy(r_dot2)
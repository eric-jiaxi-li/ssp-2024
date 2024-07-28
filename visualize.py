"""
Visualize 2012 FN62 orbit
Eric Li
"""

from vpython import *
from math import *
import numpy as np
import odlib

debug = False


# Julian day of these elements: 2460502.000185
# Generate new planets with Osculating Orbital Elements (center at Sun) at this Julian day
# A, EC, IN, OM, W, MA

fin = open("inputs/2012FN62/visualize.txt")
name_list = fin.readline().split() # Body names
r_list = np.float64(np.array(fin.readline().split())) # Asteroid radius is made-up
a_list = np.float64(np.array(fin.readline().split()))
e_list = np.float64(np.array(fin.readline().split()))
i_list = np.float64(np.array(fin.readline().split()))
omega_list = np.float64(np.array(fin.readline().split()))
w_list = np.float64(np.array(fin.readline().split()))
m_list = np.float64(np.array(fin.readline().split()))
col_list = np.array([color.white, color.gray(0.5), vector(1,0.7,0.2), color.green, color.red, vector(1,0.7,0.2), vector(0.8, 0.6, 0.6), color.cyan, color.blue])

odlib.visualize_multiple_orbits(r_list, a_list, e_list, i_list, omega_list, w_list, m_list, col_list)


# a_list = np.array([3.245761552052847, 3.870970735948419E-01, 7.233275855465966E-01, 1.000525628690563E+00, 1.523659834502866E+00, 5.202599117666169E+00, 9.562130184723967E+00, 1.930353687033573E+01, 3.021761915800814E+01])
# e_list = np.array([0.6141866747698732, 2.056492674549958E-01, 6.731253872798876E-03, 1.621348364416402E-02, 9.329437184231582E-02, 4.827540669964238E-02, 5.492259660375094E-02, 4.504514062884678E-02, 1.335627148974016E-02])
# i_list = np.array([9.98211483642601, 2.855338780923179E+01, 2.443666664720525E+01, 2.343670108483834E+01, 2.467738264916708E+01, 2.323459959325644E+01, 2.255391444000841E+01, 2.366318869414800E+01, 2.229201912670373E+01])
# omega_list = np.array([148.00823478480334, 1.098000323307333E+01, 8.003564838735068E+00, 3.599966754616262E+02, 3.366286755647931E+00, 3.249840197664308E+00, 5.949276474098442E+00, 1.851424116208393E+00, 3.481735881232009E+00])
# w_list = np.array([142.38377885236548, 6.761040833562714E+01, 1.244937007456587E+02, 1.019166684209871E+02, 3.331080758672448E+02, 1.112999441927799E+01, 8.458621110447142E+01, 1.628595797087438E+02, 3.283428388177517E+01])
# m_list = np.array([359.16509165962776, 1.098334645764942E+02, 4.519739861556728E-01, 1.866838072819970E+02, 3.303246732997781E+01, 4.450086296331610E+01, 2.598097561227970E+02, 2.537407994715349E+02, 3.226387684813254E+02])
























# ######################################################
# #
# #           VIsualize just the asteroid with
# #            options for debugging output
# #
# ######################################################
# if debug == True:
#     # Orbital elements from LiOD.py
#     # Julian day of these elements: 2460502.000185
#     a = 3.245761552052847 # Checked
#     e = 0.6141866747698732 # Checked
#     i = radians(9.98211483642601) # Checked
#     omega = radians(148.00823478480334) # Checked
#     w = radians(142.38377885236548) # Checked (145.532--close enough?)
#     m = radians(359.16509165962776) # Checked (0.9--close enough?)

#     E = odlib.solve_kepler(m, e, threshold = 1e-9) # Eccentric anomaly, rad
#     r = np.array([a * cos(E) - a * e, a * sqrt(1 - e ** 2) * sin(E), 0])

#     # Rotation matrices to get asteroid's ecliptic coordinates
#     omega_spin = np.array([[cos(omega), -sin(omega), 0], 
#                             [sin(omega), cos(omega), 0], 
#                             [0, 0, 1]])
#     i_spin = np.array([[1, 0, 0], 
#                         [0, cos(i), -sin(i)], 
#                         [0, sin(i), cos(i)]])
#     w_spin = np.array([[cos(w), -sin(w), 0], 
#                         [sin(w), cos(w), 0], 
#                         [0, 0, 1]])
#     r_ec = omega_spin @ i_spin @ w_spin @ r

#     # Render objects
#     asteroid_pos = vector(r_ec[0], r_ec[1], r_ec[2])
#     asteroid = sphere(pos = asteroid_pos * 150, radius = 15, color = color.white, texture = textures.rock)
#     asteroid.trail = curve(color = color.white)
#     sun = sphere(pos = vector(0,0,0), radius = 50, color = color.yellow, emissive = True)
#     if debug == True:
#         ecliptic = box(pos = vector(0,0,0), size = vector(2e3, 2e3, 1), color = color.blue, opacity = 0.2)


#     ######################################################
#     #
#     #                   Animation loop
#     #
#     ######################################################

#     # These are used for testing elements
#     aphelion = -1
#     perehelion = 1e9
#     i_debug = -1
#     vern_equinox_vec = np.array([1, 0, 0]) # Vernal equinox = x-axis
#     asc_node_vec = np.array([0, 0, 0])
#     perehelion_vec = np.array([0, 0, 0])
#     w_debug = -1
#     time = 0 # For debugging mean anomaly

#     period = 2000
#     while True:
#         rate(200)

#         # Update position of asteroid
#         time += 1
#         m += 2 * pi / period 
#         E = odlib.solve_kepler(m, e, threshold = 1e-9) # Eccentric anomaly, rad
#         r = np.array([a * cos(E) - a * e, a * sqrt(1 - e ** 2) * sin(E), 0])

#         # Rotation matrices to get asteroid's ecliptic coordinates
#         omega_spin = np.array([[cos(omega), -sin(omega), 0], 
#                                 [sin(omega), cos(omega), 0], 
#                                 [0, 0, 1]])
#         i_spin = np.array([[1, 0, 0], 
#                             [0, cos(i), -sin(i)], 
#                             [0, sin(i), cos(i)]])
#         w_spin = np.array([[cos(w), -sin(w), 0], 
#                             [sin(w), cos(w), 0], 
#                             [0, 0, 1]])
#         r_ec = omega_spin @ i_spin @ w_spin @ r

#         asteroid_pos = vector(r_ec[0], r_ec[1], r_ec[2])
#         asteroid.pos = asteroid_pos * 150
#         asteroid.trail.append(pos = asteroid.pos) 



#         ######################################################
#         #                   Debug output
#         ######################################################
#         if debug == True:
#             aphelion = max(aphelion, mag(asteroid_pos))
#             perehelion = min(perehelion, mag(asteroid_pos))

#             i_debug = max(i_debug, abs(degrees(atan(asteroid_pos.z / np.sqrt(asteroid_pos.x ** 2 + asteroid_pos.y ** 2)))))

#             if abs(asteroid_pos.z) < 1e-3:
#                 asc_node_vec = np.array([asteroid_pos.x, asteroid_pos.y, asteroid_pos.z])
#             if abs(mag(asteroid_pos) - perehelion) < 1e-9: # 1e-3 for most cases, 1e-9 for mean anomaly
#                 perehelion_vec = np.array([asteroid_pos.x, asteroid_pos.y, asteroid_pos.z])
#                 perehelion_time = time

#             omega_debug = degrees(acos(np.dot(asc_node_vec, vern_equinox_vec) / (odlib.mag(asc_node_vec) * odlib.mag(vern_equinox_vec))))

#             w_debug = degrees(acos(np.dot(asc_node_vec, perehelion_vec) / (odlib.mag(asc_node_vec) * odlib.mag(perehelion_vec))))



#             """
#             Comment the below lines if they lag too much!
#             """
#             # label(pos = vector(1000, 1000, 0), text = "a = " + str((aphelion + perehelion) / 2))
#             # label(pos = vector(1000, 1000, 300), text = "e = " + str((aphelion - perehelion) / (aphelion + perehelion)))
#             # label(pos = vector(1000, 1000, 600), text = "i = " + str(i_debug))
#             # label(pos = vector(1000, 1000, 900), text = "omega = " + str(omega_debug))
#             # label(pos = vector(1000, 1000, 1200), text = "w = " + str(w_debug))
#             # label(pos = vector(1000, 1000, 1500), text = "Initial m = " + str(perehelion_time / period * 360))


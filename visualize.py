"""
Visualize 2012 FN62 orbit
Eric Li
"""

from vpython import *
from math import *
import numpy as np
import odlib

debug = True

# Orbital elements from LiOD.py
a = 3.245761552052847 # Checked
e = 0.6141866747698732 # Checked
i = radians(9.98211483642601) # Checked
omega = radians(148.00823478480334)
w = radians(142.38377885236548) # Checked (145.532--close enough?)
m = radians(359.16509165962776)

E = odlib.solve_kepler(m, e, threshold = 1e-9) # Eccentric anomaly, rad
r = np.array([a * cos(E) - a * e, a * sqrt(1 - e ** 2) * sin(E), 0])

# Rotation matrices to get asteroid's ecliptic coordinates
omega_spin = np.array([[cos(omega), -sin(omega), 0], 
                        [sin(omega), cos(omega), 0], 
                        [0, 0, 1]])
i_spin = np.array([[1, 0, 0], 
                    [0, cos(i), -sin(i)], 
                    [0, sin(i), cos(i)]])
w_spin = np.array([[cos(w), -sin(w), 0], 
                    [sin(w), cos(w), 0], 
                    [0, 0, 1]])
r_ec = omega_spin @ i_spin @ w_spin @ r

# Render objects
asteroid_pos = vector(r_ec[0], r_ec[1], r_ec[2])
asteroid = sphere(pos = asteroid_pos * 150, radius = 15, color = color.white, texture = textures.rock)
asteroid.trail = curve(color = color.white)
sun = sphere(pos = vector(0,0,0), radius = 50, color = color.yellow, emissive = True)
if debug == True:
    ecliptic = box(pos = vector(0,0,0), size = vector(2e3, 2e3, 1), color = color.blue, opacity = 0.2)


######################################################
#
#                   Animation loop
#
######################################################
if debug == True:
    aphelion = -1
    perehelion = 1e9
    i_debug = -1
    asc_node_vec = np.array([0, 0, 0])
    perehelion_vec = np.array([0, 0, 0])
    w_debug = -1

time = 0
period = 2000
while True:
    rate(200)

    # Update position of asteroid
    m += 2 * pi / period 
    E = odlib.solve_kepler(m, e, threshold = 1e-9) # Eccentric anomaly, rad
    r = np.array([a * cos(E) - a * e, a * sqrt(1 - e ** 2) * sin(E), 0])

    # Rotation matrices to get asteroid's ecliptic coordinates
    omega_spin = np.array([[cos(omega), -sin(omega), 0], 
                            [sin(omega), cos(omega), 0], 
                            [0, 0, 1]])
    i_spin = np.array([[1, 0, 0], 
                        [0, cos(i), -sin(i)], 
                        [0, sin(i), cos(i)]])
    w_spin = np.array([[cos(w), -sin(w), 0], 
                        [sin(w), cos(w), 0], 
                        [0, 0, 1]])
    r_ec = omega_spin @ i_spin @ w_spin @ r

    asteroid_pos = vector(r_ec[0], r_ec[1], r_ec[2])
    asteroid.pos = asteroid_pos * 150
    asteroid.trail.append(pos = asteroid.pos) 



    ######################################################
    #                   Debug output
    ######################################################
    if debug == True:
        aphelion = max(aphelion, mag(asteroid_pos))
        perehelion = min(perehelion, mag(asteroid_pos))
        i_debug = max(i_debug, abs(degrees(atan(asteroid_pos.z / np.sqrt(asteroid_pos.x ** 2 + asteroid_pos.y ** 2)))))
        if abs(asteroid_pos.z) < 1e-3:
            asc_node_vec = np.array([asteroid_pos.x, asteroid_pos.y, asteroid_pos.z])
        if (mag(asteroid_pos) - perehelion) < 1e-3:
            perehelion_vec = np.array([asteroid_pos.x, asteroid_pos.y, asteroid_pos.z])
        w_debug = degrees(acos(np.dot(asc_node_vec, perehelion_vec) / (odlib.mag(asc_node_vec) * odlib.mag(perehelion_vec))))

        label(pos = vector(1000, 1000, 0), text = "a = " + str((aphelion + perehelion) / 2))
        label(pos = vector(1000, 1000, 300), text = "e = " + str((aphelion - perehelion) / (aphelion + perehelion)))
        label(pos = vector(1000, 1000, 600), text = "i = " + str(i_debug))
        label(pos = vector(1000, 1000, 900), text = "w = " + str(w_debug))


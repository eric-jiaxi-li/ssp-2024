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
a = 3.245761552052847
e = 0.6141866747698732
i = radians(9.98211483642601)
omega = radians(148.00823478480334)
w = radians(142.38377885236548)
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



######################################################
#
#                   Animation loop
#
######################################################
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

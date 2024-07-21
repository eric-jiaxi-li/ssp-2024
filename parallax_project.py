"""
CUB-NMSU Parallax Experiment
2012 FN62
Input format: UT (hr), RA (hr), DEC (deg)
"""

import numpy as np
import odlib
from scipy.stats import linregress
from math import *

debug = False


######################################################
#
#                Position data
#
######################################################


# Locations of CUB (X)/NMSU (Y) observatories
# dist to Earth center (km), latitude, beta_y = long relative to X
r_x = 6371 + 1.653 # km + altitude
beta_x = radians(0) 
phi_x = radians(40.00372222222222)
r_y = 6371 + 1.451
beta_y = radians(1.4355) # Maybe sign issue?
phi_y = radians(32.2931)
beta = beta_y

# Position vectors of observatories
X = np.array([r_x * cos(phi_x), 0, r_x * sin(phi_x)])
Y = np.array([r_y * cos(phi_y) * cos(beta), r_y * cos(phi_y) * sin(beta), r_y * sin(phi_y)])
C = X - Y # Distance between two sites






######################################################
#
#     RA/DEC for each site at t_obs using linreg
#
######################################################

t_obs = 4.35 # UT, hours

########################
#        X (CUB)
########################

# Read in data
t_x_all = []
H_x_all = []
delta_x_all = []
fin = open("inputs/parallax_project/parallax_cub.txt")
for line in fin.readlines():
    line = line.strip()
    t, H, delta = map(float, line.split())
    t_x_all.append(t)
    H_x_all.append(H)
    delta_x_all.append(delta)
t_x_all = np.array(t_x_all)
H_x_all = np.array(H_x_all)
delta_x_all = np.array(delta_x_all)

# Linear regression
linreg_results = linregress(t_x_all, H_x_all)
H_x = linreg_results[0] * t_obs + linreg_results[1]
linreg_results = linregress(t_x_all, delta_x_all)
delta_x = linreg_results[0] * t_obs + linreg_results[1]

# if debug == True:
#     print("HA/DEC at X:", H_x, delta_x)


########################
#        Y (NMSU)
########################

# Read in data
t_y_all = []
H_y_all = []
delta_y_all = []
fin = open("inputs/parallax_project/parallax_nmsu.txt")
for line in fin.readlines():
    line = line.strip()
    t, H, delta = map(float, line.split())
    t_y_all.append(t)
    H_y_all.append(H)
    delta_y_all.append(delta)
t_y_all = np.array(t_y_all)
H_y_all = np.array(H_y_all)
delta_y_all = np.array(delta_y_all)

# Linear regression
linreg_results = linregress(t_y_all, H_y_all)
H_y = linreg_results[0] * t_obs + linreg_results[1]
linreg_results = linregress(t_y_all, delta_y_all)
delta_y = linreg_results[0] * t_obs + linreg_results[1]

# if debug == True:
#     print("HA/DEC at Y:", H_y, delta_y)





######################################################
#
#               Find projected baseline
#
######################################################
H_x_rad = radians(H_x * 15)
H_y_rad = radians(H_y * 15)
delta_x_rad = radians(delta_x)
delta_y_rad = radians(delta_y)

# Unit vector from X to asteroid
# Observation date: 7/14/2024 4:35 UT
# LST: Mean 17:04:07.1001, Apparent 17:04:06.9515
LST = 17 + 4/60 + 7.1001/3600
H = LST - H_x # Hour angle in hours
H = radians(H * 15) % (2 * pi)
W = np.array([cos(H) * cos(delta_x_rad), sin(H) * cos(delta_x_rad), sin(delta_x_rad)])

if debug == True:
    print(H)

# Angle between C and W
theta = acos((np.dot(C, W)) / (odlib.mag(C)))

# Projected baseline, magnitude
B_mag = odlib.mag(C) * sin(theta)

# Parallax angle, rad
y = sqrt(((H_x_rad - H_y_rad) * cos(delta_x_rad)) ** 2 + (delta_x_rad - delta_y_rad) ** 2)

# Distance to asteroid in AU
d = (odlib.mag(C) * sin(theta)) / (2 * tan(y / 2)) * 6.6845871226706E-9
d_JPL = 0.26998734316940

odlib.check_error(d, d_JPL, "Distance to asteroid in AU") # 9.74% error



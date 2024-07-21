"""
OD_code1_angular_momentum.pdf

Calculate angular momentum of the asteroid, divided
by its mass

Eric Li
7/4/2024

RUNS FINE
"""
import numpy as np

debug = False

# Input format: X, Y, Z, VX, VY, VZ, LT, RG, RR
# Units: AU and days (need to convert to Gaussian Days!)
# Each value on a separate line
fin = open("inputs/testcases/LiInput.txt")
x = float(fin.readline())
y = float(fin.readline())
z = float(fin.readline())
vx = float(fin.readline())
vy = float(fin.readline())
vz = float(fin.readline())
lt = float(fin.readline())
rg = float(fin.readline())
rr = float(fin.readline())

if debug == True:
    # Print the data we read in
    print(x, y, z)
    print(vx, vy, vz)
    print(lt, rg, rr)


# Convert to Gaussian days
# t_Gauss = k_Gauss * t_normaldays
k_Gauss = 0.0172020989484 # Units: Gaussian days/day
vx /= k_Gauss
vy /= k_Gauss
vz /= k_Gauss

# Calculate and print angular momentum L (6 decimal places)
v_vec = np.array([vx, vy, vz])
r_vec = np.array([x, y, z])
L_vec = np.cross(r_vec, v_vec) # L = r x p
print(np.round(L_vec, 6)) # Angular momentum (divided by mass)

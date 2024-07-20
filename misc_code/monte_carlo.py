# Checked by Dr. F

from vpython import *
import numpy as np
import random
import matplotlib.cm as cm
import time

np.random.seed(777)

debug = False

run_brownian = False
run_hypersphere = False
run_dla = False

"""
1. Brownian Motion
- L odd and is the side length of the boundaries
"""
def brownian(L, nsteps = 1_000_000):
    # Set up canvas
    canvas(center = vector(L // 2, L // 2, 0), xmin = 0, xmax = L, ymin = 0, ymax = L)
    x = sphere(pos = vector(L // 2, L // 2, 0))

    # Every second, choose one of these directions
    dir = [vector(1, 0, 0), vector(-1, 0, 0), 
           vector(0, 1, 0), vector(0, -1, 0)]

    for i in range(nsteps):
        label(pos = vector(L, L, 0), text = "Percent completed: " + str(round(i / nsteps * 100, 3)) + "%")
        label(pos = vector(L, L - 10, 0), text = "Press SHIFT to exit")
        rate(100)
        chosen_dir = random.choice(dir)

        # Ensure that particle doesn't leave boundaries
        # If it would leave boundaries, re-choose the direction
        while True:
            if (0 < x.pos.x + chosen_dir.x and x.pos.x + chosen_dir.x < L and 
                0 < x.pos.y + chosen_dir.y and x.pos.y + chosen_dir.y < L):
                x.pos += chosen_dir
                break

        # Stop animation when shift key pressed
        if "shift" in keysdown():
            break

"""
2. Volume of hypersphere
- N points tested
- Sphere of radius r in ndim dimensions centered at origin
- Side of the hypercube around the hypersphere is 2r
  so its volume is (2r)^ndim
"""
def volume_hypersphere(r, ndim, N = 1_000_000):
    # coords[0] is list of N 0-dimensional coords
    # coords[1] is list of N 1-dimensional coords
    # etc
    coords = [] 
    for i in range(ndim):
        coords.append(np.random.rand(N) * 2 * r - r) # N numbers -1 to 1
    coords = np.array(coords)

    coords_sq = np.square(coords) # Square each entry

    # Distance of each point from origin
    distances = np.sqrt(np.sum(coords_sq, axis = 0))

    # Proportion of generated points within hypersphere
    prop_in_hsphere = np.sum(distances < r) / N

    # Volume of hypercube the hypersphere is inscribed in
    vol_hcube = pow(2 * r, ndim)

    # Use proportion to find answer
    vol_hsphere = vol_hcube * prop_in_hsphere

    return vol_hsphere




"""
3. DLA
- L odd and is the side length of the boundaries
"""
def dla(L, nparticles):

    # Set up canvas
    rate(1)
    canvas(center = vector(L // 2, L // 2, 0), xmin = 0, xmax = L, ymin = 0, ymax = L)

    occupied = np.array([[False] * L] * L)

    # Every second, choose one of these directions
    dir = [vector(1, 0, 0), vector(-1, 0, 0), 
           vector(0, 1, 0), vector(0, -1, 0)]

    # One loop iteration per particle
    for i in range(nparticles):

        current_color = vector(cm.hsv(i / nparticles * 1000)[0], cm.hsv(i / nparticles * 1000)[1], cm.hsv(i / nparticles * 1000)[2])

        x = sphere(pos = vector(L // 2, L // 2, 0), color = current_color)
        label(pos = vector(L, L, 0), text = "Particles stuck: " + str(round(i / nparticles * 100, 3)) + "%")
        label(pos = vector(L, L - 10, 0), text = "Press SHIFT to exit")

        if occupied[L // 2, L // 2]:
            time.sleep(1000)
            break

        # One loop iteration per step
        while True:

            # Stop animation when shift key pressed
            if "shift" in keysdown():
                return
            
            # Choose step direction
            # Ensure that particle doesn't leave boundaries
            # If it would leave boundaries, re-choose the direction
            chosen_dir = random.choice(dir)
            while True:
                if (0 < x.pos.x + chosen_dir.x and x.pos.x + chosen_dir.x < L and 
                    0 < x.pos.y + chosen_dir.y and x.pos.y + chosen_dir.y < L):
                    x.pos += chosen_dir
                    break
                else:
                    chosen_dir = random.choice(dir)

            x_coord = int(x.pos.x)
            y_coord = int(x.pos.y)

            # Check nearby occupations

            # Hit wall
            if x.pos.x == 1 or x.pos.y == 1 or x.pos.x == L - 1 or x.pos.y == L - 1:
                occupied[x_coord, y_coord] = True
                break
            # Adjacent to occupied cell
            else:
                if (occupied[x_coord, y_coord + 1] or occupied[x_coord, y_coord - 1] or
                    occupied[x_coord + 1, y_coord] or occupied[x_coord - 1, y_coord]):
                    occupied[x_coord, y_coord] = True
                    break


if run_brownian == True:
    print("Running Brownian motion...")
    brownian(101)
    print("Brownian motion stopped")
print()
if run_hypersphere == True:
    for i in range(3, 15):
        print("Hypersphere volume {} dim".format(i), volume_hypersphere(2, i))
print()
if run_dla == True:
    print("Running DLA...")
    dla(101, 1_000_000)
    print("DLA stopped")
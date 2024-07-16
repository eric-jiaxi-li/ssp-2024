from math import *
import matplotlib.pyplot as plt
import numpy as np

def solve_newton(guess, threshold = 1e-4):
    """
    Newguess = Oldguess - Errorofoldguess / derivative
    """
    try:
        def f(z):
            return z ** 3 - 1
        def f_prime(z):
            return 3 * z**2
        
        z = guess
        while abs(f(z) - 0) > threshold:
            z -= f(z) / f_prime(z)

        return z
    except: # if division by 0
        return 0

z1 = 1
z2 = complex(-1/2, -sqrt(3) / 2)
z3 = complex(-1/2, sqrt(3) / 2)
colors = np.array([[-1] * 2000] * 2000)

for a in range(-1000, 1000):
    print(a)
    for b in range(-1000, 1000):
        initial_guess = complex(a, b)
        root = solve_newton(initial_guess)

        err1 = abs(z1 - root)
        err2 = abs(z2 - root)
        err3 = abs(z3 - root)

        min_error = min(err1, min(err2, err3))
        if min_error == err1:
            colors[a + 1000, b + 100] = 100
        elif min_error == err2:
            colors[a + 1000, b + 1000] = 50
        elif min_error == err3:
            colors[a + 1000, b + 1000] = 0

plt.gray()
plt.imshow(colors)
plt.show()
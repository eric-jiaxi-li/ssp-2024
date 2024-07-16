import numpy as np
from math import *
np.random.seed(777)

num = 0
den = 0

for i in range(10000):
    x = np.random.uniform(-0.5, 0.5)
    y = np.random.uniform(-0.5, 0.5)

    if np.sqrt(x ** 2 + y ** 2) < 0.5:
        num += 1
    den += 1

print("Estimation for pi =", num / den * 4)


x = np.random.uniform(-0.5, 0.5, 10000)
y = np.random.uniform(-0.5, 0.5, 10000)

num = np.sum(np.sqrt(x ** 2 + y ** 2) < 0.5)
den = 10000
print("Estimation for pi =", num / den * 4)





# Integrate sin^2 ( 1 / (x * (2-x)))
# Monte carlo integration

def f(x):
    return (np.sin(1 / (x * (2 - x)))) ** 2 # Need np.sin to pass in np array

x_arr = np.random.uniform(0, 2, 10000)
y_arr = np.random.uniform(0, 1, 10000)

# print(f(x_arr))

num = np.sum(y_arr < f(x_arr))
den = 10000
print("Estimation for integral =", num / den * 2)
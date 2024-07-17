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
"""

import numpy as np
from math import *
import odlib

debug = True

def get_fg(tau1, tau3, r2, r2_dot, flag):
    """
    Params: Mostly self-explanatory. Flag: 3rd or 4th order, or
            function (what does this mean?)
    """

    return None
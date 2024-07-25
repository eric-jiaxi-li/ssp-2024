"""
Helpful functions for orbit determination

Tested using the testcases in "OD Code #1",
but may contain further bugs, especially
with negative inputs for right ascension

Also need to check comments to make sure I 
specified things like deg/rad right

Eric Li SSP 2024
"""
from math import *
from astropy.io import fits
import numpy as np
from statistics import stdev

debug = False






######################################################
#
#               Debugging utility
#
######################################################

def testF(function_name, test_value, expected):
    """
    Params: Name of function to debug, function call, expected value of function
    Return: Error, function name, value from function call, expected value
    """
    print("Error = ",
          float(abs(round(test_value - expected, 5))),
          "|", 
          getattr(function_name, "__name__", str(function_name)), 
          "=", 
          test_value, 
          "| Exp =", 
          expected)
    

def check_error(my_val, true_val, var_name, threshold = 0.02):
    """
    Params: my value, the true value of the variable,
            variable name as string, threshold percent
            (default 0.02%)
    """
    percent_error = (my_val - true_val) / true_val * 100

    if abs(percent_error) < threshold: 
        status = "Passed"
    else:
        status = "Failed"

    print("{} {} | Calculated = {} | Actual = {} | Percent error = {} %".format(status, var_name, round(my_val, 5), round(true_val, 5), percent_error))





######################################################
#
#              Unit and trig conversions
#
######################################################

def time_string_to_decimals(time_string):
    """
    https://stackoverflow.com/questions/15208516/convert-a-time-string-into-a-decimal-number-of-hours
    """
    fields = time_string.split(":")
    hours = fields[0] if len(fields) > 0 else 0.0
    minutes = fields[1] if len(fields) > 1 else 0.0
    seconds = fields[2] if len(fields) > 2 else 0.0
    return float(hours) + (float(minutes) / 60.0) + float(seconds) / pow(60.0, 2)



def quadrant_deg(sin_val, cos_val):
    """
    Params: Sine/cosine values of an angle
    Return: The angle in the correct quadrant (deg)
    """
    # Avoid worrying about edge cases
    if cos_val == 1:
        return 0
    elif sin_val == 1:
        return 90
    elif cos_val == -1:
        return 180
    elif sin_val == -1:
        return 270
    
    # General cases
    elif sin_val > 0:
        return degrees(acos(cos_val))
    elif sin_val < 0:
        return 360 - degrees(acos(cos_val))
def quadrant_rad(sin_val, cos_val):
    """
    Params: Sine/cosine values of an angle
    Return: The angle in the correct quadrant (rad)
    """
    return radians(quadrant_deg(sin_val, cos_val))



def HMS_to_deg(hours, minutes, seconds): 
    """
    Params: Right ascension in hours, minutes, seconds
    Return: This angle in decimal degrees
    """
    return 360 * (hours + minutes/60 + seconds/3600) / 24
def HMS_to_rad(hours, minutes, seconds):
    """
    Params: Right ascension in hours, minutes, seconds
    Return: This angle in decimal radians
    """
    return radians(HMS_to_deg(hours, minutes, seconds))



def DMS_to_deg(degrees, aminutes, aseconds): 
    """
    Params: Declination in degrees, arcminutes, arcseconds
    Return: This angle in decimal degrees
    """
    if degrees >= 0:
        return degrees + aminutes/60 + aseconds/3600
    else:
        return -(-degrees + aminutes/60 + aseconds/3600)
def DMS_to_rad(degrees, aminutes, aseconds):
    """
    Params: Declination in degrees, arcminutes, arcseconds
    Return: This angle in decimal radians
    """
    return radians(DMS_to_deg(degrees, aminutes, aseconds))



def RA_decimal_to_HMS(RA):
    """
    Params: Right ascension in decimals
    Return: String converting the RA to HMS, to be printed
    """
    hours = RA // (360/24)
    RA -= hours * (360/24)
    minutes = RA // (360/(24*60))
    RA -= minutes * (360/(24*60))
    seconds = RA / (360/(24*60*60))

    ret = ""
    ret += str(round(hours, 6)) + " hours "
    ret += str(round(minutes, 6)) + " minutes "
    ret += str(round(seconds, 6)) + " seconds "
    return ret



def DEC_decimal_to_DMS(DEC):
    """
    Params: Declination in decimals
    Return: String converting the Dec to DMS, to be printed
    """
    degrees = -1
    arcminutes = -1
    arcseconds = -1
    if DEC == 0:
        degrees = 0
        arcminutes = 0
        arcseconds = 0
    else:
        degrees = int(DEC)
        DEC -= degrees
        arcminutes = int(DEC / (1/60))
        DEC -= arcminutes * (1/60)
        arcseconds = DEC / (1/(60*60))

    # Negative sign only appears before the degrees
    if degrees < 0:
        arcminutes *= -1
        arcseconds *= -1

    ret = ""
    ret += str(round(degrees, 6)) + " degrees "
    ret += str(round(arcminutes, 6)) + " arcminutes "
    ret += str(round(arcseconds, 6)) + " arcseconds "
    return ret



def julian(Y, M, D, T = 0):
    """
    Params: Year, Month, Day, Time in decimal hours
    Return: Julian date at that time
    """
    return 367*Y - 7 * (Y + (M+9)//12)//4 + (275*M)//9 + D + 1721013.5 + 360.985647366 * T / 24



def days_to_GD(time):
    # Regular days to Gaussian days
    k_Gauss = 0.0172020989484
    return time * k_Gauss
def GD_to_days(time):
    # Gaussian days to regular days
    k_Gauss = 0.0172020989484
    return time / k_Gauss




######################################################
#
#              Vector geometry functions
#
######################################################

def rotate_vec(np_vector, deg_rotated, axis):
    """
    Params: 3D numpy array (vector), degrees to be rotated, axis of rotation (x, y, or z as string)
    Return: Rotated vector
    """
    # https://stackoverflow.com/questions/14607640/rotating-a-vector-in-3d-space
    c = cos(radians(deg_rotated))
    s = sin(radians(deg_rotated))

    rotate_x = np.array([[1, 0, 0],
                         [0, c, -s],
                         [0, s, c]])
    rotate_y = np.array([[c, 0, s],
                         [0, 1, 0],
                         [-s, 0, c]])
    rotate_z = np.array([[c, -s, 0],
                         [s, c, 0],
                         [0, 0, 1]])

    if axis == "x":
        return rotate_x @ np_vector
    elif axis == "y":
        return rotate_y @ np_vector
    elif axis == "z":
        return rotate_z @ np_vector
    else:
        print("rotation_matrix: Axis \"", axis, "\"is invalid", sep = "")
        return None



def mag(vector): 
    # Magnitude of vector
    return sqrt(sum(pow(element, 2) for element in vector))












######################################################
#
#              Orbit determination
#
######################################################

def find_centroid(fits_file, target_x, target_y, radius, annulus_width, method):
    """
    Params: The fits file (string) to find centroid of, the x and y coordinates of the 
            target star, the radius of the circle surrounding the target star, 
            and the annulus from which we determine the sky brightness has annulus_width
            Find sky brightness using median or mean (method)
    Return: x and y coordinates of the star's centroid + uncertainties
    """

    sky_radius = annulus_width + radius

    img = fits.getdata(fits_file)
    m = img.shape[0]
    n = img.shape[1]

    # Due to differences between Python and AstroImageJ, need to swap coordinates
    temp = target_x
    target_x = target_y
    target_y = temp

    # Check inputs
    if target_x + sky_radius >= m or target_x - sky_radius <= -1 or target_y + sky_radius >= n or target_y - sky_radius <= -1:
        return "Error: Target too close to the edges or radius too big"
    if radius <= 0 or sky_radius <= 0:
        return "Error: radius and sky_radius cannot be nonpositive"
    if method != "median" and method != "mean":
        return "Error: only median and mean are allowed to be methods"

    # Determine average sky brightness
    # https://stackoverflow.com/a/8650741
    x, y = np.ogrid[-target_x:m-target_x, -target_y:n-target_y]
    annulus_mask = np.logical_and(radius**2 < x**2 + y**2, x**2 + y**2 < sky_radius**2)

    if method == "median":
        sky_brightness = np.median(img[annulus_mask])
    elif method == "mean":
        sky_brightness = np.mean(img[annulus_mask])
    img = img - sky_brightness

    # Calculate centroid
    sky_mask = x**2 + y**2 > radius**2
    img[sky_mask] = 0 # Zero out all pixels not within the circle

    # Axis = 1 collapses the columns
    centroid_x = np.dot(np.sum(img, axis = 1), np.arange(0, m)) / np.sum(img)
    centroid_y = np.dot(np.sum(img, axis = 0), np.arange(0, n)) / np.sum(img)

    # Uncertainties
    # Remove unused columns
    indices_x, = np.where(np.all(img == 0, axis = 1) == False) # np.where returns 2 values, "indices_x," takes the first
    indices_y, = np.where(np.all(img == 0, axis = 0) == False)
    img_x = img[indices_x, :]
    img_y = img[:, indices_y]

    N = np.sum(img)
    sigma_x = np.sqrt(np.sum(np.sum(img_x, axis = 1) * (indices_x - centroid_x) ** 2) / (N * (N - 1)))
    sigma_y = np.sqrt(np.sum(np.sum(img_y, axis = 0) * (indices_y - centroid_y) ** 2) / (N * (N - 1)))

    # Swap back
    temp = sigma_x
    sigma_x = sigma_y
    sigma_y = temp

    temp = centroid_x
    centroid_x = centroid_y
    centroid_y = temp

    return centroid_x, centroid_y, sigma_x, sigma_y



def find_centroid2(fits_file, target_x, target_y, radius, annulus_inner, annulus_outer, method):
    """
    The same as find_centroid, but with an option to specify inner radius 
    of annulus
    Params: The fits file (string) to find centroid of, the x and y coordinates of the 
            target star, the radius of the circle surrounding the target star, 
            and the annulus from which we determine the sky brightness has 
            inner/outer radii annulus_inner/outer
            Find sky brightness using median or mean (method)
    Return: x and y coordinates of the star's centroid + uncertainties
    """

    img = fits.getdata(fits_file)
    m = img.shape[0]
    n = img.shape[1]

    # Due to differences between Python and AstroImageJ, need to swap coordinates
    temp = target_x
    target_x = target_y
    target_y = temp

    # Check inputs
    # This causes a bug for some reason in photometry idfk why
    # if target_x + annulus_outer >= m or target_x - annulus_outer <= -1 or target_y + annulus_outer >= n or target_y - annulus_outer <= -1:
    #     return "Error: Target too close to the edges or radius too big"
    # if radius <= 0 or annulus_outer <= 0:
    #     return "Error: radius and annulus_outer cannot be nonpositive"
    # if method != "median" and method != "mean":
    #     return "Error: only median and mean are allowed to be methods"

    # Determine average sky brightness
    # https://stackoverflow.com/a/8650741
    x, y = np.ogrid[-target_x:m-target_x, -target_y:n-target_y]
    annulus_mask = np.logical_and(annulus_inner**2 < x**2 + y**2, x**2 + y**2 < annulus_outer**2)

    if method == "median":
        sky_brightness = np.median(img[annulus_mask])
    elif method == "mean":
        sky_brightness = np.mean(img[annulus_mask])
    img = img - sky_brightness

    # Calculate centroid
    sky_mask = x**2 + y**2 > radius**2
    img[sky_mask] = 0 # Zero out all pixels not within the circle

    # Axis = 1 collapses the columns
    centroid_x = np.dot(np.sum(img, axis = 1), np.arange(0, m)) / np.sum(img)
    centroid_y = np.dot(np.sum(img, axis = 0), np.arange(0, n)) / np.sum(img)

    # Uncertainties
    # Remove unused columns
    indices_x, = np.where(np.all(img == 0, axis = 1) == False) # np.where returns 2 values, "indices_x," takes the first
    indices_y, = np.where(np.all(img == 0, axis = 0) == False)
    img_x = img[indices_x, :]
    img_y = img[:, indices_y]

    N = np.sum(img)
    sigma_x = np.sqrt(np.sum(np.sum(img_x, axis = 1) * (indices_x - centroid_x) ** 2) / (N * (N - 1)))
    sigma_y = np.sqrt(np.sum(np.sum(img_y, axis = 0) * (indices_y - centroid_y) ** 2) / (N * (N - 1)))

    # Swap back
    temp = sigma_x
    sigma_x = sigma_y
    sigma_y = temp

    temp = centroid_x
    centroid_x = centroid_y
    centroid_y = temp

    return centroid_x, centroid_y, sigma_x, sigma_y



def find_centroid_chooseparams(fits_file, target_x, target_y):
    """
    Params: The fits file (string) to find centroid of, the x and y coordinates of the 
            target star
    Return: Select the parameters that give the lowest uncertainty
    """
    min_uncertainty = 9999999
    best_radius = -1
    best_annulus_width = -1
    best_method = "X"

    for radius in range(1, 5):
        for annulus_width in range(1, 5):
            for method in ["mean", "median"]:

                centroid_x, centroid_y, sigma_x, sigma_y = find_centroid(fits_file, target_x, target_y, radius, annulus_width, method)
                uncertainty = sqrt(sigma_x ** 2 + sigma_y ** 2) # How I defined the uncertainty

                if uncertainty < min_uncertainty:
                    min_uncertainty = uncertainty
                    best_radius = radius
                    best_annulus_width = annulus_width
                    best_method = method

    return best_radius, best_annulus_width, best_method



def lspr(filename, target_x, target_y, need_convert):
    """
    Params: File containing the (x,y) centroids and (RA, DEC)
            J2000.0 coordinates of about 10 reference stars
            The (x,y) centroid of an unknown object
            need_convert: if True, need to convert from the colons
            to decimal RA/DEC.
    Return: The 6 plate constants, in degrees and deg/px
            The RA and DEC of J2000.0 coordinates of the unknown
            object, as strings
            The uncertainty of the fit in RA and DEC, in arcseconds
    """

    # Read file
    fin = open(filename)
    ref_x = []
    ref_y = []
    ref_RA = []
    ref_DEC = []
    for line in fin.readlines():
        x, y, RA, DEC = line.split()
        x = float(x)
        y = float(y)

        if need_convert == True:
            RA_h, RA_m, RA_s = map(float, RA.split(sep = ":"))
            DEC_d, DEC_m, DEC_s = map(float, DEC.split(sep = ":"))
            RA = HMS_to_deg(RA_h, RA_m, RA_s)
            DEC = DMS_to_deg(DEC_d, DEC_m, DEC_s)
        else:
            RA = float(RA)
            DEC = float(DEC)

        ref_x.append(x)
        ref_y.append(y)
        ref_RA.append(RA)
        ref_DEC.append(DEC)

    fin.close()
    n = len(ref_x) # Number of reference stars

    if debug == True:
        print()
        print(ref_x)
        print(ref_y)
        print(ref_RA)
        print(ref_DEC)

    ref_x = np.array(ref_x)
    ref_y = np.array(ref_y)
    ref_RA = np.array(ref_RA)
    ref_DEC = np.array(ref_DEC)



    # Calculate the 6 plate constants
    mat = np.array([[n, np.sum(ref_x), np.sum(ref_y)], 
                    [np.sum(ref_x), np.sum(ref_x ** 2), np.sum(ref_x * ref_y)],
                    [np.sum(ref_y), np.sum(ref_x * ref_y), np.sum(ref_y ** 2)]])
    inv_mat = np.linalg.inv(mat)

    vec_RA = np.array([np.sum(ref_RA), np.sum(ref_RA * ref_x), np.sum(ref_RA * ref_y)])
    vec_DEC = np.array([np.sum(ref_DEC), np.sum(ref_DEC * ref_x), np.sum(ref_DEC * ref_y)])

    b1, a11, a12 = inv_mat @ vec_RA
    b2, a21, a22 = inv_mat @ vec_DEC

    if debug == True:
        print()
        print("b1", b1)
        print("b2", b2)
        print("a11", a11)
        print("a12", a12)
        print("a21", a21)
        print("a22", a22)



    # Calculate uncertainties
    sigma_RA = np.sqrt(np.sum((ref_RA - b1 - a11*ref_x - a12*ref_y) ** 2) / (n - 3))
    sigma_DEC = np.sqrt(np.sum((ref_DEC - b2 - a21*ref_x - a22*ref_y) ** 2) / (n - 3))

    # ref_RA and ref_DEC are in degrees for input, so need to convert to arcsec
    sigma_RA *= 3600
    sigma_DEC *= 3600
    
    if debug == True:
        print()
        print("RA error", sigma_RA)
        print("DEC error", sigma_DEC)



    # Calculate RA and DEC
    RA = RA_decimal_to_HMS(b1 + a11*target_x + a12*target_y)
    DEC = DEC_decimal_to_DMS(b2 + a21*target_x + a22*target_y)

    if debug == True:
        print(RA, DEC)

    return b1, b2, a11, a12, a21, a22, sigma_RA, sigma_DEC, RA, DEC



def solve_kepler(M, eccentricity, threshold = 1e-4):
    """
    Params: Mean anomaly, eccentricity, maximum allowable error
    Return: Eccentric anomaly corresponding to the
            mean anomaly

    Uses Newton's method, 
    Newguess = Oldguess - Errorofoldguess / derivative
    """
    def kepler(E, eccentricity):
        # Kepler's equation: M = E - e sin(E)
        return E - eccentricity * sin(E)
    def kepler_prime(E, eccentricity):
        # Derivative of Kepler's: M' = 1 - e cos(E)
        return 1 - eccentricity * cos(E)
    
    E = M # Initial guess
    M_guess = kepler(E, eccentricity)
    while abs(M - kepler(E, eccentricity)) > threshold:
        E -= (M_guess - M) / kepler_prime(E, eccentricity)
        M_guess = kepler(E, eccentricity)

    return E



def photometry(fits_file, target_x, target_y, 
               radius, annulus_inner, annulus_outer, 
               read_noise, dark_current, gain, 
               show_centroid = True):
    """
    Params: Filepath to image, approximate x/y of object, 
            radius of aperture, annulus inner/outer radii (px)
            Read noise, dark current in e-, and gain
            show_centroid if you want to print the centroid too
    Return: Total signal S and uncertainty in ADU
            Signal-to-noise ratio (SNR)
            Instrumental magnitude m_inst = -2.5 log10(S)
            Uncertainty on instrumental magnitude,
            sigma_m_inst = 1.0875/SNR
    """

    # Reposition target_x, target_y to centroid
    # sigma_x, sigma_y not needed
    target_x, target_y, sigma_x, sigma_y = find_centroid2(fits_file, target_x, target_y, radius, annulus_inner, annulus_outer, "median")
    if show_centroid == True:
        print("Centroid = ({}, {})".format(target_x, target_y))

    temp = target_x
    target_x = target_y
    target_y = temp

    img = fits.getdata(fits_file)
    m = img.shape[0] # 1024
    n = img.shape[1] # 1024

    # Determine median sky brightness
    # https://stackoverflow.com/a/8650741
    x, y = np.ogrid[-target_x:m-target_x, -target_y:n-target_y]
    annulus_mask = np.logical_and(annulus_inner**2 < x**2 + y**2, x**2 + y**2 < annulus_outer**2)
    sky_brightness = np.median(img[annulus_mask])


    # Find total signal
    aperture_mask = x**2 + y**2 < radius**2
    S = np.sum(img[aperture_mask]) - np.sum(aperture_mask) * sky_brightness
    m_inst = -2.5 * log10(S)


    # SNR
    S_e = S
    n_ap = np.sum(aperture_mask)
    n_an = np.sum(annulus_mask)
    sky_e = sky_brightness
    D_e = dark_current
    p2 = read_noise ** 2 + gain ** 2 / 12

    SNR = sqrt(S_e) / sqrt(1 + n_ap * (1 + n_ap/n_an) * ((sky_e + D_e + p2) / (S_e)))
    sigma_m_inst = 1.0875 / SNR
    sigma_S = S / SNR # Noise is the error

    return S, sigma_S, SNR, m_inst, sigma_m_inst



def diff_photometry(fits_file, ref_stars_txt, ast_x, ast_y):
    """
    Params: Image file, text file containing approximate
            x, y, and catalog magnitude for some reference
            stars, and x and y coordinates of an asteroid
            we want to find the magnitude for.
            When performing photometry, we will use the
            parameters given in the previous section's
            testcase.
    Return: Average offset between catalog/instrumental
            magnitudes C, dm (systematic uncertainty),
            and catalog magnitude with uncertainty.
    """

    # Read input
    img = fits.getdata(fits_file)
    fin = open(ref_stars_txt)

    star_x = []
    star_y = []
    star_mag = []
    for line in fin.readlines():
        line = line.strip()
        x, y, mag = map(float, line.split())
        star_x.append(x)
        star_y.append(y)
        star_mag.append(mag)
        # if debug == True:
        #     print(star_x, star_y, star_mag)



    n = len(star_x) # Number of stars
    C = 0 # Average of m_catalog - m_instrumental for the reference stars
    m_inst_all = [] # List of all the instrumental magnitudes; to be used to calculate dm (systematic uncertainty)

    for i in range(n):
        S, sigma_S, SNR, m_inst, sigma_m_inst = photometry(fits_file, star_x[i], star_y[i], 5, 8, 13, 11, 10, 1, show_centroid = False)
        C += abs(m_inst - star_mag[i])
        m_inst_all.append(m_inst)
        
    C /= n
    dm = stdev(m_inst_all) # Systematic uncertainty

    # Calculate values for our asteroid
    S, sigma_S, SNR, m_inst, sigma_m_inst = photometry(fits_file, ast_x, ast_y, 5, 8, 13, 11, 10, 1, show_centroid = False)
    m_catalog = m_inst + C
    sigma_m_catalog = sqrt(dm ** 2 + sigma_m_inst ** 2) # Uncertainty in catalog magnitude of asteroid

    return C, m_catalog, dm, sigma_m_catalog



def gen_eph(text_file, sun_vec, earth_tilt_deg, eph_Y, eph_M, eph_D, obs_Y, obs_M, obs_D):
    """
    Params: Text file containing the orbital elements (Note:
            may vary from time to time) at observation time
            Earth-to-sun vector as a np array in equatorial coords
            Tilt of earth in degrees, 23.4384987711 deg
            Date of desired ephemeris: Y, M, D at 0 UTC
            Observation time in same format
            All units AU, days
    Return: RA/DEC of asteroid at the specified time
    """
    eph_time_julian = julian(eph_Y, eph_M, eph_D)
    obs_time_julian = julian(obs_Y, obs_M, obs_D)
    interval_Gaussian = days_to_GD(eph_time_julian - obs_time_julian)
    
    # Each value on a separate line
    fin = open(text_file)
    EC = float(fin.readline()) # Eccentricity
    QR = float(fin.readline())
    IN = float(fin.readline()) # Inclination (deg)
    OM = float(fin.readline()) # Long of asc node (deg)
    W = float(fin.readline()) # Arg of perifocus (deg)
    Tp = float(fin.readline())
    N = float(fin.readline())
    MA = float(fin.readline()) # Mean anomaly (deg)
    TA = float(fin.readline())
    A = float(fin.readline()) # Semimajor axis (AU)
    AD = float(fin.readline())
    PR = float(fin.readline())
    
	# Rename variables, convert all to rad
    a = A
    e = EC
    i = radians(IN)
    omega = radians(OM)
    w = radians(W)
    M = radians(MA)

    # Update mean anomaly
    period_Gaussian = sqrt(4 * (pi ** 2) * (a ** 3))
    M += 2 * pi * interval_Gaussian / period_Gaussian 
    M = (M % (2 * pi)) 

    E = solve_kepler(M, e, threshold = 1e-9) # Eccentric anomaly, rad

    
    r = np.array([a * cos(E) - a * e, a * sqrt(1 - e ** 2) * sin(E), 0])
    
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

    # Correct for tilt of earth
    tilt = radians(earth_tilt_deg) # Angle of earth's axis
    tilt_spin = np.array([[1, 0, 0], 
                          [0, cos(tilt), -sin(tilt)], 
                          [0, sin(tilt), cos(tilt)]])
    r_eq = tilt_spin @ r_ec # r in equatorial coordinates

    # Range vector
    rho = r_eq + sun_vec
    rho_hat = rho / mag(rho)

    # RA and DEC
    DEC = degrees(asin(rho_hat[2]))
    sin_RA = (rho_hat[1] / cos(radians(DEC)))
    cos_RA = (rho_hat[0] / cos(radians(DEC)))
    RA = quadrant_deg(sin_RA, cos_RA)
    
    return RA, DEC



def get_fg(tau1, tau3, r2, r2_dot, order = 4):
    """
    Params: See OD Guide. 3rd or 4th order
            approximation, 3 or 4
            Functions not necessary, says Dr. F
    Return: values of f1, f3, g1, g3
    """

    r2_mag = mag(r2)
    u = 1 / (r2_mag ** 3)
    z = np.dot(r2, r2_dot) / (r2_mag ** 2)
    q = np.dot(r2_dot, r2_dot) / (r2_mag ** 2) - u


    if order == 3:
        f1 = 1 - 1/2*u*tau1**2 + 1/2*u*z*tau1**3
        f3 = 1 - 1/2*u*tau3**2 + 1/2*u*z*tau3**3
        g1 = tau1 - 1/6*u*tau1**3
        g3 = tau3 - 1/6*u*tau3**3

    elif order == 4:
        f1 = 1 - 1/2*u*tau1**2 + 1/2*u*z*tau1**3 + 1/24*(3*u*q-15*u*z**2+u**2)*tau1**4
        f3 = 1 - 1/2*u*tau3**2 + 1/2*u*z*tau3**3 + 1/24*(3*u*q-15*u*z**2+u**2)*tau3**4
        g1 = tau1 - 1/6*u*tau1**3 + 1/4*u*z*tau1**4
        g3 = tau3 - 1/6*u*tau3**3 + 1/4*u*z*tau3**4

    else:
        raise Exception("Invalid order: only 3 and 4 allowed")
    

    return f1, f3, g1, g3



def get_orbital_elements(x, y, z, vx, vy, vz):
    """
    Params: in AU and days, the position vector x, y, z and the velocity
            vector vx, vy, vz. 
    Return: All 6 orbital elements in AU and degrees
    """

    # Convert to Gaussian days
    k_Gauss = 0.0172020989484
    mu = 1 # mu = G * M_sun = 1 in Gaussian days/AU

    vx /= k_Gauss
    vy /= k_Gauss
    vz /= k_Gauss

    r_vec = np.array([x, y, z]) # AU
    r_dot_vec = np.array([vx, vy, vz]) # AU/GD
    r = mag(r_vec)


    # Semimajor axis
    a = 1 / (2 / r - np.dot(r_dot_vec, r_dot_vec) / mu)


    # Eccentricity
    e = np.sqrt(1 - mag(np.cross(r_vec, r_dot_vec))**2 / (mu * a))


    # Inclination
    h = np.cross(r_vec, r_dot_vec) # Angular momentum
    i = degrees(acos(h[2] / mag(h)))


    # Longitude of ascending node
    sin_omega = h[0] / (mag(h) * sin(radians(i)))
    cos_omega = -h[1] / (mag(h) * sin(radians(i)))
    omega = quadrant_deg(sin_omega, cos_omega)


    # Argument of periapsis
    sin_nu = a / mag(h) * (1 - e**2) / e * np.dot(r_vec, r_dot_vec) / r
    cos_nu = 1 / e * (a * (1 - e**2) / r - 1)

    sin_u = r_vec[2] / (r * sin(radians(i)))
    cos_u = (r_vec[0] * cos(radians(omega)) + r_vec[1] * sin(radians(omega))) / r

    nu = quadrant_deg(sin_nu, cos_nu)
    u = quadrant_deg(sin_u, cos_u)
    w = (u - nu) % 360.0


    # Mean anomaly
    E = -1
    if 0 <= nu and nu < 180:
        E = acos(1 / e * (1 - r / a))
    elif 180 <= nu and nu < 360:
        E = 2 * pi - acos(1 / e * (1 - r / a))
    M = degrees(E - e * sin(E)) % 360
    


    return a, e, i, omega, w, M



def mog(input_file):
    """
    Params: See "Read input" section
    Output: position and velocity vectors at 2nd observation
    """
    # Constants
    k_Gauss = 0.0172020989484
    c_AU = 173.144643267 # Speed of light in au/(mean solar)day
    eps = radians(23.4384668053) # Earth's obliquity




    ######################################################
    #
    #                    Read input
    #
    ######################################################
    curr_line_number = 1
    fin = open(input_file)

    for line in fin.readlines():
        T, RA, DEC, sun_vec_0, sun_vec_1, sun_vec_2 = line.split()

        # Time of observation, JD
        T = float(T)

        # RA and DEC
        RA_components_0, RA_components_1, RA_components_2 = map(float, RA.split(":"))
        RA = HMS_to_rad(RA_components_0, RA_components_1, RA_components_2) # RA in rad
        DEC_components_0, DEC_components_1, DEC_components_2 = map(float, DEC.split(":"))
        DEC = DMS_to_rad(DEC_components_0, DEC_components_1, DEC_components_2) # DEC in rad
        
        # Earth-sun vector
        sun_vec = np.array([sun_vec_0, sun_vec_1, sun_vec_2]).astype(np.float64)

        # Assign inputs to the right variables
        if curr_line_number == 1:
            rho_hat1 = np.array([cos(RA) * cos(DEC), sin(RA) * cos(DEC), sin(DEC)])
            R1 = sun_vec
            t1 = T
        if curr_line_number == 2:
            rho_hat2 = np.array([cos(RA) * cos(DEC), sin(RA) * cos(DEC), sin(DEC)])
            R2 = sun_vec
            t2 = T
        if curr_line_number == 3:
            rho_hat3 = np.array([cos(RA) * cos(DEC), sin(RA) * cos(DEC), sin(DEC)])
            R3 = sun_vec
            t3 = T


        curr_line_number += 1

    # Original observation times in Julian Days, don't change!
    t01 = t1
    t02 = t2
    t03 = t3




    ######################################################
    #
    #                   First iteration
    #
    ######################################################
    D0 = np.dot(rho_hat1, np.cross(rho_hat2, rho_hat3))
    D11 = np.dot(np.cross(R1, rho_hat2), rho_hat3)
    D12 = np.dot(np.cross(R2, rho_hat2), rho_hat3)
    D13 = np.dot(np.cross(R3, rho_hat2), rho_hat3)
    D21 = np.dot(np.cross(rho_hat1, R1), rho_hat3)
    D22 = np.dot(np.cross(rho_hat1, R2), rho_hat3)
    D23 = np.dot(np.cross(rho_hat1, R3), rho_hat3)
    D31 = np.dot(rho_hat1, np.cross(rho_hat2, R1))
    D32 = np.dot(rho_hat1, np.cross(rho_hat2, R2))
    D33 = np.dot(rho_hat1, np.cross(rho_hat2, R3))

    tau1 = k_Gauss * (t1 - t2)
    tau3 = k_Gauss * (t3 - t2)
    tau0 = k_Gauss * (t3 - t1)

    # Initial guesses for c1, c3 using Kepler's Laws
    c1 = tau3 / tau0
    c2 = -1
    c3 = -tau1 / tau0

    # Scalar ranges of each observation
    rho1 = (c1 * D11 + c2 * D12 + c3 * D13) / (c1 * D0)
    rho2 = (c1 * D21 + c2 * D22 + c3 * D23) / (c2 * D0)
    rho3 = (c1 * D31 + c2 * D32 + c3 * D33) / (c3 * D0)

    # Position vector (sun to asteroid)
    r1 = rho1 * rho_hat1 - R1
    r2 = rho2 * rho_hat2 - R2
    r3 = rho3 * rho_hat3 - R3

    # Initial linear interpolation of velocity
    r_dot12 = (r2 - r1) / (-tau1)
    r_dot23 = (r3 - r2) / (tau3)
    r_dot2 = tau3 / tau0 * r_dot12 - tau1 / tau0 * r_dot23

    # Store vectors from previous iteration to check convergence
    last_iteration_r2 = np.copy(r2)
    last_iteration_r_dot2 = np.copy(r_dot2)

    # Lightspeed correction
    t1 = t01 - rho1 / c_AU
    t2 = t02 - rho2 / c_AU
    t3 = t03 - rho3 / c_AU



    ######################################################
    #
    #                 Subsequent iterations
    #
    ######################################################

    while True:
        tau1 = k_Gauss * (t1 - t2)
        tau3 = k_Gauss * (t3 - t2)
        tau0 = k_Gauss * (t3 - t1)

        f1, f3, g1, g3 = get_fg(tau1, tau3, r2, r_dot2)
        c1 = g3 / (f1 * g3 - g1 * f3)
        c3 = -g1 / (f1 * g3 - g1 * f3)
        d1 = -f3 / (f1 * g3 - g1 * f3)
        d3 = f1 / (f1 * g3 - g1 * f3)

        # Scalar ranges of each observation
        rho1 = (c1 * D11 + c2 * D12 + c3 * D13) / (c1 * D0)
        rho2 = (c1 * D21 + c2 * D22 + c3 * D23) / (c2 * D0)
        rho3 = (c1 * D31 + c2 * D32 + c3 * D33) / (c3 * D0)

        # Position vector (sun to asteroid)
        r1 = rho1 * rho_hat1 - R1
        r2 = rho2 * rho_hat2 - R2
        r3 = rho3 * rho_hat3 - R3

        r_dot2 = d1 * r1 + d3 * r3

        # Lightspeed correction
        t1 = t01 - rho1 / c_AU
        t2 = t02 - rho2 / c_AU
        t3 = t03 - rho3 / c_AU

        # Check for convergence
        if mag(r2 - last_iteration_r2) + mag(r_dot2 - last_iteration_r_dot2) < 1e-8:
            # Convert to ecliptic coordinates
            tilt_spin = np.linalg.inv(np.array([[1, 0, 0], 
                                                [0, cos(eps), -sin(eps)], 
                                                [0, sin(eps), cos(eps)]]))
            
            # get_orbital_elements requires days, not Gaussian days
            return tilt_spin @ r2, tilt_spin @ (r_dot2 * k_Gauss) 
        
        else:
            last_iteration_r2 = np.copy(r2)
            last_iteration_r_dot2 = np.copy(r_dot2)



def mog2(t1, RA1, DEC1, R1, 
         t2, RA2, DEC2, R2,
         t3, RA3, DEC3, R3):
    """
    Duplicate of Method of Gauss function that
    doesn't require reading from files.
    Params: observation time, RA/DEC, sun vector
            for each set of observations. Radians
    Return: Position and velocity vector at 2nd 
            observation time
    """

    # Constants
    k_Gauss = 0.0172020989484
    c_AU = 173.144643267 # Speed of light in au/(mean solar)day
    eps = radians(23.4384668053) # Earth's obliquity




    ######################################################
    #
    #                    Read input
    #
    ######################################################
    
    rho_hat1 = np.array([cos(RA1) * cos(DEC1), sin(RA1) * cos(DEC1), sin(DEC1)])
    rho_hat2 = np.array([cos(RA2) * cos(DEC2), sin(RA2) * cos(DEC2), sin(DEC2)])
    rho_hat3 = np.array([cos(RA3) * cos(DEC3), sin(RA3) * cos(DEC3), sin(DEC3)])

    # Original observation times in Julian Days, don't change!
    t01 = t1
    t02 = t2
    t03 = t3




    ######################################################
    #
    #                   First iteration
    #
    ######################################################
    D0 = np.dot(rho_hat1, np.cross(rho_hat2, rho_hat3))
    D11 = np.dot(np.cross(R1, rho_hat2), rho_hat3)
    D12 = np.dot(np.cross(R2, rho_hat2), rho_hat3)
    D13 = np.dot(np.cross(R3, rho_hat2), rho_hat3)
    D21 = np.dot(np.cross(rho_hat1, R1), rho_hat3)
    D22 = np.dot(np.cross(rho_hat1, R2), rho_hat3)
    D23 = np.dot(np.cross(rho_hat1, R3), rho_hat3)
    D31 = np.dot(rho_hat1, np.cross(rho_hat2, R1))
    D32 = np.dot(rho_hat1, np.cross(rho_hat2, R2))
    D33 = np.dot(rho_hat1, np.cross(rho_hat2, R3))

    tau1 = k_Gauss * (t1 - t2)
    tau3 = k_Gauss * (t3 - t2)
    tau0 = k_Gauss * (t3 - t1)

    # Initial guesses for c1, c3 using Kepler's Laws
    c1 = tau3 / tau0
    c2 = -1
    c3 = -tau1 / tau0

    # Scalar ranges of each observation
    rho1 = (c1 * D11 + c2 * D12 + c3 * D13) / (c1 * D0)
    rho2 = (c1 * D21 + c2 * D22 + c3 * D23) / (c2 * D0)
    rho3 = (c1 * D31 + c2 * D32 + c3 * D33) / (c3 * D0)

    # Position vector (sun to asteroid)
    r1 = rho1 * rho_hat1 - R1
    r2 = rho2 * rho_hat2 - R2
    r3 = rho3 * rho_hat3 - R3

    # Initial linear interpolation of velocity
    r_dot12 = (r2 - r1) / (-tau1)
    r_dot23 = (r3 - r2) / (tau3)
    r_dot2 = tau3 / tau0 * r_dot12 - tau1 / tau0 * r_dot23

    # Store vectors from previous iteration to check convergence
    last_iteration_r2 = np.copy(r2)
    last_iteration_r_dot2 = np.copy(r_dot2)

    # Lightspeed correction
    t1 = t01 - rho1 / c_AU
    t2 = t02 - rho2 / c_AU
    t3 = t03 - rho3 / c_AU



    ######################################################
    #
    #                 Subsequent iterations
    #
    ######################################################

    while True:
        tau1 = k_Gauss * (t1 - t2)
        tau3 = k_Gauss * (t3 - t2)
        tau0 = k_Gauss * (t3 - t1)

        f1, f3, g1, g3 = get_fg(tau1, tau3, r2, r_dot2)
        c1 = g3 / (f1 * g3 - g1 * f3)
        c3 = -g1 / (f1 * g3 - g1 * f3)
        d1 = -f3 / (f1 * g3 - g1 * f3)
        d3 = f1 / (f1 * g3 - g1 * f3)

        # Scalar ranges of each observation
        rho1 = (c1 * D11 + c2 * D12 + c3 * D13) / (c1 * D0)
        rho2 = (c1 * D21 + c2 * D22 + c3 * D23) / (c2 * D0)
        rho3 = (c1 * D31 + c2 * D32 + c3 * D33) / (c3 * D0)

        # Position vector (sun to asteroid)
        r1 = rho1 * rho_hat1 - R1
        r2 = rho2 * rho_hat2 - R2
        r3 = rho3 * rho_hat3 - R3

        r_dot2 = d1 * r1 + d3 * r3

        # Lightspeed correction
        t1 = t01 - rho1 / c_AU
        t2 = t02 - rho2 / c_AU
        t3 = t03 - rho3 / c_AU

        # Check for convergence
        if mag(r2 - last_iteration_r2) + mag(r_dot2 - last_iteration_r_dot2) < 1e-8:
            # Convert to ecliptic coordinates
            tilt_spin = np.linalg.inv(np.array([[1, 0, 0], 
                                                [0, cos(eps), -sin(eps)], 
                                                [0, sin(eps), cos(eps)]]))
            
            # get_orbital_elements requires days, not Gaussian days
            return tilt_spin @ r2, tilt_spin @ (r_dot2 * k_Gauss) 
        
        else:
            last_iteration_r2 = np.copy(r2)
            last_iteration_r_dot2 = np.copy(r_dot2)



######################################################
#
#                    Run all tests
#
######################################################
if debug == True:
    print()
    print()
    print()

    print("----------ODLIB FUNCTION TEST RESULTS----------")
    testF(HMS_to_deg, HMS_to_deg(12, 3, 5.3), 180.7720833)
    testF(HMS_to_rad, HMS_to_rad(12, 3, 5.3), 180.7720833 * pi/180)
    testF(DMS_to_deg, DMS_to_deg(-13, 45, 23.45), -13.75651389)
    testF(DMS_to_rad, DMS_to_rad(-13, 45, 23.45), -13.75651389 * pi/180)
    for arg in [0, 90, 130, 200, 300]:
        testF(quadrant_deg, quadrant_deg(sin(radians(arg)), cos(radians(arg))), arg)
    for arg in [0, 90, 130, 200, 300]:
        arg = radians(arg)
        testF(quadrant_rad, quadrant_rad(sin(arg), cos(arg)), arg)
    testF(solve_kepler, solve_kepler(3, 0.1750074901308245), 3.021045582774241)
    
    
    # ----------Commented to keep testing output clean----------
    # print(RA_decimal_to_HMS(180.7720833)) # Exp: 12h 3m 5.3s, working
    # print(DEC_decimal_to_DMS(-13.75651389)) # Exp: –13deg 45’ 23.45”, working
    # original_vec = np.array([-0.23, 0.877, 0.34])
    # print(rotate_vec(original_vec, 120, "x")) # Exp: [-0.23,  -0.73294864, 0.58950428], working
    # print(rotate_vec(original_vec, 45, "y")) # Exp: [0.07778175,  0.877, 0.40305087], working
    # print(rotate_vec(original_vec, 70, "z")) # Exp: [-0.90277506,  0.08382236,  0.34], working
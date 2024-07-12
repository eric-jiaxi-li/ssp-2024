"""
Photometry

Move over to odlib.py when done

Eric Li
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from math import *
import odlib
from statistics import stdev

debug = False

print("----------1. Aperture Photometry----------")

S, sigma_S, SNR, m_inst, sigma_m_inst = odlib.photometry("inputs/aptest.fit", 490, 293, 5, 8, 13, 11, 10, 1)
print("Signal: {} +/- {} (ADU)".format(S, sigma_S))
print("Signal-to-noise ratio: {}".format(SNR))
print("Instrumental magnitude: {} +/- {}".format(m_inst, sigma_m_inst))
print()
print()
print()

print("----------2. Differential Photometry----------")

C, m_catalog, dm, sigma_m_catalog = odlib.diff_photometry("inputs/diff_phot.fit", "inputs/stars_test.txt", 546, 327)
print("Avg offset between catalog/instrumental magnitudes", C)
print("Systematic uncertainty dm", dm)
print("Catalog magnitude: {} +/- {}".format(m_catalog, sigma_m_catalog))























######################################################
#
#               OLD DRAFTS OF FUNCTIONS
#
######################################################


# def photometry(fits_file, target_x, target_y, 
#                radius, annulus_inner, annulus_outer, 
#                read_noise, dark_current, gain, 
#                show_centroid = True):
#     """
#     Params: Filepath to image, approximate x/y of object, 
#             radius of aperture, annulus inner/outer radii (px)
#             Read noise, dark current in e-, and gain
#             show_centroid if you want to print the centroid too
#     Return: Total signal S and uncertainty in ADU
#             Signal-to-noise ratio (SNR)
#             Instrumental magnitude m_inst = -2.5 log10(S)
#             Uncertainty on instrumental magnitude,
#             sigma_m_inst = 1.0875/SNR
#     """

#     # Reposition target_x, target_y to centroid
#     # sigma_x, sigma_y not needed
#     target_x, target_y, sigma_x, sigma_y = odlib.find_centroid2(fits_file, target_x, target_y, radius, annulus_inner, annulus_outer, "median")
#     if show_centroid == True:
#         print("Centroid = ({}, {})".format(target_x, target_y))

#     # # Maybe round these???
#     # target_x = round(target_x)
#     # target_y = round(target_y)

#     # # Do we have to swap the x and y again? No clue!
#     temp = target_x
#     target_x = target_y
#     target_y = temp

#     img = fits.getdata(fits_file)
#     m = img.shape[0] # 1024
#     n = img.shape[1] # 1024
#     # if debug == True:
#     #     print(m, n)

#     # Determine median sky brightness
#     # https://stackoverflow.com/a/8650741
#     x, y = np.ogrid[-target_x:m-target_x, -target_y:n-target_y]
#     annulus_mask = np.logical_and(annulus_inner**2 < x**2 + y**2, x**2 + y**2 < annulus_outer**2)
#     sky_brightness = np.median(img[annulus_mask])

#     # if debug == True:
#     #     print(sky_brightness)
#     #     print(np.sum(annulus_mask)) # number of px in annulus
#     #     # img[annulus_mask] = 99999
#     #     plt.gray()
#     #     plt.imshow(img, vmin = 1105.1480, vmax = 1452.2652, origin = "lower")
#     #     plt.show()

#     # Find total signal
#     aperture_mask = x**2 + y**2 < radius**2
#     S = np.sum(img[aperture_mask]) - np.sum(aperture_mask) * sky_brightness
#     m_inst = -2.5 * log10(S)

#     # if debug == True:
#     #     print("radius of aperture", radius)
#     #     print("num in aperture", np.sum(aperture_mask))
#     #     print("sky brightness", sky_brightness)
#     #     print("aperture brightness", np.median(img[aperture_mask]))

#     # SNR
#     S_e = S
#     n_ap = np.sum(aperture_mask)
#     n_an = np.sum(annulus_mask)
#     sky_e = sky_brightness
#     D_e = dark_current
#     p2 = read_noise ** 2 + gain ** 2 / 12

#     SNR = sqrt(S_e) / sqrt(1 + n_ap * (1 + n_ap/n_an) * ((sky_e + D_e + p2) / (S_e)))
#     sigma_m_inst = 1.0875 / SNR
#     sigma_S = S / SNR # Noise is the error

#     return S, sigma_S, SNR, m_inst, sigma_m_inst

# # Check find_centroid2 just to be safe
# # Expected output: (489.18, 292.20)
# # Output: (489.16337125187937, 292.169271793708)
# # print(odlib.find_centroid2("inputs/aptest.fit", 490, 293, 5, 8, 13, "median"))

# def diff_photometry(fits_file, ref_stars_txt, ast_x, ast_y):
#     """
#     Params: Image file, text file containing approximate
#             x, y, and catalog magnitude for some reference
#             stars, and x and y coordinates of an asteroid
#             we want to find the magnitude for.
#             When performing photometry, we will use the
#             parameters given in the previous section's
#             testcase.
#     Return: Average offset between catalog/instrumental
#             magnitudes C, dm (systematic uncertainty),
#             and catalog magnitude with uncertainty.
#     """

#     # Read input
#     img = fits.getdata(fits_file)
#     fin = open(ref_stars_txt)

#     star_x = []
#     star_y = []
#     star_mag = []
#     for line in fin.readlines():
#         line = line.strip()
#         x, y, mag = map(float, line.split())
#         star_x.append(x)
#         star_y.append(y)
#         star_mag.append(mag)
#         # if debug == True:
#         #     print(star_x, star_y, star_mag)



#     n = len(star_x) # Number of stars
#     C = 0 # Average of m_catalog - m_instrumental for the reference stars
#     m_inst_all = [] # List of all the instrumental magnitudes; to be used to calculate dm (systematic uncertainty)

#     for i in range(n):
#         S, sigma_S, SNR, m_inst, sigma_m_inst = photometry(fits_file, star_x[i], star_y[i], 5, 8, 13, 11, 10, 1, show_centroid = False)
#         C += abs(m_inst - star_mag[i])
#         m_inst_all.append(m_inst)
        
#     C /= n
#     dm = stdev(m_inst_all) # Systematic uncertainty

#     # Calculate values for our asteroid
#     S, sigma_S, SNR, m_inst, sigma_m_inst = photometry(fits_file, ast_x, ast_y, 5, 8, 13, 11, 10, 1, show_centroid = False)
#     m_catalog = m_inst + C
#     sigma_m_catalog = sqrt(dm ** 2 + sigma_m_inst ** 2) # Uncertainty in catalog magnitude of asteroid

#     return C, m_catalog, dm, sigma_m_catalog
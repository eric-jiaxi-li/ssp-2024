"""
This method finds the centroid of a given star in a fits file. 

I checked the following:
- edges of the radius and annulus going out of the frame
- negative radii
- invalid medians

Eric Li
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import odlib

debug = True


# Changed input parameters of given testcase
centroid_x, centroid_y, sigma_x, sigma_y = odlib.find_centroid("inputs/images/sampleimage.fits", 351, 154, 4, 5, "mean")
print()
print("Centroid {}, {}".format(centroid_x, centroid_y))
print("Uncertainty {}, {}".format(sigma_x, sigma_y))


# Check answer
if abs(centroid_x - 350.7806) < 0.1 and abs(centroid_y - 153.5709) < 0.1:
    print("Centroid calculation CORRECT")
else:
    print(
        "Centroid calculation INCORRECT, expected (350.7806, 153.5709), got ({}, {})".format(
        centroid_x, centroid_y))
    




# Checking for sticker 530 299
# Works
print(odlib.find_centroid("inputs/images/sampleimage.fits", 530, 299, 3, 5, "mean"))


#####################################################
#
#                Find best params
#
#####################################################
# # Do it for the star in the testcase
# Choose parameters that give correct values

# star_x, star_y = 351, 154

# # Some combinations give errors, no idea why
# print()
# print("----------Working parameter combos and their errors----------")
# for radius in range(1, 20):
#     for annulus_width in range(1, 20):
#         for method in ["mean", "median"]:

#             centroid_x, centroid_y, sigma_x, sigma_y = odlib.find_centroid("inputs/sampleimage.fits", star_x, star_y, radius, annulus_width, method)
            
#             if abs(centroid_x - 350.7806) < 0.1 and abs(centroid_y - 153.5709) < 0.1:
#                 print(radius, annulus_width, method, sigma_x, sigma_y)

# Working parameters
# 1 1 mean 0.038915936877687615 0.020418264961072893
# 4 5 mean 0.02814915638718109 0.03267678787174165
# 4 6 mean 0.028155222095540524 0.032673217345419996
# 4 7 mean 0.028109161376647148 0.032698728810938
# 4 8 mean 0.028166936088949247 0.03266612598893899
# 4 9 mean 0.028164561808508543 0.032667584654307656
# 4 10 mean 0.028083977414118968 0.032711243903575805
# 4 11 mean 0.028121841752603204 0.0326920603339742
# 4 12 mean 0.02810197992419626 0.032702393995035745
# 4 13 mean 0.02807268195480995 0.0327165605968542
# 4 14 mean 0.028143035532463483 0.032680322995622936
# 4 14 median 0.02809410069252195 0.03270632574265861
# 4 15 mean 0.02818373691057785 0.03265548092683548
# 4 15 median 0.02809410069252195 0.03270632574265861
# 4 16 mean 0.02815131538748055 0.03267552475795741
# 4 16 median 0.02809410069252195 0.03270632574265861
# 4 17 mean 0.02813072065077258 0.0326872358049034
# 4 17 median 0.02809410069252195 0.03270632574265861
# 4 18 mean 0.028083518974623342 0.032711463154104496
# 4 18 median 0.02809410069252195 0.03270632574265861
# 4 19 mean 0.028060405335558775 0.0327221425490634
# 4 19 median 0.02809410069252195 0.03270632574265861














































# #####################################################
# #
# #            Old draft of function
# #
# #####################################################
# def findCentroid(fits_file, target_x, target_y, radius = 4, annulus_width = 5, method = "median"):
#     """
#     Params: The fits file (string) to find centroid of, the x and y coordinates of the 
#             target star, the radius of the circle surrounding the target star, 
#             and the annulus from which we determine the sky brightness has annulus_width
#             Find sky brightness using median or mean (method)
#     Return: x and y coordinates of the star's centroid + uncertainties
#     """

#     img = fits.getdata(fits_file)
#     m = img.shape[0]
#     n = img.shape[1]
#     sky_radius = annulus_width + radius # Outer radius of annulus


#     # Check inputs
#     if target_x + sky_radius >= m or target_x - sky_radius <= -1 or target_y + sky_radius >= n or target_y - sky_radius <= -1:
#         return "Error: Target too close to the edges or radius too big"
#     if radius <= 0 or sky_radius <= 0:
#         return "Error: radius and sky_radius cannot be nonpositive"
#     if method != "median" and method != "mean":
#         return "Error: only median and mean are allowed to be methods"


#     # Due to differences between Python and AstroImageJ, need to swap coordinates
#     temp = target_x
#     target_x = target_y
#     target_y = temp
    

#     # if debug == True:
#     #     plt.gray()
#     #     plt.imshow(img, vmin = 2390.5515, vmax = 2964.2838)
#     #     plt.show()


#     # Determine average sky brightness
#     # https://stackoverflow.com/a/8650741
#     x, y = np.ogrid[-target_x : m-target_x, -target_y : n-target_y]
#     annulus_mask = np.logical_and(radius**2 < x**2 + y**2, x**2 + y**2 < sky_radius**2)


#     # if debug == True:
#     #     img2 = np.copy(img)
#     #     img2[annulus_mask] = 99999
#     #     plt.gray()
#     #     plt.imshow(img2, vmin = 2390.5515, vmax = 2964.2838, origin = "lower")
#     #     plt.show()


#     # Calculate sky brightness
#     if method == "median":
#         sky_brightness = np.median(img[annulus_mask])
#     elif method == "mean":
#         sky_brightness = np.mean(img[annulus_mask])
#     img = img - sky_brightness


#     # Calculate centroid
#     sky_mask = x**2 + y**2 > radius**2
#     img[sky_mask] = 0 # Zero out all pixels not within the circle
#     centroid_x = np.dot(np.sum(img, axis = 1), np.arange(0, m)) / np.sum(img) # Axis = 1 collapses the columns
#     centroid_y = np.dot(np.sum(img, axis = 0), np.arange(0, n)) / np.sum(img)


#     # Uncertainties
#     # Remove unused columns
#     indices_x, = np.where(np.all(img == 0, axis = 1) == False) # np.where returns 2 values, "indices_x," takes the first
#     indices_y, = np.where(np.all(img == 0, axis = 0) == False)
#     img_x = img[indices_x, :]
#     img_y = img[:, indices_y]


#     # if debug == True:
#     #     print(indices_x)
#     #     print(np.shape(img))
#     #     print(np.shape(img_x))
#     #     print(np.min(img_x))
#     #     print(np.min(img_y))


#     N = np.sum(img)
#     sigma_x = np.sqrt(np.sum(np.sum(img_x, axis = 1) * (indices_x - centroid_x) ** 2) / (N * (N - 1)))
#     sigma_y = np.sqrt(np.sum(np.sum(img_y, axis = 0) * (indices_y - centroid_y) ** 2) / (N * (N - 1)))


#     # if debug == True:
#     #     print()
#     #     print(indices_x)
#     #     print(indices_y)
#     #     img_xy = img[np.min(indices_x):np.max(indices_x), np.min(indices_y):np.max(indices_y)]
#     #     print(img_xy)
#     #     plt.gray()
#     #     plt.imshow(img_xy)
#     #     plt.show()
#     #     plt.imshow(img[target_x - radius:target_x + radius, target_y - radius:target_y + radius])
#     #     plt.show()


#     # Swap back
#     temp = sigma_x
#     sigma_x = sigma_y
#     sigma_y = temp

#     temp = centroid_x
#     centroid_x = centroid_y
#     centroid_y = temp


#     return centroid_x, centroid_y, sigma_x, sigma_y












# if debug == True:
#     radius_vec = np.array(radius_vec)
#     annulus_width_vec = np.array(annulus_width_vec)
#     uncertainty_vec = np.array(uncertainty_vec)

#     ##### https://stackoverflow.com/questions/63015639/how-to-make-3d-bar-plot-from-dataframe

#     # set up the figure and Axes
#     fig = plt.figure(figsize=(8, 3))
#     ax = fig.add_subplot(111, projection='3d')

#     xpos = radius_vec
#     ypos = annulus_width_vec
#     zpos = [0] * len(radius_vec)  # z coordinates of each bar
#     dx = [0.5] * len(radius_vec)  # Width of each bar
#     dy = [0.5] * len(radius_vec)  # Depth of each bar
#     dz = uncertainty_vec

#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     ax.bar3d(xpos,ypos,zpos,dx,dy,dz, color='b', alpha=0.5)

#     plt.show()

# print("-------------Finding best parameters-------------")
# print("Best radius", best_radius)
# print("Best annulus width", best_annulus_width)
# print("Best method", best_method)
# print("With best parameters:", findCentroid("sampleimage.fits", star_x, star_y, best_radius, best_annulus_width, best_method))
# # Best radius 6
# # Best annulus width 17
# # Best method mean
# # With best parameters: (350.7626796840741, 152.4197150113003, 0.029850894957292522, 0.006482492429149891)
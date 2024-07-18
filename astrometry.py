"""
Least Squares Plate Reduction code

LCO elp0m414... in inputs folder

To get RA/DEC/centroids of reference stars, open image in DS9, create a region,
go to region -> centroid

Alternatively, just double click and switch fk5 and image

Eric Li

DONE
"""
import numpy as np
import matplotlib.pyplot as plt
import odlib

debug = True



# b1, b2, a11, a12, a21, a22, sigma_RA, sigma_DEC, RA, DEC = odlib.lspr("inputs/lspr_test.txt", 484.35, 382.62, True)
# print()
# print("----------LSPR RESULTS, TEST INPUT----------")
# print("Plate constants b1 {} b2 {} a11 {} a12 {} a21 {} a22 {} ".format(b1, b2, a11, a12, a21, a22))
# print("Uncertainties RA {} DEC {}".format(sigma_RA, sigma_DEC))
# print("RA {} DEC {}".format(RA, DEC))

# 06/27 LCO
b1, b2, a11, a12, a21, a22, sigma_RA, sigma_DEC, RA, DEC = odlib.lspr("inputs/LCO_0627_input.txt", 1235.5, 1168.5, True)
print()
print("----------LCO LSPR 06/27----------")
print("Plate constants b1 {} b2 {} a11 {} a12 {} a21 {} a22 {} ".format(b1, b2, a11, a12, a21, a22))
print("Uncertainties RA {} DEC {}".format(sigma_RA, sigma_DEC))
print("RA {} DEC {}".format(RA, DEC))

# ----------LSPR RESULTS----------
# Plate constants b1 270.99132794536087 b2 12.280544103025175 a11 -0.00021158175938146845 a12 7.054114007916581e-07 a21 6.164485238040858e-07 a22 0.00020662850034496415
# Uncertainties RA 0.0141631310323522 DEC 0.30669045765817193
# RA 18.0 hours 2.0 minutes 55.378309 seconds  DEC 12 degrees 31 arcminutes 21.90406 arcseconds

print()
print()
print()



# 07/10 LCO
b1, b2, a11, a12, a21, a22, sigma_RA, sigma_DEC, RA, DEC = odlib.lspr("inputs/LCO_0710_input.txt", 1235, 1193, True)
print()
print("----------LCO LSPR 07/10----------")
print("Plate constants b1 {} b2 {} a11 {} a12 {} a21 {} a22 {} ".format(b1, b2, a11, a12, a21, a22))
print("Uncertainties RA {} DEC {}".format(sigma_RA, sigma_DEC))
print("RA {} DEC {}".format(RA, DEC))

# Plate constants b1 276.83550283573186 b2 8.602538271696794 a11 -0.00020906207401316646 a12 4.996067777501967e-07 a21 4.960822802029037e-07 a22 0.00020657066650725745
# Uncertainties RA 0.002782904700978816 DEC 0.0018046091182027507
# RA 18.0 hours 26.0 minutes 18.697729 seconds  DEC 8 degrees 50 arcminutes 58.523058 arcseconds



# 07/17 LCO
b1, b2, a11, a12, a21, a22, sigma_RA, sigma_DEC, RA, DEC = odlib.lspr("inputs/LCO_0717_input.txt", 1231.4669, 1163.0577, True)
print()
print("----------LCO LSPR 07/17----------")
print("Plate constants b1 {} b2 {} a11 {} a12 {} a21 {} a22 {} ".format(b1, b2, a11, a12, a21, a22))
print("Uncertainties RA {} DEC {}".format(sigma_RA, sigma_DEC))
print("RA {} DEC {}".format(RA, DEC))

# Plate constants b1 281.51393849745233 b2 4.602519791722948 a11 -0.00020727770904776773 a12 2.507673279338907e-06 a21 2.497257110149144e-06 a22 0.00020653158246224156       
# Uncertainties RA 0.0038768302232221144 DEC 0.00626199644260542
# RA 18.0 hours 45.0 minutes 2.783863 seconds  DEC 4 degrees 50 arcminutes 44.891622 arcseconds



































#####################################################################
#
#
#             Old code for generating the 10 reference stars
#
#
#####################################################################
# """
# Order: 9 1 8 3 10 2 7 6 5
# """

# ########################################
# #
# #        Write data to input file
# #
# ########################################

# # No idea why the relative path doesn't work here
# filename = "C:\\Users\\user\\Desktop\\ssp-2024\\inputs\\elp0m414-sq31-20240627-0152-e91.fits.fz"




# ############################
# #  Calculate best params
# ############################


# # Asteroid
# ast_x = 1235.6 
# ast_y = 1168.6 
# ast_r, ast_annw, ast_method = odlib.find_centroid_chooseparams(filename, ast_x, ast_y)

# # Theese reference stars are ordered by center x from left to right in the image
# # These are the coordinates on the IMAGE, not the centroids
# # Manually-found radii/annulus widths: 
# #   ref_r = np.array([5, 2, 4, 1, 3, 2, 4, 2, 2])
# #   ref_skyr = np.array([10, 5, 10, 4, 7, 7, 8, 6, 6])
# ref_x = np.array([1117, 1154, 1171, 1179, 1221, 1261, 1320, 1323, 1335])
# ref_y = np.array([1316, 1103, 1243, 1174, 1315, 1086, 1241, 1280, 1250])
# ref_nstars = len(ref_x)

# # if debug == True:
# #     plt.scatter(ref_x, ref_y)
# #     plt.show()



# # Select parameters for minimizing sigmas added in quadrature
# ref_r = []
# ref_annw = []
# ref_method = []

# for i in range(ref_nstars):
#     print("Checking star", i + 1)
#     r, annw, method = odlib.find_centroid_chooseparams(filename, ref_x[i], ref_y[i])
#     ref_r.append(r)
#     ref_annw.append(annw)
#     ref_method.append(method)

# ref_r = np.array(ref_r)
# ref_annw = np.array(ref_annw)
# ref_method = np.array(ref_method)




# ############################
# #   Calculate centroids
# ############################

# # Asteroid
# ast_cx, ast_cy, ast_sigma_x, ast_sigma_y = odlib.find_centroid(filename, ast_x, ast_y, ast_r, ast_annw, ast_method)

# # Reference stars
# ref_cx = []
# ref_cy = []
# for i in range(ref_nstars):
#     cx, cy, sigma_x, sigma_y = odlib.find_centroid(filename, ref_x[i], ref_y[i], ref_r[i], ref_annw[i], ref_method[i])
#     ref_cx.append(cx)
#     ref_cy.append(cy)

# if debug == True: 
#     print("reference centroids x", ref_cx)
#     print("reference centroids y", ref_cy)




# # Reorder the RA/DECs of the reference stars to be left-to-right
# # See top of this code
# # 9 1 8 3 10 2 7 6 5
# ref_RA = [270.7558597, 270.7479374, 270.7442639, 270.7425832, 270.7337224, 
#           270.7251807, 270.7129667, 270.7122767, 270.7095747]
# ref_DEC = [12.5531397, 12.5093181, 12.5382597, 12.5240542, 12.5530958,
#            12.5059753, 12.5379383, 12.5460864, 12.5399611]

# fout = open("inputs\\LSPRinputLi.txt", "w")
# for i in range(ref_nstars):
#     fout.write(str(ref_cx[i]) + " " + str(ref_cy[i]) + " " + str(ref_RA[i]) + " " + str(ref_DEC[i]))
#     fout.write("\n")
# fout.close()

######################################################
#
#               Figure out how the order
#              in DS9 corresponds to the order
#               of the stars from left to right
#
######################################################

"""
Order: 9 1 8 3 10 2 7 6 5
"""

# going in order left to right
# 1 # Index in going left to right
# print(odlib.HMS_to_deg(18, 3, 1.45))
# print(odlib.DMS_to_deg(12, 33, 10.6))
# 270.7560416666667 # output
# 12.552944444444446 # output
# 9 # index in DS9

# 2
# print(odlib.HMS_to_deg(18, 2, 59))
# print(odlib.DMS_to_deg(12, 30, 33))
# 270.7458333333334
# 12.509166666666667
# 1

# 3
# print(odlib.HMS_to_deg(18, 2, 59))
# print(odlib.DMS_to_deg(12, 32, 17.2))
# 270.7458333333334
# 12.53811111111111
# 8

# 4
# print(odlib.HMS_to_deg(18, 2, 58.1))
# print(odlib.DMS_to_deg(12, 31, 24))
# 270.74208333333337
# 12.523333333333333
# 3

# 5
# print(odlib.HMS_to_deg(18, 2, 56))
# print(odlib.DMS_to_deg(12, 33, 11.8))
# 270.73333333333335
# 12.553277777777778
# 10

# 6
# print(odlib.HMS_to_deg(18, 2, 54))
# print(odlib.DMS_to_deg(12, 30, 20.6))
# 270.725
# 12.505722222222222
# 2

# 7
# print(odlib.HMS_to_deg(18, 2, 51.1406))
# print(odlib.DMS_to_deg(12, 32, 15.846))
# 270.71308583333337
# 12.537735
# 7

# 8
# print(odlib.HMS_to_deg(18, 2, 51))
# print(odlib.DMS_to_deg(12, 32, 46.189))
# 270.71250000000003
# 12.54616361111111
# 6

# 9
# print(odlib.HMS_to_deg(18, 2, 50.35))
# print(odlib.DMS_to_deg(12, 32, 24.8))
# 270.7097916666667
# 12.540222222222223
# 5
# https://canvas.instructure.com/courses/9410180/assignments/48000863?module_item_id=112668832


# Suppress FutureWarning for delim_whitespace = True
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



"""
https://voyages.sdss.org/expeditions/expedition-to-the-milky-way/star-clusters/hr-diagrams/
Create color-magnitude diagram for radii 1-5, M67 cluster
Center is the center provided by searching "M67" in SKyServer

SELECT TOP 500000 p.objid, p.ra, p.dec, p.u, p.g,p.r,p.i,p.z,
   p.Err_u, p.Err_g, p.Err_r,p.Err_i,p.Err_z
   FROM fGetNearbyObjEq(132.84545,11.81371,3) n, PhotoPrimary p
   WHERE n.objID=p.objID and p.type=6
"""
# for i in range(1, 6):
#    data = pd.read_csv("sdss_project/csv_files_M67/radius{}.csv".format(i))

#    # Apparent magnitude on y, color on x
#    x = data["g"] - data["r"]
#    y = data["r"] 
   
#    # Create plot
#    plt.scatter(x, y, s = 10)
#    plt.xlabel("g - r")
#    plt.ylabel("r")
#    plt.title("Color-magnitude diagram, radius {} around M67 cluster".format(i))
#    plt.xlim(-4, 6)
#    plt.ylim(25, 10) # Reverse y-axis

#    # plt.show()
#    plt.savefig("sdss_project/plots_M67/radius{}.png".format(i))


"""
Work with radius 5 only for now
https://voyages.sdss.org/expeditions/expedition-to-the-milky-way/star-clusters/distance-modulus/
Producing isochrome: metallicity and age
METALLICITY: https://arxiv.org/abs/1310.6297 Based on theoretical models the diffusion-corrected 
initial metallicity of M67 is estimated to be [Fe/H] = +0.06.
AGE: "Generating an Isochrone" says 2e8 years
"""
# # Try plotting the sample isochrome
# x = iso["LogL/Lo"]
# y = iso["LogTeff"]
# plt.scatter(x, y, s = 10)
# plt.xlabel("LogL/Lo")
# plt.ylabel("LogTeff")
# plt.title("Isochrone plotted as HR diagram using luminosity and temperature")
# plt.show()

# Superimpose Isochrone and Color-magnitude diagram (CMD)
iso = pd.read_table("sdss_project/isochrones_M67/isochrone_0.2.txt", delim_whitespace = True, skiprows = 8)
iso_x = iso["sdss_g"] - iso["sdss_r"]
iso_y = iso["sdss_r"]
plt.plot(iso_x, iso_y, "r.")

data = pd.read_csv("sdss_project/csv_files_M67/radius5.csv")
csv_x = data["g"] - data["r"]
csv_y = data["r"]
plt.plot(csv_x, csv_y, "b.")

plt.xlabel("g - r")
plt.ylabel("r")
plt.title("Isochrone (0.2 Gy) CMD Comparison")
plt.xlim(-3, 5)
plt.gca().invert_yaxis()
plt.show()

mu = 15 # Distance modulus to convert to abs. mag



"""
Try to match isochrone to scatterplot
"""
# https://www.google.com/search?q=m67+cluster+age&oq=m67+cluster+age&gs_lcrp=EgZjaHJvbWUyCggAEEUYFhgeGDkyDQgBEAAYhgMYgAQYigUyDQgCEAAYhgMYgAQYigUyDQgDEAAYhgMYgAQYigUyCggEEAAYgAQYogQyCggFEAAYgAQYogQyBggGEEUYPNIBCDE2MjFqMGoxqAIAsAIA&sourceid=chrome&ie=UTF-8
iso = pd.read_table("sdss_project/isochrones_M67/isochrone_4.0.txt", delim_whitespace = True, skiprows = 8)
iso_x = iso["sdss_g"] - iso["sdss_r"]
iso_y = iso["sdss_r"]
plt.plot(iso_x, iso_y, "r.")

data = pd.read_csv("sdss_project/csv_files_M67/radius5.csv")
csv_x = data["g"] - data["r"]
csv_y = data["r"] - mu
plt.plot(csv_x, csv_y, "b.")

plt.xlabel("g - r")
plt.ylabel("r")
plt.title("Isochrone (4.0 Gy) CMD Comparison")
plt.xlim(-3, 5)
plt.gca().invert_yaxis()
plt.show()
# https://canvas.instructure.com/courses/9410180/assignments/48000863?module_item_id=112668832

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
for i in range(1, 6):
   data = pd.read_csv("sdss_project/csv_files_M67/radius{}.csv".format(i))

   # Apparent magnitude on y, color on x
   x = data["g"] - data["r"]
   y = data["r"] 
   
   # Create plot
   plt.scatter(x, y, s = 10)
   plt.xlabel("g - r")
   plt.ylabel("r")
   plt.title("Color-magnitude diagram, radius {} around M67 cluster".format(i))
   plt.xlim(-4, 6)
   plt.ylim(25, 10) # Reverse y-axis

   # plt.show()
   plt.savefig("sdss_project/plots_M67/radius{}.png".format(i))
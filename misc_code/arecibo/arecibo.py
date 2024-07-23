"""
https://canvas.instructure.com/courses/9410180/assignments/48125346
"""
import numpy as np
import matplotlib.pyplot as plt


# # Read inputs
# fin = open("misc_code/arecibo/arecibo.txt")
# message = fin.readline()
# message_num = int(message)
# print(int(str(message_num), 2))
# message = np.float64(np.array(list(message)))
# n = len(message) # 1679


# # # Determine dimensions of image (1679 is semiprime) -> 23 73 or 73 23
# # for x in range(1,n):
# #     if 1679 % x == 0:
# #         print("Possible dimensions: ", x, n // x)
# message = np.reshape(message, (73, 23))
# plt.imshow(message)
# plt.gray()
# plt.show()





# Eric's message, using the one with prime dimensions
fin = open("misc_code/arecibo/arecibo_Eric2.txt")
message = fin.readline()
message = np.float64(np.array(list(message)))
message = np.reshape(message, (547, 809))
plt.imshow(message)
plt.gray()
plt.show()
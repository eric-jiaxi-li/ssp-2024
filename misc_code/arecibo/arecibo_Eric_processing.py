"""
Reformat it to have prime dimensions
"""

fin = open("misc_code/arecibo/arecibo_Eric1.txt")
fout = open("misc_code/arecibo/arecibo_Eric2.txt", "w")

for line in fin.readlines():
    line_changed = line.strip() + "111111111" # Change length from 800 to 809 to make it prime
    fout.write(line_changed)
fout.close()

# Check the file
fin = open("misc_code/arecibo/arecibo_Eric2.txt")
line = fin.readline()
print(len(line))
print(547 * 809)



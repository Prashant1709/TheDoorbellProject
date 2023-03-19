# Python program to explain os.mkdir() method

# importing os module
import os

# Directory
directory = "Death"

# Parent Directory path
parent_dir = "dataset/"

# Path
path = os.path.join(parent_dir, directory)

# Create the directory
# 'GeeksForGeeks' in
# '/home / User / Documents'
os.mkdir(path)
print("Directory '% s' created" % directory)

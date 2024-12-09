import os
import robotic as ry

# Set the working directory to the location of the config file
os.chdir("/home/yagz/rai_venv/robotics/PROJECT")

C = ry.Config()
C.addFile("Penvironment.g")  # Use a relative path now
C.view()

input("asda")

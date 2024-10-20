import numpy as np
import robotic as ry
import os

# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':0'

C = ry.Config()

C.addFile(ry.raiPath("../rai-robotModels/objects/kitchen.g"))

#tray
tray = C.addFrame(name="tray", parent="table1")
tray.setShape(ry.ST.ssBox, size= [0.4, 0.4, 0.05, 0.02])\
    .setColor([0.0,1.0, 0.0])\
    .setMass(.1) \
    .setContact(True) \
    .setRelativePosition([0.0, 0.0, 0.42]).setQuaternion([np.sin(np.radians(45) / 2), 0, 0, np.cos(np.radians(45) / 2)])

#handle
handle = C.addFrame(name="handle", parent="tray") 
handle.setShape(ry.ST.ssBox, size= [0.3, 0.05, 0.03, 0.005]) \
    .setColor([0.65, 0.50, 0.39]) \
    .setMass(.1) \
    .setContact(True) \
    .setRelativePosition([0.0, -0.1, 0.04])

#head
head = C.addFrame(name="head", parent="handle")
head.setShape(ry.ST.ssBox, size=  [0.1, 0.05, 0.03, 0.005]) \
    .setColor( [0.55, 0.57, 0.58]) \
    .setMass(.1) \
    .setContact(True) \
    .setRelativePosition( [0.125, 0.0, 0.0]).setQuaternion([22, 0, 0, 9])

#mug
mug = C.addFrame(name="mug", parent="tray")
mug.setShape(ry.ST.ssBox, size=[0.05, 0.05, 0.2, .01])\
   .setColor( [0.2, 0.2, 0.2]) \
   .setMass(.1) \
   .setContact(True) \
   .setRelativePosition( [0.1, 0.1, 0.12])

C.view()

# Prevent the script from exiting immediately
input("Press Enter to exit...")

# Get the pose of the hammer's handle in the World frame
handle_position = handle.getPosition()
handle_orientation = handle.getQuaternion()
# Print the results
print("Handle Position (World Frame):", handle_position)
print("Handle Orientation (World Frame):", handle_orientation)

# Get the world pose of mug and sink1
mug_position_world = mug.getPosition()
mug_orientation_world = mug.getQuaternion()

sink1 = C.getFrame("sink1")
sink1_position_world = sink1.getPosition()
sink1_orientation_world = sink1.getQuaternion()

# Function to invert a pose
def invert_pose(position, quaternion):
    # Inverting a quaternion (rotation)
    q_inv = np.array([quaternion[0], -quaternion[1], -quaternion[2], -quaternion[3]])
    
    # Inverting the translation with the inverted rotation
    p_inv = -np.array(position)
    p_inv = rotate_vector(p_inv, q_inv)
    
    return p_inv, q_inv

# Helper function to rotate a vector using a quaternion
def rotate_vector(vector, quaternion):
    q = quaternion
    t = 2 * np.cross(q[1:], vector)
    rotated_vector = vector + q[0] * t + np.cross(q[1:], t)
    return rotated_vector

# Invert sink1's pose to transform to its local frame
sink1_position_inv, sink1_orientation_inv = invert_pose(sink1_position_world, sink1_orientation_world)

# Apply the inverted sink1 transformation to the mug's world pose
mug_relative_position = rotate_vector(mug_position_world - sink1_position_world, sink1_orientation_inv)
mug_relative_orientation = mug_orientation_world * sink1_orientation_inv

# Print the results
print("Relative Position of Mug with respect to Sink1:", mug_relative_position)
print("Relative Orientation of Mug with respect to Sink1:", mug_relative_orientation)

import numpy as np
import robotic as ry
import os

# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':0'

K = ry.Config()
K.addFile("Works/two_link_manipulator.g")

target = K.addFrame("target")

joint_angles = 2 * np.pi * np.random.rand(3)

def forward_kinematics(q):
    q0 = q[0]
    q1 = q[1]
    y = np.sin(q0) + np.sin(q0 + q1)
    z = np.cos(q0) + np.cos(q0 + q1)
    return np.array([0, y, z])

pos_target = forward_kinematics(joint_angles)

target.setPosition(pos_target) # Set the target position in this line 
K.setJointState(joint_angles) # Set the joint angles in this line
K.view()

# Restart the joint configuration for next run
q = np.zeros(K.getJointDimension())
K.setJointState(q)
target.setPosition([0, 0, 0])

# Prevent the script from exiting immediately
input("Press Enter to exit...")

def Jacobian(q):
    q0, q1 = q[0], q[1]
    J = np.array([[np.cos(q0) + np.cos(q0 + q1), np.cos(q0 + q1)],
                  [-np.sin(q0) - np.sin(q0 + q1), -np.sin(q0 + q1)]])
    return J

joint_angles = [1.95205226, 3.15753276, 0] 
J= Jacobian(joint_angles) 
print(J)
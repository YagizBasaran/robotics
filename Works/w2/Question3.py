import time
import robotic as ry
import os
import numpy as np

# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':0'

# Initialize the configuration
C = ry.Config()
C.addFile("/home/yagz/rai_venv/robotics/Question-01/mini_golf.g")

C.view()

# Define frame names for the tool, ball, and gripper
tool_frame = "hammer-handle"  # Modify according to the actual frame name
ball_frame = "ball"  # Modify according to the actual frame name
gripper_frame = "l_gripper"  # Modify according to your configuration

# Step 1: Grasp the tool with the gripper
komo_grasp_tool = ry.KOMO(C, 1, 1, 0, True)

# Define objective for aligning gripper with tool handle
komo_grasp_tool.addObjective([], ry.FS.positionDiff, [gripper_frame, tool_frame], ry.OT.eq, [1e1])
komo_grasp_tool.addObjective([], ry.FS.quaternionDiff, [gripper_frame, tool_frame], ry.OT.eq, [1e1])

# Solve for grasp
ret = ry.NLP_Solver(komo_grasp_tool.nlp(), verbose=0).solve()
q_grasp = komo_grasp_tool.getPath()[-1]

# Execute grasp by setting joint state
C.setJointState(q_grasp)
C.attach(gripper_frame, tool_frame)  # Attach tool to gripper
C.view(False, "Grasping tool")
time.sleep(1)

# Step 2: Set up a single KOMO sequence to keep the tool aligned behind the ball and push forward
alignment_distance = 0.15  # Distance behind the ball for alignment
push_distance = 0.3  # Distance to move forward for pushing the ball

# Create a single KOMO instance to align and push
komo_align_and_push = ry.KOMO(C, 3, 40, 2, True)  # Longer duration and more steps for smooth motion

# Define an objective to always keep the tool at a specified distance behind the ball
for t in np.linspace(0.1, 1.0, 10):  # Spread objectives over time to enforce alignment
    komo_align_and_push.addObjective([t], ry.FS.positionDiff, [tool_frame, ball_frame], ry.OT.eq, [-alignment_distance, 0, 0])

# Define the forward push motion
komo_align_and_push.addObjective([1.0], ry.FS.positionDiff, [tool_frame, ball_frame], ry.OT.eq, [push_distance - alignment_distance, 0, 0])

# Solve for the alignment and push sequence
ret = ry.NLP_Solver(komo_align_and_push.nlp(), verbose=0).solve()
path_to_push = komo_align_and_push.getPath()

# Execute the alignment and push sequence
for q in path_to_push:
    C.setJointState(q)
    C.view(False, "Pushing the ball")
    time.sleep(0.1)

# Final cleanup and close
C.view()

# Prevent the script from exiting immediately
input("Press Enter to exit...")

import robotic as ry
import time
import os
import random

# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':0'

# Initialize the configuration
C = ry.Config()
C.addFile("/home/yagz/rai_venv/robotics/Question-01/book_shelf.g")

objects = ["book1", "book2", "book3", "book4", "mug"]
goal_frame = "goal_area"

if goal_frame not in C.getFrameNames():
    print("Defining a new goal frame at the blue area location.")
    goal = C.addFrame(goal_frame)
    goal.setPosition([1.0, 0.5, 0.0]) 
    goal.setShape(ry.ST.marker, size=[0.05])  

# Step 1: Randomly select one object and change its color
selected_object = random.choice(objects)
print(f"Selected object: {selected_object}")

new_color = [random.random(), random.random(), random.random()]
C.frame(selected_object).setColor(new_color)
print(f"Changed color of {selected_object} to {new_color}")

C.view()

# Step 2: Grasp the selected object
komo_grasp = ry.KOMO(C, 1, 1, 0, True) 

komo_grasp.addObjective([], ry.FS.positionDiff, ["l_gripper", selected_object], ry.OT.eq, [1e1])
komo_grasp.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.ineq, [1e-1])  # Avoid collisions

ret = ry.NLP_Solver(komo_grasp.nlp(), verbose=0).solve()
q_grasp = komo_grasp.getPath()[-1]

C.setJointState(q_grasp)
C.attach("l_gripper", selected_object) 
C.view(False, f"Grasping {selected_object}")
time.sleep(0.1)  

# Step 3: Move the object to the goal area (blue area)
komo_to_goal = ry.KOMO(C, 3, 30, 1, True)  
komo_to_goal.addControlObjective([], 0, 1e-1)
komo_to_goal.addObjective([0], ry.FS.qItself, [], ry.OT.eq, q_grasp)  
komo_to_goal.addObjective([1], ry.FS.positionDiff, ["l_gripper", goal_frame], ry.OT.eq, [1e1])  
komo_to_goal.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.ineq, [1e-1])

ret = ry.NLP_Solver(komo_to_goal.nlp(), verbose=0).solve()
path_to_goal = komo_to_goal.getPath()

for q in path_to_goal:
    C.setJointState(q)
    C.view(False, "Moving to goal area")
    time.sleep(0.1)  

# Manually set the object's position to the goal area
goal_position = C.frame(goal_frame).getPosition()
C.frame(selected_object).setPosition(goal_position)  
C.view(False, f"Placed {selected_object} at the goal area")
time.sleep(0.1) 

# Step 4: Return to the home position
qHome = C.getJointState()

komo_home = ry.KOMO(C, 1.5, 15, 1, True)  
komo_home.addControlObjective([], 0, 1e-1)
komo_home.addObjective([0], ry.FS.qItself, [], ry.OT.eq, path_to_goal[-1])  
komo_home.addObjective([1], ry.FS.qItself, [], ry.OT.eq, qHome)  
komo_home.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.ineq, [1e-1])

# Solve and execute return path
ret = ry.NLP_Solver(komo_home.nlp(), verbose=0).solve()
path_to_home = komo_home.getPath()

for q in path_to_home:
    C.setJointState(q)
    C.view(False, "Returning to home")
    time.sleep(0.1)

C.view()

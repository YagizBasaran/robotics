import robotic as ry
import time
import os

# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':0'

C = ry.Config()

# Load the maze, cargobot, and cargo 
C.addFile("/home/yagz/rai_venv/robotics/Question-01/environment/panda_fixGripper.g")
C.addFile("/home/yagz/rai_venv/robotics/Question-01/environment/maze.g")
C.addFile("/home/yagz/rai_venv/robotics/Question-01/environment/cargobot.g")
C.addFile("/home/yagz/rai_venv/robotics/Question-01/environment/cargo.g")

frame_names = C.getFrameNames()

if 'goal' not in frame_names:
    print("No frame named 'goal' found. Defining a new goal frame.")
    goal = C.addFrame("goal")
    goal.setPosition([1.0, 0.5, 1.0])  # Set goal position

C.view()

qHome = C.getJointState()

komo = ry.KOMO(C, 2, 20, 1, True)  # 2-second duration, 20 steps

komo.addControlObjective([], 0, 1e-1)  # Control cost
komo.addObjective([0], ry.FS.qItself, [], ry.OT.eq, qHome)  # Start at qHome
komo.addObjective([1], ry.FS.positionDiff, ['gripper', 'cargo'], ry.OT.eq, [1e1])  # Move gripper to cargo handle
komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq, [1e-1])  # Avoid collisions

ret = ry.NLP_Solver(komo.nlp(), verbose=0).solve()
q_path_to_cargo = komo.getPath()
qCargoPosition = q_path_to_cargo[-1]

for t in range(q_path_to_cargo.shape[0]):
    C.setJointState(q_path_to_cargo[t])
    C.view(False, f'waypoint {t} - Moving to cargo')
    time.sleep(0.1)
del komo

# Part A 
komo = ry.KOMO(C, 2, 20, 1, True) 
komo.setConfig(C, True)  
C.setJointState(qCargoPosition)  

komo.addControlObjective([], 0, 1e-1) 
komo.addObjective([0], ry.FS.qItself, [], ry.OT.eq, qCargoPosition)  
komo.addObjective([1], ry.FS.positionDiff, ['gripper', 'goal'], ry.OT.eq, [1e1])  
komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq, [1e-1]) 

ret = ry.NLP_Solver(komo.nlp(), verbose=0).solve()
q_path_to_goal = komo.getPath()
qGoalPosition = q_path_to_goal[-1]  

for t in range(q_path_to_goal.shape[0]):
    C.setJointState(q_path_to_goal[t])
    C.view(False, f'waypoint {t} - Moving to goal')
    time.sleep(0.1)

del komo
C.view()

# --- Part B
komo_home_to_cargo = ry.KOMO(C, 2, 20, 1, True)
komo_home_to_cargo.addControlObjective([], 0, 1e-1)  
komo_home_to_cargo.addObjective([0], ry.FS.qItself, [], ry.OT.eq, qHome)
komo_home_to_cargo.addObjective([1], ry.FS.qItself, [], ry.OT.eq, qCargoPosition) 
komo_home_to_cargo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.ineq, [1e-1])  

ret = ry.NLP_Solver(komo_home_to_cargo.nlp(), verbose=0).solve()
path_to_cargo = komo_home_to_cargo.getPath()

for q in path_to_cargo:
    C.setJointState(q)
    C.view(False, 'Moving to cargo')
    time.sleep(0.1)

# --- Part C: 
C.attach("gripper", "cargo")

komo_cargo_to_goal_attached = ry.KOMO(C, 2, 20, 1, True)
komo_cargo_to_goal_attached.addControlObjective([], 0, 1e-1)  # Control cost
komo_cargo_to_goal_attached.addObjective([0], ry.FS.qItself, [], ry.OT.eq, qCargoPosition)  # Start at qCargoPosition
komo_cargo_to_goal_attached.addObjective([1], ry.FS.qItself, [], ry.OT.eq, qGoalPosition)  # End at qGoalPosition
komo_cargo_to_goal_attached.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.ineq, [1e-1])  # Avoid collisions

ret = ry.NLP_Solver(komo_cargo_to_goal_attached.nlp(), verbose=0).solve()
path_to_goal_with_cargo = komo_cargo_to_goal_attached.getPath()

for q in path_to_goal_with_cargo:
    C.setJointState(q)
    C.view(False, 'Transporting cargo to goal')
    time.sleep(0.1)

# Detach the cargo from the gripper upon reaching the goal

# Final visualization at the goal position
C.setJointState(qGoalPosition)
C.view(False, 'Cargo placed at goal')
C.view_close()

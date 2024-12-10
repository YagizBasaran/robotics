import robotic as ry
import numpy as np
import time
import os

# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':0'

# Load the environment
C = ry.Config()
C.addFile("/home/yagz/rai_venv/robotics/penvironment.g")
C.view(False)
initial_pos = C.addFrame("initial_frame","l_gripper")
qHome = C.getJointState()

bot = ry.BotOp(C, useRealRobot=False)
bot.home(C)

# Function to align the gripper with the ring for grasping
def align_gripper_to_ring():
    approach_waypoint = C.addFrame('approach_waypoint', 'ring1')  # Using ring1 for alignment
    align_waypoint = C.addFrame('align_waypoint', 'ring1')
    approach_waypoint.setShape(ry.ST.marker, size=[.1])
    approach_waypoint.setRelativePose('t(0 0 0.1) d(90 -1 0 0)')  # Position above ring1

    align_waypoint.setShape(ry.ST.marker, size=[.1])
    align_waypoint.setRelativePose(' d(90 -1 0 0)')  # Align directly to ring1
   
    komo = ry.KOMO()
    komo.setConfig(C, True)
    komo.setTiming(2., 1, 5., 0)
    komo.addControlObjective([], 0, 1e-0)
    komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq, [1e1])
    komo.addObjective([], ry.FS.jointLimits, [], ry.OT.ineq)
    komo.addObjective([1.], ry.FS.positionDiff, ['l_gripper', 'approach_waypoint'], ry.OT.eq, [1e2])
    komo.addObjective([2.], ry.FS.positionDiff, ['l_gripper', 'align_waypoint'], ry.OT.eq, [1e2])
    #komo.addModeSwitch([1.], ry.SY.stable, ["l_gripper", 'align_waypoint'], True)
    solver = ry.NLP_Solver()
    solver.setProblem(komo.nlp())
    solver.setOptions(stopTolerance=1e-2, verbose=4)
    solver.solve()
   
    return komo.getPath()

# Function to grasp the ring
def grasp_ring():
    bot.gripperCloseGrasp(ry._left, 'ring1', force=10.0, width=0, speed=1)
    while not bot.gripperDone(ry._left):
        bot.sync(C, 0.1)
    print("Ring successfully grasped by the gripper.")

# Function to lift the ring
# def lift_ring():
#     lift_waypoint = C.addFrame('lift_waypoint', 'ring1')
#     lift_waypoint.setShape(ry.ST.marker, size=[.1])
#     lift_waypoint.setRelativePose('t(0 0 0.3)')  # Lift 30 cm upwards

#     komo = ry.KOMO()
#     komo.setConfig(C, True)
#     komo.setTiming(1., 1, 5., 0)
#     komo.addObjective([], ry.FS.jointLimits, [], ry.OT.ineq)
#     komo.addControlObjective([], 0, 1e-0)
#     komo.addObjective([1.], ry.FS.poseDiff, ['l_gripper', 'lift_waypoint'], ry.OT.eq, [1e2])
#     solver = ry.NLP_Solver()
#     solver.setProblem(komo.nlp())
#     solver.setOptions(stopTolerance=1e-2, verbose=1)
#     solver.solve()
   
#     return komo.getPath()

def throw():
    strech_frame =C.addFrame('strech_frame', 'table')
    strech_frame.setShape(ry.ST.marker, size=[.1])
    strech_frame.setRelativePosition([1, 1, 1])
    komo = ry.KOMO()
    komo.setConfig(C, True)
    komo.setTiming(2., 1, 5., 1)
    komo.addControlObjective([], 0, 1e-0)
    komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq, [1e1])
    komo.addObjective([], ry.FS.jointLimits, [], ry.OT.ineq)
    komo.addObjective([1.], ry.FS.positionDiff, ['l_gripper', 'strech_frame'], ry.OT.eq, [1e1])
    solver = ry.NLP_Solver()
    solver.setProblem(komo.nlp())
    solver.setOptions(stopTolerance=1e-2, verbose=4)
    solver.solve()
    return komo.getPath()

def strech():
    strech_frame1 =C.addFrame('strech_frame1', 'table')
    strech_frame1.setShape(ry.ST.marker, size=[.1])
    strech_frame1.setRelativePosition([0, 0.75, 1.1])
    strech_frame2 =C.addFrame('strech_frame2', 'table')
    strech_frame2.setShape(ry.ST.marker, size=[.1])
    strech_frame2.setRelativePosition([0, 2.2, 1.5])
    komo = ry.KOMO()
    komo.setConfig(C, True)
    komo.setTiming(2., 1, 5., 1)
    komo.addControlObjective([], 0, 1e-0)
    komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq, [1e1])
    komo.addObjective([], ry.FS.jointLimits, [], ry.OT.ineq)
    komo.addObjective([1.], ry.FS.positionDiff, ['l_gripper', 'strech_frame1'], ry.OT.eq, [1e1])
    komo.addObjective([2.], ry.FS.positionDiff, ['l_gripper', 'strech_frame2'], ry.OT.eq, [1e1])
    solver = ry.NLP_Solver()
    solver.setProblem(komo.nlp())
    solver.setOptions(stopTolerance=1e-2, verbose=4)
    solver.solve()
    return komo.getPath()

# Main function to execute the grasping task
def main():
    grasp_path = align_gripper_to_ring()
    bot.move(grasp_path, [1., 1.5])
    bot.wait(C, forKeyPressed=False, forTimeToEnd=True)
   
    grasp_ring()
    bot.wait(C, forKeyPressed=False, forTimeToEnd=True)
    bot.home(C)
    strech_path = strech()
    bot.move(strech_path,[.1, .2] )
    bot.gripperMove(ry._left, width=1, speed= 1)
    bot.wait(C, forKeyPressed= False, forTimeToEnd= True)
    while bot.getTimeToEnd()>0:
        bot.sync(C, .1)

main()
input("Stopping immediate close")

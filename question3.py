# Question 3 last version
import robotic as ry
import numpy as np
import os
# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':0'

C = ry.Config()
C.addFile("/home/yagz/rai_venv/robotics/mini_golf.g")
C.view(False)

bot = ry.BotOp(C, useRealRobot=False)
bot.home(C)

# Function to align the gripper with the hammer handle for grasping
def align_gripper_to_hammer():
    approach_waypoint = C.addFrame('approach_waypoint', 'hammer-handle')
    align_waypoint = C.addFrame('align_waypoint', 'hammer-handle')
    approach_waypoint.setShape(ry.ST.marker, size=[.1])
    approach_waypoint.setRelativePose('t(0 0 .1) d(90 0 0 0)') 

    align_waypoint.setShape(ry.ST.marker, size=[.1])
    align_waypoint.setRelativePose('d(90 0 0 0)') 
    
    komo = ry.KOMO()
    komo.setConfig(C, True)
    komo.setTiming(2., 1, 5., 0)
    komo.addControlObjective([], 0, 1e-0)
    komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq)
    komo.addObjective([], ry.FS.jointLimits, [], ry.OT.ineq)
    komo.addObjective([1.], ry.FS.poseDiff, ['l_gripper', 'approach_waypoint'], ry.OT.eq, [1e1]) 
    komo.addObjective([2.], ry.FS.poseDiff, ['l_gripper', 'align_waypoint'], ry.OT.eq, [1e1]) 
    solver = ry.NLP_Solver()
    solver.setProblem(komo.nlp())
    solver.setOptions(stopTolerance=1e-2, verbose=4)
    solver.solve()
    
    return komo.getPath()

# Function to grasp the hammer handle
def grasp_hammer():
    bot.gripperCloseGrasp(ry._left, 'hammer-handle', force=10.0, width=0.04, speed=0.5)
    while not bot.gripperDone(ry._left):
        bot.sync(C, 0.1)
    print("Hammer handle successfully grasped by the gripper.")

# Function to lift the hammer without rotation
def lift_hammer():
    lift_waypoint = C.addFrame('lift_waypoint', 'hammer-handle')
    lift_waypoint.setShape(ry.ST.marker, size=[.1])
    lift_waypoint.setRelativePose('t(0 0 0.3)')

    komo = ry.KOMO()
    komo.setConfig(C, True)
    komo.setTiming(1., 1, 5., 0)
    komo.addControlObjective([], 0, 1e-0)
    komo.addObjective([1.], ry.FS.poseDiff, ['l_gripper', 'lift_waypoint'], ry.OT.eq, [1e1])
    solver = ry.NLP_Solver()
    solver.setProblem(komo.nlp())
    solver.setOptions(stopTolerance=1e-2, verbose=1)
    solver.solve()
    
    return komo.getPath()

# Function to rotate hammer
def rotate_hammer_to_vertical():
    vertical_waypoint = C.addFrame('vertical_waypoint', 'hammer-handle')
    vertical_waypoint.setShape(ry.ST.marker, size=[.1])
    vertical_waypoint.setRelativePose('r(1 -90 0 0)') 

    komo = ry.KOMO()
    komo.setConfig(C, True)
    komo.setTiming(1., 1, 5., 0)
    komo.addControlObjective([], 0, 1e-0)
    komo.addObjective([1.], ry.FS.poseDiff, ['l_gripper', 'vertical_waypoint'], ry.OT.eq, [1e1])
    solver = ry.NLP_Solver()
    solver.setProblem(komo.nlp())
    solver.setOptions(stopTolerance=1e-2, verbose=1)
    solver.solve()
    
    return komo.getPath()


def prepare_straight_push():
    start_push_waypoint = C.addFrame('start_push_waypoint', 'ball')
    end_push_waypoint = C.addFrame('end_push_waypoint', 'ball')

    start_push_waypoint.setShape(ry.ST.marker, size=[.1])
    start_push_waypoint.setRelativePose('t(-0.1 0 0.05)')  

    end_push_waypoint.setShape(ry.ST.marker, size=[.1])
    end_push_waypoint.setRelativePose('t(0.3 0 0)') 

    komo = ry.KOMO()
    komo.setConfig(C, True)
    komo.setTiming(2., 1, 5., 0)
    komo.addControlObjective([], 0, 1e-0)
    komo.addObjective([], ry.FS.accumulatedCollisions, [], ry.OT.eq)
    komo.addObjective([], ry.FS.jointLimits, [], ry.OT.ineq)
    komo.addObjective([1.], ry.FS.poseDiff, ['l_gripper', 'start_push_waypoint'], ry.OT.eq, [1e1])
    komo.addObjective([2.], ry.FS.poseDiff, ['l_gripper', 'end_push_waypoint'], ry.OT.eq, [1e1])
    solver = ry.NLP_Solver()
    solver.setProblem(komo.nlp())
    solver.setOptions(stopTolerance=1e-2, verbose=1)
    solver.solve()
    
    return komo.getPath()


def release_hammer():
    bot.gripperMove(ry._left, width=0.08, speed=1.0)
    while not bot.gripperDone(ry._left):
        bot.sync(C, 0.1)
    print("Gripper opened, hammer released.")


def main():
    grasp_path = align_gripper_to_hammer()
    bot.move(grasp_path, [2., 3.])
    while bot.getTimeToEnd() > 0:
        bot.sync(C, 0.1)
    
    grasp_hammer()
    
    lift_path = lift_hammer()
    bot.move(lift_path, [2.])
    while bot.getTimeToEnd() > 0:
        bot.sync(C, 0.1)

    rotate_path = rotate_hammer_to_vertical()
    bot.move(rotate_path, [1.5])
    while bot.getTimeToEnd() > 0:
        bot.sync(C, 0.1)

    push_path = prepare_straight_push()
    bot.move(push_path, [2., 3.])
    while bot.getTimeToEnd() > 0:
        bot.sync(C, 0.1)

    release_hammer()
    
    bot.home(C)
    while bot.getTimeToEnd() > 0:
        bot.sync(C, 0.1)
    print("Returned to home position.")

main()

del bot
del C

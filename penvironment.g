world: { multibody: true }

# Table (base for the setup)
table (world): {
  shape: ssBox, Q: "t(0 0 .6)", size: [2., 4., .2, .04], color: [.3, .3, .3]
  fixed, contact, friction: .1
}

# Target (green base) attached to the table
target (table): {
  shape: ssBox, Q: "t(0 1. .1)", size: [.6, .6, .1, .04], color: [.3, .6, .3, 1]
  fixed
}

# Main ring frame on top of the target - now fixed to prevent changes
ring (target): {
  Q: "t(0 0 0.07)  d(120 1 1 1)"
  joint : rigid
}

# Individual ring segments - also fixed and without mass to keep them stable
ring1(ring): { 
  shape: capsule, Q: "t(.12 0 0)", size: [.2, .015], color: [.6, .6, .6]
  contact: 1
  mass : 0.00005
}

ring2(ring): { 
  shape: capsule, Q: "t(-.12 0 0)", size: [.2, .015], color: [.6, .6, .6]
  contact: 1
  mass : 0.00005
}

ring3(ring): { 
  shape: capsule, Q: "t(0 0 -.1) d(90 0 1 0)", size: [.2, .015], color: [.6, .6, .6]
  contact: 1
  mass : 0.00005
 
}

ring4(ring): { 
  shape: capsule, Q: "t(0 0 .1) d(90 0 1 0)", size: [.2, .015], color: [.6, .6, .6]
  contact: 1
  mass : 0.00005
  
}

# Stick placed on the table, now fixed so it won't fall or roll
stick (table): {
  shape: cylinder, Q: "t(0 -0.9 .30)", size: [.6, .015], color: [.6, .6, .6]
  joint: rigid
  contact: 1
  friction: 1000
  fixed
  # No mass specified, so it's static
}

# Panda robotic arm attached to the table
Include: </home/yagz/rai_venv/robotics/rai-robotModels/scenarios/pandaSingle.g>
(table l_panda_base): { joint: rigid, Q: "t(0 1.8 .05) d(-90 0 0 1)" }

Edit panda_finger_joint1: { joint_active: false }

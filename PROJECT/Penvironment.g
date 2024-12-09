world: { multibody: true }

# Table (base for the setup)
table (world): {
 shape: ssBox, Q: "t(0 0 .6)", size: [2., 4., .2, .04], color: [.3, .3, .3]
 fixed, contact, logical:{ }
 friction: .1
}

# Target (green base) attached to the table
target (table): {
 shape: ssBox, Q: "t(0 1. .1)", size: [.6, .6, .1, .04], color: [.3, .6, .3, 1]
}

# Hollow ring placed horizontally on top of the target
ring (target): {
 Q: "t(0 0 0.070) d(120 1 1 1)"  # Positioned directly on the target, flat
}


ring1(ring): { 
 shape: capsule, Q: "t(.12 0 0)", size: [.2, .015], color: [.6, .6, .6]
 logical: {object} 
}
ring2(ring): { 
 shape: capsule, Q: "t(-.12 0 0)", size: [.2, .015], color: [.6, .6, .6]
 logical: {object} 
}
ring3(ring): { 
 shape: capsule, Q: "t(0 0 -.1) d(90 0 1 0)", size: [.2, .015], color: [.6, .6, .6]
 logical: {object} 
}
ring4(ring): { 
 shape: capsule, Q: "t(0 0 .1) d(90 0 1 0)", size: [.2, .015], color: [.6, .6, .6]
 logical: {object}, contact: -1 
}

# Stick repositioned vertically at the facing edge of the table
stick (table): {
 shape: capsule, Q: "t(0 -1.8 .30) d(90 0 0 0)", size: [.6, .03], color: [.6, .6, .6]
 joint: rigid
 mass: 1
}

# Panda robotic arm attached to the table
Include: <../panda/panda.g>
(table panda_base): { joint: rigid, Q: "t(0 1.8 .05) d(-90 0 0 1)" }

# Disable active joint in the Panda arm
Edit panda_finger_joint1: { joint_active: false }

base_origin: { X: [0, 0, .08] }

base (base_origin): {
 joint: transXYPhi, limits: [-10,10,-10,10,-4,4],
 shape: ssCylinder, size: [.1, .3, .02], contact: 1 }

Prefix: "l_"
Include: <panda_fixGripper.g>

Prefix: False

Edit l_panda_base (base): { Q: "t(0 0 .05) d(90 0 0 1)" }

Edit l_panda_joint2: { q: -.5 }
Edit l_panda_joint4: { q: -2 }
Edit l_panda_joint7: { q: -.5 }

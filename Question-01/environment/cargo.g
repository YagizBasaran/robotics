worldbase {}

# Useful Info: Difference between X and Q is; Q is relative Pose
cargo_handle: { X: "t(1.7 -1. 0.45) d(90 0 1 0)", shape: capsule, size: [.2 .012], color: [1 0 0], mass: .1, contact: 1 }
cargo(cargo_handle): { Q: "t(0.25 0 0) d(0 0 1 0)", shape: ssBox, size: [.4 .4 .4,.05], color: [1 .5 0], mass: .1, contact: 1 }
cargo_handle_l(cargo_handle): { Q: "t(0.025 0 0.115) d(90 0 1 0)", shape: capsule, size: [.05 .012], color: [1 0 0], mass: .1, contact: 1 }
cargo_handle_l(cargo_handle): { Q: "t(0.025 0 -0.115) d(90 0 1 0)", shape: capsule, size: [.05 .012], color: [1 0 0], mass: .1, contact: 1 }


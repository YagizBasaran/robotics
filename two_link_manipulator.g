world: {}

zero (world): {
    shape: sphere, size: [0.06],
    mass: 1.0,
    X:"T t(0 0 0) d(180 0 0 1)" 
}

joint1(zero):{
   joint: hingeX,
   pre:"T t(0 0 0)" 
}

link1 (joint1): {
    shape: capsule, size: [1.0, 0.05],  # Changed length to 1.0 meters
    color: [0.0, 0.0, 1.0],
    Q: [0.0, 0.0, 0.5]  # Adjusted the position to match the new length
}

joint2(link1):{
   joint: hingeX,
   pre:"T t(0 0.0 0.5)"  # Adjusted to be at the end of link1's new length
}

link2 (joint2): {
    shape: capsule, size: [1.0, 0.05],  # Changed length to 1.0 meters
    color: [1.0, 0.0, 0.0],
    Q: [0.0, 0.0, 0.5]  # Adjusted the position to match the new length
}

joint3 (link2): {
    joint: hingeX,
    pre:"T t(0 0.0 0.5)",  # Adjusted to be at the end of link2's new length
}

end-effector (joint3): {
    shape: sphere, size: [0.06],
    color: [0.0, 1.0, 0.0],
    Q: [0.0, 0.0, 0.03]
}

target: {
    X: "t(0 1 1) d(0 0 0 1)",
    shape: box,
    size: [0.2 0.2 0.2 0.5],
    color: [1 1 0],
    mass: .1,
    contact: true
}

world: {}

zero (world): {
    shape: sphere, size: [0.05],
    mass: 1.0,
    X:"T t(0 0 0) d(180 0 0 1)" 
}

joint1(zero):{
   joint: hingeX,
   pre:"T t(0 0 0)" 
}

link1 (joint1): {
    shape: capsule, size: [0.3, 0.05],
    color: [0.0, 0.0, 1.0],
    Q: [0.0, 0.0, 0.2]
}

joint2(link1):{
   joint: hingeX,
   pre:"T t(0 0.0 .15)"

}

link2 (joint2): {
    shape: capsule, size: [0.2, 0.05],
    color: [1.0, 0.0, 0.0],
    Q: [0.0, 0.0, 0.15]
}

joint3 (link2): {
    joint: hingeX,
    pre:"T t(0 0.0 .12)",
}

end-effector (joint3): {
    shape: sphere, size: [0.05],
    color: [0.0, 1.0, 0.0],
    Q: [0.0, 0.0, 0.03]
}



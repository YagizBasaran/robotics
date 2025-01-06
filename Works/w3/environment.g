world: {}


Include: <../rai-robotModels/scenarios/pandaSingle.g>

bin (table): {shape: ssBox, Q: [0.0, 0.4, 0.08], size: [0.8, 0.8, 0.06, .02], color: [.6, .6, .6], joint: rigid, friction: .1}
side1 (bin): {shape: ssBox, Q: [0.36, 0.0, 0.08], size: [0.08, 0.8, 0.16, .02], color: [.6, .6, .6], joint: rigid, friction: .1}
side2 (bin): {shape: ssBox, Q: [0.0, -0.36, 0.08], size: [0.8, 0.08, 0.16, .02], color: [.6, .6, .6], joint: rigid, friction: .1}
side1 (bin): {shape: ssBox, Q: [-0.36, 0.0, 0.08], size: [0.08, 0.8, 0.16, .02], color: [.6, .6, .6], joint: rigid, friction: .1}
side4 (bin): {shape: ssBox, Q: [0.0, 0.36, 0.08], size: [0.8, 0.08, 0.16, .02], color: [.6, .6, .6], joint: rigid, friction: .1}


bin-2 (table): {shape: ssBox, Q: [-0.60, -0.35, 0.08], size: [0.8, 0.8, 0.06, .02], color: [.6, .6, .6], joint: rigid, friction: .1}
side1-2 (bin-2): {shape: ssBox, Q: [0.36, 0.0, 0.08], size: [0.08, 0.8, 0.16, .02], color: [.6, .6, .6], joint: rigid, friction: .1}
side2-2 (bin-2): {shape: ssBox, Q: [0.0, -0.36, 0.08], size: [0.8, 0.08, 0.16, .02], color: [.6, .6, .6], joint: rigid, friction: .1}
side1-2 (bin-2): {shape: ssBox, Q: [-0.36, 0.0, 0.08], size: [0.08, 0.8, 0.16, .02], color: [.6, .6, .6], joint: rigid, friction: .1}
side4-2 (bin-2): {shape: ssBox, Q: [0.0, 0.36, 0.08], size: [0.8, 0.08, 0.16, .02], color: [.6, .6, .6], joint: rigid, friction: .1}


soap_0 (bin):{
    joint: rigid,
    shape: ssBox,
    size: [0.04, 0.08, 0.04, 0.01]
    Q: "t(0.0 0.0 0.06)",
    mass: 0.1,
    contact:1
}


rolling-pin_0 (bin):{
    joint: rigid,
    shape: ssBox,
    size: [0.002, 0.002, 0.18, 0.02]
    Q: "t(0.2 0.0 0.06) d(90 1 0 0 ) d(45 0 1 1)",
    mass: 0.1,
    contact:1
}
rolling-pin_1 (rolling-pin_0):{
    shape: ssBox,
    size: [0.001, 0.001, 0.25, 0.01]
    Q: "t(0.0 0.0 0.0)",
    mass: 0.1,
    contact:1
}
bottle_0 (bin):{
    joint: rigid,
    shape: ssBox,
    size: [0.03, 0.05, 0.20, 0.02],
    Q: "t(-0.2 -0.05 0.06) d(90 1 0 0 )",
    mass: 0.1,
    contact: 1
}

bottle_1 (bottle_0):{
    shape: ssBox,
    size: [0.10, 0.05, 0.10, 0.02],
    Q: [0.025, 0.0,-0.05],
    mass: 0.1,
    contact: 1
}

bottle_2 (bottle_0):{
    shape: ssBox,
    size: [0.06, 0.05, 0.07, 0.02],
    Q: "t(0.022 0.0 0.00) d(-45 0 1 0)",
    mass: 0.1,
    contact: 1

}
bottle_3 (bottle_0):{
    shape: ssBox,
    size: [0.04, 0.04, 0.01, 0.01],
    Q: "t(0.0 0.0 0.1)",
    mass: 0.1,
    contact: 1

}

bottle_4 (bottle_0):{
    shape: ssBox,
    size: [0.025, 0.025, 0.04, 0.01],
    Q: "t(-0.01 0.0 0.12)",
    mass: 0.1,
    contact: 1

}
bottle_5 (bottle_0):{
    shape: ssBox,
    size: [0.020, 0.020, 0.06, 0.01],
    Q: "t(0.01 0.0 0.14) d(60 0 1 0)",
    mass: 0.1,
    contact: 1
}

bottle_6 (bottle_0):{
    shape: ssBox,
    size: [0.005, 0.015, 0.06, 0.001],
    Q: "t(0.01 0.0 0.12) d(120 0 1 0)",
    mass: 0.1,
    contact: 1

}
bottle_7 (bottle_0):{
    shape: ssBox,
    size: [0.005, 0.015, 0.02, 0.001],
    Q: "t(0.01 0.0 0.13) d(10 0 1 0)",
    mass: 0.1,
    contact: 1
}

### Cameras 

camera1(world):{
    shape: marker, size: [0.1],
    focalLength: 0.895, width: 640, height: 360, zRange: [0.5, 100]
    Q: "t(-0.5 -0.1 1.08) d(-120 1 0 0) d(45 0 1 0)"
}

camera2(world):{
    shape: marker, size: [0.1],
    focalLength: 0.895, width: 640, height: 360, zRange: [0.5, 100]
    Q: "t(0.5 -0.1 1.08) d(-120 1 0 0) d(-45 0 1 0)"
}

camera3(world):{
    shape: marker, size: [0.1],
    focalLength: 0.895, width: 640, height: 360, zRange: [0.5, 100]
    Q: "t(0.5 1.0 1.08) d(180 0 1 0) d(60 1 0 0) d(45 0 1 0)"
}

camera4(world):{
    shape: marker, size: [0.1],
    focalLength: 0.895, width: 640, height: 360, zRange: [0.5, 100]
    Q: "t(-0.5 1.0 1.08) d(180 0 1 0) d(60 1 0 0) d(-45 0 1 0)"
}

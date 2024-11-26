frame floorwalls: { }

frame _0(floorwalls): { shape: box, size: [10, 10, 0.01], color: [0.4, 0.4, 0.4], Q: [0, 0, +0.02, 1, 0, 0, 0]  ,contact: 0}
front _1(floorwalls): { shape: box, size: [6, 0.02, 1.2], color: [0.82, 0.7, 0.55], Q: [2, -4, 0.62, 1, 0, 0, 0] ,contact: True}
front _2(floorwalls): { shape: box, size: [2, 0.02, 1.2], color: [0.82, 0.7, 0.55], Q: [2, -2, 0.62, 1, 0, 0, 0] ,contact: True}
front _3(floorwalls): { shape: box, size: [2, 0.02, 1.2], color: [0.82, 0.7, 0.55], Q: [-4, -2, 0.62, 1, 0, 0, 0] ,contact: True}
front _4(floorwalls): { shape: box, size: [4, 0.02, 1.2], color: [0.82, 0.7, 0.55], Q: [-3, -4, 0.62, 1, 0, 0, 0] ,contact: True}
back _1(floorwalls): { shape: box, size: [2, 0.02, 1.2], color: [0.82, 0.7, 0.55], Q: [0, 2, 0.62, 1, 0, 0, 0] ,contact: True}
back _2(floorwalls): { shape: box, size: [8, 0.02, 1.2], color: [0.82, 0.7, 0.55], Q: [1, 4, 0.62, 1, 0, 0, 0] ,contact: True}
side _left1(floorwalls): { shape: box, size: [0.02, 4, 1.2], color: [0.82, 0.7, 0.55], Q: [1, 0, 0.62, 1, 0, 0, 0] ,contact: 1}
side _left2(floorwalls): { shape: box, size: [0.02, 4, 1.2], color: [0.82, 0.7, 0.55], Q: [3, 0, 0.62, 1, 0, 0, 0],contact: True }
side _left3(floorwalls): { shape: box, size: [0.02, 8, 1.2], color: [0.82, 0.7, 0.55], Q: [5, 0, 0.62, 1, 0, 0, 0],contact: True }
side _right1(floorwalls): { shape: box, size: [0.02, 6, 1.2], color: [0.82, 0.7, 0.55], Q: [-1, -1, 0.62, 1, 0, 0, 0] ,contact: True}
side _right2(floorwalls): { shape: box, size: [0.02, 6, 1.2], color: [0.82, 0.7, 0.55], Q: [-3, 1, 0.62, 1, 0, 0, 0],contact: True }
side _right3(floorwalls): { shape: box, size: [0.02, 2, 1.2], color: [0.82, 0.7, 0.55], Q: [-5, -3, 0.62, 1, 0, 0, 0] ,contact: True}
goal_area(floorwalls): { shape: marker, size: [1, 1, 1], color: [0, 0, 1, 0.5], Q: [-4.5, -3, 0.03, 1, 0, 0, 0]}

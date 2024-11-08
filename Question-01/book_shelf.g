world: {}


Include: <../rai-robotModels/scenarios/pandaSingle.g>

base (world):{ shape: ssBox, size: [0.3, 0.7, 0.05, 0.001], joint: rigid, Q: [0.4 ,0.30, 0.675], color: [0.76, 0.60, 0.42], contact: 1}
leg1 (base): { shape: ssBox, size: [0.3, 0.05, 0.6, 0.001], joint: rigid, Q: [0.0, 0.35, 0.275], color: [0.76, 0.60, 0.42], contact: 1}
leg2 (base): { shape: ssBox, size: [0.3, 0.05, 0.6, 0.001], joint: rigid, Q: [0.0, -0.35, 0.275], color: [0.76, 0.60, 0.42], contact: 1}
layer1 (base):{ shape: ssBox, size: [0.3, 0.7, 0.05, 0.001], joint: rigid, Q: [0.0 ,0.0, 0.20], color: [0.76, 0.60, 0.42], contact: 1}
layer2 (base):{ shape: ssBox, size: [0.3, 0.7, 0.05, 0.001], joint: rigid, Q: [0.0 ,0.0, 0.50], color: [0.76, 0.60, 0.42], contact: 1}

book1(base): { shape: ssBox, size: [0.15, 0.05, 0.16, 0.001], joint: rigid, Q: [-0.1, 0.0, 0.305], color: [0.80, 0.80, 0.80]}
book2(base): { shape: ssBox, size: [0.15, 0.07, 0.20, 0.001], joint: rigid, Q: [-0.1, 0.25, 0.325], color: [0.80, 0.80, 0.80]}
book-non(base): { shape: ssBox, size: [0.20, 0.15, 0.05, 0.001], joint: rigid, Q: [-0.1, -0.15, 0.55], color: [0.80, 0.80, 0.80]}
book3(base): { shape: ssBox, size: [0.20, 0.15, 0.05, 0.001], joint: rigid, Q: [-0.15, -0.05, 0.60], color: [0.80, 0.80, 0.80]}
book4(base): { shape: ssBox, size: [0.15, 0.05, 0.20, 0.001], joint: rigid, Q: [-0.1, 0.15, 0.625], color: [0.80, 0.80, 0.80]}
mug(base): { shape: ssBox, size: [0.06, 0.06, 0.10, 0.005], joint: rigid, Q: [0.0, -0.20, 0.275], color: [0.80, 0.80, 0.80]}
mug-h1(mug): { shape: ssBox, size: [0.01, 0.04, 0.01, 0.001], joint: rigid, Q: [0.0, -0.04, -0.015], color: [0.80, 0.80, 0.80]}
mug-h2(mug): { shape: ssBox, size: [0.01, 0.04, 0.01, 0.001], joint: rigid, Q: [0.0, -0.04, 0.015], color: [0.80, 0.80, 0.80]}
mug-h3(mug): { shape: ssBox, size: [0.01, 0.01, 0.04, 0.001], joint: rigid, Q: [0.0, -0.06, 0], color: [0.80, 0.80, 0.80]}

goal (world):{ shape: ssBox, size: [0.4, 0.4, 0.01, 0.001], joint: rigid, Q: [-0.4 ,0.30, 0.665], color: [0.0, 0.0, 1.0], contact: 1}

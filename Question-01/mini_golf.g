world: {}


Include: <../rai-robotModels/scenarios/pandaSingle.g>

platform-1 (table): {shape: ssBox, size: [0.4,0.3,0.1,0.005], joint: rigid, Q: [-0.10, 0.40, 0.05], color: [0.1, 0.1, 0.1], contact: 1, mass: 0.1} 
platform-2 (platform-1): {shape: ssBox, size: [0.1,0.05,0.1,0.005], joint: rigid, Q: [0.25, 0.125, 0], color: [0.1, 0.1, 0.1], contact: 1, mass: 0.1} 
platform-3 (platform-1): {shape: ssBox, size: [0.1,0.05,0.1,0.005], joint: rigid, Q: [0.25, -0.125, 0], color: [0.1, 0.1, 0.1], contact: 1, mass: 0.1} 
platform-4 (platform-1): {shape: ssBox, size: [0.1,0.3,0.1,0.005], joint: rigid, Q: [0.35, 0, 0], color: [0.1, 0.1, 0.1], contact: 1, mass: 0.1} 
 

ball (platform-1): {shape: ssBox, size: [0.05, 0.05, 0.05, 0.020], joint: rigid, Q: [-0.15, 0.0, 0.08], color: [0.35,0.98,1.0], contact: 1, mass: 0.00001} 

hammer-handle (table): {shape: ssBox, size: [0.04, 0.25, 0.03, 0.005], joint: rigid, Q: [-0.4, 0.05, 0.055], color: [0.76, 0.60, 0.48], contact: 1, mass: 0.05} 
hammer-head (hammer-handle): {shape: ssBox, size: [0.12, 0.08, 0.06, 0.005],  Q: [0.0, 0.14, 0.0], color: [0.1, 0.2, 0.6], contact: 1, mass: 0.05} 



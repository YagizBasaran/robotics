import robotic as ry
import matplotlib.pyplot as plt
import os

# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':0'

C = ry.Config()
C.addFile(ry.raiPath('scenarios/pandaSingle.g'))
C.view()
cam = ry.CameraView(C)
cam.setCamera('cameraTop')
rgb, depth = cam.computeImageAndDepth(C)
pcl = ry.depthImage2PointCloud(depth, cam.getFxycxy())
print(rgb.shape, depth.shape, pcl.shape)
print(C.view_fxycxy())
fig = plt.figure()
fig.add_subplot(1,2,1)
plt.imshow(rgb)
fig.add_subplot(1,2,2)
plt.imshow(depth)
plt.show()
f = C.addFrame('pcl', 'cameraTop')
f.setPointCloud(pcl, [255,0,0])
C.view()

# Prevent the script from exiting immediately
input("Press Enter to exit...")
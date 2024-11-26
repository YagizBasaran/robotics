#my RAI robotics version: 0.1.10
#open3d version: 0.13.0
import robotic as ry
import numpy as np
import os
import open3d as o3d
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':0'

# Initialize configuration
C = ry.Config()
C.addFile("/home/yagz/rai_venv/robotics/Q1/environment.g")
C.view()

cam = ry.CameraView(C)
camera_frames = ["camera1", "camera2", "camera3", "camera4"]
all_points_world = []

bin_min = np.array([-0.3, 0.1, 0.725]) 
bin_max = np.array([0.3, 0.7, 0.77])    

f_bbox = C.addFrame("bounding_box", "world")
f_bbox.setShape(ry.ST.ssBox, size=[
    bin_max[0] - bin_min[0],
    bin_max[1] - bin_min[1],
    bin_max[2] - bin_min[2], 0.01])
f_bbox.setPosition([
    (bin_max[0] + bin_min[0]) / 2,
    (bin_max[1] + bin_min[1]) / 2,
    (bin_max[2] + bin_min[2]) / 2])
f_bbox.setColor([0, 0, 0, 0])
C.view()

for cam_frame in camera_frames:
    cam.setCamera(cam_frame)
    
    rgb, depth = cam.computeImageAndDepth(C)
    depth = depth.astype(np.float32)
    depth[depth < 0] = np.nan 

    pcl = ry.depthImage2PointCloud(depth, cam.getFxycxy())
    pcl = pcl.reshape(-1, 3)  

    pcl = pcl[~np.isnan(pcl).any(axis=1)]

    f_cam = C.frame(cam_frame)
    position = f_cam.getPosition()
    rotation_matrix = f_cam.getRotationMatrix()
    pcl_world = (rotation_matrix @ pcl.T).T + position  

    mask = np.all((pcl_world >= bin_min) & (pcl_world <= bin_max), axis=1)
    pcl_cropped = pcl_world[mask]

    if pcl_cropped.size > 0:
        f_crop = C.addFrame(f"crop_pcl_{cam_frame}", "world")
        f_crop.setPointCloud(points=pcl_cropped, colors=[0, 0, 255])
        C.view()
        all_points_world.append(pcl_cropped)
    else:
        print(f"No points in cropped point cloud for camera '{cam_frame}'.")

if len(all_points_world) == 0:
    print("No point clouds were captured from the cameras.")
    exit()

merged_pcl = np.vstack(all_points_world)

f_pcl = C.addFrame("merged_pcl", "world")
f_pcl.setPointCloud(points=merged_pcl, colors=[0, 0, 255])
C.view()

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(merged_pcl)

pcd.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.02, max_nn=30)
)

pcd.orient_normals_consistent_tangent_plane(30)

normals = np.asarray(pcd.normals)

n_clusters = 3 
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
labels = kmeans.fit_predict(merged_pcl)

# cluster_colors = np.array([
#     [1.0, 0.0, 0.0],  # Cluster 0: Red
#     [0.0, 1.0, 0.0],  # Cluster 1: Green
#     [0.0, 0.0, 1.0],  # Cluster 2: Blue
# ])
# colors = cluster_colors[labels]

colors = plt.cm.get_cmap("tab10", n_clusters)(labels / (n_clusters - 1))[:, :3]

pcd.colors = o3d.utility.Vector3dVector(colors)

o3d.visualization.draw_geometries(
    [pcd], point_show_normal=True, window_name="Point Cloud with Normals",width=800,height=600
)

# Prevent the script from exiting immediately
input("Press Enter to exit...")

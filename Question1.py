from sklearn.cluster import KMeans
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import robotic as ry
import os
# Set the DISPLAY environment variable
os.environ['DISPLAY'] = ':0'
# Initialize configuration
C = ry.Config()
C.addFile("/home/yagz/rai_venv/robotics/Q1/environment.g")
C.view()  # Retained as per your request

camera_frames = ["camera1", "camera2", "camera3", "camera4"]
all_points_world = []

# Define the bounding box (adjust to match your bin's dimensions)
bin_min = np.array([-0.3, 0.1, 0.725])  # Adjusted bounding box minimum coordinates
bin_max = np.array([0.3, 0.7, 0.77])    # Adjusted bounding box maximum coordinates

# Visualize bounding box (optional)
f_bbox = C.addFrame("bounding_box", "world")
f_bbox.setShape(ry.ST.ssBox, size=[
    bin_max[0] - bin_min[0],
    bin_max[1] - bin_min[1],
    bin_max[2] - bin_min[2], 0.01])
f_bbox.setPosition([
    (bin_max[0] + bin_min[0]) / 2,
    (bin_max[1] + bin_min[1]) / 2,
    (bin_max[2] + bin_min[2]) / 2])
f_bbox.setColor([0, 1, 0, 0.2])  # Transparent green bounding box
C.view()

# Process each camera
for cam_frame in camera_frames:
    if cam_frame not in C.getFrameNames():
        print(f"Camera frame '{cam_frame}' does not exist.")
        continue

    # Set the camera frame
    f = C.getFrame(cam_frame)
    C.view_setCamera(f)

    # Capture RGB and Depth
    try:
        rgb = C.view_getRgb()
        depth = C.view_getDepth()
        depth = depth.astype(np.float32)
        print(f"Successfully captured images from camera '{cam_frame}'")
    except Exception as e:
        print(f"Error capturing images from camera '{cam_frame}': {e}")
        continue

    # Replace invalid depth values
    depth[depth <= 0] = np.nan

    # Get the intrinsic parameters
    fxycxy = C.view_fxycxy()

    # Convert depth image to point cloud
    try:
        pcl = ry.depthImage2PointCloud(depth, fxycxy).reshape(-1, 3)
    except Exception as e:
        print(f"Error converting depth image to point cloud for '{cam_frame}': {e}")
        continue

    # Transform point cloud to world frame
    position = f.getPosition()
    R_cam_world = f.getRotationMatrix()
    pcl_world = (R_cam_world @ pcl.T).T + position

    # Crop point cloud
    mask = np.all((pcl_world >= bin_min) & (pcl_world <= bin_max), axis=1)
    pcl_cropped = pcl_world[mask]
    all_points_world.append(pcl_cropped)

    # Optional: Visualize cropped point cloud
    if pcl_cropped.size > 0:
        f_crop = C.addFrame(f"crop_pcl_{cam_frame}", "world")
        f_crop.setPointCloud(points=pcl_cropped, colors=[0, 255, 0])
        C.view()
    else:
        print(f"No points in cropped point cloud for camera '{cam_frame}'.")

# Merge all cropped point clouds
if len(all_points_world) == 0:
    print("No point clouds were captured from the cameras.")
    exit()

merged_pcl = np.vstack(all_points_world)
print(f"Final merged point cloud shape: {merged_pcl.shape}")

# Visualize merged point cloud
if merged_pcl.size > 0:
    f_pcl = C.addFrame("merged_pcl", "world")
    f_pcl.setPointCloud(points=merged_pcl, colors=[0, 0, 255])
    C.view()
else:
    print("Merged point cloud is empty.")

# --- Perform K-Means Clustering ---
n_clusters = 3  # Number of objects in the bin
kmeans = KMeans(n_clusters=n_clusters, random_state=0)
labels = kmeans.fit_predict(merged_pcl)

# Assign colors to clusters
colors = plt.cm.get_cmap("tab10", n_clusters)(labels / (n_clusters - 1))[:, :3]

# Create Open3D point cloud for visualization
o3d_pcl = o3d.geometry.PointCloud()
o3d_pcl.points = o3d.utility.Vector3dVector(merged_pcl)
o3d_pcl.colors = o3d.utility.Vector3dVector(colors)

# Visualize segmented point cloud
o3d.visualization.draw_geometries([o3d_pcl], window_name="Segmented Point Cloud")

# Save the segmented point cloud
o3d.io.write_point_cloud("segmented_point_cloud.ply", o3d_pcl)
print("Segmented point cloud saved to 'segmented_point_cloud.ply'.")

# Reset the camera to default
C.view_setCamera(None)

# Prevent the script from exiting immediately
input("Press Enter to exit...")


#!!!!!!!!!!!!!!!!!
#CLOSE THE "Point Cloud with Normals" WINDOW FIRST OR TERMINAL IS FREEZES

import robotic as ry
import numpy as np
import os
import open3d as o3d
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import time

os.environ['DISPLAY'] = ':0'

C = ry.Config()
C.addFile("/home/yagz/rai_venv/robotics/Q1/environment.g")
C.view()

cam = ry.CameraView(C)
camera_frames = ["camera1", "camera2", "camera3", "camera4"]
all_points_world = []

bin_min = np.array([-0.3, 0.1, 0.725])
bin_max = np.array([0.3, 0.7, 0.77])

f_bbox = C.addFrame("bounding_box", "world")
f_bbox.setShape(ry.ST.ssBox, size=[bin_max[0] - bin_min[0], bin_max[1] - bin_min[1], bin_max[2] - bin_min[2], 0.01])
f_bbox.setPosition([(bin_max[0] + bin_min[0]) / 2, (bin_max[1] + bin_min[1]) / 2, (bin_max[2] + bin_min[2]) / 2])
f_bbox.setColor([0, 0, 0, 0])
C.view()

for cam_frame in camera_frames:
    cam.setCamera(cam_frame)
    rgb, depth = cam.computeImageAndDepth(C)
    depth = depth.astype(np.float32)
    depth[depth < 0] = np.nan
    pcl = ry.depthImage2PointCloud(depth, cam.getFxycxy()).reshape(-1, 3)
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

pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.02, max_nn=30))
pcd.orient_normals_consistent_tangent_plane(30)

normals = np.asarray(pcd.normals)

n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)
labels = kmeans.fit_predict(merged_pcl)

colors = plt.colormaps["tab10"](labels / (n_clusters - 1))[:, :3]
pcd.colors = o3d.utility.Vector3dVector(colors)

o3d.visualization.draw_geometries([pcd], point_show_normal=True, window_name="Segmented Point Cloud with Normals", width=800, height=600)

points = np.asarray(pcd.points)
normals = np.asarray(pcd.normals)
grasp_points = {}

for cluster_id in range(n_clusters):
    cluster_mask = labels == cluster_id
    cluster_points = points[cluster_mask]
    cluster_normals = normals[cluster_mask]
    best_score = -1
    best_pair = None
    num_samples = min(500, len(cluster_points))
    indices = np.random.choice(len(cluster_points), num_samples, replace=False)

    for i in indices:
        p1 = cluster_points[i]
        n1 = cluster_normals[i]
        dot_products = np.dot(cluster_normals, -n1)
        candidates = np.where(dot_products > 0.95)[0]

        for j in candidates:
            if i == j:
                continue
            p2 = cluster_points[j]
            n2 = cluster_normals[j]
            distance = np.linalg.norm(p1 - p2)
            if 0.05 < distance < 0.15:
                score = dot_products[j] / distance
                if score > best_score:
                    best_score = score
                    best_pair = (p1, p2, n1, n2)

    if best_pair is not None:
        grasp_points[cluster_id] = best_pair
    else:
        print(f"No antipodal grasp found for cluster {cluster_id}")

def rotation_matrix_from_vectors(vec1, vec2):
    a, b = vec1 / np.linalg.norm(vec1), vec2 / np.linalg.norm(vec2)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    if s == 0:
        if c > 0:
            return np.eye(3)
        else:
            axis = np.eye(3)[np.argmin(np.abs(a))]
            return -np.eye(3) + 2 * np.outer(axis, axis)
    vx = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    R = np.eye(3) + vx + vx @ vx * ((1 - c) / (s ** 2))
    return R

def rotation_matrix_to_quaternion(R):
    m = R
    t = np.trace(m)
    if t > 0:
        S = np.sqrt(t + 1.0) * 2
        qw = 0.25 * S
        qx = (m[2, 1] - m[1, 2]) / S
        qy = (m[0, 2] - m[2, 0]) / S
        qz = (m[1, 0] - m[0, 1]) / S
    elif (m[0, 0] > m[1, 1]) and (m[0, 0] > m[2, 2]):
        S = np.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2
        qw = (m[2, 1] - m[1, 2]) / S
        qx = 0.25 * S
        qy = (m[0, 1] + m[1, 0]) / S
        qz = (m[0, 2] + m[2, 0]) / S
    elif m[1, 1] > m[2, 2]:
        S = np.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2
        qw = (m[0, 2] - m[2, 0]) / S
        qx = (m[0, 1] + m[1, 0]) / S
        qy = 0.25 * S
        qz = (m[1, 2] + m[2, 1]) / S
    else:
        S = np.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2
        qw = (m[1, 0] - m[0, 1]) / S
        qx = (m[0, 2] + m[2, 0]) / S
        qy = (m[1, 2] + m[2, 1]) / S
        qz = 0.25 * S
    return np.array([qw, qx, qy, qz])

bot = ry.BotOp(C, False)

cluster_id = 0
if cluster_id not in grasp_points:
    print(f"No grasp points found for cluster {cluster_id}")
else:
    p1, p2, n1, n2 = grasp_points[cluster_id]
    grasp_center = (p1 + p2) / 2
    grasp_direction = (n1 + n2) / 2
    grasp_direction /= np.linalg.norm(grasp_direction)

    f_grasp = C.addFrame(f"grasp_{cluster_id}", "world")
    f_grasp.setPosition(grasp_center)

    approach_axis = np.array([0, 0, 1])
    rotation_matrix = rotation_matrix_from_vectors(approach_axis, grasp_direction)
    quat = rotation_matrix_to_quaternion(rotation_matrix)
    f_grasp.setQuaternion(quat.tolist())

    C.view()

    komo = ry.KOMO()
    komo.setModelConfig(C)  # Updated function
    komo.setTiming(1.0, 20, 5.0)
    komo.addObjective([], ry.FS.positionDiff, ["gripperCenter", f"grasp_{cluster_id}"], ry.OT.sos, [0, 0, 0])
    komo.addObjective([], ry.FS.quaternionDiff, ["gripperCenter", f"grasp_{cluster_id}"], ry.OT.sos, [0, 0, 0, 0])
    komo.addObjective([1.0], ry.FS.distance, ["gripper", f"grasp_{cluster_id}"], ry.OT.eq, [0])
    komo.optimize()
    path = komo.getPath_qAll()

    for q in path:
        bot.move(q, [0.1])
        bot.wait()

    bot.gripperClose()
    time.sleep(1)

    place_position = [0.0, 0.5, 0.9]
    f_place = C.addFrame("place_position", "world")
    f_place.setPosition(place_position)

    komo = ry.KOMO()
    komo.setModelConfig(C)  # Updated function
    komo.setTiming(1.0, 20, 5.0)
    komo.addObjective([], ry.FS.positionDiff, ["gripperCenter", "place_position"], ry.OT.sos, [0, 0, 0])
    komo.addObjective([], ry.FS.quaternionDiff, ["gripperCenter"], ry.OT.sos, [0, 0, 0, 0])
    komo.optimize()
    path = komo.getPath_qAll()

    for q in path:
        bot.move(q, [0.1])
        bot.wait()

    bot.gripperOpen()
    time.sleep(1)

    home_position = C.getJointState()
    bot.move(home_position, [1.0])
    bot.wait()

input("Press Enter to exit...")

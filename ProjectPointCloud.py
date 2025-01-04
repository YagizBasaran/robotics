import robotic as ry
import numpy as np
import open3d as o3d
import os

os.environ['DISPLAY'] = ':0'

def main():
    #------------------------------------------------
    # 1) Load environment
    #------------------------------------------------
    C = ry.Config()
    C.addFile("penvironment.g")  # Path if needed

    cam_view = ry.CameraView(C)
    camera_frames = ["camera1", "camera2"]
    all_points_world = []

    # Table bounding box
    table_min = [-1.0, -2.0, 0.5]
    table_max = [ 1.0,  2.0, 1.5]

    # Target bounding box (as before)
    target_min = [-0.35,  0.65, 0.64]
    target_max = [ 0.35,  1.35, 0.78]

    # Stick bounding box (example values, adjust if needed)
    stick_min  = [-0.05, -1.05, 0.58]
    stick_max  = [ 0.05, -0.95, 1.22]

    print("Capturing from cameras:", camera_frames)

    #------------------------------------------------
    # 2) Capture & merge
    #------------------------------------------------
    for cf in camera_frames:
        print(f"\n--- {cf} ---")
        cam_view.setCamera(cf)
        rgb, depth = cam_view.computeImageAndDepth(C)
        depth = depth.astype(np.float32)
        depth[depth < 0] = np.nan

        pcl_cam = ry.depthImage2PointCloud(depth, cam_view.getFxycxy())
        pcl_cam = pcl_cam.reshape(-1, 3)
        pcl_cam = pcl_cam[~np.isnan(pcl_cam).any(axis=1)]
        if pcl_cam.size == 0:
            print(f"{cf}: no valid points.")
            continue

        f_cam = C.frame(cf)
        R_cam = f_cam.getRotationMatrix()
        t_cam = f_cam.getPosition()
        pcl_world = (R_cam @ pcl_cam.T).T + t_cam

        # Crop to the table region
        mask_table = np.all((pcl_world >= table_min) & (pcl_world <= table_max), axis=1)
        pcl_table = pcl_world[mask_table]
        print(f"{cf}: {len(pcl_table)} points in table bounding box.")

        if len(pcl_table) > 0:
            all_points_world.append(pcl_table)

    if not all_points_world:
        print("No points in table region from any camera.")
        return

    merged_pcl = np.vstack(all_points_world)
    print(f"Merged table points: {len(merged_pcl)}")

    #------------------------------------------------
    # 3) Color logic: red for all, blue for target or stick
    #------------------------------------------------
    n_pts = len(merged_pcl)
    colors = np.tile([1.0, 0.0, 0.0], (n_pts, 1))  # all red by default

    # mask for target
    in_target = np.all((merged_pcl >= target_min) & (merged_pcl <= target_max), axis=1)
    # mask for stick
    in_stick  = np.all((merged_pcl >= stick_min)  & (merged_pcl <= stick_max),  axis=1)

    # points that are either in the target or in the stick
    in_target_or_stick = np.logical_or(in_target, in_stick)

    # color those points blue
    colors[in_target_or_stick] = [0.0, 0.0, 1.0]
    colors[in_target] = [0.3,0.8,0.3]

    #------------------------------------------------
    # 4) Create Open3D cloud & visualize
    #------------------------------------------------
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(merged_pcl)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    # If you want fast display, skip normal estimation
    # pcd.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.02, max_nn=30))
    # pcd.orient_normals_consistent_tangent_plane(30)

    print("Opening Open3D window. Close/ESC to exit.")
    vis = o3d.visualization.Visualizer()
    vis.create_window("Table + Target + Stick", 800, 600)
    vis.add_geometry(pcd)

    while True:
        vis.update_geometry(pcd)
        if not vis.poll_events():
            break
        vis.update_renderer()

    vis.destroy_window()
    print("Done.")

if __name__ == "__main__":
    main()

import open3d as o3d
import numpy as np
import os

os.environ['DISPLAY'] = ':0'

def main():
    # Create a simple Nx3 numpy array to mimic a point cloud
    pts = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1]
    ])

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pts)

    # Manual Visualizer approach
    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name="Test Minimal Open3D", width=800, height=600)
    vis.add_geometry(pcd)

    print("DEBUG: Visualizer loop starting...")

    while True:
        # update the geometry
        vis.update_geometry(pcd)
        # poll for events (keyboard/mouse)
        if not vis.poll_events():
            print("DEBUG: poll_events() returned False, exiting loop.")
            break
        vis.update_renderer()

    print("DEBUG: Destroying window, script will end.")
    vis.destroy_window()

if __name__ == "__main__":
    main()
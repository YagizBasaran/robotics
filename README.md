# robotics
Make sure to check out these videos below. For further insight, check out the report in the repository.

https://www.youtube.com/watch?v=u-8IV7ruLa4 1 minute version

https://www.youtube.com/watch?v=RDgTNJuO_pg Detailed version
# Ring Throwing with Precision Constraints



## 🚀 **Overview**
This project showcases the development of a **ring-throwing to a pole in robotic system**. The system is powered by the **Robotic library (`ry`)** (version 0.1.10) for simulation and control, and features:
- A **thrower robot** that calculates optimal trajectories and velocities to throw a ring.

This project demonstrates cutting-edge robotics concepts, including:
- 🎯 **Trajectory Optimization**
- 🤖 **Kinematics and Dynamics Simulation**
- 🛠️ **Object Tracking and Manipulation**


## ✨ **Features**


### **Thrower Robot**
- 📐 **Optimal Velocity Calculation**: Computes the throwing velocity using kinematic and dynamic constraints.
- 🌌 **Trajectory Simulation**: Models ring trajectories accounting for gravity and release parameters.
- 🔄 **Inversion Handling**: Manages trajectory flipping for complex *pole* placements.


### **Path Finding**
- First, find the best way to grasp the ring.
- Second, decide which throwing motion is the most optimal (not frisbee in this case, catapult is better)
- Third, get into the position to obtain velocity.
- Lastly, decide where to release the ring and finish the throwing.

### **Simulation Environment**
- 🛠️ Built using the **[robotic](https://github.com/MarcToussaint/robotic/) library (`ry`)** by [Marc Toussaint](https://github.com/MarcToussaint). Thanks Marc!
- 🎥 **Visualization Support**: Displays trajectories and robot movements in real-time.


## 💡 **Key Highlights**
- A perfect demonstration of **real-time robotics simulation**.
- Integrates advanced algorithms like **trajectory optimization** for dynamic adaptability.
- **Modular and extensible** design for further enhancements and experimentation.

## 🏆 **Future Work**
- Enhance the vision system to include **machine learning-based tracking** for better ring trajectory estimation.
- Optimize RRT algorithms for faster and more efficient pathfinding.
- Add precision and computer vision to the system.


## ✅ **Installation** 


## 👥 Team members:

Mertcan Dağdelen

Süleyman Yağız Başaran

Bartu Özyıldırım

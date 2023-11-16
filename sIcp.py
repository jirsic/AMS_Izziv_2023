from simpleicp import PointCloud, SimpleICP
import numpy as np

X_fix=np.genfromtxt("C:/Users/jerne/Desktop/Faks/2_Stopnja/2_Letnik/Analiza medicinskih slik/AMS_Izziv_2023/meshRef.txt")
X_mov=np.genfromtxt("C:/Users/jerne/Desktop/Faks/2_Stopnja/2_Letnik/Analiza medicinskih slik/AMS_Izziv_2023/meshTra.txt")

pc_fix=PointCloud(X_fix, columns=['x', 'y', 'z'])
pc_mov=PointCloud(X_mov, columns=['x', 'y', 'z'])

icp=SimpleICP()
icp.add_point_clouds(pc_fix, pc_mov)
H, X_mov_transformed, rigid_body_transformation_params, distance_residuals = icp.run(max_overlap_distance=10000)
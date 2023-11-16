import copy
import numpy as np
import open3d as o3d
from probreg import cpd
import trimesh

sdata=o3d.io.read_triangle_mesh("C:/Users/jerne/Desktop/Faks/2_Stopnja/2_Letnik/Analiza medicinskih slik/AMS_Izziv_2023/Registration Cases/Case_01_CTA_PT00109_20151218.obj")
source = o3d.geometry.PointCloud()
source.points = o3d.utility.Vector3dVector(sdata.vertices)

tdata=o3d.io.read_triangle_mesh("C:/Users/jerne/Desktop/Faks/2_Stopnja/2_Letnik/Analiza medicinskih slik/AMS_Izziv_2023/Registration Cases/Case_01_CTA_PT00109_20130905.obj")
target = o3d.geometry.PointCloud()
target.points = o3d.utility.Vector3dVector(tdata.vertices)

tf_param, _, _ = cpd.registration_cpd(source, target)

result = copy.deepcopy(source)
result.points = tf_param.transform(result.points)

source.paint_uniform_color([1, 0, 0])
target.paint_uniform_color([0, 1, 0])
result.paint_uniform_color([0, 0, 1])

o3d.visualization.draw_geometries([source, target, result])

print(tf_param.t, tf_param.rot)


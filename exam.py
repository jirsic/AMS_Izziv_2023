import copy
import numpy as np
import open3d as o3
from probreg import cpd
import trimesh

# load source and target point cloud
sdata = trimesh.load_mesh('Registration Cases\Case_11_CTA_PT00056_20171114.obj')
tdata = o3.io.read_triangle_mesh('Registration Cases\Case_11_CTA_PT00056_20190716.obj')


print(sdata)
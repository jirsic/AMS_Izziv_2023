import os
import trimesh
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from simpleicp import PointCloud, SimpleICP

'''path='Registration Cases'
dirList=os.listdir(path)
fNames=[]
idx=[0]
i=0

for file in dirList:
    if file.endswith(".obj"):
        fNames.append(file)
        if fNames[i-1][5:7]!=fNames[i][5:7]:
            idx.append(i)
        i+=1

print(idx)'''

mesh11 = trimesh.load_mesh("C:/Users/jerne/Desktop/Faks/2_Stopnja/2_Letnik/Analiza medicinskih slik/AMS_Izziv_2023/Registration Cases/Case_07_CTA_PT00018_20140925.obj")
mesh12 = trimesh.load_mesh("C:/Users/jerne/Desktop/Faks/2_Stopnja/2_Letnik/Analiza medicinskih slik/AMS_Izziv_2023/Registration Cases/Case_07_CTA_PT00018_20200701.obj")

meshRef=np.array(mesh11.vertices)
np.savetxt('meshRef.txt', meshRef, fmt='%1.6f')

meshTra=np.array(mesh12.vertices)
np.savetxt('meshTra.txt', meshTra, fmt='%1.6f')
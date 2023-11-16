import probFun
import copy
import open3d as o3d
from probreg import cpd
import numpy as np

path='Registration Cases'

fileNames, relFilePaths, indexes=probFun.load_dirData(path)

caseNm='10'
trsMatrices, sourceMesh, targetMeshes, dist=probFun.load_selCases(relFilePaths, indexes, caseNm)

#triMatrices=probFun.getTrimeshTransMatrices(trsMatrices, dist)

if trsMatrices.scale<0.5:
    sprem='defekt'
    trsMatrices.scale=1

resultMeshes=probFun.apply_transformations(trsMatrices, sourceMesh, dist) #NEKAJ NE DELA!!!!

if sprem=='defekt':
    resultMeshes=probFun.correct_defect(targetMeshes, resultMeshes, trsMatrices, dist)

#probFun.show_transformedMeshes(sourceMesh, targetMeshes, resultMeshes, dist)
source=sourceMesh
target=targetMeshes
result=resultMeshes
source.paint_uniform_color([1, 0, 0])
target.paint_uniform_color([0, 1, 0])
result.paint_uniform_color([0, 0, 1])
o3d.visualization.draw_geometries([result, target])
print(source)
print(target)
print(result)
import os
import copy
import trimesh
import numpy as np
import open3d as o3d
from probreg import cpd
from probreg import bcpd
from probreg import callbacks
import matplotlib.pyplot as plt


def load_dirData(path):
    dirList=os.listdir(path)
    fNames=[]
    fPaths=[]
    idx=[0]
    i=0

    for file in dirList:
        if file.endswith(".obj"):
            fNames.append(file)
            fPaths.append(os.path.join(path, file))
            if fNames[i-1][5:7]!=fNames[i][5:7]:
                idx.append(i)

            print('Found file: ', file)
            i+=1
    
    idx.append(i)
    print('Directory reading finished')
    print('Indexes of first case procedures: ', idx)

    return fNames, fPaths, idx

def load_selCases(fPaths, idx, caseNm):
    caseNm=int(caseNm)
    src=fPaths[idx[caseNm-1]]
    dist=idx[caseNm]-idx[caseNm-1]-1

    if dist>1:
        trsMatrix=[]
        trg=[]
        source=[]
        for i in range(1, dist):
            tgt=fPaths[idx[caseNm-1]+i]
            print(f'Computing transformation matrix for {tgt} and {src}')
            transform, source, target=find_selectedTransforms(src, tgt)
            trg.append(target)
            trsMatrix.append(transform)
    else:
        tgt=fPaths[idx[caseNm-1]+1]
        print(f'Computing transformation matrix for {tgt} and {src}')
        transform, source, target=find_selectedTransforms(src, tgt)
        trg=target
        trsMatrix=transform


    return trsMatrix, source, trg, dist

def find_selectedTransforms(src, tgt):
    sdata=o3d.io.read_triangle_mesh(src)
    source = o3d.geometry.PointCloud()
    source.points = o3d.utility.Vector3dVector(sdata.vertices)

    tdata=o3d.io.read_triangle_mesh(tgt)
    target = o3d.geometry.PointCloud()
    target.points = o3d.utility.Vector3dVector(tdata.vertices)

    tf_param, _, _ = cpd.registration_cpd(source, target)

    return tf_param, source, target
    
def apply_transformations(trsMatrices, sourceMesh, dist):
    

    if dist>2:
        trsMeshes=[]
        for i in range(dist-1):
            result=copy.deepcopy(sourceMesh)
            result.points=trsMatrices[i].transform(result.points)
            trsMeshes.append(result)
    else:
        result=copy.deepcopy(sourceMesh)
        result.points=trsMatrices.transform(result.points)
        trsMeshes=result

    return trsMeshes

def apply_transformations(trsMatrices, sourceMesh, dist):
    

    if dist>2:
        trsMeshes=[]
        for i in range(dist-1):
            result=copy.deepcopy(sourceMesh)
            result.points=trsMatrices[i].transform(result.points)
            trsMeshes.append(result)
    else:
        result=copy.deepcopy(sourceMesh)
        result.points=trsMatrices.transform(result.points)
        trsMeshes=result

    return trsMeshes
            

def show_transformedMeshes(source, target, resultMeshes, dist):
    
    for i in range(dist):
        source.paint_uniform_color([1, 0, 0])
        target[i].paint_uniform_color([0, 1, 0])
        resultMeshes[i].paint_uniform_color([0, 0, 1])
        o3d.visualization.draw_geometries([source, target[i], resultMeshes[i]])
            
def getTrimeshTransMatrices(trsMatrices, dist):
    triMatrices=np.empty((4,4))

    for i in range(dist-1):
        triMatrices[:3, :3]=trsMatrices[i].rot
        triMatrices[:3, 3]=trsMatrices[i].t
        triMatrices[3, :]=[0, 0, 0, 1]
    
    return triMatrices

def correct_defect(targetMeshes, resultMeshes1, trsMatrices, dist):
    meanTrg, meanRes=np.mean(np.array(targetMeshes.points), axis=0), np.mean(np.array(resultMeshes1.points), axis=0)
    trs=np.subtract(meanTrg, meanRes)
    trsMatrices.rot=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    trsMatrices.t=np.array(trs)
    resultMeshes1=apply_transformations(trsMatrices, resultMeshes1, dist)
    tf_param, _, _ = cpd.registration_cpd(resultMeshes1, targetMeshes)
    resultMeshes2=apply_transformations(tf_param, resultMeshes1, dist)

    #ni lepo, dela pa :)
    return resultMeshes2
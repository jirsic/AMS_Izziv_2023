import os
import copy
import trimesh
import numpy as np
import open3d as o3d
from probreg import cpd
import matplotlib.pyplot as plt

class func():
    def __init__(self, path):
        self.path=path

    def load_dirData(self, path):
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

                print('Loaded file: ', file)
                i+=1
    
        print('Directory reading finished')
        print('Indexes of first case procedures: ', idx)

        return fNames, fPaths, idx
    
    def load_selCases(self, fPaths, idx, caseNm):
        trsMatrix=[]
        trg=[]
        source=[]
        caseNm=int(caseNm)
        src=fPaths[idx[caseNm-1]]
        dist=idx[caseNm+1]-idx[caseNm]

        for i in range(dist):
            tgt=fPaths[idx[caseNm]+i]
            print(f'Computing transformation matrix {i+1}/{dist}')
            transform, source, target=self.find_selectedTransforms(src, tgt)
            trg.append(target)
            trsMatrix.append(transform)

        return trsMatrix, source, trg

    def find_selectedTransforms(self, src, tgt):
        sdata=o3d.io.read_triangle_mesh(src)
        source = o3d.geometry.PointCloud()
        source.points = o3d.utility.Vector3dVector(sdata.vertices)

        tdata=o3d.io.read_triangle_mesh(tgt)
        target = o3d.geometry.PointCloud()
        target.points = o3d.utility.Vector3dVector(tdata.vertices)

        tf_param, _, _ = cpd.registration_cpd(source, target)

        return tf_param, source, target
    
    def apply_transformations(self, trsMatrices, sourceMesh):
        trsMeshes=[]

        for i in range(len(trsMatrices)):
            result=copy.deepcopy(sourceMesh)
            result.points=trsMatrices[i].transform(result.points)
            trsMeshes.append(result)

        return trsMeshes
            

    def show_transformedMeshes(self, source, target, resultMeshes):
        nmOfCases=len(resultMeshes)

        for i in range(nmOfCases):
            source.paint_uniform_color([1, 0, 0])
            target[i].paint_uniform_color([0, 1, 0])
            resultMeshes[i].paint_uniform_color([0, 0, 1])
            o3d.visualization.draw_geometries([source, target[i], resultMeshes[i]])
            

import os
import copy
import trimesh
import numpy as np
import open3d as o3d
from probreg import cpd
import matplotlib.pyplot as plt

class func():
    def __init__(self, janez):
        self.janez=janez

    def load_dirData(self, path, prtSts):
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
                
                if prtSts==1:
                    print('Found file: ', file)
                i+=1

        idx.append(i)
        print('Directory reading finished')
        print('Indexes of first case procedures: ', idx)

        return fNames, fPaths, idx
    
    def load_selCases1(self, fPaths, idx, caseNm):
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
    
    def load_selCases(self, src, tgt):
        redo=1

        transform, source, target=self.find_selectedTransforms(src, tgt)
        trg=target
        trsMatrix=transform

        if trsMatrix.scale<0.5:
            trsMatrix.sprem='DEFEKT'
            trsMatrix.scale=1
        else: 
            trsMatrix.sprem='OK'


        return trsMatrix, source, trg, redo

    def find_selectedTransforms(self, src, tgt):
        sdata=o3d.io.read_triangle_mesh(src)
        source = o3d.geometry.PointCloud()
        source.points = o3d.utility.Vector3dVector(sdata.vertices)

        tdata=o3d.io.read_triangle_mesh(tgt)
        target = o3d.geometry.PointCloud()
        target.points = o3d.utility.Vector3dVector(tdata.vertices)

        tf_param, _, _ = cpd.registration_cpd(source, target)

        return tf_param, source, target
    
    def apply_transformations(self, trsMatrices, sourceMesh, redo):

        if redo>1:
            trsMeshes=[]

            for i in range(redo):
                result=copy.deepcopy(sourceMesh)
                result.points=trsMatrices[i].transform(result.points)
                trsMeshes.append(result)
        else:
            result=copy.deepcopy(sourceMesh)
            result.points=trsMatrices.transform(result.points)
            trsMeshes=result

        return trsMeshes
            

    def show_transformedMeshes(self, source, target, resultMeshes):
        nmOfCases=len(resultMeshes)

        for i in range(nmOfCases):
            source.paint_uniform_color([1, 0, 0])
            target[i].paint_uniform_color([0, 1, 0])
            resultMeshes[i].paint_uniform_color([0, 0, 1])
            o3d.visualization.draw_geometries([source, target[i], resultMeshes[i]])


    def correct_defect1(self, targetMeshes, resultMeshes1, trsMatrices):
        redo=1
        meanTrg, meanRes=np.mean(np.array(targetMeshes.points), axis=0), np.mean(np.array(resultMeshes1.points), axis=0)
        trs=np.subtract(meanTrg, meanRes)
        trsMatrices.rot=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        trsMatrices.t=np.array(trs)
        resultMeshes1=self.apply_transformations(trsMatrices, resultMeshes1, redo)
        tf_param, _, _ = cpd.registration_cpd(resultMeshes1, targetMeshes)
        resultMeshes2=self.apply_transformations(tf_param, resultMeshes1, redo)


        #ni lepo, dela pa :)
        return resultMeshes2
            
    def show_transformedMeshes(self, source, target, resultMeshes, redo):
    
        source.paint_uniform_color([1, 0, 0])
        target.paint_uniform_color([0, 1, 0])
        resultMeshes.paint_uniform_color([0, 0, 1])
        o3d.visualization.draw_geometries([target, resultMeshes])


    def getTrimeshTransMatrices1(self, trsMatrices, redo):
        triMatrices=np.empty((4,4))

        for i in range(redo-1):
            triMatrices[:3, :3]=trsMatrices[i].rot
            triMatrices[:3, 3]=trsMatrices[i].t
            triMatrices[3, :]=[0, 0, 0, 1]
        
        return triMatrices
    
    def save_mesh(self, resultMeshes, path):
        o3d.io.write_point_cloud(path, resultMeshes)
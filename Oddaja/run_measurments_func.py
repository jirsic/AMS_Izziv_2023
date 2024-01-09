import trimesh
import numpy as np
import open3d as o3d
import math
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull, convex_hull_plot_2d, Delaunay
import collections


def in_hull(p, hull):
    
    if not isinstance(hull,Delaunay):
        hull = Delaunay(hull)

    return hull.find_simplex(p)>=0


def computeAneurysmVolume(path, display=[0,0,0], STEP=0.15):
    mesh=trimesh.load_mesh(path)

    points=np.array(mesh.vertices)
    labels=np.array(mesh.visual.vertex_colors[:,0])
    labels2=np.array(np.nonzero(labels))
    ntsk=points[labels2]
    nArr=ntsk[0][:][:]

    displayPointCloud=display[0]
    displayVoxeled=display[1]

    if displayPointCloud==1:
        pcd=o3d.geometry.PointCloud()
        pcd.points=o3d.utility.Vector3dVector(nArr)
        o3d.visualization.draw_geometries([pcd])


    fct=1/STEP

    for xA in range(nArr.shape[0]):
        for zA in range(3):
            nArr[xA,zA]=math.ceil(nArr[xA, zA]*fct)/fct

    nArr=np.unique(nArr, axis=0)


    xMin, xMax=min(nArr[:,0]), max(nArr[:,0])
    yMin, yMax=min(nArr[:,1]), max(nArr[:,1])
    zMin, zMax=min(nArr[:,2]), max(nArr[:,2])

    xMG=np.arange(xMin, xMax, STEP)
    yMG=np.arange(yMin, yMax, STEP)
    zMG=np.arange(zMin, zMax, STEP)

    gArr=np.vstack(np.meshgrid(yMG,zMG)).reshape(2,-1).T

    list=gArr.tolist()
    uniX=np.unique(nArr[:,0])
    voxels=[]
    i=0

    for x in uniX:
        meanX=np.asarray(np.where(nArr[:,0]==x))
        meanX=meanX[0][::]
        meanPlot=nArr[meanX,:]
        points1=np.c_[meanPlot[:,1],meanPlot[:,2]]

        #print(i)
        if points1.shape[0]>2:
            hull = ConvexHull(points1)

            xpMin, xpMax, ypMin, ypMax=[np.min(points1[:,0]), np.max(points1[:,0]), np.min(points1[:,1]), np.max(points1[:,1])]

            sez=[]
            for xL in list:
                if xpMin <= xL[0] <= ypMax and ypMin <= xL[1] <=ypMax:
                    idx=in_hull([xL[0], xL[1]], points1)
                    if idx==True:
                        sez.append(xL)
            sez=np.array(sez, x)
            vox=np.c_[sez, np.ones(sez.shape[0])*x]
            voxels.append(vox)


            '''
            plt.figure()
            for simplex in hull.simplices:
                plt.plot(points1[simplex, 0], points1[simplex, 1], 'k-')
                plt.plot(points1[:,0], points1[:,1], 'o')
                plt.plot(sez[:,0], sez[:,1], '+')'''
            
        i+=1
    voksli=np.concatenate(voxels)
        
    if displayVoxeled==1:
        pcd2=o3d.geometry.PointCloud()
        pcd2.points = o3d.utility.Vector3dVector(voksli)
        voxel_grid2 = o3d.geometry.VoxelGrid.create_from_point_cloud(pcd2, voxel_size=STEP)
        o3d.visualization.draw_geometries([voxel_grid2])


    aneurysmSize=(voksli.shape[0]*(STEP**3))

    xMaxDist=xMax-xMin
    yMaxDist=yMax-yMin
    zMaxDist=zMax-zMin

    maxConDist=computeMaxDist(voksli, STEP)

    return aneurysmSize, xMaxDist, yMaxDist, zMaxDist, maxConDist, voksli

def computeMaxDist(voksli, STEP):
    nmP=[0, 0, 0]
    '''for i in range(3):
        uniX=np.unique(voksli[:,i])

        for j in range(len(uniX)):
            nm=voksli[i].count(uniX(j))

            if nm>nmP[i]:
                nmP[i]=nm'''
    counterX = collections.Counter(voksli[:,0])
    counterY = collections.Counter(voksli[:,1])
    counterZ = collections.Counter(voksli[:,2])

    cX=max(counterX.values())
    cY=max(counterY.values())
    cZ=max(counterZ.values())

    return [cX, cY, cZ]

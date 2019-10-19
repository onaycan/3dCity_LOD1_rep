import math
import matplotlib.pyplot as plt
import numpy as np

import triangle as tr
import vertices as vertex
from scipy.interpolate import griddata


def constrained_polygon_triangulation(_points):
    N=int(_points.size/2)
    
    #print(N)
    i = np.arange(N)
    seg = np.stack([i, i + 1], axis=1) % N
    #points = np.array([[0, 0], [0, 10], [5, 10], [5, 5], [10, 5], [10, 10],[15, 10], [15, 0]]) 
    A = dict(vertices=_points,segments=seg)
    try:
        B = tr.triangulate(A,'p')
    except: 
        return {},False
    else:
        return B['triangles'],True
    #tr.compare(plt, A, B)
    #print(B['triangles'])
    #plt.show()


def permutation_symbol(i,j,k):
    return (i-j)*(j-k)*(k-i)/2

def cross_product(v1,v2):
    normal=[0.0,0.0,0.0]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                normal[i]+=permutation_symbol(i,j,k)*v1[j]*v2[k]
    return normal

def dot_product(v1, v2):
    return math.sqrt(v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2])

def elevate_floors_mid(ground_vertices, beamsets):
    ground_xy=np.array([]).reshape(0,2)
    ground_z=np.array([]).reshape(0,1)
    beamset_mids=np.array([]).reshape(0,2)
    for v in ground_vertices.values():
        ground_xy=np.vstack([ground_xy,[v.coordsX[0],v.coordsX[1]]])
        ground_z=np.vstack([ground_z,[v.coordsX[2]]])
    for b in beamsets.values():
        beamset_mids=np.vstack([beamset_mids,[b.mid[0],b.mid[1]]])
    #print(ground_xy.shape)
    #print(ground_z.shape)
    #print(beamset_mids.shape)
    interp=griddata(ground_xy, ground_z, beamset_mids, method='linear')
    #print(interp)
    coun=0
    for b in beamsets.values():
        for v in b.vertices:
            v.coordsX[2]=interp.item(coun)
        coun+=1
    #print(coun)


def elevate_floors_corners(ground_vertices, beamsets):
    ground_xy=np.array([]).reshape(0,2)
    ground_z=np.array([]).reshape(0,1)
    beamset_corners=np.array([]).reshape(0,2)
    for v in ground_vertices.values():
        ground_xy=np.vstack([ground_xy,[v.coordsX[0],v.coordsX[1]]])
        ground_z=np.vstack([ground_z,[v.coordsX[2]]])
    for b in beamsets.values():
        for v in b.vertices:
            beamset_corners=np.vstack([beamset_corners,[v.coordsX[0],v.coordsX[1]]])
    #print(ground_xy.shape)
    #print(ground_z.shape)
    #print(beamset_corners.shape)
    interp=griddata(ground_xy, ground_z, beamset_corners, method='linear')
    #print(interp)
    coun=0
    for b in beamsets.values():
        for v in b.vertices:
            v.coordsX[2]=interp.item(coun)
            coun+=1
    #print(coun)

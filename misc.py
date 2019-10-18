import math
import matplotlib.pyplot as plt
import numpy as np

import triangle as tr

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


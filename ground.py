import numpy as np
from scipy.spatial import Delaunay
import vertices
import triangles
import vtk_interaction

def ground_geometry():
    number_of_triangles=0
    origin=[]
    ground_vertices={}
    ground_triangles={}    

    with open("elevations/elevations.txt",'r') as f:
        lines=f.read().splitlines()
        coun=0
        for l in lines:
            current_coords_lat_long=l.split()
            temp=current_coords_lat_long[0]
            current_coords_lat_long[0]=current_coords_lat_long[1]
            current_coords_lat_long[1]=temp
            ground_vertices["g"+str(coun)]=vertices.vertex("g"+str(coun),current_coords_lat_long)
            ground_vertices["g"+str(coun)].coordsX[2]=float(current_coords_lat_long[2])
            coun+=1 
            

    #for i in range(2):
    origin.append(min([v.coords_lat_long[0] for v in ground_vertices.values()]))
    origin.append(min([v.coords_lat_long[1] for v in ground_vertices.values()]))
    maxo=max([v.coords_lat_long[0] for v in ground_vertices.values()])

    dummy_v1=vertices.vertex("-1",[maxo,origin[1]])
    nw=dummy_v1.dist_2_another_vertex_in_m(origin)



    for gv in ground_vertices.values():
        gv.convert_lat_long2m(origin)

    points=np.array([]).reshape(0,2)    
    for ver in ground_vertices.values():
        points=np.vstack([points,[ver.coordsX[0],ver.coordsX[1]]])    


    coun=0
    trigls = Delaunay(points)
    for tri in trigls.simplices:
        #print(tri)
        ground_triangles["gt"+str(coun)]=triangles.triangle("gt"+str(coun),[ground_vertices["g"+str(tri[0])],ground_vertices["g"+str(tri[1])],ground_vertices["g"+str(tri[2])]],number_of_triangles)
        number_of_triangles+=1
        coun+=1

    return origin,ground_vertices,ground_triangles ,nw
#print(trigls.simplices)
#
#triangle_or_truss=True
#wireframe=True
#vtk_interactor=vtk_interaction.vtk_interactor()
#vtk_interactor.insert_all_vertices(ground_vertices.values())
#for t in ground_triangles.values():
#    vtk_interactor.insert_triangle(t)
#
#vtk_interactor.visualize(triangle_or_truss, wireframe)
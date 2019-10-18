import math
import numpy as np



class triangle:
    def __init__(self,_id,_vertices):
        self.id=_id
        self.vertices=[]
        self.vertices.append(_vertices[0])
        self.vertices.append(_vertices[1])
        self.vertices.append(_vertices[2])
        self.all_coords=np.array([]).reshape(0,3)
        for v in self.vertices:
            self.all_coords=np.vstack([self.all_coords,[v.coords[0],v.coords[1],0.0]])
        self.mid=list(np.mean(self.all_coords,axis=0))
        #print(self.mid)
    '''
    def check_inside_nonconvex_boundaries(self, _boundaries):
        p1=np.subtract(self.all_coords[1],self.all_coords[0])
        p2=np.subtract(self.all_coords[2],self.all_coords[1])
        p3=np.array([0.0,0.0,1.0])
        cross=np.cross(p1,p2)
        dot=np.dot(cross,p3)
        #print(dot)
        if dot<0:
            return False
        else:
            return True
        #print("check")
        #for b in range(len(_boundaries)-1):
        #    p1=np.array([_boundaries[b].coords[0],_boundaries[b].coords[1],0.0])
        #    p2=np.array([_boundaries[b+1].coords[0],_boundaries[b+1].coords[1],0.0])
        #    p3=np.array([0.0,0.0,1.0])
        #    c_p1=np.subtract(p1,self.mid) 
        #    c_p2=np.subtract(p2,self.mid)
        #    cross=np.cross(c_p1,c_p2)
        #    dot=np.dot(cross,p3)
        #    #print(dot)
        #    if dot<0.0:
        #        return False
        #return True
    '''
            
             
import math



class truss:
    def __init__(self,_id,_vertices):
        self.id=_id
        self.vertices=[]
        self.vertices.append(_vertices[0])
        self.vertices.append(_vertices[1])
        self.dir=[]
        for i in range(3):
            self.dir.append(self.vertices[1].coordsX[i]-self.vertices[0].coordsX[i])
        self.length=math.sqrt(self.dir[0]*self.dir[0]+self.dir[1]*self.dir[1]+self.dir[2]*self.dir[2])
    #def dot_product(self, _anytruss):
    #    return math.sqrt(self.dir[0]*_anytruss.dir[0]+self.dir[1]*_anytruss.dir[1]+self.dir[2]*_anytruss.dir[2])
    #def check_if_beam(self):
    #    returnvalue=False
    #    if self.dir[1]==0.0:
    #        returnvalue=True
    #    return returnvalue
    #def check_if_column(self):
    #    returnvalue=False
    #    if self.dir[0]==0.0 and self.dir[2]==0:
    #        returnvalue=True
    #    return returnvalue
    #def check_if_edge(self):
        

        
             
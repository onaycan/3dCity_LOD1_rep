
import vertices
import triangles

class baseset:
    def __init__(self,_id):
        self.id=_id
        self.vertices=[]
        self.triangles=[]
    def append_vertex(self,_vertex):
        self.vertices.append(_vertex)
    def append_triangle(self,_triangle):
        self.triangles.append(_triangle)        
    
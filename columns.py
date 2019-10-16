
import vertices
import trusses

class column:
    def __init__(self,_id):
        self.id=_id
        self.vertices=[]
        self.trusses=[]
    def append_vertex(self,_vertex):
        self.vertices.append(_vertex)
    def append_truss(self,_truss):
        self.trusses.append(_truss)        
    